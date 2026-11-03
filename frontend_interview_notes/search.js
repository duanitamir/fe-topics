// Keep navigation available without making phone readers scroll past every topic.
(() => {
  const menu = document.querySelector('[data-topic-menu]');
  if (!menu) return;
  const desktop = matchMedia('(min-width: 751px)');
  const update = () => { menu.open = desktop.matches; };
  update();
  desktop.addEventListener('change', update);
})();

(() => {
  'use strict';
  const input = document.querySelector('[data-notes-search]');
  const results = document.querySelector('[data-search-results]');
  const status = document.querySelector('[data-search-status]');
  const parse = query => (query.match(/"[^"]+"|\S+/g) || [])
    .map(term => term.replace(/^"|"$/g, '').toLocaleLowerCase()).filter(Boolean);
  function matches(text, terms) {
    const lower = text.toLocaleLowerCase();
    const ranges = [];
    for (const term of terms) {
      let start = 0, at;
      while ((at = lower.indexOf(term, start)) !== -1) {
        ranges.push([at, at + term.length]);
        start = at + term.length;
      }
    }
    ranges.sort((a, b) => a[0] - b[0]);
    return ranges.reduce((merged, range) => {
      const last = merged[merged.length - 1];
      if (last && range[0] <= last[1]) last[1] = Math.max(last[1], range[1]);
      else merged.push(range.slice());
      return merged;
    }, []);
  }
  function marked(text, terms, ranges = matches(text, terms)) {
    const fragment = document.createDocumentFragment();
    let offset = 0;
    for (const [start, end] of ranges) {
      fragment.append(document.createTextNode(text.slice(offset, start)));
      const mark = document.createElement('mark');
      mark.textContent = text.slice(start, end);
      fragment.append(mark);
      offset = end;
    }
    fragment.append(document.createTextNode(text.slice(offset)));
    return fragment;
  }
  function excerpt(text, terms) {
    const ranges = matches(text, terms);
    const start = ranges.length ? Math.max(0, ranges[0][0] - 90) : 0;
    const end = Math.min(text.length, start + 300);
    return (start ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }
  function search() {
    const query = input.value.trim();
    const terms = parse(query);
    results.replaceChildren();
    try {
      const url = new URL(location.href);
      if (query) url.searchParams.set('q', query); else url.searchParams.delete('q');
      history.replaceState(null, '', url);
    } catch { /* Some file:// environments restrict history writes. */ }
    if (!terms.length) {
      status.textContent = 'Search every topic, explanation, table, and code snippet. Use quotes for an exact phrase.';
      return;
    }
    if (!Array.isArray(window.NOTES_SEARCH_INDEX)) {
      status.textContent = 'The search index could not load. Keep search-index.js alongside this page and reload.';
      return;
    }
    const found = window.NOTES_SEARCH_INDEX.map(record => {
      const text = (record.topic + ' ' + record.heading + ' ' + record.text).toLocaleLowerCase();
      if (!terms.every(term => text.includes(term))) return null;
      const score = terms.reduce((sum, term) => sum +
        (record.text.toLocaleLowerCase().includes(term) ? 5 : 0) +
        (record.heading.toLocaleLowerCase().includes(term) ? 2 : 0), 0) +
        (record.text.toLocaleLowerCase().includes(query.toLocaleLowerCase()) ? 10 : 0);
      return { record, score };
    }).filter(Boolean).sort((a, b) => b.score - a.score);
    const topics = new Set(found.map(item => item.record.page)).size;
    status.textContent = found.length
      ? `${found.length} matching passages across ${topics} ${topics === 1 ? 'topic' : 'topics'}.`
      : 'No matches. Try fewer words, a different spelling, or an API name.';
    const fragment = document.createDocumentFragment();
    for (const { record } of found) {
      const item = document.createElement('li');
      const meta = document.createElement('p');
      meta.className = 'search-result-meta';
      meta.textContent = record.topic + ' · ' + record.kind;
      const link = document.createElement('a');
      link.href = record.page + '?q=' + encodeURIComponent(query) + '#' + record.anchor;
      link.append(marked(record.heading || record.topic, terms));
      const preview = document.createElement('p');
      preview.append(marked(excerpt(record.text, terms), terms));
      item.append(meta, link, preview);
      fragment.append(item);
    }
    results.append(fragment);
  }
  if (input) {
    input.value = new URLSearchParams(location.search).get('q') || '';
    if (results) {
      let timer;
      input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(search, 100); });
      input.form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); search(); });
      input.addEventListener('search', search);
      search();
    }
    document.addEventListener('keydown', event => {
      const editing = event.target instanceof Element && event.target.closest('input,textarea,select,[contenteditable="true"]');
      if (((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') ||
          (event.key === '/' && !editing && !event.ctrlKey && !event.metaKey && !event.altKey)) {
        event.preventDefault(); input.focus(); input.select();
      }
    });
  }
  // Preserve syntax-token spans while marking matches in a result destination.
  if (!results && location.hash && location.search) {
    const terms = parse(new URLSearchParams(location.search).get('q') || '');
    let anchor;
    try { anchor = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(anchor);
    if (!target || !terms.length) return;
    const walker = document.createTreeWalker(target, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    // Match across syntax-token spans, then apply only each node's portion.
    const ranges = matches(nodes.map(node => node.data).join(''), terms);
    let offset = 0;
    for (const node of nodes) {
      const end = offset + node.data.length;
      const local = ranges.filter(([start, stop]) => start < end && stop > offset)
        .map(([start, stop]) => [Math.max(0, start - offset), Math.min(end, stop) - offset]);
      if (local.length) node.replaceWith(marked(node.data, terms, local));
      offset = end;
    }
    target.classList.add('search-destination');
    target.scrollIntoView({ block: 'center', behavior: 'instant' });
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  }
})();

// Scrollspy: share one current-section marker across every topic's sidebar.
(() => {
  'use strict';
  const sidebar = document.querySelector('.page-toc') || document.querySelector('aside');
  const links = [...document.querySelectorAll('.subnav a[href^="#"]')];
  const sections = links.map(link => {
    const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
    if (!target) return null;
    const status = document.createElement('span');
    status.className = 'section-reading-status';
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    marker.setAttribute('viewBox', '0 0 16 16');
    marker.setAttribute('aria-hidden', 'true');
    marker.classList.add('section-progress-check');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M4 8l2.5 2.5L12 5');
    marker.append(path);
    link.append(marker, status);
    return { link, target, status };
  }).filter(Boolean);
  if (!sections.length) return;

  let current = null;
  let frame = 0;
  function update() {
    frame = 0;
    // The reading line is near the top; keep the current section through its body.
    const headerHeight = document.querySelector('.site-header')?.getBoundingClientRect().height || 0;
    const readingLine = headerHeight + 56;
    let next = sections[0];
    for (const section of sections) {
      if (section.target.getBoundingClientRect().top <= readingLine) next = section;
      else break;
    }
    // A short final section may never reach the reading line.
    if (window.scrollY > 0 && window.scrollY + window.innerHeight >=
        document.documentElement.scrollHeight - 2) {
      next = sections[sections.length - 1];
    }
    if (next === current) return;
    const activeIndex = sections.indexOf(next);
    sections.forEach((section, index) => {
      const state = index < activeIndex ? 'read' : index === activeIndex ? 'reading' : 'upcoming';
      section.link.dataset.readingState = state;
      section.status.textContent = state === 'read' ? ' — Read' : state === 'reading' ? ' — Reading' : '';
      if (state === 'reading') section.link.setAttribute('aria-current', 'location');
      else section.link.removeAttribute('aria-current');
    });
    current = next;
    const location = document.querySelector('[data-header-section]');
    if (location) {
      const label = current.link.cloneNode(true);
      label.querySelectorAll('.section-reading-status, svg').forEach(node => node.remove());
      location.textContent = label.textContent.trim();
      location.href = current.link.hash;
      location.title = location.textContent;
    }

    // Reveal the marker inside a scrolling desktop sidebar without moving the page
    // or focus. Leave the mobile Browse topics disclosure under the reader's control.
    if (sidebar && matchMedia('(min-width: 1200px)').matches) {
      const item = current.link.getBoundingClientRect();
      const container = sidebar.getBoundingClientRect();
      if (item.top < container.top + 12) sidebar.scrollTop += item.top - container.top - 12;
      else if (item.bottom > container.bottom - 12) {
        sidebar.scrollTop += item.bottom - container.bottom + 12;
      }
    }
  }
  function schedule() {
    if (!frame) frame = requestAnimationFrame(update);
  }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  window.addEventListener('hashchange', schedule);
  window.addEventListener('pageshow', schedule);
  if ('ResizeObserver' in window) new ResizeObserver(schedule).observe(document.querySelector('main'));
  schedule();
})();

// The secondary outline is pinned open on wide screens and optional on smaller ones.
(() => {
  const outline = document.querySelector('[data-page-outline]');
  if (!outline) return;
  const wide = matchMedia('(min-width: 1200px)');
  const update = () => { outline.open = wide.matches; };
  update();
  wide.addEventListener('change', update);
})();

// Keep the sticky header and anchor offsets aligned with wrapped mobile content.
(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const syncHeight = () => document.documentElement.style.setProperty('--header-height', `${header.offsetHeight}px`);
  syncHeight();
  if ('ResizeObserver' in window) new ResizeObserver(syncHeight).observe(header);
})();

