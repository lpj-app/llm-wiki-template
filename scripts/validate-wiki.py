#!/usr/bin/env python3
"""
Checks/fixes hierarchical tags and domain backlinks in wiki/domains/ and
wiki/shared/concepts/. Both are derivable from `domain` (or `linked_domains`),
so no LLM judgment is needed. Only the tags line is rewritten; every other
frontmatter field passes through untouched.

Usage:
  python3 scripts/validate-wiki.py --check   # report only, exit 1 if violations
  python3 scripts/validate-wiki.py --fix     # auto-repair in place
"""
import re, sys
from pathlib import Path

WIKI_DOMAINS = Path("wiki/domains")
WIKI_SHARED = Path("wiki/shared/concepts")
SKIP_DIRS = {"_template"}

def parse_list(raw):
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [x.strip() for x in inner.split(",") if x.strip()] if inner else []
    return [raw]

def get_scalar(fm_lines, key):
    for line in fm_lines:
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip()
    return None

def get_tags_block(fm_lines):
    """Returns (start, end, tags) for the tags field, single- or multi-line."""
    for i, line in enumerate(fm_lines):
        if line.startswith("tags:"):
            rest = line.split(":", 1)[1].strip()
            if rest.startswith("["):
                inner = rest[1:-1] if rest.endswith("]") else rest[1:]
                tags = [t.strip() for t in inner.split(",") if t.strip()]
                return i, i, tags
            tags = []
            j = i + 1
            while j < len(fm_lines) and fm_lines[j].strip().startswith("- "):
                tags.append(fm_lines[j].strip()[2:].strip())
                j += 1
            return i, j - 1, tags
    return None, None, []

def set_tags(fm_lines, start, end, new_tags):
    new_line = "tags: [" + ", ".join(new_tags) + "]"
    return fm_lines[:start] + [new_line] + fm_lines[end + 1:]

def expected_tags(domain):
    parts = domain.split("/")
    return [parts[0], domain] if len(parts) == 2 else None

def backlink(domain):
    return f"[[wiki/domains/{domain}/overview]]"

def write_back(path, fm_lines, body):
    fm = "\n".join(fm_lines)
    path.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")

def check_file(path, fix):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return []
    fm_lines = m.group(1).split("\n")
    body = m.group(2)
    domain = get_scalar(fm_lines, "domain")
    tag_start, tag_end, tags = get_tags_block(fm_lines)
    issues = []

    if domain == "shared":
        linked = parse_list(get_scalar(fm_lines, "linked_domains") or "")
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
            new_tags = want_tags + [t for t in tags if t not in want_tags]
            if tag_start is not None:
                fm_lines = set_tags(fm_lines, tag_start, tag_end, new_tags)
            for d in missing_links:
                body += f"\n- {backlink(d)}\n"
            write_back(path, fm_lines, body)
        return issues

    if not domain or path.name == "overview.md":
        return issues
    exp = expected_tags(domain)
    if not exp:
        return issues
    missing_tags = [t for t in exp if t not in tags[:2]]
    link = backlink(domain)
    missing_link = link not in body
    if missing_tags:
        issues.append(f"{path}: missing/misordered tags {exp}")
    if missing_link:
        issues.append(f"{path}: missing domain backlink {link}")
    if fix and (missing_tags or missing_link):
        if missing_tags:
            new_tags = exp + [t for t in tags if t not in exp]
            if tag_start is not None:
                fm_lines = set_tags(fm_lines, tag_start, tag_end, new_tags)
        if missing_link:
            body = body.replace("## Related", f"## Related\n- {link}", 1) if "## Related" in body else body + f"\n{link}\n"
        write_back(path, fm_lines, body)
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
    print("All pages have correct hierarchical tags and domain backlinks.")

if __name__ == "__main__":
    main()
