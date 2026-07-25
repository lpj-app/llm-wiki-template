# Schema & Conventions

## Frontmatter (all wiki pages)
type: entity | concept | source | overview | lernzettel | query
domain: <life-area>/<domain-name>
tags: [life-area, life-area/domain-name, subject, ...free-form content tags]
The first three tags are always auto-derived and come first: life-area and life-area/domain-name from the domain field, subject from the domain's overview.md. This is what makes a topic findable across multiple courses/semesters even when their domain slugs differ (e.g. hsm-03-statistik and hsm-06-angewandte-statistik can both carry #statistik). Free-form content tags (topics, concepts) come after those three, however many make sense. Never omit the three hierarchical tags, even if it feels redundant with the domain field — the domain field isn't clickable/searchable in Obsidian's tag pane, the tags are.
For domains that are a coding project (almost always life-area projekte, but any domain with real source code qualifies): after subject, add one further tag per programming language actually used in the project's source files — one language, one tag; multiple languages, multiple tags (e.g. python, java, typescript, csharp, cpp, c, php, html, css, bash, powershell, sql, kotlin, swift, dart, nix). Base this on the real source files in raw/, not build/config file extensions (a lone eslint.config.js in an otherwise all-TypeScript project doesn't earn a javascript tag). Apply consistently across every page of the domain (overview/entity/concept/source), not just overview.md. A domain with no actual code (design assets, pure docker-compose/config, an empty scaffold) simply gets no language tag — that's correct, not a gap.
Keep tags atomic, and don't let subject silently duplicate one: before finalizing subject, check it doesn't just restate a language tag the domain already carries (e.g. subject browser-spiele-javascript next to tag javascript — drop the language part from subject, the tag already covers it). Prefer English for added atomic tags unless a German term is clearly more natural for that concept (mixed-language tags across the wiki are fine, en bloc consistency is not required). subject may still be a short compound phrase (e.g. web-app-entwicklung, 2fa-hardware-token) — that's fine, it's one concept and its job is cross-domain topic-matching, not atomicity. Only split it further when it's genuinely bundling two independent, separately-useful facets (e.g. platform + genre, like "browser" + "game" for a browser game) — in that case add both as their own atomic tags in addition to subject, rather than inventing an ever-longer compound subject string.
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
Files: kebab-case.md. Life-area folders: fixed set, see LIFE_AREAS in .wiki.conf. Domain folders inside them: kebab-case, one per concrete topic.

## When to create vs extend
Check wiki/index.md and wiki/shared/concepts/ first. If a close match exists, extend it (log as extend) and bump `updated`. Only create new when the subject is genuinely distinct.
