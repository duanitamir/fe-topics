# Frontend Topics

A browsable engineering reference covering JavaScript, TypeScript, React, browser APIs, networking, security, application patterns and system design. Includes practical examples, connected diagrams, full-text search, contextual reference previews and passage tags.

## Open the guide

Open `index.html` or `frontend_topics.html` in a browser. No server or build step is required. The guide has two areas: **General tech** and **System design**.

For GitHub Pages, publish the `main` branch from the repository root. The root `index.html` opens the guide with relative links that work under the repository URL.

## System design

Open `frontend_topics/system-design.html` or use **System design** in the header. Worked cases cover a chat application, a reusable autocomplete package and dynamic job discovery. Each connects requirements, UI/component structure, API contracts, architecture, data flow, operational concerns and tradeoffs.

## Editing

Topic pages and shared assets live in `frontend_topics/`. Read `AGENTS.md` for content and navigation conventions. Generated pages and indexes are committed so the guide works immediately after cloning.

After editing content, rebuild from the repository root:

```sh
# Requires Python 3 and Pygments for syntax highlighting.
python3 frontend_topics/tools/build_navigation.py
python3 frontend_topics/tools/build_tags.py
python3 frontend_topics/tools/highlight_snippets.py
python3 frontend_topics/tools/build_search_index.py
```

The search rebuild also refreshes offline reference previews. Historical local snapshots in `backups/` are excluded from version control.
