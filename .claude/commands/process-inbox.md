---
description: Process everything currently sitting in raw/inbox/ — convert, classify, ingest.
---

Follow the "Path A — /process-inbox" workflow defined in AGENTS.md exactly, for every file currently in raw/inbox/ (recurse into subfolders if any exist, ignore dotfiles and anything already marked .converted-*).

Do not ask for confirmation before creating a new domain or converting a file — use the defaults and judgment calls defined in AGENTS.md. Only pause and ask if a file's domain is a genuine toss-up between two very close existing domains.

When done, report back in plain language, no jargon:
- How many files were processed
- Which domain each one went to (flag new domains as "created new")
- Anything skipped, and why

Do not narrate your internal steps unless asked — just do the work and give the summary.
