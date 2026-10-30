# Frontend Interview Notes

An offline study guide for senior and principal engineering interviews, with a frontend focus. Includes 19 topics, code examples, full-text search, passage tags, and a guided learning path.

Open `frontend_interview_notes.html` in a browser. No server or build step is required.

## Editing

Topic pages and shared assets live in `frontend_interview_notes/`. Read `AGENTS.md` for the content and navigation conventions.

The generated pages and search index are committed so the guide works immediately after cloning. After editing content, rebuild from the project root:

```sh
# Requires Python 3 and Pygments for syntax highlighting.
python3 frontend_interview_notes/tools/build_tags.py
python3 frontend_interview_notes/tools/highlight_snippets.py
python3 frontend_interview_notes/tools/build_search_index.py
```

Historical local snapshots in `backups/` are excluded from version control.