// Internal reading references open an offline preview without losing reading position.
(() => {
  const scriptURL = new URL(document.currentScript?.src || 'search.js', location.href);
  let loading, activeLink, panel;
  function load() {
    if (window.NOTES_REFERENCE_PREVIEWS) return Promise.resolve(window.NOTES_REFERENCE_PREVIEWS);
    if (!loading) loading = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = new URL('reference-previews.js', scriptURL).href;
      script.onload = () => resolve(window.NOTES_REFERENCE_PREVIEWS);
      script.onerror = () => reject(new Error('Preview unavailable'));
      document.head.append(script);
    }).catch(error => { loading = null; throw error; });
    return loading;
  }
  function close(restore = false) {
    if (!panel) return;
    panel.remove(); panel = null;
    activeLink?.setAttribute('aria-expanded', 'false');
    activeLink?.removeAttribute('aria-controls');
    if (restore && activeLink?.isConnected) activeLink.focus({ preventScroll: true });
    activeLink = null;
  }
  function position() {
    if (!panel || !activeLink) return;
    const anchor = activeLink.getBoundingClientRect();
    const margin = 12, height = panel.offsetHeight, width = panel.offsetWidth;
    const below = innerHeight - anchor.bottom - margin;
    const top = below >= height ? anchor.bottom + 10 : Math.max(margin, anchor.top - height - 10);
    panel.style.left = `${Math.max(margin, Math.min(anchor.left, innerWidth - width - margin))}px`;
    panel.style.top = `${Math.min(top, Math.max(margin, innerHeight - height - margin))}px`;
  }
  const links = [...document.querySelectorAll('.reading-card a[href]')].filter(link => {
    if (link.closest('.passage-tags')) return false;
    const url = new URL(link.href);
    return !!url.hash && url.protocol === location.protocol && url.host === location.host &&
      url.pathname.startsWith(new URL('.', scriptURL).pathname) && url.pathname.endsWith('.html');
  });
  for (const link of links) {
    link.classList.add('reference-link');
    link.setAttribute('aria-haspopup', 'dialog');
    link.setAttribute('aria-expanded', 'false');
    link.addEventListener('click', async event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      if (activeLink === link) { close(true); return; }
      close(); activeLink = link;
      const url = new URL(link.href);
      const key = url.pathname.split('/').pop() + '#' + decodeURIComponent(url.hash.slice(1));
      panel = document.createElement('div'); panel.id = 'reference-preview';
      panel.className = 'reference-preview'; panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-labelledby', 'reference-preview-title');
      const head = document.createElement('div'); head.className = 'reference-preview-head';
      const title = document.createElement('h2'); title.id = 'reference-preview-title'; title.textContent = link.textContent.trim();
      const dismiss = document.createElement('button'); dismiss.type = 'button'; dismiss.className = 'reference-close';
      dismiss.setAttribute('aria-label', 'Close reference preview'); dismiss.textContent = '×';
      dismiss.addEventListener('click', () => close(true)); head.append(title, dismiss);
      const topic = document.createElement('p'); topic.className = 'reference-preview-topic';
      const body = document.createElement('div'); body.className = 'reference-preview-body';
      body.setAttribute('aria-live', 'polite'); body.textContent = 'Loading reference…';
      const jump = document.createElement('a'); jump.className = 'reference-jump'; jump.href = link.href; jump.textContent = 'Go to section →';
      panel.append(head, topic, body, jump); document.body.append(panel);
      link.setAttribute('aria-expanded', 'true'); link.setAttribute('aria-controls', panel.id);
      position(); dismiss.focus({ preventScroll: true });
      const openedPanel = panel;
      try {
        const data = (await load())[key];
        if (panel !== openedPanel) return;
        body.replaceChildren();
        if (data) {
          title.textContent = data.title; topic.textContent = data.topic;
          for (const text of data.blocks) { const p = document.createElement('p'); p.textContent = text; body.append(p); }
        } else body.textContent = 'This reference has no excerpt yet. Open the section to read it.';
      } catch {
        if (panel !== openedPanel) return;
        body.textContent = 'The preview could not load. You can still open the section.';
      }
      position();
    });
  }
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && panel) { event.preventDefault(); close(true); }
  });
  document.addEventListener('pointerdown', event => {
    if (panel && !panel.contains(event.target) && !activeLink?.contains(event.target)) close();
  });
  document.addEventListener('focusin', event => {
    if (panel && !panel.contains(event.target) && event.target !== activeLink) close();
  });
  window.addEventListener('resize', position);
  window.addEventListener('scroll', () => { if (panel) position(); }, { passive: true });
})();
