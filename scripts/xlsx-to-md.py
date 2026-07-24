#!/usr/bin/env python3
"""
Convert .xlsx to Markdown tables using stdlib 
Usage: xlsx-to-md.py <input.xlsx> <output.md>
       xlsx-to-md.py --selftest
"""
import io
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
R_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def col_to_index(ref):
    letters = re.match(r"[A-Za-z]+", ref).group()
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch.upper()) - ord("A") + 1)
    return idx - 1


def load_shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.findall(".//m:t", NS))
            for si in root.findall("m:si", NS)]


def load_sheets(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rel_map = {r.get("Id"): r.get("Target") for r in rels}
    sheets = []
    for sheet in wb.findall(".//m:sheets/m:sheet", NS):
        target = rel_map.get(sheet.get(R_ID))
        if target:
            sheets.append((sheet.get("name"), "xl/" + target.lstrip("/")))
    return sheets


def cell_value(c, shared):
    v = c.find("m:v", NS)
    if v is None:
        t = c.find("m:is/m:t", NS)
        return t.text if t is not None else ""
    val = v.text or ""
    if c.get("t") == "s" and val.isdigit() and int(val) < len(shared):
        return shared[int(val)]
    return val


def sheet_to_rows(z, path, shared):
    root = ET.fromstring(z.read(path))
    rows = []
    for row in root.findall(".//m:sheetData/m:row", NS):
        cells, maxcol = {}, -1
        for c in row.findall("m:c", NS):
            idx = col_to_index(c.get("r"))
            cells[idx] = cell_value(c, shared).replace("|", "\\|").replace("\n", " ")
            maxcol = max(maxcol, idx)
        rows.append([cells.get(i, "") for i in range(maxcol + 1)])
    return rows


def rows_to_markdown(rows):
    if not rows:
        return "_(empty sheet)_\n"
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    header, *body = rows
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join(["---"] * width) + " |"]
    lines += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(lines) + "\n"


def convert(z):
    shared = load_shared_strings(z)
    out = []
    for name, path in load_sheets(z):
        out.append(f"## {name}\n")
        out.append(rows_to_markdown(sheet_to_rows(z, path, shared)))
    return "\n".join(out)


def selftest():
    parts = {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
</Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""",
        "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>
</workbook>""",
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>""",
        "xl/sharedStrings.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="1" uniqueCount="1">
<si><t>Name</t></si>
</sst>""",
        "xl/worksheets/sheet1.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="str"><v>Age</v></c></row>
<row r="2"><c r="A2" t="str"><v>Alice</v></c><c r="B2"><v>30</v></c></row>
</sheetData>
</worksheet>""",
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, content in parts.items():
            z.writestr(name, content)
    buf.seek(0)
    with zipfile.ZipFile(buf) as z:
        result = convert(z)
    expected = "## Sheet1\n\n| Name | Age |\n| --- | --- |\n| Alice | 30 |\n"
    assert result == expected, f"selftest mismatch:\n{result!r}\n!=\n{expected!r}"
    print("selftest OK")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        selftest()
        return
    if len(sys.argv) != 3:
        sys.exit("Usage: xlsx-to-md.py <input.xlsx> <output.md>")
    with zipfile.ZipFile(sys.argv[1]) as z:
        markdown = convert(z)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(markdown)


if __name__ == "__main__":
    main()
