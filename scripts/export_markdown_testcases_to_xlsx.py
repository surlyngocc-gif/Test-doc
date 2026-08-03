from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.md"
OUTPUT = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.xlsx"


def slug_heading(line: str) -> str:
    return line.strip().lstrip("#").strip()


def split_md_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [html.unescape(cell.strip().replace("<br>", "\n")) for cell in line.split("|")]


def is_separator(row: list[str]) -> bool:
    return bool(row) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in row)


def extract_sections(text: str) -> dict[str, list[list[str]] | list[str]]:
    sections: dict[str, list[list[str]] | list[str]] = {
        "Requirement Summary": [],
        "Risk Assessment": [],
        "Traceability Matrix": [],
        "Test Case": [],
        "Open Questions": [],
        "Statistics": [],
    }
    current = ""
    pending_heading = ""
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("#"):
            heading = slug_heading(line)
            if heading in sections:
                current = heading
            pending_heading = heading
            continue
        if current and line.startswith("|"):
            row = split_md_row(line)
            if not is_separator(row):
                sections[current].append(row)  # type: ignore[union-attr]
            continue
        if current == "Open Questions" and line.startswith("- "):
            sections[current].append([line[2:].strip()])  # type: ignore[union-attr]
            continue
        if pending_heading == "Tổng quan Requirement" and line.startswith("|"):
            current = "Requirement Summary"
        elif pending_heading == "Đánh giá Risk" and line.startswith("|"):
            current = "Risk Assessment"
    return sections


def col_name(index: int) -> str:
    name = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def cell_ref(row: int, col: int) -> str:
    return f"{col_name(col)}{row}"


def is_number(value: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", value.strip()))


def style_for(sheet: str, row_idx: int, col_idx: int, value: str) -> int:
    if row_idx == 1:
        return 1
    if sheet == "Summary":
        return 3 if col_idx == 0 else 4
    if sheet == "Statistics":
        return 3 if col_idx == 0 else 4
    if sheet == "Risk Assessment":
        if col_idx == 7 and value == "High":
            return 5
        if col_idx == 7 and value == "Medium":
            return 6
        if col_idx == 7 and value == "Low":
            return 7
        if is_number(value):
            return 4
    if sheet == "Test Cases":
        if col_idx == 4 and value == "Critical":
            return 5
        if col_idx == 5 and value == "High":
            return 5
        if col_idx == 5 and value == "Medium":
            return 6
        if col_idx == 5 and value == "Low":
            return 7
    return 2


def make_sheet_xml(sheet_name: str, rows: list[list[str]], widths: list[float]) -> str:
    max_col = max((len(row) for row in rows), default=1)
    width_xml = "".join(
        f'<col min="{i + 1}" max="{i + 1}" width="{widths[i] if i < len(widths) else 18}" customWidth="1"/>'
        for i in range(max_col)
    )
    sheet_data = []
    for r_idx, row in enumerate(rows, start=1):
        height = 28 if r_idx == 1 else 54 if sheet_name == "Test Cases" else 34
        cells = []
        for c_idx in range(max_col):
            value = row[c_idx] if c_idx < len(row) else ""
            ref = cell_ref(r_idx, c_idx)
            style = style_for(sheet_name, r_idx, c_idx, value)
            if is_number(value) and sheet_name in {"Risk Assessment", "Statistics"} and r_idx > 1 and c_idx > 0:
                cells.append(f'<c r="{ref}" s="{style}"><v>{value}</v></c>')
            else:
                cells.append(
                    f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{escape(value)}</t></is></c>'
                )
        sheet_data.append(f'<row r="{r_idx}" ht="{height}" customHeight="1">{"".join(cells)}</row>')
    auto_filter = ""
    if len(rows) > 1 and max_col > 1:
        auto_filter = f'<autoFilter ref="A1:{cell_ref(len(rows), max_col - 1)}"/>'
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheetViews><sheetView workbookViewId="0" showGridLines="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
  <cols>{width_xml}</cols>
  <sheetData>{''.join(sheet_data)}</sheetData>
  {auto_filter}
</worksheet>'''


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = "".join(
        f'<sheet name="{escape(name)}" sheetId="{i + 1}" r:id="rId{i + 1}"/>'
        for i, name in enumerate(sheet_names)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>{sheets}</sheets></workbook>'''


def workbook_rels(sheet_names: list[str]) -> str:
    rels = "".join(
        f'<Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i + 1}.xml"/>'
        for i, _ in enumerate(sheet_names)
    )
    style_id = len(sheet_names) + 1
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}<Relationship Id="rId{style_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''


def content_types(sheet_names: list[str]) -> str:
    sheets = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i, _ in enumerate(sheet_names)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  {sheets}
</Types>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="4">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Calibri"/></font>
    <font><b/><color rgb="FF1F2937"/><sz val="11"/><name val="Calibri"/></font>
    <font><color rgb="FF1F2937"/><sz val="11"/><name val="Calibri"/></font>
  </fonts>
  <fills count="7">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFEAF2F8"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFE2E2"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2F0D9"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFD9E2EC"/></left><right style="thin"><color rgb="FFD9E2EC"/></right><top style="thin"><color rgb="FFD9E2EC"/></top><bottom style="thin"><color rgb="FFD9E2EC"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="8">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="4" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="5" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="6" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def root_rels() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'''


def summary_rows(sections: dict[str, list[list[str]] | list[str]]) -> list[list[str]]:
    stats = {row[0]: row[1] for row in sections["Statistics"][1:]}  # type: ignore[index]
    return [
        ["Thông tin", "Giá trị"],
        ["Nguồn", str(SOURCE.relative_to(ROOT))],
        ["File Excel", str(OUTPUT.relative_to(ROOT))],
        ["Tổng Requirement", stats.get("Tổng Requirement", "")],
        ["Tổng Test Case", stats.get("Tổng Test Case", "")],
        ["High Risk", stats.get("High Risk", "")],
        ["Medium Risk", stats.get("Medium Risk", "")],
        ["Low Risk", stats.get("Low Risk", "")],
        ["Coverage %", stats.get("Coverage %", "")],
    ]


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    sections = extract_sections(text)
    sheets: list[tuple[str, list[list[str]], list[float]]] = [
        ("Summary", summary_rows(sections), [28, 84]),
        ("Requirements", sections["Requirement Summary"], [18, 120]),  # type: ignore[list-item]
        ("Risk Assessment", sections["Risk Assessment"], [18, 14, 16, 20, 18, 22, 12, 14, 14, 18, 74]),  # type: ignore[list-item]
        ("Traceability", sections["Traceability Matrix"], [18, 36]),  # type: ignore[list-item]
        ("Test Cases", sections["Test Case"], [14, 24, 28, 46, 14, 14, 62, 48, 70, 76, 24, 16, 30]),  # type: ignore[list-item]
        ("Open Questions", [["Open Question"], *sections["Open Questions"]], [120]),  # type: ignore[list-item]
        ("Statistics", sections["Statistics"], [28, 16]),  # type: ignore[list-item]
    ]
    sheet_names = [name for name, _, _ in sheets]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types(sheet_names))
        zf.writestr("_rels/.rels", root_rels())
        zf.writestr("xl/workbook.xml", workbook_xml(sheet_names))
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels(sheet_names))
        zf.writestr("xl/styles.xml", styles_xml())
        for idx, (name, rows, widths) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", make_sheet_xml(name, rows, widths))
    print(OUTPUT)


if __name__ == "__main__":
    main()
