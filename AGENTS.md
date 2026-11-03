## Frontend topics: editing policy

These user-requested instructions apply to the `frontend_topics.html` index and all topic pages in `frontend_topics/` in this project, in this and future sessions.

- Read the existing document before editing. Enrich the matching topic or subtopic instead of duplicating explanations. Add a new topic only when no suitable one exists; cross-link related concepts.
- Use simple, clear explanations with principal-engineer depth: accurate mechanisms, diagnosis, tradeoffs, and practical examples without unnecessary length.
- Always preserve professional terminology. Name each mechanism explicitly and explain it in plain language (for example, output encoding, HTML sanitization, parameter binding, reconciliation, forced synchronous layout). Do not replace precise terms with vague analogies.
- Keep technical claims and examples accurate, including distinctions between related concepts. Preserve existing content and the established page structure outside the requested scope.
- Update sidebar navigation for new sections; verify HTML structure, unique IDs, and working fragment targets. Summarize substantive additions and their locations in the final response.

- The notes are now a multi-page site: `frontend_topics.html` is the index; `frontend_topics/*.html` contain individual topics; `frontend_topics/styles.css` is shared styling. Preserve this structure and keep each topic’s content in one canonical page. Update the index, navigation, and cross-page fragment links when adding topics. The index script maps legacy single-page anchors to topic pages; extend that map for any new index-compatible anchors.

- Code snippets must have accurate language classes and visible language labels with offline syntax highlighting. Keep diagrams labeled as diagrams, not code. Shared token styles live in `frontend_topics/syntax.css`; regenerate colored spans with `frontend_topics/tools/highlight_snippets.py` using a Python environment with Pygments (currently `/Users/tduani/.local/pipx/venvs/zalando-cli-bundle/bin/python`). Preserve decoded snippet text when highlighting, and classify any new snippet languages accurately in the generator.

- Connect related concepts with contextual cross-references at the point of use, targeting the precise section or paragraph (add descriptive IDs when necessary). Explain why a linked concept matters; preserve one canonical explanation instead of repeating it. Add return references when useful, validate all cross-page targets, and retain index compatibility mappings for new anchors.

- React Hooks entries use a consistent study structure: Purpose; When to use; Example with explanation; When not to use & alternatives; Benefits & tradeoffs; Pitfalls & guarantees; Related concepts. Keep each hook individually anchored and listed in the hook index. Preserve category anchors and distinguish limitations/tradeoffs from implementation mistakes.

- Offline full-text search is available from every page via `search.html`, `search.js`, and the generated `search-index.js`. After content edits, run syntax highlighting first, then `python3 frontend_topics/tools/build_search_index.py` to refresh searchable passages and generated deep-link IDs. Never hand-edit the generated index. Keep search results inclusive of all topic text and code, with direct passage links, and validate index targets after rebuilding.

- The learning path is grouped as Language foundations → Browser foundations → React application design → API implementation → Production quality, recorded in `frontend_topics/topics.json`. Keep topic navigation, index groups, and previous/next links in that order. Within a page, introduce mental models before implementation, place tradeoffs next to their mechanism, and put review at the end. Use h1 for the page title, h2 for main sections, h3 for subsections (h4 within structured hook entries). Each topic has a collapsible On this page outline. Preserve existing authored and generated IDs during moves; the syntax/search rebuild tools now retain deep-link IDs.

- Preserve the user’s preferred sidebar behavior: on every topic page, show ordered subtopic links in the dedicated On this page secondary sidebar. The primary sidebar contains topic links only (this supersedes the earlier inline-subtopics preference). Keep these links synchronized with the page outline after any reorganization; retain the grouped learning path and mobile Browse topics control.

- Present explanatory flows as semantic HTML figures using the shared `.flow-diagram` components (ordered steps, parallel outcomes, timelines), not ASCII diagrams in code blocks. Preserve technical detail and existing deep-link IDs. Figures must remain readable on mobile and be indexed as Diagram passages by the search builder; actual source examples retain syntax highlighting.

- Preserve the shared sidebar scrollspy in `search.js`: mark exactly one current subsection with `aria-current="location"` as the reader scrolls, including direct fragment/search destinations and short final sections. Keep the selected topic's `aria-current="page"`, visible active styling, and mobile disclosure behavior intact.

- Sidebar progress is position-based, not persisted completion: earlier subsections show Read, the current subsection Reading, and later subsections no status. Recompute reversibly when scrolling upward; use accessible status text without visible repeated labels. Preserve the quiet progress rail: checkmarks for earlier sections, an accent dot and soft highlight for the current section, and outlined upcoming markers. Avoid bold/underline status styling; respect reduced motion.

- Topic pages use a plain `.topic-introduction` followed by separate `.reading-card` sections for each h2, inside a transparent `.topic-page` wrapper. Preserve chapter grouping, text, anchors, sidebar progress, and search coverage; avoid restoring one large enclosing surface.

- On wide screens (1200px+), On this page lives in a sticky secondary sidebar to the left of the reading cards, between the primary topic navigation and content. At narrower widths it becomes an expandable outline above the cards. Keep a single outline DOM with existing passage IDs, active/read progress, and no duplicate subsection list in the primary topic sidebar.

- Passage tags use the controlled vocabulary and explicit paragraph/h3-to-tags mapping in `frontend_topics/tags.json` (one to three tags at the precise explanation). Run `tools/build_tags.py` after editing tags or tagged prose/headings, then syntax highlighting when code changed, then `tools/build_search_index.py`. The tag builder generates passage tag links, the offline `tags.html` browser, and its navigation links; do not hand-edit generated passage tags/results. Tag browsing is passage-level and separate from passage search; exclude `tags.html` from the search index. Preserve sidebar scrollspy and the single On this page outline.

