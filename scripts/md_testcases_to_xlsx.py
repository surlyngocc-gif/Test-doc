#!/usr/bin/env python3
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.md"
OUTPUT = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.xlsx"


def col_name(index):
    name = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def cell_ref(row_idx, col_idx):
    return f"{col_name(col_idx)}{row_idx + 1}"


def split_md_row(line):
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip().replace("<br>", "\n") for cell in text.split("|")]


def is_separator(line):
    cells = split_md_row(line)
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells if cell.strip())


def parse_tables(md_text):
    lines = md_text.splitlines()
    tables = []
    current_heading = "Sheet"
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            current_heading = line.lstrip("#").strip()
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            header = split_md_row(lines[i])
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_md_row(lines[i]))
                i += 1
            tables.append((current_heading, header, rows))
            continue
        i += 1
    return tables


def parse_metadata(md_text):
    match = re.search(r"<!--\s*TC_META\s*(\{.*?\})\s*-->", md_text, re.S)
    return json.loads(match.group(1)) if match else {}


def parse_open_questions(md_text):
    match = re.search(r"# Open Questions\s*(.*?)(?:\n# |\Z)", md_text, re.S)
    if not match:
        return []
    questions = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            questions.append([stripped[2:]])
    return questions


def normalize_sheet_name(name, used):
    mapping = {
        "Tổng quan Requirement": "Requirements",
        "Đánh giá Risk": "Risk Assessment",
        "Traceability Matrix": "Traceability",
        "Test Case": "Test Cases",
        "Statistics": "Statistics",
    }
    base = mapping.get(name, name)
    base = re.sub(r"[\[\]:*?/\\]", " ", base).strip()[:31] or "Sheet"
    candidate = base
    suffix = 2
    while candidate in used:
        tail = f" {suffix}"
        candidate = f"{base[:31 - len(tail)]}{tail}"
        suffix += 1
    used.add(candidate)
    return candidate


def style_id(value, row_idx=0):
    if row_idx == 0:
        return 1
    if isinstance(value, (int, float)):
        return 3
    return 2


def xml_cell(value, row_idx, col_idx):
    ref = cell_ref(row_idx, col_idx)
    sid = style_id(value, row_idx)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}" s="{sid}"><v>{value}</v></c>'
    text = "" if value is None else str(value)
    return f'<c r="{ref}" s="{sid}" t="inlineStr"><is><t xml:space="preserve">{escape(text)}</t></is></c>'


def sheet_xml(rows, widths):
    max_cols = max((len(row) for row in rows), default=1)
    max_rows = max(len(rows), 1)
    ref = f"A1:{cell_ref(max_rows - 1, max_cols - 1)}"
    cols = []
    for idx in range(max_cols):
        width = widths[idx] if idx < len(widths) else 22
        cols.append(f'<col min="{idx + 1}" max="{idx + 1}" width="{width}" customWidth="1"/>')
    row_xml = []
    for r, row in enumerate(rows):
        height = 24 if r == 0 else 48
        cells = "".join(xml_cell(value, r, c) for c, value in enumerate(row))
        row_xml.append(f'<row r="{r + 1}" ht="{height}" customHeight="1">{cells}</row>')
    freeze = (
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '<selection pane="bottomLeft"/>'
        '</sheetView></sheetViews>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{ref}"/>'
        f'{freeze}'
        '<sheetFormatPr defaultRowHeight="18"/>'
        f'<cols>{"".join(cols)}</cols>'
        f'<sheetData>{"".join(row_xml)}</sheetData>'
        f'<autoFilter ref="{ref}"/>'
        '</worksheet>'
    )


def styles_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Calibri"/></font>
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
  <cellXfs count="4">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment horizontal="right" vertical="top"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def build_xlsx(sheets):
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for idx in range(1, len(sheets) + 1):
        content_types.append(f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    content_types.append("</Types>")

    workbook_sheets = []
    workbook_rels = []
    for idx, (name, _, _) in enumerate(sheets, start=1):
        workbook_sheets.append(f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>')
        workbook_rels.append(f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>')
    workbook_rels.append(f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>')

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<workbookPr/>'
        '<sheets>'
        + "".join(workbook_sheets)
        + '</sheets></workbook>'
    )
    rels_root = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(workbook_rels)
        + '</Relationships>'
    )
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    core_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:creator>QA Copilot</dc:creator>
  <cp:lastModifiedBy>QA Copilot</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''
    app_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>QA Copilot</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{len(sheets)}</vt:i4></vt:variant></vt:vector></HeadingPairs>
  <TitlesOfParts><vt:vector size="{len(sheets)}" baseType="lpstr">{"".join(f"<vt:lpstr>{escape(name)}</vt:lpstr>" for name, _, _ in sheets)}</vt:vector></TitlesOfParts>
</Properties>'''

    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "".join(content_types))
        zf.writestr("_rels/.rels", rels_root)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("docProps/app.xml", app_xml)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        zf.writestr("xl/styles.xml", styles_xml())
        for idx, (_, rows, widths) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(rows, widths))


def main():
    md_text = SOURCE.read_text(encoding="utf-8")
    metadata = parse_metadata(md_text)
    tables = parse_tables(md_text)
    questions = parse_open_questions(md_text)
    used = set()
    sheets = []

    stats_table = next((rows for heading, header, rows in tables if heading == "Statistics"), [])
    stats = {row[0]: row[1] for row in stats_table if len(row) >= 2}
    summary_rows = [
        ["Field", "Value"],
        ["Source", str(SOURCE)],
        ["Generated At", metadata.get("generated_at", "")],
        ["Scope", metadata.get("scope", "")],
        ["Total Requirements", stats.get("Tổng Requirement", "")],
        ["Total Test Cases", stats.get("Tổng Test Case", "")],
        ["Coverage", stats.get("Coverage %", "")],
        ["High Risk Requirements", stats.get("High Risk", "")],
        ["Medium Risk Requirements", stats.get("Medium Risk", "")],
        ["Low Risk Requirements", stats.get("Low Risk", "")],
    ]
    sheets.append(("Summary", summary_rows, [24, 90]))

    for heading, header, rows in tables:
        name = normalize_sheet_name(heading, used)
        widths = [18] * len(header)
        if name == "Requirements":
            widths = [16, 110]
        elif name == "Risk Assessment":
            widths = [14, 14, 16, 18, 18, 20, 12, 14, 12, 18, 55]
        elif name == "Traceability":
            widths = [16, 38]
        elif name == "Test Cases":
            widths = [10, 20, 24, 38, 12, 12, 46, 42, 56, 62, 24, 12, 28]
        elif name == "Statistics":
            widths = [28, 16]
        sheets.append((name, [header] + rows, widths))

    if questions:
        sheets.append(("Open Questions", [["Open Question"]] + questions, [120]))

    build_xlsx(sheets)
    print(OUTPUT)


if __name__ == "__main__":
    main()
