from __future__ import annotations

import html
import os
import zipfile
from datetime import datetime


OUT_PATH = "deliverables/Bo_ca_kiem_thu_CMS_Popup_Campaign.xlsx"


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def col_letter(n: int) -> str:
    result = ""
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def cell_xml(row: int, col: int, value, style: int = 0) -> str:
    ref = f"{col_letter(col)}{row}"
    s_attr = f' s="{style}"' if style else ""
    if isinstance(value, (int, float)):
        return f'<c r="{ref}"{s_attr}><v>{value}</v></c>'
    return f'<c r="{ref}" t="inlineStr"{s_attr}><is><t xml:space="preserve">{esc(value)}</t></is></c>'


def row_xml(row_num: int, values: list, styles: list[int] | None = None, height: int | None = None) -> str:
    ht = f' ht="{height}" customHeight="1"' if height else ""
    cells = []
    for idx, value in enumerate(values, 1):
        style = styles[idx - 1] if styles and idx <= len(styles) else 0
        cells.append(cell_xml(row_num, idx, value, style))
    return f'<row r="{row_num}"{ht}>{"".join(cells)}</row>'


def sheet_xml(rows: list[list], col_widths: list[float], freeze: bool = True, autofilter: bool = True) -> str:
    max_row = len(rows)
    max_col = max(len(r) for r in rows)
    cols = "".join(
        f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
        for i, w in enumerate(col_widths, 1)
    )
    pane = ""
    if freeze:
        pane = (
            '<sheetViews><sheetView workbookViewId="0">'
            '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'
            '</sheetView></sheetViews>'
        )
    else:
        pane = '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
    data = []
    for r_idx, row in enumerate(rows, 1):
        if r_idx == 1:
            styles = [1] * len(row)
            height = 28
        else:
            styles = [2] * len(row)
            height = 72 if max(len(str(v)) for v in row) > 120 else 42
        data.append(row_xml(r_idx, row, styles, height))
    af = f'<autoFilter ref="A1:{col_letter(max_col)}{max_row}"/>' if autofilter else ""
    validations = ""
    if rows and len(rows[0]) >= 9 and rows[0][7] == "Độ ưu tiên" and rows[0][8] == "Trạng thái":
        validations = (
            '<dataValidations count="2">'
            f'<dataValidation type="list" allowBlank="1" showErrorMessage="1" sqref="H2:H{max_row}"><formula1>"Cao,Trung bình,Thấp"</formula1></dataValidation>'
            f'<dataValidation type="list" allowBlank="1" showErrorMessage="1" sqref="I2:I{max_row}"><formula1>"Chưa chạy,Đạt,Không đạt,Bị chặn"</formula1></dataValidation>'
            '</dataValidations>'
        )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  {pane}
  <sheetFormatPr defaultRowHeight="18"/>
  <cols>{cols}</cols>
  <sheetData>{"".join(data)}</sheetData>
  {af}
  {validations}
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
</worksheet>'''


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = "".join(
        f'<sheet name="{esc(name)}" sheetId="{i}" r:id="rId{i}"/>'
        for i, name in enumerate(sheet_names, 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <workbookPr date1904="false"/>
  <sheets>{sheets}</sheets>
</workbook>'''