- Tags belong at the specific definition, mechanism, or h3 subsection, not every h2/card header. Preserve exact passage deep links in tag results; do not infer that every concept in a broad card shares its tags. Use `tags.json` passages as the explicit source of truth.

- General design discussion foundations now include JavaScript, async programming, TypeScript, HTTP/networking, accessibility, build tooling, backend/API fundamentals, and GraphQL. Keep these distinct from the separate System Design track; cross-reference their canonical mechanisms from React/pattern pages instead of repeating them. New pages have explicitly declared per-snippet languages honored by the highlighter.

- Primary topic navigation uses native expandable chapter groups (`details.nav-group`): open the current topic’s chapter by default, with indented topic links, topic counts, and a clear active marker. Keep General tech and Browse by tag in `.navigation-tools`, separate from chapters; the search form replaces the duplicate search link. Preserve this structure when regenerating navigation or tags. The primary desktop sidebar is 260px; the secondary On this page sidebar remains separate.

- Search lives in the shared sticky `.site-header`, not the primary sidebar. Keep one search input per page and the Ctrl/⌘ K shortcut. The header trail displays topic → current h2 subsection, updated by the same scrollspy as On this page. Preserve header-aware anchor offsets and sidebar sticky heights; mobile header stacks the location above search. The tag generator must preserve this shell and use the correct Browse by tag header label.

- General tech and Browse by tag now belong in `.header-links` in the sticky header, not the topic sidebar. Preserve the `<!-- header-links -->` insertion marker used by the tag generator. Primary sidebar contains topic chapters only.

- Keep the primary sidebar focused on topic navigation: do not restore the Frontend Topics brand title or Concepts, examples, and design discussion answers description.

- Project root: `the repository root`. Open `frontend_topics.html` as the entry point. Historical snapshots are in `backups/`; edit the active guide only.

- Node.js runtime has its own API implementation page; reference the existing browser event-loop foundation rather than duplicating it. Routing & Navigation follows application patterns and references canonical URL-state ownership. JavaScript mechanics owns property descriptors, coercion, iteration protocols, and module evaluation; TypeScript owns variance, overloads, type transformations, and reusable component typing.

- System Design is a separate study area: `system-design.html` is its entrance and `system-design-chat.html` is the first worked case. In `topics.json`, groups with `area: "system-design"` have their own sidebar and previous/next sequence. Engineering groups default to `engineering`. Keep the general learning-path index separate; connect tracks through the header, search, tags, and precise references. Run `tools/build_navigation.py` before tags/highlighting/search after navigation changes. Preserve all previous anchors and use original worked examples with explicit assumptions and tradeoffs.

- System Design uses four explicit design discussion stages: Understand the problem → Propose high-level design → Design deep-dive → Wrap up. Keep reusable UI/UX, REST/idempotency, consistency, architecture/load-balancing, caching/CDN, monitoring, and fallback principles in the fundamentals page; apply them concretely in cases with precise cross-references.

- Technology/pattern comparisons should compare solutions to the same problem, identify overlapping versus complementary responsibilities, explain when each earns its cost, and link to canonical mechanisms. State Ownership contains the hooks/state taxonomy and Context/useReducer vs Redux Toolkit vs XState/query-cache comparisons; Application Patterns contains same-problem and checkout alternatives. Avoid presenting hooks versus state or Context versus statecharts as mutually exclusive categories.

- Every System Design case study includes a static UI wireframe, a labeled architecture/data-flow sketch, and an illustrative directory layout with dependency/ownership explanations. Use semantic HTML figures, not ASCII code blocks. Reusable Autocomplete is the component/package design case; distinguish framework-independent core, framework adapter, optional presentation, and host-owned data/auth/cache contracts.

- Case-study sketches must include connected box-and-arrow diagrams for page/component structure, module/service architecture, and a critical interaction sequence. Label communication arrows and state ownership; provide accessible descriptions, readable mobile scrolling, and full-size offline SVG links. Wireframes and directory layouts supplement these diagrams.

- The two user-facing study areas are “General tech” and “System design”. Use these labels consistently in the header, area entrances and navigation generators; do not label General tech as Learning path.

- Internal fragment references inside reading cards open an accessible offline contextual preview on ordinary click, with an explicit Go to section link. Preserve modified-click navigation, Escape/outside dismissal, focus restoration, mobile containment, and original href fallback. Preview excerpts are generated from canonical passages by tools/build_reference_previews.py, automatically invoked by build_search_index.py; never hand-edit reference-previews.js.

- React Rendering order: overview → update cycle → Server/Client execution comparison → dedicated Server and Client cards → boundary rules/composition → CSR/SSR → hydration → streaming → combined lifecycle → error recovery → choices → recap. Keep definitions before delivery mechanisms and preserve all original anchors when reorganizing.

- Application Design Patterns follows Foundations → Code-level patterns → Architecture and evolution → Distributed workflows and recovery → Compare and review. Keep SOLID in one reading card, with each principle immediately followed by its meaning and before/after example, place the common-use lookup near the end, and preserve the grouped secondary outline with short labels and one link per reading card.

- Present this repository as a general engineering reference. Use Frontend Topics branding and the General tech / System design areas; keep prose, README, filenames, navigation, generated indexes and tooling free of recruiting/preparation framing.

- The canonical Git remote for this project is git@github.com:duanitamir/fe-topics.git (origin), owned by the personal duanitamir account. Always use this remote for this repository and keep the repository private. Do not push to the previous work-account repository or enable public publishing without an explicit request. Repository-local SSH configuration selects the personal account key.
