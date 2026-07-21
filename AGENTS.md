# Agent Instructions — LLM Wiki

## Purpose
This repo is a self-maintaining personal knowledge base covering everything: work, daily life, school, university, projects, ideas, home. Raw material comes in once and never changes. You (the agent) read it, extract what matters, and keep a clean, cross-linked wiki of it. The wiki is what gets queried — not the raw folder.

## Layers
- wiki/domains/<life-area>/<domain>/ — one folder per concrete topic (e.g. domains/schule/mathe/, domains/projekte/myvirtualcompany/). Life-areas (arbeit, alltag, schule, studium, projekte, ideen, home, archive) are pure organization, not domains themselves — never put wiki pages directly in a life-area folder, always one level deeper in a named domain.
- wiki/shared/concepts/ — concepts that recur across more than one domain live here instead of being duplicated.

## Raw material — two entry points
raw/ has no fixed subfolder taxonomy. It only has two kinds of content:
1. raw/inbox/ — the single, simple drop point. Anything lands here without whoever dropped it needing to know a domain or file type: PDFs, scans, docx, plain text, anything.
2. raw/<life-area>/<domain>/ — already-sorted material. Either created by you during processing, or placed there manually by someone who already knows exactly which domain a file belongs to.

Both are valid ingest sources, handled by two workflows that converge on the same steps. raw/ is read-only once a file is filed under raw/<life-area>/<domain>/ — NEVER edit or delete anything there, regardless of what's asked, unless the human explicitly requests raw-folder cleanup as its own separate task. After converting or moving any file into a raw/<life-area>/<domain>/ location, run chmod 444 on it immediately — this is a local safety net in addition to the pre-commit hook, in case a file gets touched before it's committed.

### Path A — /process-inbox (no domain knowledge required)
Triggered by the /process-inbox slash command. For every file in raw/inbox/:
1. If it isn't already plain text/Markdown, convert it to Markdown yourself using pandoc via the Bash tool. If a format can't be converted automatically (e.g. a scan needing OCR), skip it and report why instead of guessing at content.
2. Decide which life-area and domain it belongs to. Check wiki/index.md and existing domain overviews first. If a close match exists, use it. If nothing fits, create a new domain (copy wiki/domains/_template/, pick a sensible kebab-case name, add it to wiki/index.md) rather than forcing a bad fit. Don't ask unless it's a genuine toss-up between two very close existing domains.
3. Move the converted file from raw/inbox/ into raw/<life-area>/<domain>/.
4. Run the ingest workflow (below) on it.
5. Once inbox is empty, report a short plain-language summary: how many files, which domain each went to, which domains were newly created, anything skipped and why.

### Path B — direct path ingest (domain already known)
Triggered when asked to "ingest <path>" where <path> is either a single file or a folder under raw/<life-area>/<domain>/. The domain is already fixed by the path — no classification step needed, unlike Path A.

**Single file:** convert it first if it isn't Markdown yet, then run the ingest workflow directly against that domain.

**Folder:**
1. Recursively list all files in the folder (skip hidden files and anything named .converted-*).
2. For each file, check whether it's already referenced as a raw_path in any existing wiki/domains/<life-area>/<domain>/sources/*.md frontmatter. If yes, skip it — it's already ingested.
Note: this skip applies only to re-summarizing the raw file itself. It does not freeze the entity/concept pages that file originally contributed to — those stay fully open to being extended by newly ingested files, per step 2 of the shared ingest workflow.
3. Convert any remaining files that aren't already Markdown.
4. If more than 25 files remain to be newly ingested, stop and ask whether to process all of them now in this session or split into smaller batches — do not silently attempt a huge batch in one go, quality degrades. For 25 or fewer, just proceed.
5. Run the ingest workflow on each remaining file in turn, same domain for all of them since the folder already fixes it.
6. Report a summary: how many files were newly ingested, how many were skipped as already-done, and the resulting overview.md/lernzettel updates.

