from __future__ import annotations

import html
import os
import zipfile
from datetime import datetime


OUT_PATH = "deliverables/Ke_hoach_kiem_thu_CMS_Popup_Campaign.docx"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def run_xml(text: str, bold: bool = False, color: str | None = None, size: int | None = None) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    if size:
        props.append(f'<w:sz w:val="{size * 2}"/>')
        props.append(f'<w:szCs w:val="{size * 2}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r>"


def para(text: str = "", style: str | None = None, bold: bool = False, color: str | None = None, size: int | None = None,
         num_id: int | None = None, level: int = 0, keep_next: bool = False) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        ppr.append("<w:keepNext/>")
    if num_id is not None:
        ppr.append(f'<w:numPr><w:ilvl w:val="{level}"/><w:numId w:val="{num_id}"/></w:numPr>')
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr_xml}{run_xml(text, bold=bold, color=color, size=size)}</w:p>"


def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def cell(text: str, width: int, fill: str | None = None, bold: bool = False, align: str = "left") -> str:
    shd = f'<w:shd w:fill="{fill}"/>' if fill else ""
    jc = f'<w:jc w:val="{align}"/>' if align != "left" else ""
    return (
        f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}'
        '<w:tcMar><w:top w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'
        "</w:tcPr>"
        f"<w:p><w:pPr>{jc}</w:pPr>{run_xml(text, bold=bold)}</w:p></w:tc>"
    )


def table(headers: list[str], rows: list[list[str]], widths: list[int]) -> str:
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    tbl = [
        '<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblInd w:w="120" w:type="dxa"/>'
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="B8C2CC"/>'
        '<w:left w:val="single" w:sz="4" w:color="B8C2CC"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="B8C2CC"/>'
        '<w:right w:val="single" w:sz="4" w:color="B8C2CC"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="D8DEE6"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="D8DEE6"/></w:tblBorders>'
        '<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        "</w:tblPr>",
        f"<w:tblGrid>{grid}</w:tblGrid>",
    ]
    tbl.append("<w:tr>" + "".join(cell(h, w, fill="F2F4F7", bold=True, align="center") for h, w in zip(headers, widths)) + "</w:tr>")
    for row in rows:
        tbl.append("<w:tr>" + "".join(cell(v, w) for v, w in zip(row, widths)) + "</w:tr>")
    tbl.append("</w:tbl>")
    return "".join(tbl)


def bullet(text: str) -> str:
    return para(text, num_id=1)


def numbered(text: str) -> str:
    return para(text, num_id=2)