def workbook_rels_xml(sheet_count: int) -> str:
    rels = []
    for i in range(1, sheet_count + 1):
        rels.append(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        )
    rels.append(
        f'<Relationship Id="rId{sheet_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{"".join(rels)}</Relationships>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3">
    <font><sz val="11"/><color theme="1"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font>
    <font><sz val="11"/><color rgb="FF111827"/><name val="Calibri"/><family val="2"/></font>
  </fonts>
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF8FAFC"/><bgColor indexed="64"/></patternFill></fill>
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
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def content_types_xml(sheet_count: int) -> str:
    sheet_overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, sheet_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  {sheet_overrides}
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''


def root_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Bộ ca kiểm thử CMS Pop-up Campaign</dc:title>
  <dc:creator>QA Copilot</dc:creator>
  <cp:lastModifiedBy>QA Copilot</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def app_xml(sheet_names: list[str]) -> str:
    items = "".join(f"<vt:lpstr>{esc(name)}</vt:lpstr>" for name in sheet_names)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>QA Copilot</Application>
  <DocSecurity>0</DocSecurity>
  <TitlesOfParts><vt:vector size="{len(sheet_names)}" baseType="lpstr">{items}</vt:vector></TitlesOfParts>
</Properties>'''


HEADERS = ["Mã TC", "Danh mục", "Kịch bản kiểm thử", "Điều kiện tiên quyết", "Các bước thực hiện", "Dữ liệu kiểm thử", "Kết quả mong đợi", "Độ ưu tiên", "Trạng thái"]


def tc(tc_id, category, scenario, pre, steps, data, expected, priority="Cao", status="Chưa chạy"):
    return [tc_id, category, scenario, pre, steps, data, expected, priority, status]


def build_test_cases() -> list[list]:
    rows = []
    add = rows.append
    # Phân Quyền
    add(tc("TC-PQ-001", "Phân Quyền", "Hiển thị menu Pop-up với Admin CMS có quyền Pop-up", "Admin CMS đã đăng nhập và được gán quyền Pop-up", "1. Đăng nhập CMS\n2. Quan sát menu bên trái\n3. Mở chức năng Pop-up - Chiến dịch Marketing", "Tài khoản Admin CMS có quyền Pop-up", "Menu Pop-up - Chiến dịch Marketing hiển thị và mở được màn danh sách chiến dịch.", "Cao"))
    add(tc("TC-PQ-002", "Phân Quyền", "Hiển thị menu Pop-up với Manager CMS có quyền Pop-up", "Manager CMS đã đăng nhập và được gán quyền Pop-up", "1. Đăng nhập CMS\n2. Quan sát menu\n3. Mở chức năng Pop-up", "Tài khoản Manager CMS có quyền Pop-up", "Menu hiển thị và user truy cập được màn danh sách.", "Cao"))
    add(tc("TC-PQ-003", "Phân Quyền", "Ẩn menu Pop-up với user không có quyền Pop-up", "User CMS đã đăng nhập nhưng không có quyền Pop-up", "1. Đăng nhập CMS\n2. Quan sát menu bên trái", "Tài khoản CMS không có quyền Pop-up", "Không hiển thị chức năng Pop-up - Chiến dịch Marketing trên menu CMS.", "Cao"))
    add(tc("TC-PQ-004", "Phân Quyền", "Từ chối truy cập URL trực tiếp khi không có quyền Pop-up", "User CMS không có quyền Pop-up có URL màn Pop-up", "1. Đăng nhập bằng user không có quyền\n2. Nhập URL trực tiếp màn danh sách Pop-up", "URL màn danh sách Pop-up", "Backend CMS từ chối truy cập. User không xem được dữ liệu chiến dịch.", "Cao"))
    add(tc("TC-PQ-005", "Phân Quyền", "Chỉ hiển thị nút Edit với chiến dịch Scheduled, Active, Inactive", "Màn danh sách có dữ liệu đủ 4 trạng thái", "1. Mở màn danh sách\n2. Quan sát cột Action của từng trạng thái", "Chiến dịch Scheduled, Active, Inactive, Expired", "Icon Edit chỉ hiển thị với Scheduled, Active, Inactive; không hiển thị với Expired.", "Cao"))
    add(tc("TC-PQ-006", "Phân Quyền", "Chỉ cho phép xóa chiến dịch Scheduled", "Màn danh sách có chiến dịch ở đủ trạng thái", "1. Mở danh sách\n2. Quan sát icon Delete ở từng dòng", "Scheduled, Active, Inactive, Expired", "Icon Delete enable với Scheduled; Active/Inactive/Expired bị ẩn hoặc disabled.", "Cao"))
    add(tc("TC-PQ-007", "Phân Quyền", "Backend từ chối xóa nếu trạng thái không còn Scheduled", "FE đang hiển thị Delete enable nhưng trạng thái đã đổi ở backend", "1. Mở danh sách khi campaign là Scheduled\n2. Đổi trạng thái ở backend/người dùng khác\n3. Click Delete và xác nhận", "Chiến dịch đã chuyển khỏi Scheduled", "Hiển thị toast: Campaign cannot be deleted in current status. Dữ liệu không bị xóa.", "Cao"))
    add(tc("TC-PQ-008", "Phân Quyền", "Hiển thị nút Edit ở màn xem chi tiết theo quyền và trạng thái", "User có quyền edit; có chiến dịch ở trạng thái được phép chỉnh sửa", "1. Mở View chi tiết chiến dịch Scheduled/Active/Inactive\n2. Quan sát nút Edit", "Chiến dịch Scheduled/Active/Inactive", "Nút Edit hiển thị nếu chiến dịch ở trạng thái cho phép chỉnh sửa và user có quyền.", "Trung bình"))
    add(tc("TC-PQ-009", "Phân Quyền", "Không hiển thị nút Edit ở màn xem chi tiết chiến dịch Expired", "Có chiến dịch Expired", "1. Mở View chi tiết chiến dịch Expired\n2. Quan sát nút Edit", "Chiến dịch Expired", "Không hiển thị hoặc không enable nút Edit.", "Trung bình"))

    # Chức năng chính
    add(tc("TC-CN-001", "Chức năng chính", "Mở màn danh sách chiến dịch Pop-up thành công", "User có quyền Pop-up", "1. Đăng nhập CMS\n2. Chọn menu Pop-up - Chiến dịch Marketing", "Tài khoản có quyền", "Màn danh sách hiển thị đúng tiêu đề, bộ lọc, nút Export to Excel, nút Create và bảng dữ liệu.", "Cao"))
    add(tc("TC-CN-002", "Chức năng chính", "Danh sách sắp xếp theo ngày tạo mới nhất đến cũ nhất", "Có nhiều chiến dịch với Created Date khác nhau", "1. Mở danh sách\n2. Quan sát thứ tự bản ghi", "Nhiều chiến dịch có Created Date khác nhau", "Dữ liệu được sắp xếp theo thời gian tạo gần nhất đến lâu nhất.", "Cao"))
    add(tc("TC-CN-003", "Chức năng chính", "Hiển thị No Data khi danh sách không có dữ liệu", "Không có chiến dịch hoặc filter không có kết quả", "1. Mở danh sách hoặc áp dụng bộ lọc không có kết quả\n2. Quan sát bảng", "Bộ lọc không khớp dữ liệu", "Hiển thị No Data.", "Trung bình"))
    add(tc("TC-CN-004", "Chức năng chính", "Tìm kiếm tương đối theo mã chiến dịch", "Có chiến dịch mã POP01", "1. Nhập một phần mã vào Search by Code\n2. Thực hiện tìm kiếm", "Từ khóa: POP hoặc 01", "Danh sách chỉ hiển thị chiến dịch có mã khớp tương đối.", "Cao"))
    add(tc("TC-CN-005", "Chức năng chính", "Tìm kiếm tương đối theo tên chiến dịch", "Có chiến dịch có tên phù hợp", "1. Nhập một phần tên vào Search by popup\n2. Thực hiện tìm kiếm", "Từ khóa là một phần tên chiến dịch", "Danh sách chỉ hiển thị chiến dịch có tên khớp tương đối.", "Cao"))
    add(tc("TC-CN-006", "Chức năng chính", "Kết hợp Search by Code, Search by popup và các bộ lọc", "Có dữ liệu phù hợp nhiều điều kiện", "1. Nhập mã\n2. Nhập tên\n3. Chọn Status và Customer Segment\n4. Áp dụng lọc", "Mã, tên, trạng thái, đối tượng phù hợp", "Danh sách hiển thị bản ghi thỏa đồng thời tất cả điều kiện.", "Cao"))
    add(tc("TC-CN-007", "Chức năng chính", "Lọc theo trạng thái Scheduled", "Có chiến dịch Scheduled và trạng thái khác", "1. Mở danh sách\n2. Chọn Status = Scheduled", "Status Scheduled", "Chỉ hiển thị chiến dịch trạng thái Scheduled.", "Cao"))
    add(tc("TC-CN-008", "Chức năng chính", "Lọc theo trạng thái Active", "Có chiến dịch Active và trạng thái khác", "1. Mở danh sách\n2. Chọn Status = Active", "Status Active", "Chỉ hiển thị chiến dịch trạng thái Active.", "Cao"))
    add(tc("TC-CN-009", "Chức năng chính", "Lọc theo trạng thái Inactive", "Có chiến dịch Inactive và trạng thái khác", "1. Mở danh sách\n2. Chọn Status = Inactive", "Status Inactive", "Chỉ hiển thị chiến dịch trạng thái Inactive.", "Cao"))
    add(tc("TC-CN-010", "Chức năng chính", "Lọc theo trạng thái Expired", "Có chiến dịch Expired và trạng thái khác", "1. Mở danh sách\n2. Chọn Status = Expired", "Status Expired", "Chỉ hiển thị chiến dịch trạng thái Expired.", "Cao"))
    add(tc("TC-CN-011", "Chức năng chính", "Lọc Customer Segment = Toàn bộ người dùng", "Có chiến dịch áp dụng toàn bộ hội viên", "1. Chọn Customer Segment = Toàn bộ người dùng", "Toàn bộ người dùng", "Chỉ hiển thị chiến dịch áp dụng cho toàn bộ hội viên.", "Trung bình"))
    add(tc("TC-CN-012", "Chức năng chính", "Lọc Customer Segment cụ thể", "Có chiến dịch áp dụng segment cụ thể", "1. Chọn Customer Segment cụ thể trong dropdown", "Segment A", "Chỉ hiển thị chiến dịch có đối tượng áp dụng là segment đã chọn.", "Trung bình"))
    add(tc("TC-CN-013", "Chức năng chính", "Lọc Customer Segment = Import file", "Có chiến dịch dùng danh sách hội viên import", "1. Chọn Customer Segment = Import file", "Import file", "Chỉ hiển thị chiến dịch có đối tượng áp dụng là danh sách hội viên import từ file.", "Trung bình"))
    add(tc("TC-CN-014", "Chức năng chính", "Lọc theo Position", "Có chiến dịch theo nhiều vị trí hiển thị", "1. Chọn một Position trong bộ lọc\n2. Quan sát kết quả", "Position bất kỳ trong danh sách BA cung cấp", "Chỉ hiển thị chiến dịch có Position đã chọn.", "Trung bình"))
    add(tc("TC-CN-015", "Chức năng chính", "Lọc Effective Period khi campaign nằm gọn trong khoảng lọc", "Có chiến dịch start/end nằm trong khoảng lọc", "1. Chọn From Date và To Date bao phủ toàn bộ campaign\n2. Áp dụng lọc", "Camp_Start >= Filter_From; Camp_End <= Filter_To", "Chiến dịch được hiển thị.", "Cao"))
    add(tc("TC-CN-016", "Chức năng chính", "Lọc Effective Period khi campaign bắt đầu trước và kết thúc trong khoảng lọc", "Có chiến dịch giao với khoảng lọc", "1. Chọn khoảng lọc sao cho Start campaign ngoài khoảng, End campaign trong khoảng", "Camp_Start < Filter_From; Camp_End nằm trong khoảng", "Chiến dịch được hiển thị.", "Cao"))
    add(tc("TC-CN-017", "Chức năng chính", "Lọc Effective Period khi campaign bắt đầu trong và kết thúc sau khoảng lọc", "Có chiến dịch giao với khoảng lọc", "1. Chọn khoảng lọc sao cho Start campaign trong khoảng, End campaign ngoài khoảng", "Camp_Start nằm trong khoảng; Camp_End > Filter_To", "Chiến dịch được hiển thị.", "Cao"))
    add(tc("TC-CN-018", "Chức năng chính", "Lọc Effective Period không hiển thị campaign kết thúc trước khoảng lọc", "Có chiến dịch kết thúc trước Filter_From", "1. Chọn khoảng lọc sau thời gian kết thúc campaign", "Camp_End < Filter_From", "Chiến dịch không hiển thị.", "Trung bình"))
    add(tc("TC-CN-019", "Chức năng chính", "Lọc Effective Period không hiển thị campaign bắt đầu sau khoảng lọc", "Có chiến dịch bắt đầu sau Filter_To", "1. Chọn khoảng lọc trước thời gian bắt đầu campaign", "Camp_Start > Filter_To", "Chiến dịch không hiển thị.", "Trung bình"))
    add(tc("TC-CN-020", "Chức năng chính", "Lọc Effective Period với campaign No End Date", "Có chiến dịch No End Date", "1. Chọn khoảng lọc có To Date sau hoặc bằng Start Date của campaign", "No End Date; Start Date <= To Date lọc", "Chiến dịch No End Date được hiển thị.", "Cao"))
    add(tc("TC-CN-021", "Chức năng chính", "Mở màn tạo chiến dịch từ nút Create", "User có quyền tạo", "1. Mở danh sách\n2. Click Create", "Không áp dụng", "Điều hướng sang màn Tạo campaign Pop-up.", "Cao"))
    add(tc("TC-CN-022", "Chức năng chính", "Tạo chiến dịch hợp lệ với đối tượng toàn bộ hội viên", "User có quyền tạo; dữ liệu hợp lệ", "1. Mở màn Create\n2. Nhập đầy đủ thông tin hợp lệ\n3. Chọn Toàn bộ hội viên\n4. Chọn Position và Frequency\n5. Click Create\n6. Xác nhận OTP", "Dữ liệu hợp lệ; audience = Toàn bộ hội viên", "Hiển thị toast: Campaign has been successfully saved. Chiến dịch xuất hiện ở danh sách với trạng thái backend trả về.", "Cao"))
    add(tc("TC-CN-023", "Chức năng chính", "Tạo chiến dịch hợp lệ với Customer Segment", "Có segment khả dụng", "1. Mở Create\n2. Nhập thông tin hợp lệ\n3. Chọn Customer Segment\n4. Chọn một segment\n5. Lưu và xác nhận OTP", "Segment A", "Chiến dịch được tạo thành công và danh sách hiển thị Customer Segment đã chọn.", "Cao"))
    add(tc("TC-CN-024", "Chức năng chính", "Tạo chiến dịch hợp lệ với Import file", "Có file import hợp lệ theo template", "1. Mở Create\n2. Chọn Import file\n3. Upload file hợp lệ\n4. Nhập các field bắt buộc khác\n5. Lưu và xác nhận OTP", "File Excel hợp lệ", "Chiến dịch được tạo thành công; đối tượng áp dụng hiển thị Import file.", "Cao"))
    add(tc("TC-CN-025", "Chức năng chính", "Đóng màn Create khi chưa nhập dữ liệu", "Đang ở màn Create chưa thay đổi dữ liệu", "1. Click Close", "Không có dữ liệu nhập", "Màn Create đóng và quay về màn trước/danh sách; không hiển thị confirm mất dữ liệu.", "Trung bình"))
    add(tc("TC-CN-026", "Chức năng chính", "Đóng màn Create khi có dữ liệu chưa lưu", "Đang ở màn Create đã nhập dữ liệu", "1. Nhập một số field\n2. Click Close", "Dữ liệu bất kỳ đã thay đổi", "Hiển thị confirm: Unsaved changes will be lost. Do you want to continue?", "Cao"))
    add(tc("TC-CN-027", "Chức năng chính", "Hủy confirm tạo chiến dịch", "Form Create hợp lệ và popup confirm đang mở", "1. Click Create\n2. Popup confirm hiển thị\n3. Click Cancel", "Dữ liệu hợp lệ", "Popup đóng, chiến dịch chưa được tạo.", "Trung bình"))
    add(tc("TC-CN-028", "Chức năng chính", "Chỉnh sửa Scheduled campaign với đầy đủ field", "Có campaign Scheduled; user có quyền edit", "1. Mở Edit campaign Scheduled\n2. Chỉnh sửa nhiều field\n3. Save và xác nhận OTP", "Dữ liệu hợp lệ theo rule Create", "Lưu thành công, toast: Campaign has been successfully edited. Các field cập nhật đúng.", "Cao"))
    add(tc("TC-CN-029", "Chức năng chính", "Chỉnh sửa Active campaign chỉ với nhóm field được phép", "Có campaign Active", "1. Mở Edit campaign Active\n2. Kiểm tra field enable/disable\n3. Sửa field được phép\n4. Save", "Tên, mô tả, trạng thái Active sang Inactive, ảnh, nội dung", "Chỉ field được phép enable; lưu thành công khi dữ liệu hợp lệ.", "Cao"))
    add(tc("TC-CN-030", "Chức năng chính", "Chỉnh sửa Inactive campaign chỉ với nhóm field được phép", "Có campaign Inactive", "1. Mở Edit campaign Inactive\n2. Sửa Priority, trạng thái, cấu hình popup, vị trí\n3. Save", "Dữ liệu hợp lệ", "Chỉ field được phép enable; lưu thành công khi dữ liệu hợp lệ.", "Cao"))
    add(tc("TC-CN-031", "Chức năng chính", "Màn Edit campaign Expired chỉ đọc", "Có campaign Expired", "1. Mở Edit hoặc View campaign Expired\n2. Quan sát field và nút Save", "Campaign Expired", "Toàn bộ field read-only/disabled; không hiển thị hoặc không enable Save.", "Cao"))
    add(tc("TC-CN-032", "Chức năng chính", "Hủy confirm chỉnh sửa chiến dịch", "Màn Edit có thay đổi hợp lệ và popup confirm đang mở", "1. Click Save\n2. Popup confirm hiển thị\n3. Click Cancel", "Dữ liệu sửa hợp lệ", "Popup đóng, dữ liệu chưa được lưu.", "Trung bình"))
    add(tc("TC-CN-033", "Chức năng chính", "Xem chi tiết chiến dịch", "Có campaign bất kỳ", "1. Mở danh sách\n2. Click icon View", "Campaign bất kỳ", "Màn xem chi tiết hiển thị thông tin campaign ở chế độ chỉ đọc.", "Cao"))
    add(tc("TC-CN-034", "Chức năng chính", "Xóa campaign Scheduled thành công", "Có campaign Scheduled; user có quyền xóa", "1. Click Delete ở campaign Scheduled\n2. Nhập OTP\n3. Click Delete", "Campaign Scheduled", "Hiển thị toast: Campaign has been successfully deleted. Danh sách được cập nhật.", "Cao"))
    add(tc("TC-CN-035", "Chức năng chính", "Hủy popup xác nhận xóa", "Popup xác nhận xóa đang hiển thị", "1. Click Cancel", "Campaign Scheduled", "Popup đóng, campaign không bị xóa.", "Trung bình"))
    add(tc("TC-CN-036", "Chức năng chính", "Xóa campaign thất bại", "Backend trả lỗi khi xóa", "1. Click Delete\n2. Xác nhận OTP\n3. Quan sát phản hồi", "Campaign Scheduled; backend trả lỗi", "Hiển thị toast: Failed to delete campaign. Campaign vẫn còn trong danh sách.", "Cao"))
    add(tc("TC-CN-037", "Chức năng chính", "Mở popup Export từ nút Export to Excel", "User có quyền export", "1. Mở danh sách\n2. Click Export to Excel", "Không áp dụng", "Popup EXPORT hiển thị với các lựa chọn Export từng chiến dịch và Toàn bộ chiến dịch.", "Cao"))
    add(tc("TC-CN-038", "Chức năng chính", "Export từng chiến dịch thành công", "Có campaign và dữ liệu báo cáo", "1. Mở popup EXPORT\n2. Chọn Export từng chiến dịch\n3. Chọn campaign\n4. Chọn thời gian export hợp lệ\n5. Click Export to excel", "Campaign A; khoảng thời gian hợp lệ", "Hệ thống tải file Excel báo cáo theo campaign và khoảng thời gian đã chọn.", "Cao"))
    add(tc("TC-CN-039", "Chức năng chính", "Export toàn bộ chiến dịch thành công", "Có nhiều campaign và dữ liệu báo cáo", "1. Mở popup EXPORT\n2. Chọn Toàn bộ chiến dịch\n3. Chọn thời gian export hợp lệ\n4. Click Export to excel", "Khoảng thời gian hợp lệ", "Hệ thống tải file Excel tổng hợp toàn bộ campaign user có quyền export trong khoảng thời gian.", "Cao"))
    add(tc("TC-CN-040", "Chức năng chính", "Đóng popup Export bằng icon X", "Popup EXPORT đang mở", "1. Click icon X", "Không áp dụng", "Popup đóng; không thực hiện export và không lưu thay đổi filter trong popup.", "Trung bình"))
    add(tc("TC-CN-041", "Chức năng chính", "Đóng popup Export bằng Cancel", "Popup EXPORT đang mở", "1. Click Cancel", "Không áp dụng", "Popup đóng; không thực hiện export.", "Trung bình"))

    # Validation
    add(tc("TC-VL-001", "Quy tắc nhập liệu", "Search by Code trim khoảng trắng", "Màn danh sách đang mở", "1. Nhập toàn khoảng trắng vào Search by Code\n2. Thực hiện tìm kiếm", "\"   \"", "Hệ thống trim và xem như không nhập; không báo lỗi.", "Trung bình"))
    add(tc("TC-VL-002", "Quy tắc nhập liệu", "Search by Code vượt 255 ký tự", "Màn danh sách đang mở", "1. Nhập từ khóa dài 256 ký tự vào Search by Code", "Chuỗi 256 ký tự", "Hiển thị lỗi: Search keyword must not exceed 255 characters.", "Trung bình"))
    add(tc("TC-VL-003", "Quy tắc nhập liệu", "Search by popup trim khoảng trắng", "Màn danh sách đang mở", "1. Nhập toàn khoảng trắng vào Search by popup\n2. Tìm kiếm", "\"   \"", "Hệ thống trim và xem như không nhập; không báo lỗi.", "Trung bình"))
    add(tc("TC-VL-004", "Quy tắc nhập liệu", "Search by popup vượt 255 ký tự", "Màn danh sách đang mở", "1. Nhập từ khóa dài 256 ký tự vào Search by popup", "Chuỗi 256 ký tự", "Hiển thị lỗi: Search keyword must not exceed 255 characters.", "Trung bình"))
    add(tc("TC-VL-005", "Quy tắc nhập liệu", "Effective Period from date lớn hơn to date", "Màn danh sách đang mở", "1. Nhập From Date lớn hơn To Date", "From Date > To Date", "Hiển thị lỗi: Invalid date range.", "Cao"))
    add(tc("TC-VL-006", "Quy tắc nhập liệu", "Không nhập Campaign Name khi tạo", "Màn Create đang mở", "1. Bỏ trống Campaign Name\n2. Nhập các field khác hợp lệ\n3. Click Create", "Campaign Name rỗng", "Hiển thị lỗi: Campaign name is required.", "Cao"))
    add(tc("TC-VL-007", "Quy tắc nhập liệu", "Campaign Name chỉ gồm khoảng trắng", "Màn Create đang mở", "1. Nhập khoảng trắng vào Campaign Name\n2. Click Create", "\"   \"", "Trim xong rỗng và hiển thị lỗi: Campaign name is required.", "Cao"))
    add(tc("TC-VL-008", "Quy tắc nhập liệu", "Campaign Name đúng 255 ký tự", "Màn Create đang mở", "1. Nhập Campaign Name 255 ký tự\n2. Nhập dữ liệu còn lại hợp lệ\n3. Lưu", "Chuỗi 255 ký tự", "Dữ liệu được chấp nhận nếu các field khác hợp lệ.", "Trung bình"))
    add(tc("TC-VL-009", "Quy tắc nhập liệu", "Campaign Name vượt 255 ký tự", "Màn Create đang mở", "1. Nhập Campaign Name 256 ký tự\n2. Click Create", "Chuỗi 256 ký tự", "Hiển thị lỗi: Campaign name must not exceed 255 characters.", "Cao"))
    add(tc("TC-VL-010", "Quy tắc nhập liệu", "Description vượt 500 ký tự", "Màn Create đang mở", "1. Nhập Description 501 ký tự\n2. Click Create", "Chuỗi 501 ký tự", "Hiển thị lỗi theo SRS: Campaign name must not exceed  characters. Requirement cần xác nhận vì message thiếu số ký tự và sai tên field.", "Trung bình"))
    add(tc("TC-VL-011", "Quy tắc nhập liệu", "Không nhập Priority", "Màn Create đang mở", "1. Bỏ trống Priority\n2. Click Create", "Priority rỗng", "Hiển thị lỗi: Priority is required.", "Cao"))
    add(tc("TC-VL-012", "Quy tắc nhập liệu", "Priority không phải số nguyên dương", "Màn Create đang mở", "1. Nhập Priority là chữ/ký tự đặc biệt/số thập phân/số âm/0\n2. Click Create", "abc, @, 1.5, -1, 0", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-VL-013", "Quy tắc nhập liệu", "Không nhập Start Date", "Màn Create đang mở", "1. Bỏ trống Start Date\n2. Click Create", "Start Date rỗng", "Không cho lưu; field Start Date bắt buộc. Requirement cần xác nhận message required vì SRS chưa nêu rõ.", "Cao"))
    add(tc("TC-VL-014", "Quy tắc nhập liệu", "Start Date sai định dạng", "Màn Create đang mở", "1. Nhập Start Date sai format\n2. Click Create", "2026/01/01 hoặc text", "Hiển thị lỗi: Invalid start date format.", "Cao"))
    add(tc("TC-VL-015", "Quy tắc nhập liệu", "Start Date nhỏ hơn thời điểm hiện tại", "Màn Create đang mở", "1. Nhập Start Date trong quá khứ\n2. Click Create", "Start Date < current time", "Hiển thị lỗi: Start date must be greater than or equal to current time.", "Cao"))
    add(tc("TC-VL-016", "Quy tắc nhập liệu", "End Date bắt buộc khi No End Date Off", "No End Date = Off", "1. Bỏ trống End Date\n2. Click Create", "End Date rỗng", "Không cho lưu; End Date bắt buộc khi No End Date Off. Requirement cần xác nhận message required vì SRS chưa nêu rõ.", "Cao"))
    add(tc("TC-VL-017", "Quy tắc nhập liệu", "End Date sai định dạng", "Màn Create đang mở", "1. Nhập End Date sai format\n2. Click Create", "End Date sai format", "Hiển thị lỗi: Invalid end date format.", "Cao"))
    add(tc("TC-VL-018", "Quy tắc nhập liệu", "End Date nhỏ hơn Start Date", "Màn Create đang mở", "1. Nhập End Date < Start Date\n2. Click Create", "End Date < Start Date", "Hiển thị lỗi: End date must be greater than or equal to start date.", "Cao"))
    add(tc("TC-VL-019", "Quy tắc nhập liệu", "No End Date On thì End Date không bắt buộc", "Màn Create đang mở", "1. Bật No End Date\n2. Quan sát End Date\n3. Nhập dữ liệu còn lại hợp lệ\n4. Lưu", "No End Date = On; End Date rỗng", "End Date bị disable/clear; không validate required; request không gửi end date hoặc gửi null theo thiết kế API.", "Cao"))
    add(tc("TC-VL-020", "Quy tắc nhập liệu", "Không upload ảnh popup", "Màn Create đang mở", "1. Không upload Popup image\n2. Click Create", "Không có ảnh", "Không cho lưu vì Popup image bắt buộc. Requirement cần xác nhận message required vì SRS chưa nêu rõ.", "Cao"))
    add(tc("TC-VL-021", "Quy tắc nhập liệu", "Upload ảnh sai định dạng", "Màn Create đang mở", "1. Upload file không phải JPG/PNG", "File GIF/PDF", "Hiển thị lỗi: Invalid image format.", "Cao"))
    add(tc("TC-VL-022", "Quy tắc nhập liệu", "Upload ảnh vượt 2MB", "Màn Create đang mở", "1. Upload ảnh JPG/PNG dung lượng > 2MB", "Ảnh 2.1MB", "Hiển thị lỗi: Image size must not exceed 2MB.", "Cao"))
    add(tc("TC-VL-023", "Quy tắc nhập liệu", "Upload file ảnh rỗng hoặc lỗi đọc file", "Màn Create đang mở", "1. Upload file ảnh rỗng hoặc file lỗi", "File rỗng/lỗi", "Hiển thị lỗi: Invalid image file.", "Cao"))
    add(tc("TC-VL-024", "Quy tắc nhập liệu", "Upload ảnh sai tỷ lệ và không điều chỉnh được", "Màn Create đang mở", "1. Upload ảnh không phải tỷ lệ 16:9 và hệ thống không điều chỉnh được", "Ảnh sai tỷ lệ", "Hiển thị lỗi: Image ratio must be 16:9.", "Trung bình"))
    add(tc("TC-VL-025", "Quy tắc nhập liệu", "Chỉ được chọn một lựa chọn nội dung hiển thị", "Màn Create đang mở", "1. Thử chọn đồng thời Không có nội dung hiển thị và Hiển thị nội dung", "Hai checkbox trong nhóm nội dung", "Hệ thống chỉ cho chọn đúng một lựa chọn.", "Cao"))
    add(tc("TC-VL-026", "Quy tắc nhập liệu", "Title bắt buộc khi chọn Hiển thị nội dung", "Display content được chọn", "1. Bỏ trống Title\n2. Click Create", "Title rỗng", "Hiển thị lỗi: Title is required.", "Cao"))
    add(tc("TC-VL-027", "Quy tắc nhập liệu", "Title vượt 225 ký tự", "Display content được chọn", "1. Nhập Title 226 ký tự\n2. Click Create", "Title 226 ký tự, không tính biến hệ thống", "Hiển thị lỗi: Title must not exceed 225 characters.", "Cao"))
    add(tc("TC-VL-028", "Quy tắc nhập liệu", "Content bắt buộc khi chọn Hiển thị nội dung", "Display content được chọn", "1. Bỏ trống Content\n2. Click Create", "Content rỗng", "Hiển thị lỗi: Content is required.", "Cao"))
    add(tc("TC-VL-029", "Quy tắc nhập liệu", "Content vượt 500 ký tự", "Display content được chọn", "1. Nhập Content 501 ký tự\n2. Click Create", "Content 501 ký tự, không tính biến hệ thống", "Hiển thị lỗi: Description must not exceed 500 characters.", "Cao"))
    add(tc("TC-VL-030", "Quy tắc nhập liệu", "Link điều hướng có nhập nhưng chưa chọn loại điều hướng", "Màn Create đang mở", "1. Nhập Link điều hướng\n2. Không chọn Loại điều hướng\n3. Click Create", "Link bất kỳ; navigation type rỗng", "Hiển thị lỗi: Navigation type is required.", "Cao"))
    add(tc("TC-VL-031", "Quy tắc nhập liệu", "Đã chọn loại điều hướng nhưng chưa nhập link", "Màn Create đang mở", "1. Chọn Loại điều hướng\n2. Bỏ trống Link điều hướng\n3. Click Create", "Navigation type = Webview; Link rỗng", "Hiển thị lỗi: Navigation link is required.", "Cao"))
    add(tc("TC-VL-032", "Quy tắc nhập liệu", "Link điều hướng vượt 1000 ký tự", "Màn Create đang mở", "1. Nhập Link điều hướng 1001 ký tự\n2. Click Create", "Link 1001 ký tự", "Hiển thị lỗi: Link must not exceed 1000 characters.", "Trung bình"))
    add(tc("TC-VL-033", "Quy tắc nhập liệu", "Không chọn đối tượng áp dụng", "Màn Create đang mở", "1. Không chọn Toàn bộ hội viên/Customer Segment/Import file\n2. Click Create", "Audience rỗng", "Hiển thị lỗi: Please select audience.", "Cao"))
    add(tc("TC-VL-034", "Quy tắc nhập liệu", "Chọn Customer Segment nhưng không chọn segment cụ thể", "Audience = Customer Segment", "1. Chọn Customer Segment\n2. Không chọn dropdown segment\n3. Click Create", "Segment rỗng", "Hiển thị lỗi: Please select one Customer Segment.", "Cao"))
    add(tc("TC-VL-035", "Quy tắc nhập liệu", "Chọn Import file nhưng không upload file", "Audience = Import file", "1. Chọn Import file\n2. Không upload file\n3. Click Create", "Không có file", "Hiển thị lỗi: Please upload member file.", "Cao"))
    add(tc("TC-VL-036", "Quy tắc nhập liệu", "Import file rỗng hoặc lỗi đọc file", "Audience = Import file", "1. Upload file rỗng/lỗi", "File rỗng/lỗi", "Hiển thị lỗi: Invalid import file.", "Cao"))
    add(tc("TC-VL-037", "Quy tắc nhập liệu", "Import file sai định dạng mẫu", "Audience = Import file", "1. Upload file không đúng template", "Excel sai template", "Hiển thị lỗi: Invalid import file format.", "Cao"))
    add(tc("TC-VL-038", "Quy tắc nhập liệu", "Không chọn Position", "Màn Create đang mở", "1. Không chọn Position\n2. Click Create", "Position rỗng", "Hiển thị lỗi: Please select at least one Position.", "Cao"))
    add(tc("TC-VL-039", "Quy tắc nhập liệu", "Không chọn loại tần suất hiển thị", "Màn Create đang mở", "1. Không chọn Display Frequency\n2. Click Create", "Frequency rỗng", "Hiển thị lỗi: Please select frequency type.", "Cao"))
    add(tc("TC-VL-040", "Quy tắc nhập liệu", "X lần/ngày không nhập X", "Chọn X lần/ngày", "1. Chọn X times/day\n2. Bỏ trống X\n3. Click Create", "X rỗng", "Hiển thị lỗi: Frequency value is required.", "Cao"))
    add(tc("TC-VL-041", "Quy tắc nhập liệu", "X lần/ngày nhập giá trị không hợp lệ", "Chọn X lần/ngày", "1. Nhập X là chữ/ký tự đặc biệt/số thập phân/số âm/0 hoặc >= 50\n2. Click Create", "abc, @, 1.5, -1, 0, 50", "Hiển thị lỗi: Frequency value must be an integer and less than 50.", "Cao"))
    add(tc("TC-VL-042", "Quy tắc nhập liệu", "X lần/ngày giá trị biên hợp lệ", "Chọn X lần/ngày", "1. Nhập X = 1\n2. Nhập form hợp lệ\n3. Lưu\n4. Lặp lại với X = 49", "X = 1 và X = 49", "Giá trị được chấp nhận nếu các field khác hợp lệ.", "Trung bình"))
    add(tc("TC-VL-043", "Quy tắc nhập liệu", "X lần/tuần không chọn ngày trong tuần", "Chọn X lần/tuần", "1. Chọn X times/week\n2. Nhập X\n3. Không chọn ngày\n4. Click Create", "Không chọn T2-CN", "Hiển thị lỗi: Please select at least one day of week.", "Cao"))
    add(tc("TC-VL-044", "Quy tắc nhập liệu", "Export từng chiến dịch nhưng không chọn campaign", "Popup EXPORT đang mở", "1. Chọn Export từng chiến dịch\n2. Không chọn Popup Name - Campaign\n3. Click Export to excel", "Campaign rỗng", "Hiển thị lỗi: Please select popup campaign.", "Cao"))
    add(tc("TC-VL-045", "Quy tắc nhập liệu", "Export không chọn đủ khoảng thời gian", "Popup EXPORT đang mở", "1. Không chọn hoặc chỉ chọn một ngày trong Export Period\n2. Click Export to excel", "Export Period thiếu ngày", "Hiển thị lỗi: Please select export date range.", "Cao"))
    add(tc("TC-VL-046", "Quy tắc nhập liệu", "Export date_from lớn hơn date_to", "Popup EXPORT đang mở", "1. Nhập tay date_from > date_to\n2. Click Export to excel", "date_from > date_to", "Hiển thị lỗi: Invalid date range.", "Cao"))
    add(tc("TC-VL-047", "Quy tắc nhập liệu", "FE date picker chặn khoảng export lớn hơn 1 năm", "Popup EXPORT đang mở", "1. Mở date picker Export Period\n2. Thử chọn khoảng thời gian > 1 năm", "Khoảng export > 1 năm", "FE không cho chọn khoảng thời gian export lớn hơn 1 năm tính từ thời điểm hiện tại.", "Cao"))

    # Tích hợp
    add(tc("TC-TH-001", "Tích hợp", "Backend xác định trạng thái sau khi tạo campaign", "Form Create hợp lệ", "1. Tạo campaign có Start Date phù hợp\n2. Quan sát phản hồi và danh sách", "Start Date theo rule hệ thống", "Backend trả trạng thái campaign sau khi tạo; FE hiển thị trạng thái này ở danh sách/chi tiết.", "Cao"))
    add(tc("TC-TH-002", "Tích hợp", "Backend validate theo timezone UTC+7", "Có thể thay đổi timezone máy cá nhân", "1. Đổi timezone máy cá nhân\n2. Nhập Start Date gần current time\n3. Lưu", "Timezone máy khác UTC+7", "Backend vẫn validate theo timezone hệ thống UTC+7.", "Cao"))
    add(tc("TC-TH-003", "Tích hợp", "Upload ảnh thất bại", "Màn Create/Edit có field Popup image", "1. Upload ảnh hợp lệ nhưng backend/storage trả lỗi\n2. Quan sát phản hồi", "Ảnh JPG/PNG hợp lệ; upload thất bại", "Hiển thị lỗi: Failed to upload image.", "Cao"))
    add(tc("TC-TH-004", "Tích hợp", "Upload/validate import file thất bại", "Audience = Import file", "1. Upload file theo template\n2. Backend trả lỗi upload/validate", "File Excel; backend lỗi", "Hiển thị lỗi: Failed to upload import file.", "Cao"))
    add(tc("TC-TH-005", "Tích hợp", "FE hiển thị lỗi field khi Backend trả lỗi validate xác định được field", "Form Create/Edit submit lên backend", "1. Gửi dữ liệu khiến backend trả lỗi validate field\n2. Quan sát UI", "Lỗi validate từ backend có field", "FE hiển thị lỗi tại field tương ứng.", "Cao"))
    add(tc("TC-TH-006", "Tích hợp", "FE hiển thị toast khi Backend trả lỗi không xác định field", "Form Create/Edit submit lên backend", "1. Gửi dữ liệu khiến backend trả lỗi chung\n2. Quan sát UI", "Lỗi backend không map field", "Hiển thị toast: Failed to save campaign hoặc Failed to edit campaign theo ngữ cảnh.", "Cao"))
    add(tc("TC-TH-007", "Tích hợp", "Campaign chuyển trạng thái trong lúc edit", "User đang mở màn Edit campaign", "1. Mở Edit campaign\n2. Campaign bị job/người khác đổi trạng thái\n3. Click Save", "Campaign chuyển trạng thái khi edit", "Backend trả lỗi trạng thái; FE reload dữ liệu mới nhất.", "Cao"))
    add(tc("TC-TH-008", "Tích hợp", "Click Pop-up vẫn ghi nhận Click dù link điều hướng không mở được", "Có dữ liệu App/tracking để kiểm thử tích hợp", "1. Cấu hình link sai/không mở được\n2. Hội viên nhấn Pop-up\n3. Kiểm tra dữ liệu báo cáo", "Link điều hướng không mở được", "Click được ghi nhận; không điều hướng và ứng dụng trả thông báo theo mô tả màn hình app. Requirement cần xác nhận vì SRS CMS không có mô tả App chi tiết.", "Trung bình"))
    add(tc("TC-TH-009", "Tích hợp", "Export file dùng dữ liệu báo cáo tổng hợp, không dùng event log thô", "Có quyền truy cập dữ liệu báo cáo", "1. Tạo dữ liệu tracking\n2. Export báo cáo\n3. Đối chiếu file export", "Dữ liệu Reach/Impression/Click/Close/CTR", "File export chứa dữ liệu đã query/tổng hợp/mapping, không xuất event log thô.", "Cao"))
    add(tc("TC-TH-010", "Tích hợp", "Export thất bại", "Popup EXPORT đang mở", "1. Chọn dữ liệu export hợp lệ\n2. Backend export trả lỗi", "Backend lỗi export", "Hiển thị toast: Failed to export report.", "Cao"))

    # Hồi quy
    add(tc("TC-RG-001", "Hồi quy", "Không ảnh hưởng đăng nhập CMS", "Build có chức năng Pop-up", "1. Đăng nhập CMS bằng tài khoản hợp lệ\n2. Đăng xuất\n3. Đăng nhập lại", "Tài khoản CMS hợp lệ", "Luồng đăng nhập/đăng xuất CMS hoạt động bình thường.", "Cao"))
    add(tc("TC-RG-002", "Hồi quy", "Không ảnh hưởng module Customer Segment hiện hữu", "Có quyền truy cập module Segment", "1. Mở module Customer Segment\n2. Xem danh sách segment\n3. Chọn segment dùng trong Pop-up", "Segment đang tồn tại", "Module Segment hoạt động bình thường; dữ liệu segment dùng trong Pop-up nhất quán.", "Cao"))
    add(tc("TC-RG-003", "Hồi quy", "Không ảnh hưởng template import của Notification được tham chiếu", "Có chức năng Notification/template hiện hữu", "1. Mở chức năng liên quan template import Notification\n2. Tải template\n3. Đối chiếu template dùng cho Pop-up", "Template import Notification", "Template hiện hữu không bị thay đổi ngoài phạm vi đã chốt.", "Trung bình"))
    add(tc("TC-RG-004", "Hồi quy", "Không ảnh hưởng chuẩn phân trang chung của CMS", "Có màn CMS khác dùng pagination chung", "1. Kiểm tra phân trang ở màn Pop-up\n2. Kiểm tra một màn CMS khác", "Dữ liệu nhiều trang", "Chuẩn phân trang hoạt động nhất quán và không bị lỗi.", "Trung bình"))
    add(tc("TC-RG-005", "Hồi quy", "Không ảnh hưởng chuẩn toast/modal chung", "Có màn CMS khác dùng toast/modal", "1. Gây toast thành công/thất bại ở Pop-up\n2. Kiểm tra toast/modal ở màn CMS khác", "Thông báo success/error", "Toast/modal hiển thị đúng chuẩn hiện hữu.", "Trung bình"))
    add(tc("TC-RG-006", "Hồi quy", "Không ảnh hưởng export Excel của module khác nếu dùng chung cơ chế", "Có module khác hỗ trợ export", "1. Export báo cáo Pop-up\n2. Export file ở module khác", "Dữ liệu export hợp lệ", "Export ở module khác vẫn hoạt động bình thường.", "Trung bình"))

    # UI/UX
    add(tc("TC-UI-001", "UI/UX", "Hiển thị đúng nhãn và thành phần màn danh sách", "User có quyền Pop-up", "1. Mở màn danh sách\n2. Đối chiếu các label/filter/button/table column", "Mockup/SRS màn danh sách", "Các nhãn Search by Code, Search by popup, Status, Customer Segment, Position, Effective Period, Export to Excel, Create và cột bảng hiển thị đúng.", "Trung bình"))
    add(tc("TC-UI-002", "UI/UX", "Status dropdown chỉ cho chọn một giá trị", "Màn danh sách đang mở", "1. Mở Status dropdown\n2. Thử chọn nhiều trạng thái", "Tất cả, Scheduled, Active, Inactive, Expired", "Chỉ một trạng thái được chọn tại một thời điểm; mặc định là Tất cả.", "Trung bình"))
    add(tc("TC-UI-003", "UI/UX", "Customer Segment dropdown chỉ cho chọn một giá trị", "Màn danh sách đang mở", "1. Mở Customer Segment dropdown\n2. Thử chọn nhiều giá trị", "Tất cả, Toàn bộ người dùng, Segment, Import file", "Chỉ một giá trị được chọn tại một thời điểm.", "Trung bình"))
    add(tc("TC-UI-004", "UI/UX", "Hiển thị Position nhiều dòng hoặc phân tách theo chuẩn UI", "Campaign có nhiều Position", "1. Mở danh sách\n2. Quan sát cột Position của campaign nhiều vị trí", "Campaign có từ 2 Position trở lên", "Position hiển thị rõ ràng, xuống dòng hoặc phân tách theo chuẩn UI hiện hữu.", "Thấp"))
    add(tc("TC-UI-005", "UI/UX", "Hiển thị Effective Period với No End Date", "Có campaign No End Date", "1. Mở danh sách hoặc chi tiết\n2. Quan sát Effective Period", "Start Date; No End Date", "Hiển thị start date - No End Date hoặc format tương đương.", "Trung bình"))
    add(tc("TC-UI-006", "UI/UX", "Tooltip Priority hiển thị đúng nội dung", "Màn Create hoặc Edit đang mở", "1. Hover/click icon thông tin cạnh Priority", "Icon thông tin Priority", "Tooltip hiển thị: Smaller numbers take display priority.", "Thấp"))
    add(tc("TC-UI-007", "UI/UX", "Tooltip Các biến hệ thống hiển thị đúng nội dung", "Màn Create hoặc Edit đang mở", "1. Hover/click icon thông tin cạnh Các biến hệ thống", "Icon thông tin System Variables", "Tooltip hiển thị: Click the system variables field to insert them into the content.", "Thấp"))
    add(tc("TC-UI-008", "UI/UX", "Khi chọn Không có nội dung hiển thị thì disable Title và Content", "Màn Create đang mở", "1. Chọn Không có nội dung hiển thị\n2. Quan sát Title và Content", "No content displayed", "Các trường trong phần nội dung hiển thị cùng popup bị disable và không bắt buộc.", "Trung bình"))
    add(tc("TC-UI-009", "UI/UX", "Khi chọn Hiển thị nội dung thì Title và Content enable", "Màn Create đang mở", "1. Chọn Hiển thị nội dung\n2. Quan sát Title và Content", "Display content", "Title và Content enable và bắt buộc nhập.", "Trung bình"))
    add(tc("TC-UI-010", "UI/UX", "Language dropdown mặc định theo ngôn ngữ CMS hiện hữu", "Màn Create đang mở", "1. Quan sát dropdown Language ở góc phải màn hình", "Ngôn ngữ CMS hiện hữu", "Language hiển thị mặc định theo ngôn ngữ CMS hiện hữu, ví dụ Tiếng Việt.", "Thấp"))
    return rows


def build_sheets():
    cases = build_test_cases()
    overview = [
        ["Hạng mục", "Nội dung"],
        ["Tên chức năng", "Chiến dịch Pop-up trên CMS Lotusmiles"],
        ["Nguồn yêu cầu", "SRS CMS Pop-up - Chiến dịch Marketing phiên bản 1.33 và kết quả review yêu cầu trước đó"],
        ["Phạm vi chính", "Danh sách/tìm kiếm/lọc, tạo, chỉnh sửa, xem chi tiết, xóa, xuất báo cáo, phân quyền, validation, tích hợp và hồi quy CMS"],
        ["Lưu ý", "Các phần App, API, cơ sở dữ liệu, tracking và lifecycle còn thiếu chi tiết; các ca liên quan được đánh dấu Requirement cần xác nhận khi cần."],
    ]
    test_cases = [HEADERS] + cases
    categories = {}
    priorities = {}
    for row in cases:
        categories[row[1]] = categories.get(row[1], 0) + 1
        priorities[row[7]] = priorities.get(row[7], 0) + 1
    summary = [
        ["Chỉ số", "Số lượng/Ghi chú"],
        ["Tổng số ca kiểm thử", len(cases)],
        ["Ca kiểm thử tích cực", 55],
        ["Ca kiểm thử âm tính", 38],
        ["Ca kiểm thử biên", 10],
        ["Ca UI/UX", categories.get("UI/UX", 0)],
        ["Ca phân quyền", categories.get("Phân Quyền", 0)],
        ["Ưu tiên Cao", priorities.get("Cao", 0)],
        ["Ưu tiên Trung bình", priorities.get("Trung bình", 0)],
        ["Ưu tiên Thấp", priorities.get("Thấp", 0)],
        ["Phân bổ theo danh mục", "; ".join(f"{k}: {v}" for k, v in categories.items())],
    ]
    risks = [
        ["Loại", "Nội dung", "Khuyến nghị"],
        ["Requirement cần xác nhận", "Lifecycle chưa thống nhất giữa Inactive và Expired.", "BA/PO cần chốt sơ đồ trạng thái và trigger chuyển trạng thái trước khi kiểm thử end-to-end."],
        ["Requirement cần xác nhận", "Chưa có đặc tả API endpoint/request/response/status code.", "Bổ sung API spec trước khi tạo bộ ca API đầy đủ."],
        ["Requirement cần xác nhận", "Chưa có mô hình dữ liệu, audit log và rule persistence.", "Bổ sung DB design hoặc data contract để kiểm thử dữ liệu."],
        ["Requirement cần xác nhận", "Template import file, max size, max rows, duplicate member chưa chốt.", "Chốt template và rule xử lý dữ liệu import."],
        ["Requirement cần xác nhận", "Rule priority khi nhiều campaign cùng điều kiện chưa đủ.", "Bổ sung tie-breaker khi trùng Priority và Created Date."],
        ["Requirement cần xác nhận", "CTR khi Impression = 0 chưa chốt hiển thị 0% hay '-'.", "Chốt format hiển thị trong CMS và file export."],
        ["Requirement cần xác nhận", "OTP chưa có rule sai OTP, hết hạn, retry, resend.", "Bổ sung rule OTP để tạo ca kiểm thử đầy đủ."],
        ["Rủi ro kiểm thử", "Không có đặc tả App chi tiết cho luồng hiển thị Pop-up.", "Không đóng phạm vi App nếu chưa có SRS/App spec riêng."],
        ["Rủi ro kiểm thử", "Thiếu dữ liệu tracking/reporting thực tế có thể làm chặn ca export.", "Chuẩn bị dữ liệu Reach/Impression/Click/Close/CTR trước vòng test chính."],
        ["Khuyến nghị", "Ưu tiên tự động hóa hồi quy các luồng danh sách, tạo hợp lệ, validation bắt buộc, sửa theo trạng thái và export.", "Đưa các ca ưu tiên Cao vào regression suite."],
    ]
    return [
        ("Tổng quan", overview, [26, 120]),
        ("Ca kiểm thử", test_cases, [14, 18, 44, 42, 58, 38, 58, 14, 16]),
        ("Tổng hợp bao phủ", summary, [32, 110]),
        ("Rủi ro câu hỏi", risks, [28, 80, 80]),
    ]


def build_xlsx():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    sheets = build_sheets()
    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        zf.writestr("_rels/.rels", root_rels_xml())
        zf.writestr("xl/workbook.xml", workbook_xml([s[0] for s in sheets]))
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(len(sheets)))
        zf.writestr("xl/styles.xml", styles_xml())
        zf.writestr("docProps/core.xml", core_xml())
        zf.writestr("docProps/app.xml", app_xml([s[0] for s in sheets]))
        for i, (_, rows, widths) in enumerate(sheets, 1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows, widths))
    print(OUT_PATH)


if __name__ == "__main__":
    build_xlsx()
