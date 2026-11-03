// Offline, URL-addressable tag filtering. Native links preserve browser back/forward.
(() => {
  const selected = new URLSearchParams(location.search).get('tag') || '';
  const filters = [...document.querySelectorAll('[data-tag-filter]')];
  const valid = filters.some(link => link.dataset.tagFilter === selected);
  const status = document.querySelector('[data-tag-status]');
  let count = 0;
  const topics = new Set();
  for (const card of document.querySelectorAll('[data-passage-tags]')) {
    const visible = valid && (!selected || card.dataset.passageTags.split(' ').includes(selected));
    card.hidden = !visible;
    if (visible) { count++; topics.add(card.dataset.topic); }
  }
  for (const link of filters) {
    if (valid && link.dataset.tagFilter === selected) link.setAttribute('aria-current', 'true');
  }
  const active = filters.find(link => link.dataset.tagFilter === selected);
  const label = active?.querySelector('.tag-label')?.textContent.trim();
  status.textContent = !valid ? 'Unknown tag. Choose a tag above or select All explanations.'
    : `${count} ${count === 1 ? 'explanation' : 'explanations'}${selected ? ' tagged “' + label + '”' : ''} across ${topics.size} ${topics.size === 1 ? 'topic' : 'topics'}.`;
})();
