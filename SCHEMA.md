# Schema & Conventions

## Frontmatter (all wiki pages)
type: entity | concept | source | overview | lernzettel | query
domain: <life-area>/<domain-name>
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | stable
aliases: [] — for entity/concept pages only, alternate names/terms this page is also known as (e.g. a concept taught under different names across courses or years)

## Fixed page bodies

### overview
# <Domain Name> — Overview
## Summary
## Key entities
## Key concepts
## Open questions

### entity / concept
# <Title>
## Summary
## Details
## Related
## Sources
- [[raw/path/to/file.md]] — verified: yes|no — <one-line note>

### source
(frontmatter also includes: raw_path: raw/..., verified: yes|no)
# <Title>
## Summary
## Extracted into
[[wikilinks]] to entity/concept/lernzettel pages this source fed into.

### lernzettel
(frontmatter also includes: exam_date: YYYY-MM-DD or null)
# <Title> — Lernzettel
## Kernpunkte
## Definitionen
## Formeln / Merksätze
## Verweise
## Sources
- [[raw/path/to/file.md]] — verified: yes|no — <one-line note>

### query
# <Question>
## Answer
## Sources
- [[raw/path/to/file.md]] — verified: yes|no — <one-line note>

## Naming
Files: kebab-case.md. Life-area folders: fixed set (arbeit, alltag, schule, studium, projekte, ideen, home, archive). Domain folders inside them: kebab-case, one per concrete topic.

## When to create vs extend
Check wiki/index.md and wiki/shared/concepts/ first. If a close match exists, extend it (log as extend) and bump `updated`. Only create new when the subject is genuinely distinct.