## Ingest workflow (shared by both entry points)
0. Before writing any page's frontmatter, derive its two hierarchical tags from the domain it belongs to (life-area, life-area/domain-name) and place them first in tags. Before finishing any page, confirm it links back to [[wiki/domains/<life-area>/<domain>/overview]] using the full path — this is not optional, check it explicitly, don't rely on remembering to add it naturally.
1. Write a summary page under the domain's sources/, citing the raw file path, with verified: no in frontmatter. For a folder-level Path B ingest, steps 1-5 repeat per new file, but wiki/index.md and wiki/log.md are updated once at the end, not per file, to avoid redundant writes.
2. Create or update entities/ and concepts/ pages. Before creating any new page, actively check for an existing match in this order: (a) list this domain's entities/ and concepts/ folders directly — don't rely solely on wiki/index.md, which can lag behind recent changes, (b) check wiki/shared/concepts/, (c) check wiki/index.md as a final cross-check across other domains. If a match exists, even a partial or older one, do not create a duplicate — update the existing page instead: append the new raw source as an additional line in its Sources section, extend Summary/Details if the new source adds real information, and bump `updated`. A raw file being skipped as already-ingested (see Path B) never means the entity/concept pages it originally fed into are frozen — extending old pages with new sources is the primary mechanism that keeps the wiki connected over years, not a separate or optional step. When comparing against existing pages, don't rely on filename matching alone — check each candidate page's aliases field, and if a filename doesn't match but the topic plausibly could be the same thing (e.g. 'Differentiationsregeln' vs. an existing 'ableitungsregeln.md'), open the candidate page and compare its title/Summary before deciding it's genuinely new. If it turns out to be the same concept under a different name, add the new name to that page's aliases field instead of creating a duplicate.
3. Update the domain's overview.md if this source changes the synthesis, and its lernzettel/ if applicable.
4. Update wiki/index.md: add or refresh this domain's one-line entry under Active/Archived domains. Never list individual pages here — a domain's own overview.md and its entities/concepts/sources folders are the record of what's inside it. wiki/index.md only tracks which domains and shared concepts exist and where their overview lives.
5. Append one line to wiki/log.md.

## Domains
domains/<life-area>/<name>/overview.md — evolving synthesis of this domain, the "front page"
domains/<life-area>/<name>/entities/ — people, tools, orgs, models, projects, one file each
domains/<life-area>/<name>/concepts/ — domain-specific ideas/techniques/terms, one file each
domains/<life-area>/<name>/sources/ — one summary page per raw/ source assigned to this domain
domains/<life-area>/<name>/lernzettel/ — condensed exam-prep pages, derived from this domain's concepts (see below)
domains/<life-area>/<name>/queries/ — optional, notable Q&A worth keeping verbatim

To create a new domain: copy wiki/domains/_template/ into wiki/domains/<life-area>/<new-name>/, fill in overview.md, add an entry to wiki/index.md under "Active domains."

## Shared concepts
Before creating a new concept page inside a domain: check wiki/shared/concepts/ first. If a concept already exists there, link to it instead of duplicating. If a concept that exists in one domain turns out to be relevant in a second domain, move it to wiki/shared/concepts/, update both domains to link to the shared version, and log the move in wiki/cross-links.md. Never let the same concept exist as separate pages in two domains.
When moving a concept into wiki/shared/concepts/, set domain: shared and populate linked_domains with every domain that references it. Don't worry about getting tags/backlinks perfectly right by hand here — scripts/validate-wiki.py --fix runs automatically on commit and will correct anything missed.

## Lernzettel
A lernzettel is NOT a fresh synthesis from raw/ — it's a condensed, exam-oriented distillation of concepts that already exist in this domain (or in shared/). Bullet points, definitions, formulas — no prose synthesis. When an ingest updates a concept that a lernzettel depends on, check whether the lernzettel needs updating too.

## Verification
You may write verified: no on any source citation or source page — that's the default and it's fine. You must NEVER write verified: yes yourself, under any circumstance, even if the source seems unambiguous. Only the human flips that flag, after checking the wiki page against the raw source themselves. If asked to "verify" something, explain what you checked instead of setting the flag.

## Fixed page structure
Every wiki page follows the exact section layout defined in SCHEMA.md for its type. Do not freelance the structure — if a page needs something SCHEMA.md doesn't cover, flag it instead of improvising a new layout.

## Cross-linking
Use [[wikilinks]] for any reference, inside or across domains/life-areas. Whenever a link crosses a domain boundary, also add one line to wiki/cross-links.md.
Format: [YYYY-MM-DD] domain-a/page.md -> domain-b/page.md | one-line reason

## Logging
One line per action in wiki/log.md: ## [YYYY-MM-DD] action | domain | subject
Actions: ingest, create, extend, cross-link, move-to-shared, archive.
Use "create" only for a genuinely new entity/concept/domain. Use "extend" when an existing entity/concept page gets a new source appended — this is the action that shows a concept growing over time across multiple ingests, and it should be the more common of the two once a domain has some history.
Rotate to log-YYYY.md past ~500 entries.

## Archiving
When a domain is finished (course completed, project closed), move its folder to wiki/domains/archive/<life-area>/<name>/ as-is. Do not move any concepts it references out of wiki/shared/concepts/ — those stay active and linkable.

## On automated graph tools (Graphify, etc.)
Not part of this setup and not required for it to work. Tags + backlinks + the shared-concepts rule above are the connection mechanism for now. If a graph-extraction pass is added later, treat it as a periodic external audit that suggests cross-links.md entries and shared/ moves — never as something that edits wiki/ pages directly without going through this same workflow.
