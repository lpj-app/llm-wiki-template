---
description: Scan the whole wiki/ for orphaned pages, dead links, likely duplicates, and stale drafts. Read-only — writes findings to a report, never edits other pages.
---

Scan wiki/ (not raw/) and produce a report. This command is diagnostic only — do not edit, move, or delete any file other than wiki/audit-report.md itself.

Check for:
1. **Orphaned pages** — entity/concept pages with no incoming [[wikilinks]] from any overview.md, other entity/concept page, or lernzettel, and not listed in wiki/index.md as a shared concept.
2. **Dead links** — any [[wikilink]] anywhere in wiki/ pointing to a file that doesn't exist.
3. **Likely cross-domain duplicates** — entity/concept pages in different domains with similar titles, aliases, or overlapping Summary content that aren't yet linked to each other or consolidated in wiki/shared/concepts/.
4. **Stale drafts** — pages with status: draft, listed so a human can decide whether to promote or revisit them.
5. **Broken source references** — any sources/ page whose raw_path no longer resolves to an existing file under raw/.

Write the findings to wiki/audit-report.md, overwriting any previous run, with a timestamp header and one section per check above. For each finding, give the file path(s) and a one-line reason — don't propose or make the fix yourself, this command only reports.

After writing the file, give a short plain-language summary in chat: counts per category, and which ones seem worth acting on first.
