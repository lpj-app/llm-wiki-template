#!/usr/bin/env python3
"""
Validates and (with --fix) auto-repairs hierarchical tags and domain backlinks
across wiki/domains/ and wiki/shared/concepts/. Tags are: life-area,
life-area/domain-name, and subject (read from that domain's overview.md) —
all three fully derivable, no LLM judgment needed.
"""
import re, sys
from pathlib import Path

WIKI_DOMAINS = Path("wiki/domains")
WIKI_SHARED = Path("wiki/shared/concepts")
SKIP_DIRS = {"_template"}

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return None, None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields, m.group(2)

def parse_list(raw):
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [x.strip() for x in inner.split(",") if x.strip()] if inner else []
    return [raw]

_subject_cache = {}
def get_subject(domain):
    if domain in _subject_cache:
        return _subject_cache[domain]
    ov = WIKI_DOMAINS / domain / "overview.md"
    subject = None
    if ov.exists():
        fields, _ = parse_frontmatter(ov.read_text(encoding="utf-8"))
        if fields:
            subject = fields.get("subject")
    if not subject:
        # heuristic fallback: strip a leading code-like token (e.g. "hsm-02-")
        name = domain.split("/")[-1]
        stripped = re.sub(r"^[a-z0-9]+-\d+-", "", name)
        subject = stripped if stripped != name else name
        subject += "  # NEEDS-REVIEW: no subject set in overview.md, guessed from folder name"
    _subject_cache[domain] = subject
    return subject

def expected_tags(domain):
    parts = domain.split("/")
    if len(parts) != 2:
        return None
    subject = get_subject(domain)
    return [parts[0], domain, subject.split("  #")[0]]

def backlink(domain):
    return f"[[wiki/domains/{domain}/overview]]"

def write_back(path, fields, tags, body):
    fields["tags"] = "[" + ", ".join(tags) + "]"
    fm = "\n".join(f"{k}: {v}" for k, v in fields.items())
    path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")

def check_file(path, fix):
    text = path.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)
    if fields is None:
        return []
    domain = fields.get("domain")
    tags = parse_list(fields.get("tags", ""))
    issues = []

    if domain == "shared":
        linked = parse_list(fields.get("linked_domains", ""))
        want_tags = ["shared"]
        for d in linked:
            exp = expected_tags(d)
            if exp:
                want_tags += [t for t in exp if t not in want_tags]
        missing_tags = [t for t in want_tags if t not in tags]
        missing_links = [d for d in linked if backlink(d) not in body]
        if missing_tags:
            issues.append(f"{path}: missing tags {missing_tags}")
        if missing_links:
            issues.append(f"{path}: missing backlinks to {missing_links}")
        if fix and (missing_tags or missing_links):
            tags = want_tags + [t for t in tags if t not in want_tags]
            for d in missing_links:
                body += f"\n{backlink(d)}\n"
            write_back(path, fields, tags, body)
        return issues

    if not domain or path.name == "overview.md":
        return issues
    exp = expected_tags(domain)
    if not exp:
        return issues
    missing_tags = [t for t in exp if t not in tags[:3]]
    link = backlink(domain)
    missing_link = link not in body
    if missing_tags:
        issues.append(f"{path}: missing/misordered tags {exp}")
    if missing_link:
        issues.append(f"{path}: missing domain backlink {link}")
    if "NEEDS-REVIEW" in get_subject(domain):
        issues.append(f"{path}: subject guessed, not set — add subject: to {domain}/overview.md")
    if fix and (missing_tags or missing_link):
        if missing_tags:
            tags = exp + [t for t in tags if t not in exp]
        if missing_link:
            body = body.replace("## Related", f"## Related\n{link}", 1) if "## Related" in body else body + f"\n{link}\n"
        write_back(path, fields, tags, body)
    return issues

def main():
    fix = "--fix" in sys.argv
    issues = []
    for base in (WIKI_DOMAINS, WIKI_SHARED):
        if base.exists():
            for path in base.rglob("*.md"):
                if not any(part in SKIP_DIRS for part in path.parts):
                    issues += check_file(path, fix)
    label = "Fixed" if fix else "Found"
    if issues:
        print(f"{label} {len(issues)} issue(s):")
        for i in issues:
            print(f"  - {i}")
        sys.exit(0 if fix else 1)
    print("All pages have correct hierarchical tags, subject, and domain backlinks.")

if __name__ == "__main__":
    main()
