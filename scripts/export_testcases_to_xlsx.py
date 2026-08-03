#!/usr/bin/env python3
import html
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.md"
OUTPUT_DIR = ROOT / "outputs/testcases-excel"
OUTPUT = OUTPUT_DIR / "TC_CMS_Popup - Chiến dịch Marketing.xlsx"


def clean_text(value):
    value = value.replace("<br>", "\n")
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("\\-", "-").replace("\\=", "=").replace("\\_", "_")
    value = value.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return html.unescape(value).strip()


def split_md_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells = []
    current = []
    escaped = False
    for char in line:
        if char == "\\" and not escaped:
            escaped = True
            current.append(char)
            continue
        if char == "|" and not escaped:
            cells.append(clean_text("".join(current)))
            current = []
        else:
            current.append(char)
        escaped = False
    cells.append(clean_text("".join(current)))
    return cells


def is_delimiter(line):
    return bool(re.match(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", line.strip()))


def extract_table(lines, section_title):
    in_section = False
    rows = []
    for line in lines:
        if line.strip() == section_title:
            in_section = True
            continue
        if in_section and line.startswith("# ") and line.strip() != section_title:
            break
        if in_section and line.strip().startswith("|"):
            if not is_delimiter(line):
                rows.append(split_md_row(line))
    return rows


def extract_open_questions(lines):
    questions = []
    in_section = False
    for line in lines:
        if line.strip() == "# Open Questions":
            in_section = True
            continue
        if in_section and line.startswith("# "):
            break
        if in_section and line.strip().startswith("- "):
            questions.append([clean_text(line.strip()[2:])])
    return [["Open Question"]] + questions


def extract_metadata(text):
    match = re.search(r"<!-- TC_META\s*(.*?)\s*-->", text, re.S)
    rows = [["Key", "Value"]]
    if not match:
        return rows
    try:
        data = json.loads(match.group(1))
        rows.extend([[str(key), str(value)] for key, value in data.items()])
    except json.JSONDecodeError:
        rows.append(["raw", clean_text(match.group(1))])
    rows.append(["exported_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    rows.append(["source_markdown", str(SOURCE)])
    return rows


def col_name(index):
    index += 1
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def cell_ref(row, col):
    return f"{col_name(col)}{row + 1}"


def xml_cell(row, col, value, style=0):
    ref = cell_ref(row, col)
    style_attr = f' s="{style}"' if style else ""
    if value is None or value == "":
        return f'<c r="{ref}"{style_attr}/>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}"{style_attr}><v>{value}</v></c>'
    text = escape(str(value), {'"': "&quot;"})
    return f'<c r="{ref}" t="inlineStr"{style_attr}><is><t xml:space="preserve">{text}</t></is></c>'


def normalize_rows(rows):
    width = max((len(row) for row in rows), default=1)
    return [row + [""] * (width - len(row)) for row in rows], width


def sheet_xml(rows, freeze=True, autofilter=True):
    rows, width = normalize_rows(rows)
    row_xml = []
    for r, row in enumerate(rows):
        style = 2 if r == 0 else 0
        cells = "".join(xml_cell(r, c, value, style) for c, value in enumerate(row))
        row_xml.append(f'<row r="{r + 1}">{cells}</row>')
    max_row = max(len(rows), 1)
    max_col = max(width, 1)
    dim = f"A1:{col_name(max_col - 1)}{max_row}"
    widths = []
    for c in range(max_col):
        sample = [str(row[c]) for row in rows[:80] if c < len(row)]
        max_len = max([len(s.split("\n")[0]) for s in sample] + [8])
        width_value = min(max(max_len + 2, 10), 55)
        if c in (7, 8, 9):
            width_value = 55
        widths.append(f'<col min="{c + 1}" max="{c + 1}" width="{width_value}" customWidth="1"/>')
    pane = ""
    if freeze:
        pane = (
            '<sheetViews><sheetView workbookViewId="0">'
            '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'
            '</sheetView></sheetViews>'
        )
    filter_xml = f'<autoFilter ref="{dim}"/>' if autofilter and len(rows) > 1 else ""
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{dim}"/>'
        f'{pane}'
        f'<cols>{"".join(widths)}</cols>'
        f'<sheetData>{"".join(row_xml)}</sheetData>'
        f'{filter_xml}'
        '</worksheet>'
    )


def styles_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="14"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFD9E2F3"/></left><right style="thin"><color rgb="FFD9E2F3"/></right><top style="thin"><color rgb="FFD9E2F3"/></top><bottom style="thin"><color rgb="FFD9E2F3"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def content_types(sheet_count):
    sheet_overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, sheet_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  {sheet_overrides}
</Types>'''


def workbook_xml(sheet_names):
    sheets = "".join(
        f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        for idx, name in enumerate(sheet_names, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>{sheets}</sheets>
</workbook>'''


def workbook_rels(sheet_count):
    rels = "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        for i in range(1, sheet_count + 1)
    )
    rels += f'<Relationship Id="rId{sheet_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>'''


def package_rels():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def doc_props():
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>TC_CMS_Popup - Chiến dịch Marketing</dc:title>
  <dc:creator>QA Copilot</dc:creator>
  <cp:lastModifiedBy>QA Copilot</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>QA Copilot</Application>
</Properties>'''
    return core, app


def main():
    text = SOURCE.read_text(encoding="utf-8")
    lines = text.splitlines()
    sheets = {
        "Metadata": extract_metadata(text),
        "Requirement Summary": extract_table(lines, "# Requirement Summary"),
        "Risk Assessment": extract_table(lines, "# Risk Assessment"),
        "Traceability": extract_table(lines, "# Traceability Matrix"),
        "Test Cases": extract_table(lines, "# Test Case"),
        "Open Questions": extract_open_questions(lines),
        "Statistics": extract_table(lines, "# Statistics"),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    core, app = doc_props()
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types(len(sheets)))
        zf.writestr("_rels/.rels", package_rels())
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        zf.writestr("xl/workbook.xml", workbook_xml(list(sheets.keys())))
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels(len(sheets)))
        zf.writestr("xl/styles.xml", styles_xml())
        for idx, rows in enumerate(sheets.values(), start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(rows))
    print(OUTPUT)
    for name, rows in sheets.items():
        print(f"{name}: {max(len(rows) - 1, 0)} rows")


if __name__ == "__main__":
    main()
