# Frontend Interview Notes

An offline study guide for senior and principal engineering interviews, with a frontend focus. Includes 19 engineering topics and a separate System Design track, code examples, full-text search, passage tags, and a guided learning path.

Open `frontend_interview_notes.html` in a browser. No server or build step is required.

## System Design

Open `frontend_interview_notes/system-design.html` or use **System design** in the header. The first worked case is a chat web app, with requirements, estimates, component roles, message flows, consistency, recovery, scaling, and frontend behavior. A second case designs a reusable autocomplete package, including accessibility, async behavior, public exports, and directory structure. Each case includes UI and architecture sketches.

## Editing

Topic pages and shared assets live in `frontend_interview_notes/`. Read `AGENTS.md` for the content and navigation conventions.

The generated pages and search index are committed so the guide works immediately after cloning. After editing content, rebuild from the project root:

```sh
# Requires Python 3 and Pygments for syntax highlighting.
python3 frontend_interview_notes/tools/build_navigation.py
python3 frontend_interview_notes/tools/build_tags.py
python3 frontend_interview_notes/tools/highlight_snippets.py
python3 frontend_interview_notes/tools/build_search_index.py
```

Historical local snapshots in `backups/` are excluded from version control.
