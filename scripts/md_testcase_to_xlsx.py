#!/usr/bin/env python3
import html
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def clean_cell(value):
    value = value.strip()
    value = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    value = re.sub(r"\\([|_\-+])", r"\1", value)
    return html.unescape(value)


def split_md_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells = []
    cur = []
    escaped = False
    for ch in line:
        if escaped:
            cur.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == "|":
            cells.append(clean_cell("".join(cur)))
            cur = []
        else:
            cur.append(ch)
    cells.append(clean_cell("".join(cur)))
    return cells


def is_separator(line):
    cells = split_md_row(line)
    return all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells if c.strip())


def extract_table_after(lines, heading):
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    if start is None:
        return []
    table_lines = []
    in_table = False
    for line in lines[start + 1 :]:
        if line.startswith("# ") and in_table:
            break
        if line.strip().startswith("|"):
            in_table = True
            if not is_separator(line):
                table_lines.append(line)
        elif in_table:
            break
    return [split_md_row(line) for line in table_lines]


def extract_open_questions(lines):
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "# Open Questions":
            start = i
            break
    if start is None:
        return []
    questions = []
    for line in lines[start + 1 :]:
        if line.startswith("# "):
            break
        if line.strip().startswith("- "):
            questions.append([clean_cell(line.strip()[2:])])
    return [["Open Question"]] + questions


def get_xml_text(text):
    if text is None:
        return ""
    return escape(str(text), {'"': "&quot;"})


def make_sheet_xml(rows, widths=None, frozen=True, autofilter=True):
    max_cols = max((len(r) for r in rows), default=1)
    widths = widths or {}
    xml = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        "<sheetViews><sheetView workbookViewId=\"0\">",
    ]
    if frozen and len(rows) > 1:
        xml.append('<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>')
    xml.append("</sheetView></sheetViews>")
    xml.append("<cols>")
    for c in range(1, max_cols + 1):
        width = widths.get(c, 18)
        xml.append(f'<col min="{c}" max="{c}" width="{width}" customWidth="1"/>')
    xml.append("</cols>")
    xml.append("<sheetData>")
    for r_idx, row in enumerate(rows, 1):
        height = 24 if r_idx == 1 else 42
        xml.append(f'<row r="{r_idx}" ht="{height}" customHeight="1">')
        for c_idx in range(1, max_cols + 1):
            value = row[c_idx - 1] if c_idx <= len(row) else ""
            ref = f"{col_letter(c_idx)}{r_idx}"
            style = 1 if r_idx == 1 else 2
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                xml.append(f'<c r="{ref}" s="{style}"><v>{value}</v></c>')
            else:
                text = get_xml_text(value)
                xml.append(f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>')
        xml.append("</row>")
    xml.append("</sheetData>")
    if autofilter and len(rows) > 1:
        xml.append(f'<autoFilter ref="A1:{col_letter(max_cols)}{len(rows)}"/>')
    xml.append("</worksheet>")
    return "".join(xml)


def styles_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Calibri"/></font>
    <font><sz val="10"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFD9E2EC"/></left>
      <right style="thin"><color rgb="FFD9E2EC"/></right>
      <top style="thin"><color rgb="FFD9E2EC"/></top>
      <bottom style="thin"><color rgb="FFD9E2EC"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def content_types(sheet_count):
    overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, sheet_count + 1):
        overrides.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        + "".join(overrides)
        + "</Types>"
    )


def workbook_xml(sheet_names):
    sheets = []
    for i, name in enumerate(sheet_names, 1):
        sheets.append(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>" + "".join(sheets) + "</sheets></workbook>"
    )


def workbook_rels(sheet_count):
    rels = []
    for i in range(1, sheet_count + 1):
        rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>')
    rels.append(f'<Relationship Id="rId{sheet_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>"


def root_rels():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


def core_xml():
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:creator>QA Copilot</dc:creator>
  <cp:lastModifiedBy>QA Copilot</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>"""


def app_xml(sheet_names):
    names = "".join(f"<vt:lpstr>{escape(n)}</vt:lpstr>" for n in sheet_names)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>QA Copilot</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{len(sheet_names)}</vt:i4></vt:variant></vt:vector></HeadingPairs>
  <TitlesOfParts><vt:vector size="{len(sheet_names)}" baseType="lpstr">{names}</vt:vector></TitlesOfParts>
</Properties>"""


def main():
    if len(sys.argv) != 3:
        print("Usage: md_testcase_to_xlsx.py input.md output.xlsx", file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    lines = src.read_text(encoding="utf-8").splitlines()

    req = extract_table_after(lines, "# Requirement Summary")
    risk = extract_table_after(lines, "# Risk Assessment")
    trace = extract_table_after(lines, "# Traceability Matrix")
    cases = extract_table_after(lines, "# Test Case")
    questions = extract_open_questions(lines)
    stats = extract_table_after(lines, "# Statistics")

    summary = [
        ["Metric", "Value"],
        ["Source Markdown", str(src)],
        ["Generated At", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Requirements", max(0, len(req) - 1)],
        ["Test Cases", max(0, len(cases) - 1)],
        ["Open Questions", max(0, len(questions) - 1)],
    ]
    if stats:
        summary += [["", ""]] + stats

    sheets = [
        ("Summary", summary, {1: 28, 2: 90}),
        ("Requirements", req, {1: 18, 2: 120}),
        ("Risk Assessment", risk, {1: 16, 2: 14, 3: 16, 4: 20, 5: 20, 6: 22, 7: 12, 8: 13, 9: 17, 10: 70}),
        ("Traceability", trace, {1: 18, 2: 90}),
        ("Test Cases", cases, {1: 12, 2: 18, 3: 26, 4: 12, 5: 12, 6: 42, 7: 45, 8: 38, 9: 70, 10: 80, 11: 18, 12: 12, 13: 18}),
        ("Open Questions", questions, {1: 120}),
    ]

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(len(sheets)))
        z.writestr("_rels/.rels", root_rels())
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("docProps/app.xml", app_xml([s[0] for s in sheets]))
        z.writestr("xl/workbook.xml", workbook_xml([s[0] for s in sheets]))
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels(len(sheets)))
        z.writestr("xl/styles.xml", styles_xml())
        for idx, (_, rows, widths) in enumerate(sheets, 1):
            z.writestr(f"xl/worksheets/sheet{idx}.xml", make_sheet_xml(rows, widths))
    print(out)


if __name__ == "__main__":
    raise SystemExit(main())