def build_document_body() -> str:
    parts: list[str] = []
    parts.append(para("KẾ HOẠCH KIỂM THỬ", "Title"))
    parts.append(para("Chức năng Chiến dịch Pop-up trên CMS Lotusmiles", "Subtitle"))
    parts.append(table(
        ["Thông tin", "Giá trị"],
        [
            ["Dự án", "Lotusmiles - Quản lý chiến dịch Pop-up trên CMS"],
            ["Phiên bản tài liệu", "1.0"],
            ["Nguồn đầu vào", "SRS CMS Pop-up - Chiến dịch Marketing phiên bản 1.33 và kết quả review yêu cầu"],
            ["Người lập", "Trưởng nhóm QA"],
            ["Ngày lập", "07/07/2026"],
            ["Trạng thái", "Dự thảo chờ BA/PO xác nhận các điểm mở"],
        ],
        [2200, 7160],
    ))
    parts.append(para("Ghi chú trọng yếu", "Heading2"))
    parts.append(para(
        "Tài liệu SRS hiện đặc tả chi tiết phần CMS, nhưng còn thiếu hoặc chưa chốt nhiều nội dung về ứng dụng, API, cơ sở dữ liệu, ghi nhận sự kiện, vòng đời trạng thái và phân quyền chi tiết. Kế hoạch kiểm thử này ưu tiên phạm vi CMS đã có căn cứ, đồng thời ghi nhận các hạng mục chưa đủ thông tin trong phần câu hỏi mở và rủi ro.",
        "Normal",
    ))

    parts.append(para("1. Tổng quan dự án", "Heading1"))
    parts.append(table(
        ["Hạng mục", "Nội dung"],
        [
            ["Tên dự án", "Lotusmiles - Quản lý chiến dịch Pop-up trên CMS"],
            ["Tên chức năng", "Chiến dịch Pop-up trên CMS"],
            ["Mô tả", "Cho phép đội vận hành tạo, chỉnh sửa, xem, xóa, lọc, quản lý trạng thái và xuất báo cáo chiến dịch Pop-up hiển thị trên ứng dụng Lotusmiles."],
            ["Mục tiêu kiểm thử", "Xác nhận chức năng CMS hoạt động đúng yêu cầu, dữ liệu hợp lệ được xử lý chính xác, quyền truy cập được kiểm soát, báo cáo xuất đúng quy tắc đã chốt và các rủi ro yêu cầu được phát hiện sớm."],
            ["Đối tượng sử dụng", "Admin CMS, Manager CMS có quyền Pop-up, người dùng CMS không có quyền Pop-up, hội viên ứng dụng là đối tượng nhận Pop-up."],
        ],
        [2200, 7160],
    ))

    parts.append(para("2. Phạm vi kiểm thử", "Heading1"))
    parts.append(para("2.1. Trong phạm vi", "Heading2"))
    in_scope = [
        "Màn danh sách chiến dịch Pop-up: tìm kiếm theo mã/tên, lọc theo trạng thái, đối tượng, vị trí, thời gian hiệu lực, phân trang, sắp xếp và hiển thị dữ liệu.",
        "Tạo chiến dịch Pop-up: thông tin chung, thời gian hiệu lực, ảnh, nội dung hiển thị, biến hệ thống, điều hướng, đối tượng áp dụng, vị trí, tần suất, xác nhận OTP.",
        "Chỉnh sửa chiến dịch theo trạng thái Scheduled, Active, Inactive, Expired theo phạm vi trường được phép chỉnh sửa.",
        "Xem chi tiết chiến dịch ở chế độ chỉ đọc.",
        "Xóa chiến dịch ở trạng thái Scheduled, xác nhận OTP, cập nhật danh sách sau xóa.",
        "Xuất báo cáo theo từng chiến dịch và toàn bộ chiến dịch theo khoảng thời gian.",
        "Kiểm thử quy tắc nhập liệu, tình huống âm tính, trạng thái rỗng, trạng thái lỗi, phân quyền, thao tác đồng thời cơ bản và hồi quy CMS.",
    ]
    parts.extend(bullet(x) for x in in_scope)
    parts.append(para("2.2. Ngoài phạm vi", "Heading2"))
    out_scope = [
        "Kiểm thử chi tiết ứng dụng hiển thị Pop-up nếu chưa có đặc tả ứng dụng đầy đủ.",
        "Kiểm thử API chuyên sâu nếu chưa có tài liệu endpoint, request, response, mã lỗi và quyền API.",
        "Kiểm thử cơ sở dữ liệu chuyên sâu nếu chưa có mô hình dữ liệu, nhật ký kiểm toán và quy tắc lưu trữ dữ liệu.",
        "Kiểm thử hiệu năng tải lớn cho nhập file và xuất báo cáo nếu chưa có tiêu chí số lượng dữ liệu.",
        "Kiểm thử bảo mật chuyên sâu như kiểm thử xâm nhập; chỉ thực hiện kiểm tra quyền chức năng ở mức QA.",
    ]
    parts.extend(bullet(x) for x in out_scope)

    parts.append(para("3. Chiến lược kiểm thử", "Heading1"))
    parts.append(table(
        ["Loại kiểm thử", "Cách tiếp cận", "Ưu tiên"],
        [
            ["Kiểm thử chức năng", "Xác minh từng luồng CMS theo SRS: danh sách, tạo, sửa, xem, xóa, xuất báo cáo.", "Cao"],
            ["Kiểm thử giao diện", "Đối chiếu bản thiết kế màn hình, nhãn, trạng thái nút, trạng thái rỗng, thông báo lỗi, popup xác nhận.", "Trung bình"],
            ["Kiểm thử quy tắc nhập liệu", "Bao phủ trường bắt buộc, độ dài tối đa, khoảng ngày, tải file lên, tần suất, đối tượng áp dụng, điều hướng và kỳ xuất báo cáo.", "Cao"],
            ["Kiểm thử tích hợp", "Kiểm tra tích hợp Segment, tải file lên, xuất báo cáo và ghi nhận sự kiện/báo cáo ở mức có tài liệu hỗ trợ.", "Cao"],
        ["Kiểm thử API", "Thực hiện khi có đặc tả API; hiện ghi nhận là phụ thuộc mở.", "Trung bình"],
            ["Kiểm thử cơ sở dữ liệu", "Kiểm tra lưu trữ dữ liệu, trạng thái, xóa, nhật ký kiểm toán và dữ liệu báo cáo khi có quyền truy cập và lược đồ dữ liệu.", "Trung bình"],
            ["Kiểm thử phân quyền", "Xác minh menu, truy cập URL trực tiếp, thao tác theo vai trò và trạng thái chiến dịch.", "Cao"],
            ["Kiểm thử tương thích", "Kiểm thử các trình duyệt CMS được dự án hỗ trợ sau khi PO xác nhận danh sách.", "Trung bình"],
            ["Kiểm thử hồi quy", "Chạy lại bộ ca kiểm thử ưu tiên cao cho các chức năng CMS liên quan và mô-đun Segment/Notification nếu bị ảnh hưởng.", "Cao"],
            ["Kiểm thử khói", "Xác nhận bản dựng có thể đăng nhập, mở menu Pop-up, tải danh sách, tạo dữ liệu tối thiểu.", "Cao"],
            ["Kiểm thử xác nhận nhanh", "Xác nhận các lỗi đã sửa và luồng liên quan trực tiếp.", "Cao"],
            ["Kiểm thử khám phá", "Tập trung vào thao tác đồng thời, dữ liệu cũ trên màn hình, nhập liệu bất thường, xuất báo cáo không có dữ liệu và trạng thái biên.", "Trung bình"],
            ["Kiểm thử âm tính", "Bao phủ sai quyền, sai trạng thái, dữ liệu không hợp lệ, lỗi tải lên, lỗi xuất báo cáo, mất phiên đăng nhập.", "Cao"],
        ],
        [1900, 5960, 1500],
    ))

    parts.append(para("4. Mức kiểm thử", "Heading1"))
    parts.append(table(
        ["Mức kiểm thử", "Mục tiêu", "Chủ sở hữu"],
        [
            ["Kiểm thử đơn vị", "Tham chiếu để Dev xác nhận logic kiểm tra dữ liệu, vòng đời trạng thái, phân quyền và tính toán báo cáo.", "Dev"],
            ["Kiểm thử tích hợp", "Xác minh CMS phối hợp đúng với dịch vụ máy chủ, Segment, tải dữ liệu lên, xuất báo cáo và ghi nhận sự kiện.", "QA/Dev"],
            ["Kiểm thử hệ thống", "Kiểm thử toàn trình trên môi trường tích hợp theo luồng nghiệp vụ CMS.", "QA"],
            ["Kiểm thử chấp nhận người dùng", "Hỗ trợ BA/PO và vận hành xác nhận nghiệp vụ chiến dịch.", "QA/BA/PO"],
            ["Kiểm thử hồi quy", "Đảm bảo thay đổi không ảnh hưởng chức năng CMS liên quan.", "QA"],
            ["Kiểm thử khói", "Xác nhận bản dựng đủ ổn định để bắt đầu kiểm thử chi tiết.", "QA"],
        ],
        [2200, 5560, 1600],
    ))

    parts.append(para("5. Môi trường kiểm thử", "Heading1"))
    parts.append(table(
        ["Thành phần", "Yêu cầu/Trạng thái"],
        [
            ["Môi trường", "Môi trường kiểm thử tích hợp hoặc UAT có dữ liệu CMS và tài khoản phân quyền."],
            ["Giao diện CMS", "Đường dẫn CMS kiểm thử cần được cung cấp trước khi thực thi."],
            ["Dịch vụ máy chủ", "Dịch vụ CMS, Pop-up, Segment và xuất báo cáo đã triển khai đúng phiên bản."],
            ["Cơ sở dữ liệu", "Có dữ liệu chiến dịch, segment, hội viên, ghi nhận sự kiện/báo cáo phục vụ kiểm thử."],
            ["API", "Endpoint và tài liệu API chưa có trong SRS; cần bổ sung trước khi kiểm thử API đầy đủ."],
            ["Trình duyệt", "Cần PO/Dev xác nhận danh sách hỗ trợ, tối thiểu nên gồm Chrome và Edge phiên bản hiện hành."],
            ["Tài khoản kiểm thử", "Admin CMS có quyền Pop-up, Manager CMS có quyền Pop-up, user CMS không có quyền Pop-up, tài khoản chỉ xem nếu có."],
            ["Quyền yêu cầu", "Xem, tạo, chỉnh sửa, xóa, xuất báo cáo, tải ảnh lên, nhập file; ma trận quyền cần được xác nhận."],
        ],
        [2200, 7160],
    ))

    parts.append(para("6. Tiêu chí đầu vào", "Heading1"))
    for item in [
        "SRS hoặc tài liệu bổ sung đã được BA/PO phê duyệt cho phạm vi CMS.",
        "Các điểm mở mức cao về vòng đời trạng thái, phân quyền, xuất báo cáo và nhập file đã có câu trả lời hoặc được đánh dấu chấp nhận rủi ro.",
        "Bản dựng đã triển khai lên môi trường kiểm thử và vượt kiểm thử khói kỹ thuật.",
        "Tài khoản, quyền, dữ liệu segment, dữ liệu hội viên, mẫu nhập file và dữ liệu chiến dịch mẫu đã sẵn sàng.",
        "Công cụ quản lý lỗi và nơi lưu báo cáo kiểm thử đã được thống nhất.",
    ]:
        parts.append(bullet(item))

    parts.append(para("7. Tiêu chí đầu ra", "Heading1"))
    for item in [
        "Toàn bộ ca kiểm thử ưu tiên cao đã được thực thi.",
        "Không còn lỗi mức Chặn hoặc Nghiêm trọng đang mở trong phạm vi phát hành.",
        "Lỗi mức Cao còn mở phải có phương án xử lý hoặc chấp nhận rủi ro bởi PO.",
        "Kiểm thử hồi quy các luồng CMS chính đã hoàn tất.",
        "Báo cáo thực thi và báo cáo tổng kết kiểm thử đã được gửi cho các bên liên quan.",
        "Các điểm chưa kiểm thử do thiếu yêu cầu được ghi nhận minh bạch trong báo cáo.",
    ]:
        parts.append(bullet(item))

    parts.append(para("8. Sản phẩm bàn giao kiểm thử", "Heading1"))
    parts.append(table(
        ["Sản phẩm", "Mô tả"],
        [
            ["Kế hoạch kiểm thử", "Tài liệu hiện tại, dùng để thống nhất phạm vi, chiến lược, rủi ro và lịch kiểm thử."],
            ["Bộ ca kiểm thử", "Ca kiểm thử chi tiết theo màn hình, luồng nghiệp vụ, quy tắc nhập liệu, phân quyền, xuất báo cáo và tình huống âm tính."],
            ["Dữ liệu kiểm thử", "Chiến dịch, segment, file nhập hợp lệ/không hợp lệ, tài khoản phân quyền, dữ liệu báo cáo."],
            ["Báo cáo lỗi", "Lỗi ghi nhận trên công cụ quản lý lỗi với mức độ, bước tái hiện, kết quả thực tế và mong đợi."],
            ["Báo cáo thực thi", "Tiến độ chạy test, trạng thái đạt, không đạt, bị chặn và danh sách lỗi liên quan."],
            ["Báo cáo tổng kết", "Kết luận chất lượng, rủi ro tồn đọng và khuyến nghị phát hành."],
        ],
        [2500, 6860],
    ))

    parts.append(para("9. Phân tích rủi ro", "Heading1"))
    parts.append(table(
        ["Nhóm rủi ro", "Mô tả", "Ảnh hưởng", "Xác suất", "Giảm thiểu"],
        [
            ["Kỹ thuật", "Thiếu đặc tả API, lược đồ cơ sở dữ liệu và hợp đồng ghi nhận sự kiện.", "Không kiểm thử được toàn trình đầy đủ.", "Cao", "Yêu cầu tài liệu bổ sung trước khi đóng phạm vi kiểm thử."],
            ["Nghiệp vụ", "Vòng đời trạng thái chưa thống nhất giữa Inactive và Expired.", "Sai trạng thái chiến dịch, sai thao tác CMS, sai hiển thị trên ứng dụng.", "Cao", "BA/PO chốt sơ đồ trạng thái và điều kiện kích hoạt chuyển trạng thái."],
            ["Nghiệp vụ", "Quy tắc ưu tiên khi nhiều chiến dịch cùng điều kiện chưa đủ.", "Chiến dịch marketing hiển thị không đúng ưu tiên.", "Trung bình", "Bổ sung quy tắc phân định rõ ràng theo Priority, ngày tạo và điều kiện khác."],
            ["Dữ liệu", "Nhập file chưa có mẫu, số dòng tối đa và quy tắc xử lý trùng.", "Không kiểm soát được đối tượng áp dụng và lỗi vận hành.", "Cao", "Chốt mẫu nhập, quy tắc nhập liệu và bộ file kiểm thử chuẩn."],
            ["Báo cáo", "CTR, trường hợp không có dữ liệu, múi giờ và sự kiện ghi nhận trùng chưa chốt.", "Số liệu báo cáo không đáng tin cậy.", "Cao", "Chốt công thức, cách làm tròn, múi giờ và quy tắc chống trùng sự kiện."],
            ["Phân quyền", "Ma trận quyền theo vai trò và thao tác chưa đầy đủ.", "Rủi ro truy cập hoặc xuất dữ liệu sai quyền.", "Trung bình", "Bổ sung ma trận phân quyền và kiểm thử URL trực tiếp."],
            ["Môi trường", "Thiếu dữ liệu segment, hội viên và báo cáo giống thực tế.", "Nhiều ca kiểm thử bị chặn hoặc kết quả không đại diện.", "Trung bình", "Chuẩn bị dữ liệu trước vòng thực thi chính."],
            ["Tiến độ", "Nhiều điểm mở có thể làm phát sinh thay đổi sau khi ca kiểm thử đã viết.", "Tăng effort cập nhật ca kiểm thử và hồi quy.", "Trung bình", "Chốt yêu cầu theo mốc, quản lý thay đổi bằng phiên bản."],
        ],
        [1300, 2600, 2200, 1100, 2160],
    ))

    parts.append(para("10. Giả định và câu hỏi mở", "Heading1"))
    parts.append(para("10.1. Giả định", "Heading2"))
    for item in [
        "Phạm vi kiểm thử chính của tài liệu này là CMS vì SRS hiện mô tả CMS chi tiết nhất.",
        "Các tiêu chuẩn CMS chung như phân trang, toast, modal, session timeout và quyền nền tảng sẽ được cung cấp từ tài liệu chuẩn CMS hiện hữu.",
        "Kiểm thử API, cơ sở dữ liệu và ứng dụng chỉ được lập chi tiết sau khi có tài liệu bổ sung hoặc xác nhận chính thức.",
    ]:
        parts.append(bullet(item))
    parts.append(para("10.2. Câu hỏi mở cần BA/PO xác nhận", "Heading2"))
    questions = [
        "Khi chiến dịch hết End Date, trạng thái cuối là Expired hay tự chuyển Inactive?",
        "Có chức năng sao chép chiến dịch không? Nếu có, trường nào được sao chép và trường nào phải nhập lại?",
        "Danh sách Position chính thức gồm những giá trị nào và lấy từ nguồn nào?",
        "Nếu nhiều chiến dịch cùng Position, cùng Priority và cùng Created Date thì chiến dịch nào được ưu tiên?",
        "Chiến dịch No End Date được dừng bằng cách nào và có bao giờ chuyển Expired không?",
        "Ứng dụng gọi và hiển thị Pop-up tại thời điểm nào trong vòng đời ứng dụng?",
        "Format hợp lệ cho từng loại điều hướng là gì?",
        "Nếu không xử lý được biến hệ thống thì ứng dụng hiển thị thế nào?",
        "Mẫu nhập file có cột bắt buộc, dung lượng tối đa, số dòng tối đa và quy tắc trùng dữ liệu như thế nào?",
        "Customer Segment bị sửa hoặc xóa sau khi chiến dịch tạo thì chiến dịch dùng dữ liệu chụp tại thời điểm tạo hay dữ liệu mới nhất?",
        "CTR khi Impression bằng 0 hiển thị là 0% hay dấu gạch ngang?",
        "Xuất dữ liệu có áp dụng phân quyền theo người sở hữu, nhóm hoặc vai trò không?",
        "OTP có thời hạn, retry, resend và error message như thế nào?",
        "Đặc tả API sẽ được bổ sung trong SRS hay quản lý ở tài liệu riêng?",
        "Có bắt buộc nhật ký kiểm toán cho tạo, chỉnh sửa, xóa, xuất báo cáo và thay đổi trạng thái không?",
    ]
    parts.extend(numbered(q) for q in questions)

    parts.append(para("11. Kế hoạch nguồn lực", "Heading1"))
    parts.append(table(
        ["Vai trò", "Số lượng", "Trách nhiệm", "Ước lượng"],
        [
            ["Trưởng nhóm QA", "1", "Quản lý kế hoạch, review ca kiểm thử, phân tích rủi ro, báo cáo chất lượng.", "20-30 giờ"],
            ["QA chức năng", "1-2", "Thiết kế và thực thi ca kiểm thử CMS, quy tắc nhập liệu, phân quyền, xuất báo cáo và hồi quy.", "8-12 ngày công"],
            ["QA API/cơ sở dữ liệu", "1", "Kiểm thử API/DB khi có tài liệu và quyền truy cập.", "3-5 ngày công"],
            ["BA/PO", "1-2", "Giải đáp yêu cầu, xác nhận UAT và chấp nhận rủi ro.", "Theo lịch dự án"],
            ["Dev/DevOps", "Theo nhóm", "Hỗ trợ bản dựng, môi trường, log, dữ liệu và sửa lỗi.", "Theo lịch dự án"],
        ],
        [1800, 1200, 4200, 2160],
    ))
    parts.append(para("Ước lượng hồi quy: 2-4 ngày công cho bộ ca kiểm thử ưu tiên cao, tùy số lượng lỗi sửa và phạm vi ảnh hưởng.", "Normal"))

    parts.append(para("12. Lịch kiểm thử dự kiến", "Heading1"))
    parts.append(table(
        ["Mốc", "Hoạt động", "Thời lượng dự kiến", "Điều kiện hoàn tất"],
        [
            ["Review yêu cầu", "Phân tích SRS, ghi nhận gap, xác nhận câu hỏi mở.", "1-2 ngày", "Danh sách gap/rủi ro được gửi BA/PO."],
            ["Kế hoạch kiểm thử", "Hoàn thiện và thống nhất phạm vi, chiến lược, nguồn lực.", "1 ngày", "Kế hoạch kiểm thử được review."],
            ["Thiết kế ca kiểm thử", "Viết ca kiểm thử CMS, quy tắc nhập liệu, phân quyền, xuất báo cáo và tình huống âm tính.", "3-5 ngày", "Ca kiểm thử được Trưởng nhóm QA rà soát."],
            ["Chuẩn bị dữ liệu", "Tạo tài khoản, segment, chiến dịch, file nhập và dữ liệu báo cáo.", "1-2 ngày", "Dữ liệu sẵn sàng trên môi trường kiểm thử."],
            ["Thực thi kiểm thử", "Chạy ca kiểm thử theo ưu tiên và ghi nhận lỗi.", "5-8 ngày", "Hoàn tất ca kiểm thử ưu tiên cao và trung bình."],
            ["Hồi quy", "Chạy lại luồng chính và ca kiểm thử liên quan lỗi đã sửa.", "2-4 ngày", "Không còn lỗi chặn/nghiêm trọng."],
            ["Hỗ trợ UAT", "Hỗ trợ BA/PO xác nhận nghiệp vụ.", "1-3 ngày", "UAT được xác nhận hoặc danh sách tồn đọng."],
            ["Xác minh phát hành", "Kiểm thử khói sau triển khai bản ứng viên phát hành.", "0.5-1 ngày", "Báo cáo xác minh phát hành."],
        ],
        [1500, 3600, 1700, 2560],
    ))

    parts.append(para("13. Chỉ số kiểm thử", "Heading1"))
    parts.append(table(
        ["Chỉ số", "Cách theo dõi"],
        [
            ["Tổng số ca kiểm thử", "Theo bộ ca kiểm thử đã phê duyệt."],
            ["Đã thực thi", "Số ca kiểm thử có kết quả Đạt, Không đạt hoặc Bị chặn."],
            ["Đạt", "Ca kiểm thử có kết quả đúng mong đợi."],
            ["Không đạt", "Ca kiểm thử phát hiện lỗi hoặc sai khác yêu cầu."],
            ["Bị chặn", "Ca kiểm thử không thể chạy do môi trường, dữ liệu, quyền hoặc thiếu yêu cầu."],
            ["Chưa thực thi", "Ca kiểm thử chưa chạy tại thời điểm báo cáo."],
            ["Tổng số lỗi", "Theo công cụ quản lý lỗi, phân loại theo severity và priority."],
            ["Phân bố mức độ lỗi", "Chặn, Nghiêm trọng, Cao, Trung bình, Thấp."],
            ["Tỷ lệ lỗi rò rỉ", "Áp dụng sau phát hành nếu có lỗi môi trường thật trong phạm vi chức năng."],
        ],
        [2700, 6660],
    ))

    parts.append(para("14. Khuyến nghị", "Heading1"))
    recommendations = [
        "Chốt sơ đồ trạng thái chiến dịch trước khi viết ca kiểm thử chi tiết để tránh sai lệch kỳ vọng giữa CMS và ứng dụng.",
        "Bổ sung đặc tả API và hợp đồng dữ liệu cho tải lên, nhập file, xuất báo cáo, ghi nhận sự kiện và phân quyền.",
        "Chuẩn hóa toàn bộ thông báo kiểm tra dữ liệu, đặc biệt thông báo của Description, Navigation và Frequency.",
        "Xây dựng bộ dữ liệu kiểm thử chuẩn gồm chiến dịch theo từng trạng thái, segment, file nhập hợp lệ/không hợp lệ và dữ liệu ghi nhận sự kiện.",
        "Ưu tiên tự động hóa hồi quy cho luồng danh sách, tạo chiến dịch hợp lệ, quy tắc nhập liệu bắt buộc, sửa theo trạng thái và xuất báo cáo.",
        "Không đóng kiểm thử toàn trình nếu các câu hỏi mở về ứng dụng, ghi nhận sự kiện, vòng đời trạng thái và quyền xuất báo cáo chưa được xác nhận.",
    ]
    parts.extend(bullet(x) for x in recommendations)

    sect = (
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr>'
    )
    parts.append(sect)
    return "".join(parts)


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:before="0" w:after="80"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:b/><w:color w:val="0B2545"/><w:sz w:val="52"/><w:szCs w:val="52"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="240"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:color w:val="555555"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="320" w:after="160"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>
</w:styles>"""


def numbering_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="1">
    <w:multiLevelType w:val="hybridMultilevel"/>
    <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/>
      <w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/><w:spacing w:after="160" w:line="280" w:lineRule="auto"/></w:pPr>
      <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>
  <w:abstractNum w:abstractNumId="2">
    <w:multiLevelType w:val="hybridMultilevel"/>
    <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/>
      <w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/><w:spacing w:after="160" w:line="280" w:lineRule="auto"/></w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="2"><w:abstractNumId w:val="2"/></w:num>
</w:numbering>"""


def document_xml() -> str:
    body = build_document_body()
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14"><w:body>{body}</w:body></w:document>"""


def content_types_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""


def rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


def document_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""


def settings_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/><w:defaultTabStop w:val="720"/><w:compat/>
</w:settings>"""


def core_xml() -> str:
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Kế hoạch kiểm thử chức năng Chiến dịch Pop-up trên CMS</dc:title>
  <dc:creator>Trưởng nhóm QA</dc:creator>
  <cp:lastModifiedBy>Trưởng nhóm QA</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>"""


def app_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
</Properties>"""


def build_docx() -> None:
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    files = {
        "[Content_Types].xml": content_types_xml(),
        "_rels/.rels": rels_xml(),
        "word/document.xml": document_xml(),
        "word/_rels/document.xml.rels": document_rels_xml(),
        "word/styles.xml": styles_xml(),
        "word/numbering.xml": numbering_xml(),
        "word/settings.xml": settings_xml(),
        "docProps/core.xml": core_xml(),
        "docProps/app.xml": app_xml(),
    }
    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    print(OUT_PATH)


if __name__ == "__main__":
    build_docx()
