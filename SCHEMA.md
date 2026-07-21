# Schema & Conventions

## Frontmatter (all wiki pages)
type: entity | concept | source | overview | lernzettel | query
domain: <life-area>/<domain-name>
tags: [life-area, life-area/domain-name, subject, ...free-form content tags]
The first three tags are always auto-derived and come first: life-area and life-area/domain-name from the domain field, subject from the domain's overview.md. This is what makes a topic findable across multiple courses/semesters even when their domain slugs differ (e.g. hsm-03-statistik and hsm-06-angewandte-statistik can both carry #statistik). Free-form content tags (topics, concepts) come after those three, however many make sense. Never omit the three hierarchical tags, even if it feels redundant with the domain field — the domain field isn't clickable/searchable in Obsidian's tag pane, the tags are.
linked_domains: [] — required ONLY for pages under wiki/shared/concepts/ (domain: shared). Lists every life-area/domain that references this shared concept, e.g. [studium/hsm-02-mathe, projekte/myvirtualcompany]. Updated every time a new domain starts referencing an existing shared concept.
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | stable
aliases: [] — for entity/concept pages only, alternate names/terms this page is also known as (e.g. a concept taught under different names across courses or years)

## Domain backlink (mandatory on every page)
Every entity, concept, source, lernzettel, and query page must link back to its domain's overview using the FULL vault-relative path, never the short form:
[[wiki/domains/<life-area>/<domain>/overview]]
Never write [[overview]] alone — every domain has a file with that exact name, so a short link is ambiguous the moment more than one domain exists. This backlink goes in the page's existing "Related" section (entity/concept) or as the first line under the header (source/lernzettel/query) if no Related section exists in that page type's fixed body.
For shared concepts (domain: shared), this becomes multiple backlinks — one per entry in linked_domains — placed in the page's Related section, same as a normal concept page, just one line per linked domain instead of one line total.

## Fixed page bodies

### overview
(frontmatter also includes: subject: <plain human-readable field name, e.g. "statistik", "netzwerktechnik" — independent of the domain folder's slug/course-code>)
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
