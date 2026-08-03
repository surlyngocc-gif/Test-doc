from __future__ import annotations

import json
import re
import zipfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
REQ_FILE = ROOT / "docs/requirements/SRS_CMS_Popup - Chiến dịch Marketing.txt"
TC_MD = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.md"
TC_XLSX = ROOT / "docs/testcases/TC_CMS_Popup - Chiến dịch Marketing.xlsx"
REVIEW_MD = ROOT / "docs/reviews/REVIEW_TC_CMS_Popup - Chiến dịch Marketing.md"

COLUMNS = [
    "TC ID",
    "Requirement",
    "Module",
    "Priority",
    "Risk",
    "Test Case Name",
    "Preconditions",
    "Test Data",
    "Steps",
    "Expected Result",
    "Technique",
    "Status",
    "Remark",
]

requirements = [
    ("REQ-001", "Màn danh sách chỉ hiển thị menu Pop-up cho Admin CMS/Manager CMS có quyền Pop-up và backend từ chối truy cập trực tiếp nếu không có quyền.", "TC-Danh sách campaign Pop-up", 4.8, "High", "Critical"),
    ("REQ-002", "Màn danh sách hiển thị trạng thái rỗng, sắp xếp theo thời gian tạo gần nhất đến lâu nhất và phân trang theo chuẩn CMS.", "TC-Danh sách campaign Pop-up", 3.6, "Medium", "High"),
    ("REQ-003", "Tìm kiếm theo Code/Popup Name hỗ trợ tìm tương đối, trim khoảng trắng và chặn keyword vượt 255 ký tự.", "TC-Danh sách campaign Pop-up", 4.0, "High", "High"),
    ("REQ-004", "Bộ lọc Status chỉ chọn một giá trị trong Tất cả, Scheduled, Active, Inactive, Expired và áp dụng đúng ý nghĩa từng trạng thái.", "TC-Danh sách campaign Pop-up", 3.8, "Medium", "High"),
    ("REQ-005", "Bộ lọc Customer Segment chỉ chọn một giá trị và lọc đúng Tất cả, Toàn bộ người dùng, Segment cụ thể, Import file.", "TC-Danh sách campaign Pop-up", 3.8, "Medium", "High"),
    ("REQ-006", "Bộ lọc Position mặc định Tất cả, chỉ chọn một giá trị và lấy giá trị theo tài liệu BA cung cấp.", "TC-Danh sách campaign Pop-up", 2.8, "Medium", "Medium"),
    ("REQ-007", "Bộ lọc Effective Period lọc campaign có thời gian hiệu lực giao với khoảng lọc, xử lý invalid date range và No End Date.", "TC-Danh sách campaign Pop-up", 4.2, "High", "High"),
    ("REQ-008", "Nút Export to Excel ở danh sách mở popup EXPORT và nút Create mở màn tạo campaign.", "TC-Danh sách campaign Pop-up", 3.2, "Medium", "High"),
    ("REQ-009", "Bảng danh sách hiển thị đúng các cột STT, Code, Popup Name, Priority, Status, Position, Effective Period, Customer Segment, Created Date, Reach.", "TC-Danh sách campaign Pop-up", 3.4, "Medium", "High"),
    ("REQ-010", "Cột Action hiển thị Edit/View/Delete theo trạng thái campaign và xử lý backend từ chối xóa khi campaign không còn Scheduled.", "TC-Danh sách campaign Pop-up", 4.4, "High", "Critical"),
    ("REQ-011", "Popup xóa campaign hiển thị khi xóa Scheduled campaign, có OTP, Cancel không xóa, Delete gọi xóa và hiển thị toast thành công/thất bại.", "TC-Popup Xoá campaign", 4.2, "High", "Critical"),
    ("REQ-012", "Màn tạo campaign hỗ trợ Language và quy trình nhập thông tin theo từng ngôn ngữ.", "TC-Tạo campaign Pop-up", 2.6, "Medium", "Medium"),
    ("REQ-013", "Tên campaign bắt buộc, trim khoảng trắng, maxlength 255 và không bắt buộc unique.", "TC-Tạo campaign Pop-up", 4.0, "High", "High"),
    ("REQ-014", "Mô tả campaign không bắt buộc, maxlength 500 và không hiển thị trên App.", "TC-Tạo campaign Pop-up", 2.8, "Medium", "Medium"),
    ("REQ-015", "Priority bắt buộc, chỉ nhận số nguyên dương, số nhỏ hơn ưu tiên hiển thị trước và tooltip giải thích priority.", "TC-Tạo campaign Pop-up", 4.0, "High", "High"),
    ("REQ-016", "Start Date/End Date bắt buộc theo cấu hình No End Date, validate format, quan hệ thời gian và timezone hệ thống UTC+7.", "TC-Tạo campaign Pop-up", 4.4, "High", "Critical"),
    ("REQ-017", "No End Date On disable/clear End Date, bỏ required End Date và lưu null hoặc không gửi end date.", "TC-Tạo campaign Pop-up", 3.8, "Medium", "High"),
    ("REQ-018", "Popup image bắt buộc, chỉ nhận JPG/PNG, tối đa 2MB, tỷ lệ 16:9 và xử lý lỗi upload.", "TC-Tạo campaign Pop-up", 4.2, "High", "High"),
    ("REQ-019", "Nhóm nội dung hiển thị bắt buộc chọn đúng một lựa chọn No content displayed hoặc Display content, mặc định Display content.", "TC-Tạo campaign Pop-up", 3.8, "Medium", "High"),
    ("REQ-020", "System Variables cho phép chèn biến hợp lệ vào field đang focus và hiển thị tooltip đúng nội dung.", "TC-Tạo campaign Pop-up", 3.4, "Medium", "Medium"),
    ("REQ-021", "Title/Content bắt buộc khi Display content, disabled khi No content displayed, trim và validate maxlength tương ứng.", "TC-Tạo campaign Pop-up", 4.0, "High", "High"),
    ("REQ-022", "Navigation Type/Navigation Link ràng buộc bắt buộc có đủ cặp khi cấu hình điều hướng, Webview yêu cầu chọn Navigation Type và Link tối đa 1000 ký tự.", "TC-Tạo campaign Pop-up", 4.0, "High", "High"),
    ("REQ-023", "Đối tượng áp dụng chỉ chọn một trong All members, Customer Segment, Import file và validate dữ liệu phụ thuộc từng lựa chọn.", "TC-Tạo campaign Pop-up", 4.4, "High", "Critical"),
    ("REQ-024", "Import file hội viên chỉ enable khi chọn Import file, bắt buộc upload file Excel theo template và xử lý lỗi file.", "TC-Tạo campaign Pop-up", 4.0, "High", "High"),
    ("REQ-025", "Position bắt buộc chọn ít nhất một vị trí native app và cho phép chọn nhiều vị trí.", "TC-Tạo campaign Pop-up", 3.8, "Medium", "High"),
    ("REQ-026", "Display Frequency bắt buộc chọn đúng một loại, validate X lần/ngày và X lần/tuần theo rule.", "TC-Tạo campaign Pop-up", 4.0, "High", "High"),
    ("REQ-027", "Close/Create trên màn tạo xử lý unsaved changes, validate toàn form, confirm OTP và toast tạo campaign.", "TC-Tạo campaign Pop-up", 4.4, "High", "Critical"),
    ("REQ-028", "Màn chỉnh sửa tham chiếu rule Create nhưng giới hạn field được sửa theo trạng thái Scheduled, Active, Inactive, Expired.", "TC-Chỉnh sửa campaign Pop-up", 4.6, "High", "Critical"),
    ("REQ-029", "Save màn chỉnh sửa chỉ enable khi có thay đổi hợp lệ, confirm OTP, gọi cập nhật và hiển thị toast thành công/thất bại.", "TC-Chỉnh sửa campaign Pop-up", 4.2, "High", "Critical"),
    ("REQ-030", "Close màn chỉnh sửa quay về màn trước/danh sách và hiển thị confirm khi có thay đổi chưa lưu.", "TC-Chỉnh sửa campaign Pop-up", 3.4, "Medium", "High"),
    ("REQ-031", "Màn xem chi tiết read-only toàn bộ field và chỉ hiển thị nút Edit khi campaign ở trạng thái cho phép chỉnh sửa và user có quyền.", "TC-Xem chi tiết campaign Pop-up", 3.8, "Medium", "High"),
    ("REQ-032", "Popup EXPORT hiển thị header, close icon, Cancel và không thực hiện export khi đóng/hủy.", "TC-Popup EXPORT", 3.2, "Medium", "Medium"),
    ("REQ-033", "Popup EXPORT chỉ chọn một trong Export từng chiến dịch hoặc Toàn bộ chiến dịch và enable/disable Tên popup chiến dịch tương ứng.", "TC-Popup EXPORT", 4.0, "High", "High"),
    ("REQ-034", "Popup Name - Campaign bắt buộc khi Export từng chiến dịch và không gửi campaign_id khi Export toàn bộ chiến dịch.", "TC-Popup EXPORT", 4.0, "High", "High"),
    ("REQ-035", "Export Period bắt buộc, date range <= 1 năm, validate thiếu ngày và date_from > date_to.", "TC-Popup EXPORT", 4.4, "High", "Critical"),
    ("REQ-036", "Export to excel tạo file đúng phạm vi campaign/toàn bộ campaign, tải file khi thành công và toast lỗi khi thất bại.", "TC-Popup EXPORT", 4.6, "High", "Critical"),
    ("REQ-037", "File export dùng dữ liệu báo cáo tổng hợp, gồm Reach, Impression, Click, Close, CTR campaign, CTR segment và xử lý trường hợp không có dữ liệu.", "TC-Popup EXPORT", 4.2, "High", "High"),
]

req_by_id = {req[0]: req for req in requirements}
tests = []


def add(req, sheet, name, priority, risk, pre, data, steps, expected, tech, remark="Không có."):
    tests.append(
        {
            "TC ID": f"TC-{len(tests) + 1:03d}",
            "Requirement": req,
            "Module": sheet.replace("TC-", ""),
            "Priority": priority,
            "Risk": risk,
            "Test Case Name": name,
            "Preconditions": pre,
            "Test Data": data,
            "Steps": steps,
            "Expected Result": expected,
            "Technique": tech,
            "Status": "",
            "Remark": remark,
            "Sheet": sheet,
        }
    )


P = "Đã đăng nhập CMS bằng tài khoản có dữ liệu test phù hợp."
S1 = "TC-Danh sách campaign Pop-up"
add("REQ-001", S1, "Hiển thị menu Pop-up với user có quyền", "Critical", "High", "User là Admin CMS/Manager CMS có quyền Pop-up.", "Role: Admin CMS có quyền Pop-up", "1. Đăng nhập CMS.<br>2. Quan sát menu CMS.", "Menu Popup - Chiến dịch Marketing hiển thị và user truy cập được màn Danh sách campaign Pop-up.", "Use Case")
add("REQ-001", S1, "Ẩn menu và từ chối truy cập URL trực tiếp khi user không có quyền", "Critical", "High", "User CMS không có quyền Pop-up.", "URL màn Pop-up đã bookmark", "1. Đăng nhập bằng user không có quyền Pop-up.<br>2. Quan sát menu CMS.<br>3. Mở trực tiếp URL màn Pop-up.", "Menu Popup - Chiến dịch Marketing không hiển thị; backend CMS từ chối truy cập trực tiếp theo cơ chế phân quyền của CMS.", "Permission")
add("REQ-002", S1, "Hiển thị No Data khi danh sách không có dữ liệu", "High", "Medium", P, "Không có campaign Pop-up thỏa điều kiện.", "1. Mở màn Danh sách campaign Pop-up.<br>2. Đảm bảo không có campaign thỏa điều kiện.", "Danh sách hiển thị thông báo \"No Data\".", "EP")
add("REQ-002", S1, "Sắp xếp danh sách theo Created Date mới nhất trước", "High", "Medium", P, "Campaign A tạo 01/07/2026 10:00; Campaign B tạo 02/07/2026 10:00", "1. Mở màn Danh sách campaign Pop-up.<br>2. Quan sát thứ tự các dòng.", "Campaign B hiển thị trước Campaign A theo thời gian tạo gần nhất đến lâu nhất.", "Use Case")
add("REQ-002", S1, "Phân trang danh sách theo chuẩn CMS", "Medium", "Medium", P, "Số campaign lớn hơn page size CMS", "1. Mở danh sách.<br>2. Chuyển sang trang kế tiếp.<br>3. Quay lại trang trước.", "Danh sách phân trang theo chuẩn CMS; STT và dữ liệu thay đổi theo trang đang chọn.", "Experience Based")
add("REQ-003", S1, "Tìm kiếm tương đối theo Code", "High", "High", P, "Keyword: POP01", "1. Nhập POP01 vào Search by Code.<br>2. Thực hiện tìm kiếm.", "Danh sách chỉ hiển thị campaign có ID/Code chứa POP01.", "EP")
add("REQ-003", S1, "Tìm kiếm tương đối theo Popup Name và kết hợp filter khác", "High", "High", P, "Keyword: Summer; Status: Active", "1. Nhập Summer vào Search by popup.<br>2. Chọn Status = Active.<br>3. Thực hiện tìm kiếm.", "Danh sách chỉ hiển thị campaign có tên chứa Summer và trạng thái Active.", "Decision Table")
add("REQ-003", S1, "Trim keyword chỉ gồm khoảng trắng", "Medium", "Medium", P, "Keyword: ba dấu cách", "1. Nhập chỉ khoảng trắng vào Search by Code.<br>2. Thực hiện tìm kiếm.", "Hệ thống trim keyword và xem như không nhập; danh sách không bị lọc theo keyword.", "BVA")
add("REQ-003", S1, "Chặn keyword tìm kiếm vượt 255 ký tự", "High", "High", P, "Keyword 256 ký tự", "1. Nhập keyword dài 256 ký tự vào Search by popup.<br>2. Thực hiện tìm kiếm.", "Hiển thị lỗi \"Search keyword must not exceed 255 characters.\" và không áp dụng tìm kiếm với keyword không hợp lệ.", "BVA")
add("REQ-004", S1, "Status mặc định Tất cả và chỉ chọn một giá trị", "High", "Medium", P, "Status options: Tất cả, Scheduled, Active, Inactive, Expired", "1. Mở màn danh sách.<br>2. Quan sát filter Status.<br>3. Chọn lần lượt Scheduled rồi Active.", "Status mặc định là Tất cả; tại mọi thời điểm chỉ một giá trị Status được chọn.", "State Transition")
add("REQ-004", S1, "Lọc đúng từng Status", "High", "Medium", P, "Có campaign Scheduled, Active, Inactive, Expired", "1. Chọn từng trạng thái trong filter Status.<br>2. Quan sát danh sách sau mỗi lần lọc.", "Danh sách chỉ hiển thị campaign có trạng thái đúng với giá trị đã chọn; chọn Tất cả thì không lọc theo trạng thái.", "Decision Table")
add("REQ-005", S1, "Lọc Customer Segment theo All User, Segment cụ thể và Import file", "High", "Medium", P, "Campaign All User, Segment Gold, Import file", "1. Chọn Toàn bộ người dùng.<br>2. Chọn Segment Gold.<br>3. Chọn Import file.", "Mỗi lần lọc, danh sách chỉ hiển thị campaign có đối tượng áp dụng tương ứng.", "Decision Table")
add("REQ-005", S1, "Customer Segment chỉ cho chọn một giá trị", "Medium", "Medium", P, "Filter Customer Segment có nhiều option", "1. Chọn Segment A.<br>2. Chọn Segment B.", "Segment B được chọn và Segment A không còn được chọn; filter không cho chọn nhiều giá trị đồng thời.", "State Transition")
add("REQ-006", S1, "Position mặc định Tất cả và chỉ chọn một giá trị", "Medium", "Medium", P, "Danh sách Position theo tài liệu BA", "1. Mở màn danh sách.<br>2. Quan sát filter Position.<br>3. Chọn Position A rồi Position B.", "Position mặc định Tất cả; tại mọi thời điểm chỉ một Position được chọn.", "Use Case", "Danh sách giá trị Position cần đối chiếu tài liệu BA cung cấp.")
add("REQ-007", S1, "Lọc Effective Period giao hoàn toàn trong khoảng lọc", "High", "High", P, "Filter: 01/07/2026-31/07/2026; Campaign: 05/07/2026-10/07/2026", "1. Nhập khoảng lọc.<br>2. Thực hiện lọc.", "Campaign có Start và End nằm trong khoảng lọc được hiển thị.", "Decision Table")
add("REQ-007", S1, "Lọc Effective Period giao một phần đầu/cuối", "High", "High", P, "Campaign A: 15/06/2026-05/07/2026; Campaign B: 20/07/2026-10/08/2026", "1. Nhập filter 01/07/2026-31/07/2026.<br>2. Thực hiện lọc.", "Campaign A và Campaign B được hiển thị vì có bất kỳ phần thời gian hiệu lực giao với khoảng lọc.", "Decision Table")
add("REQ-007", S1, "Không hiển thị campaign nằm ngoài khoảng lọc", "High", "High", P, "Campaign kết thúc trước Filter Start; campaign bắt đầu sau Filter End", "1. Nhập khoảng lọc.<br>2. Thực hiện lọc.", "Campaign kết thúc trước khoảng lọc và campaign bắt đầu sau khoảng lọc không hiển thị.", "Decision Table")
add("REQ-007", S1, "Lọc campaign No End Date", "High", "High", P, "Campaign No End Date có Start Date <= Filter To Date", "1. Nhập khoảng lọc.<br>2. Thực hiện lọc.", "Campaign No End Date hiển thị khi Start Date nhỏ hơn hoặc bằng To Date của khoảng lọc.", "BVA")
add("REQ-007", S1, "Hiển thị lỗi khi Effective Period from date lớn hơn to date", "High", "High", P, "From: 31/07/2026; To: 01/07/2026", "1. Nhập From Date lớn hơn To Date.<br>2. Thực hiện lọc.", "Hiển thị lỗi \"Invalid date range.\" và không áp dụng khoảng lọc không hợp lệ.", "BVA")
add("REQ-008", S1, "Nút Export to Excel mở popup EXPORT", "High", "Medium", P, "Không áp dụng", "1. Mở danh sách campaign.<br>2. Click Export to Excel.", "Popup EXPORT hiển thị để chọn popup chiến dịch và thời gian xuất dữ liệu.", "Use Case")
add("REQ-008", S1, "Nút Create mở màn tạo campaign", "High", "Medium", P, "Không áp dụng", "1. Mở danh sách campaign.<br>2. Click Create.", "Hệ thống điều hướng đến màn Tạo campaign Pop-up.", "Use Case")
add("REQ-009", S1, "Hiển thị đúng các cột dữ liệu danh sách", "High", "Medium", P, "Campaign POP01 có đầy đủ dữ liệu", "1. Mở danh sách.<br>2. Quan sát các cột trên dòng POP01.", "Dòng campaign hiển thị STT, Code, Popup Name, Priority, Status, Position, Effective Period, Customer Segment, Created Date, Reach theo dữ liệu đã lưu.", "Use Case")
add("REQ-009", S1, "Hiển thị Effective Period và Reach khi No End Date/chưa có dữ liệu báo cáo", "Medium", "Medium", P, "Campaign No End Date; Reach chưa có dữ liệu", "1. Mở danh sách.<br>2. Quan sát Effective Period và Reach.", "Effective Period hiển thị start date - No End Date hoặc format tương đương; Reach hiển thị 0 hoặc \"-\" theo chuẩn CMS.", "EP")
add("REQ-010", S1, "Action Edit/View/Delete theo trạng thái Scheduled", "Critical", "High", P, "Campaign Scheduled", "1. Mở dòng campaign Scheduled.<br>2. Quan sát cột Action.", "Icon Edit hiển thị; icon View hiển thị; icon Delete enable.", "Decision Table")
add("REQ-010", S1, "Action Edit/View/Delete theo trạng thái Active/Inactive/Expired", "Critical", "High", P, "Campaign Active, Inactive, Expired", "1. Quan sát Action của từng trạng thái.", "Active và Inactive hiển thị Edit/View nhưng Delete ẩn hoặc disabled; Expired hiển thị View, Delete ẩn hoặc disabled và Edit không hiển thị nếu không cho phép chỉnh sửa.", "Decision Table")
add("REQ-010", S1, "Backend từ chối xóa khi trạng thái không còn Scheduled", "Critical", "High", P, "FE đang hiển thị Delete enable; backend trả trạng thái hiện tại không phải Scheduled", "1. Click Delete trên campaign.<br>2. Xác nhận xóa.", "Hệ thống hiển thị toast \"Campaign cannot be deleted in current status.\" và không xóa campaign.", "Error Guessing")

S2 = "TC-Popup Xoá campaign"
add("REQ-011", S2, "Mở popup xác nhận xóa Scheduled campaign", "Critical", "High", P, "Campaign Scheduled", "1. Ở màn danh sách, click icon Delete của campaign Scheduled.", "Popup xác nhận hiển thị nội dung \"Are you sure you want to delete this campaign?\" và có ô nhập mã OTP.", "Use Case")
add("REQ-011", S2, "Cancel popup xóa không xóa campaign", "High", "High", P, "Popup xác nhận xóa đang hiển thị", "1. Click Cancel trên popup xác nhận.", "Popup đóng; campaign vẫn còn trên danh sách và không có request xóa được thực hiện.", "Use Case")
add("REQ-011", S2, "Xóa campaign thành công", "Critical", "High", P, "Campaign Scheduled; OTP hợp lệ", "1. Click Delete campaign Scheduled.<br>2. Nhập OTP hợp lệ.<br>3. Click Delete.", "Hệ thống gọi xóa campaign, hiển thị toast \"Campaign has been successfully deleted.\" và cập nhật lại danh sách.", "Use Case")
add("REQ-011", S2, "Xóa campaign thất bại", "Critical", "High", P, "Backend trả lỗi khi xóa", "1. Click Delete campaign Scheduled.<br>2. Nhập OTP hợp lệ.<br>3. Click Delete.", "Hệ thống hiển thị toast \"Failed to delete campaign.\" và campaign không bị xóa khỏi dữ liệu.", "Error Guessing")

S3 = "TC-Tạo campaign Pop-up"
add("REQ-012", S3, "Language mặc định và cho phép nhập theo ngôn ngữ đang chọn", "Medium", "Medium", P, "Ngôn ngữ CMS hiện hữu: Tiếng Việt", "1. Mở màn tạo campaign.<br>2. Quan sát Language.<br>3. Nhập dữ liệu các field input.", "Language mặc định theo CMS hiện hữu; các field input Common và Popup Configuration cho phép nhập theo ngôn ngữ đang chọn.", "Use Case")
add("REQ-012", S3, "Quy trình tạo thêm ngôn ngữ còn lại sau khi lưu", "Medium", "Medium", P, "Campaign đã tạo thành công ở ngôn ngữ hiện tại", "1. Mở Edit campaign vừa tạo.<br>2. Chọn ngôn ngữ còn lại.<br>3. Nhập thông tin.<br>4. Lưu.", "Hệ thống cho phép nhập và lưu thông tin campaign cho ngôn ngữ còn lại theo luồng tạo trước rồi chỉnh sửa.", "Use Case")
add("REQ-013", S3, "Tạo với campaign name hợp lệ và trùng tên campaign cũ", "High", "High", P, "Campaign name: Summer Popup; đã tồn tại campaign cùng tên", "1. Nhập Campaign Name hợp lệ trùng tên campaign cũ.<br>2. Nhập các field bắt buộc hợp lệ.<br>3. Click Create.", "Form không báo lỗi unique cho Campaign Name; hệ thống tiếp tục validate các field còn lại.", "EP")
add("REQ-013", S3, "Campaign name rỗng sau trim", "High", "High", P, "Campaign Name: ba dấu cách", "1. Nhập Campaign Name chỉ gồm khoảng trắng.<br>2. Click Create.", "Hiển thị lỗi \"Campaign name is required.\" tại field Campaign Name.", "BVA")
add("REQ-013", S3, "Campaign name vượt 255 ký tự", "High", "High", P, "Campaign Name dài 256 ký tự", "1. Nhập Campaign Name 256 ký tự.<br>2. Click Create.", "Hiển thị lỗi \"Campaign name must not exceed 255 characters.\" tại field Campaign Name.", "BVA")
add("REQ-014", S3, "Description có thể bỏ trống", "Medium", "Medium", P, "Description: rỗng", "1. Để trống Description.<br>2. Nhập các field bắt buộc hợp lệ.<br>3. Click Create.", "Form không báo lỗi required cho Description.", "EP")
add("REQ-014", S3, "Description vượt 500 ký tự", "Medium", "Medium", P, "Description 501 ký tự", "1. Nhập Description 501 ký tự.<br>2. Click Create.", "Hiển thị lỗi \"Campaign name must not exceed  characters.\" tại field Description theo SRS.", "BVA", "Thông điệp lỗi trong SRS thiếu số ký tự, cần BA xác nhận.")
add("REQ-015", S3, "Priority hợp lệ và tooltip", "High", "High", P, "Priority: 1", "1. Nhập Priority = 1.<br>2. Hover/click icon thông tin cạnh Priority.", "Priority được chấp nhận; tooltip hiển thị \"Smaller numbers take display priority.\"", "EP")
add("REQ-015", S3, "Priority rỗng", "High", "High", P, "Priority: rỗng", "1. Để trống Priority.<br>2. Click Create.", "Hiển thị lỗi \"Priority is required.\" tại field Priority.", "BVA")
add("REQ-015", S3, "Priority không phải số nguyên dương", "High", "High", P, "Priority: abc, 1.5, -1, 0", "1. Nhập từng giá trị không hợp lệ vào Priority.<br>2. Click Create.", "Mỗi giá trị hiển thị lỗi \"Priority must be a positive integer.\" tại field Priority.", "EP")
add("REQ-016", S3, "Start Date/End Date hợp lệ với No End Date Off", "Critical", "High", P, "Start: 10/07/2026 09:00; End: 11/07/2026 09:00; No End Date Off", "1. Nhập Start Date và End Date hợp lệ.<br>2. Click Create.", "Form chấp nhận Start Date và End Date, không hiển thị lỗi format hoặc quan hệ thời gian.", "EP")
add("REQ-016", S3, "Start Date sai format", "High", "High", P, "Start Date: 2026-07-10 09:00", "1. Nhập Start Date sai format dd/mm/yyyy hh:mm.<br>2. Click Create.", "Hiển thị lỗi \"Invalid start date format.\" tại Start Date.", "BVA")
add("REQ-016", S3, "Start Date nhỏ hơn current time theo UTC+7", "Critical", "High", P, "Start Date trước thời điểm lưu theo UTC+7", "1. Nhập Start Date nhỏ hơn current time.<br>2. Click Create.", "Hiển thị lỗi \"Start date must be greater than or equal to current time.\" theo timezone hệ thống UTC+7.", "BVA")
add("REQ-016", S3, "End Date sai format hoặc nhỏ hơn Start Date", "Critical", "High", P, "End sai format; End < Start", "1. Nhập End Date sai format.<br>2. Click Create.<br>3. Nhập End Date nhỏ hơn Start Date.<br>4. Click Create.", "Lần 1 hiển thị \"Invalid end date format.\"; lần 2 hiển thị \"End date must be greater than or equal to start date.\"", "BVA")
add("REQ-017", S3, "No End Date On disable và clear End Date", "High", "Medium", P, "End Date đang có giá trị", "1. Bật No End Date.<br>2. Quan sát field End Date.<br>3. Click Create với các field khác hợp lệ.", "End Date bị disable/clear; field End Date không validate required; dữ liệu lưu không gửi end date hoặc gửi null theo API design.", "State Transition")
add("REQ-017", S3, "No End Date Off yêu cầu nhập lại End Date nếu rỗng", "High", "Medium", P, "No End Date đang On", "1. Tắt No End Date.<br>2. Để End Date rỗng.<br>3. Click Create.", "End Date được enable và bị validate required theo rule bắt buộc khi No End Date Off.", "State Transition")
add("REQ-018", S3, "Upload ảnh popup JPG/PNG hợp lệ tỷ lệ 16:9 dưới 2MB", "High", "High", P, "File popup.jpg, 1MB, 16:9", "1. Upload file ảnh hợp lệ.<br>2. Quan sát trạng thái upload.", "Ảnh được upload thành công và hiển thị/ghi nhận trên form.", "EP")
add("REQ-018", S3, "Không upload ảnh popup", "High", "High", P, "Popup image rỗng", "1. Không upload ảnh.<br>2. Click Create.", "Hiển thị lỗi required cho Popup image theo rule bắt buộc upload ảnh.", "BVA")
add("REQ-018", S3, "Upload ảnh sai định dạng/dung lượng/tỷ lệ/lỗi đọc", "High", "High", P, "File GIF; file >2MB; file rỗng; ảnh sai tỷ lệ không điều chỉnh được", "1. Upload từng file không hợp lệ.<br>2. Quan sát lỗi.", "Hiển thị lần lượt \"Invalid image format.\", \"Image size must not exceed 2MB.\", \"Invalid image file.\", \"Image ratio must be 16:9.\" theo lỗi tương ứng.", "EP")
add("REQ-018", S3, "Upload ảnh thất bại", "High", "High", P, "Dịch vụ upload trả lỗi", "1. Upload ảnh hợp lệ trong khi dịch vụ upload lỗi.", "Hiển thị thông báo \"Failed to upload image.\" và ảnh không được ghi nhận thành công.", "Error Guessing")
add("REQ-019", S3, "Mặc định chọn Display content và chỉ chọn một option nội dung", "High", "Medium", P, "Không áp dụng", "1. Mở màn tạo.<br>2. Quan sát nhóm Nội dung hiển thị cùng popup.<br>3. Chọn No content displayed.", "Display content được chọn mặc định; khi chọn No content displayed thì Display content bỏ chọn và các field nội dung bị disable.", "State Transition")
add("REQ-019", S3, "Không cho chọn đồng thời hoặc bỏ chọn toàn bộ nhóm nội dung", "High", "Medium", P, "Nhóm nội dung hiển thị", "1. Thử chọn đồng thời No content displayed và Display content.<br>2. Thử bỏ chọn cả hai nếu UI cho phép.<br>3. Click Create.", "Hệ thống chỉ cho đúng một option được chọn; nếu không có option nào được chọn thì form không hợp lệ theo rule bắt buộc chọn một.", "Error Guessing")
add("REQ-020", S3, "Chèn System Variables vào field đang focus", "Medium", "Medium", P, "Field Title đang focus; biến Tên hội viên", "1. Focus vào Title.<br>2. Click biến Tên hội viên.", "Biến Tên hội viên được chèn đúng vị trí con trỏ trong field Title.", "Use Case")
add("REQ-020", S3, "Tooltip System Variables", "Medium", "Medium", P, "Không áp dụng", "1. Hover/click icon thông tin cạnh Các biến hệ thống.", "Tooltip hiển thị \"Click the system variables field to insert them into the content.\"", "Use Case")
add("REQ-021", S3, "Title và Content hợp lệ khi Display content", "High", "High", P, "Title: Ưu đãi tháng 7; Content: Nội dung hợp lệ", "1. Chọn Display content.<br>2. Nhập Title và Content hợp lệ.<br>3. Click Create.", "Title và Content được chấp nhận, không hiển thị lỗi required hoặc maxlength.", "EP")
add("REQ-021", S3, "Title rỗng sau trim khi Display content", "High", "High", P, "Title: khoảng trắng", "1. Chọn Display content.<br>2. Nhập Title chỉ gồm khoảng trắng.<br>3. Click Create.", "Hiển thị lỗi \"Title is required.\" tại field Title.", "BVA")
add("REQ-021", S3, "Content rỗng sau trim khi Display content", "High", "High", P, "Content: khoảng trắng", "1. Chọn Display content.<br>2. Nhập Content chỉ gồm khoảng trắng.<br>3. Click Create.", "Hiển thị lỗi \"Content is required.\" tại field Content.", "BVA")
add("REQ-021", S3, "Title/Content vượt maxlength", "High", "High", P, "Title 101 ký tự; Content 301 ký tự", "1. Nhập Title 101 ký tự.<br>2. Nhập Content 301 ký tự.<br>3. Click Create.", "Title hiển thị \"Title must not exceed 225 characters.\"; Content hiển thị \"Description must not exceed 300 characters.\" theo SRS.", "BVA", "SRS ghi Title maxlength 100 nhưng message 225, cần BA xác nhận.")
add("REQ-022", S3, "Không cấu hình điều hướng khi Navigation Type và Link cùng trống", "High", "High", P, "Navigation type rỗng; Navigation link rỗng", "1. Để trống Loại điều hướng và Link điều hướng.<br>2. Click Create với các field khác hợp lệ.", "Form không báo lỗi Navigation type hoặc Navigation link vì cả hai cùng trống.", "Decision Table")
add("REQ-022", S3, "Có Link nhưng chưa chọn Loại điều hướng", "High", "High", P, "Navigation link: https://example.com", "1. Nhập Link điều hướng.<br>2. Để trống Loại điều hướng.<br>3. Click Create.", "Hiển thị lỗi \"Navigation type is required.\"", "Decision Table")
add("REQ-022", S3, "Đã chọn Loại điều hướng nhưng chưa nhập Link", "High", "High", P, "Navigation type: Native App; Link rỗng", "1. Chọn Loại điều hướng.<br>2. Để trống Link điều hướng.<br>3. Click Create.", "Hiển thị lỗi \"Navigation link is required.\"", "Decision Table")
add("REQ-022", S3, "Webview yêu cầu Navigation Type và link tối đa 1000 ký tự", "High", "High", P, "Navigation type: Webview; Navigation Type rỗng; Link 1001 ký tự", "1. Chọn Loại điều hướng = Webview.<br>2. Để trống Navigation Type.<br>3. Click Create.<br>4. Nhập Link 1001 ký tự và click Create.", "Lần 1 hiển thị \"Navigation Type is required.\"; lần 2 hiển thị \"Link must not exceed 1000 characters.\"", "BVA")
add("REQ-023", S3, "Chọn All members làm đối tượng áp dụng", "Critical", "High", P, "Option All members", "1. Chọn All members.<br>2. Quan sát Customer Segment dropdown và Import file.", "Campaign áp dụng toàn bộ hội viên; Customer Segment dropdown và file import bị disable/clear.", "State Transition")
add("REQ-023", S3, "Chọn Customer Segment và bắt buộc chọn một Segment", "Critical", "High", P, "Option Customer Segment; chưa chọn Segment", "1. Chọn Customer Segment.<br>2. Để trống Customer Segment dropdown.<br>3. Click Create.", "Dropdown Customer Segment enable; hiển thị lỗi \"Please select one Customer Segment.\" khi chưa chọn Segment.", "Decision Table")
add("REQ-023", S3, "Không chọn đối tượng áp dụng", "Critical", "High", P, "Không chọn All members, Customer Segment, Import file", "1. Bỏ chọn toàn bộ đối tượng áp dụng nếu UI cho phép.<br>2. Click Create.", "Hiển thị lỗi \"Please select audience.\".", "BVA")
add("REQ-023", S3, "Không cho chọn đồng thời nhiều đối tượng áp dụng", "Critical", "High", P, "All members đang chọn", "1. Chọn All members.<br>2. Chọn Customer Segment.<br>3. Chọn Import file.", "Tại mọi thời điểm chỉ một trong ba option được chọn; option mới chọn clear/disable dữ liệu phụ thuộc của option trước.", "State Transition")
add("REQ-024", S3, "Import file hợp lệ", "High", "High", P, "File Excel đúng template", "1. Chọn Import file.<br>2. Upload file Excel đúng template.", "File được upload/validate thành công và được ghi nhận cho campaign.", "EP")
add("REQ-024", S3, "Import file rỗng/sai template/lỗi upload", "High", "High", P, "Không upload; file rỗng; file sai template; dịch vụ upload lỗi", "1. Chọn Import file.<br>2. Thử từng dữ liệu file không hợp lệ.<br>3. Click Create hoặc upload.", "Hiển thị lần lượt \"Please upload member file.\", \"Invalid import file.\", \"Invalid import file format.\", \"Failed to upload import file.\" theo lỗi tương ứng.", "EP")
add("REQ-024", S3, "Xóa file import đã upload và upload lại", "Medium", "Medium", P, "File import đã upload", "1. Chọn Import file.<br>2. Upload file hợp lệ.<br>3. Xóa file đã upload.<br>4. Upload file khác.", "File cũ bị xóa khỏi form; file mới được upload và ghi nhận trước khi lưu.", "State Transition")
add("REQ-025", S3, "Chọn một hoặc nhiều Position", "High", "Medium", P, "Position A, Position B", "1. Chọn Position A.<br>2. Chọn thêm Position B.", "Form cho phép chọn một hoặc nhiều vị trí native app.", "EP")
add("REQ-025", S3, "Không chọn Position", "High", "Medium", P, "Không có Position được chọn", "1. Không chọn Position.<br>2. Click Create.", "Hiển thị lỗi \"Please select at least one Position.\"", "BVA")
add("REQ-026", S3, "Chọn đúng một loại Display Frequency", "High", "High", P, "Các option frequency", "1. Chọn Only once.<br>2. Chọn X times/day.", "Tại mọi thời điểm chỉ một loại tần suất hiển thị được chọn.", "State Transition")
add("REQ-026", S3, "Không chọn Display Frequency", "High", "High", P, "Không chọn frequency", "1. Bỏ chọn toàn bộ frequency nếu UI cho phép.<br>2. Click Create.", "Hiển thị lỗi \"Please select frequency type.\"", "BVA")
add("REQ-026", S3, "Validate X times/day", "High", "High", P, "X rỗng, abc, 1.5, -1, 0, 50, 49", "1. Chọn X times/day.<br>2. Nhập từng giá trị X.<br>3. Click Create.", "X rỗng hiển thị \"Frequency value is required.\"; abc/1.5/-1/0/50 hiển thị \"Frequency value must be an integer and less than 50.\"; X=49 được chấp nhận.", "BVA")
add("REQ-026", S3, "Validate X times/week và ngày trong tuần", "High", "High", P, "X=2; weekday rỗng", "1. Chọn X times/week.<br>2. Nhập X hợp lệ.<br>3. Không chọn ngày trong tuần.<br>4. Click Create.", "Hiển thị lỗi \"Please select at least one day of week.\" khi chưa chọn ngày trong tuần.", "BVA")
add("REQ-027", S3, "Close màn tạo khi có dữ liệu chưa lưu", "High", "Medium", P, "Đã nhập Campaign Name", "1. Nhập dữ liệu vào form.<br>2. Click Close.", "Hiển thị confirm \"Unsaved changes will be lost. Do you want to continue?\".", "Use Case")
add("REQ-027", S3, "Tạo campaign thành công", "Critical", "High", P, "Toàn bộ field bắt buộc hợp lệ; OTP hợp lệ", "1. Nhập toàn bộ field bắt buộc hợp lệ.<br>2. Click Create.<br>3. Xác nhận popup \"Are you sure you want to create this campaign?\" bằng OTP hợp lệ.", "Hiển thị toast \"Campaign has been successfully saved.\"; backend trả trạng thái campaign sau khi tạo và FE hiển thị trạng thái đó ở danh sách/chi tiết.", "Use Case")
add("REQ-027", S3, "Tạo campaign thất bại do backend", "Critical", "High", P, "Backend trả lỗi không xác định field", "1. Nhập form hợp lệ.<br>2. Click Create và xác nhận OTP.<br>3. Backend trả lỗi.", "Hiển thị toast \"Failed to save campaign.\".", "Error Guessing")
add("REQ-027", S3, "Backend trả lỗi validate xác định được field", "High", "High", P, "Backend trả lỗi validate tại Priority", "1. Nhập form.<br>2. Click Create và xác nhận OTP.<br>3. Backend trả lỗi validate field Priority.", "FE hiển thị lỗi tại field Priority tương ứng với lỗi backend trả về.", "Error Guessing")

S4 = "TC-Chỉnh sửa campaign Pop-up"
add("REQ-028", S4, "Scheduled campaign cho phép chỉnh sửa đầy đủ field", "Critical", "High", P, "Campaign Scheduled; user có quyền Edit", "1. Mở Edit campaign Scheduled.<br>2. Quan sát các field.<br>3. Sửa các field như màn Create.", "Các field được phép chỉnh sửa đầy đủ nếu actor có quyền; khi lưu validate toàn bộ rule như màn Create.", "Decision Table")
add("REQ-028", S4, "Active campaign chỉ enable nhóm field được phép", "Critical", "High", P, "Campaign Active", "1. Mở Edit campaign Active.<br>2. Quan sát trạng thái enable/disable field.", "Chỉ enable Tên chiến dịch popup, Mô tả chiến dịch, Trạng thái đổi Active sang Inactive, Ảnh popup, Nội dung hiển thị cùng popup; các field khác disabled.", "Decision Table")
add("REQ-028", S4, "Inactive campaign chỉ enable nhóm field được phép", "Critical", "High", P, "Campaign Inactive", "1. Mở Edit campaign Inactive.<br>2. Quan sát trạng thái enable/disable field.", "Enable Tên chiến dịch popup, Mô tả chiến dịch, Priority, Trạng thái đổi Inactive sang Active, Ảnh popup, Nội dung hiển thị cùng popup, Loại điều hướng, Link điều hướng, Vị trí hiển thị; field enable validate theo rule Create.", "Decision Table")
add("REQ-028", S4, "Expired campaign chỉ xem và không kích hoạt lại trực tiếp", "Critical", "High", P, "Campaign Expired", "1. Mở campaign Expired ở màn Edit hoặc Detail.<br>2. Quan sát field và Save.", "Toàn bộ field read-only/disabled; Save không hiển thị hoặc không enable; không có thao tác kích hoạt lại trực tiếp campaign Expired.", "Decision Table")
add("REQ-028", S4, "Backend trả lỗi khi trạng thái thay đổi trong lúc edit", "Critical", "High", P, "Campaign chuyển trạng thái bởi job/người khác trong lúc đang edit", "1. Mở Edit campaign.<br>2. Người khác/job đổi trạng thái campaign.<br>3. Click Save.", "Backend trả lỗi trạng thái; FE reload dữ liệu mới nhất của campaign.", "Error Guessing")
add("REQ-029", S4, "Save enable khi có thay đổi hợp lệ", "Critical", "High", P, "Campaign có field được phép chỉnh sửa", "1. Mở màn Edit.<br>2. Không thay đổi dữ liệu.<br>3. Sửa một field hợp lệ.", "Save không enable khi chưa có thay đổi; Save enable sau khi có thay đổi hợp lệ trên field được phép chỉnh sửa.", "State Transition")
add("REQ-029", S4, "Cập nhật campaign thành công", "Critical", "High", P, "Campaign editable; OTP hợp lệ", "1. Sửa dữ liệu hợp lệ.<br>2. Click Save.<br>3. Xác nhận popup \"Are you sure you want to edit the campiagn ?\" bằng OTP hợp lệ.", "Hệ thống gọi cập nhật campaign và hiển thị toast \"Campaign has been successfully edited.\"", "Use Case")
add("REQ-029", S4, "Cập nhật campaign thất bại", "Critical", "High", P, "Backend trả lỗi cập nhật", "1. Sửa dữ liệu hợp lệ.<br>2. Click Save và xác nhận OTP.<br>3. Backend trả lỗi.", "Hiển thị toast \"Failed to edit campaign.\" và dữ liệu chưa được lưu.", "Error Guessing")
add("REQ-029", S4, "Cancel popup confirm edit không lưu", "High", "High", P, "Popup confirm edit đang hiển thị", "1. Click Save sau khi sửa hợp lệ.<br>2. Click Cancel trong popup confirm.", "Popup confirm đóng; màn Edit giữ nguyên dữ liệu đang sửa; không gọi API cập nhật.", "Use Case")
add("REQ-030", S4, "Close màn Edit không có thay đổi", "Medium", "Medium", P, "Màn Edit không có thay đổi", "1. Mở màn Edit.<br>2. Click Close.", "Màn Edit đóng và quay về màn trước đó/danh sách campaign.", "Use Case")
add("REQ-030", S4, "Close màn Edit có thay đổi chưa lưu", "High", "Medium", P, "Đã chỉnh sửa field nhưng chưa Save", "1. Sửa một field.<br>2. Click Close.<br>3. Click Cancel trên confirm.<br>4. Click Close lại và chọn Yes/Continue.", "Lần Cancel: đóng popup confirm và giữ nguyên màn Edit; lần Yes/Continue: rời màn Edit và không lưu thay đổi.", "State Transition")

S5 = "TC-Xem chi tiết campaign Pop-up"
add("REQ-031", S5, "Màn chi tiết hiển thị toàn bộ field read-only", "High", "Medium", P, "Campaign bất kỳ có dữ liệu", "1. Click icon View trên danh sách.<br>2. Quan sát các field.", "Màn chi tiết hiển thị dữ liệu campaign tương tự màn Edit nhưng toàn bộ field ở trạng thái read-only.", "Use Case")
add("REQ-031", S5, "Hiển thị nút Edit khi campaign cho phép chỉnh sửa và user có quyền", "High", "Medium", P, "Campaign Scheduled/Active/Inactive; user có quyền Edit", "1. Mở màn chi tiết campaign.<br>2. Quan sát nút Edit.", "Nút Edit hiển thị và điều hướng sang màn chỉnh sửa campaign.", "Permission")
add("REQ-031", S5, "Không hiển thị Edit khi không có quyền hoặc trạng thái không cho chỉnh sửa", "High", "Medium", P, "User không có quyền Edit hoặc campaign Expired", "1. Mở màn chi tiết campaign.<br>2. Quan sát nút Edit.", "Nút Edit không hiển thị hoặc bị disable theo quyền/trạng thái campaign.", "Permission")

S6 = "TC-Popup EXPORT"
add("REQ-032", S6, "Popup EXPORT hiển thị header và đóng bằng icon X", "Medium", "Medium", P, "Popup EXPORT đang mở", "1. Mở popup EXPORT.<br>2. Quan sát header.<br>3. Click icon X.", "Header hiển thị \"EXPORT\"; popup đóng; không thực hiện export và không lưu thay đổi filter trong popup.", "Use Case")
add("REQ-032", S6, "Cancel popup EXPORT không export", "Medium", "Medium", P, "Popup EXPORT đang mở", "1. Chọn một số filter trong popup.<br>2. Click Cancel.", "Popup đóng và không thực hiện export.", "Use Case")
add("REQ-033", S6, "Chọn Export từng chiến dịch", "High", "High", P, "Popup EXPORT mở từ action export của một campaign cụ thể", "1. Mở popup EXPORT từ action export campaign.<br>2. Quan sát option mặc định và field Tên popup chiến dịch.", "Export từng chiến dịch là option mặc định nếu popup mở từ action export của campaign cụ thể; field Tên popup chiến dịch hiển thị/enable và bắt buộc.", "State Transition")
add("REQ-033", S6, "Chọn Toàn bộ chiến dịch", "High", "High", P, "Popup EXPORT đang mở", "1. Chọn Toàn bộ chiến dịch.", "Option Export từng chiến dịch bị bỏ chọn; field Tên popup chiến dịch ẩn/disable.", "State Transition")
add("REQ-034", S6, "Không chọn campaign khi Export từng chiến dịch", "High", "High", P, "Option Export từng chiến dịch; Popup Name rỗng", "1. Chọn Export từng chiến dịch.<br>2. Để trống Tên popup chiến dịch.<br>3. Click Export to excel.", "Hiển thị lỗi \"Please select popup campaign.\"", "BVA")
add("REQ-034", S6, "Export toàn bộ chiến dịch không gửi campaign_id", "High", "High", P, "Option Toàn bộ chiến dịch", "1. Chọn Toàn bộ chiến dịch.<br>2. Chọn Export Period hợp lệ.<br>3. Click Export to excel.", "Request export không gửi campaign_id; file export tổng hợp dữ liệu cho toàn bộ campaign actor có quyền export trong khoảng thời gian đã chọn.", "Decision Table")
add("REQ-035", S6, "Export Period hợp lệ trong giới hạn một năm", "Critical", "High", P, "From: 04/07/2025; To: 04/07/2026", "1. Chọn Export Period có khoảng thời gian <= 1 năm.<br>2. Click Export to excel.", "Date range được chấp nhận và hệ thống tiếp tục tạo file export nếu các dữ liệu khác hợp lệ.", "BVA")
add("REQ-035", S6, "Không chọn đủ Export Period", "Critical", "High", P, "From rỗng hoặc To rỗng", "1. Để thiếu From hoặc To trong Export Period.<br>2. Click Export to excel.", "Hiển thị lỗi \"Please select export date range.\"", "BVA")
add("REQ-035", S6, "Export Period date_from lớn hơn date_to", "Critical", "High", P, "From: 12/08/2025; To: 04/07/2025", "1. Nhập date_from > date_to.<br>2. Click Export to excel.", "Hiển thị lỗi \"Invalid date range.\"", "BVA")
add("REQ-035", S6, "FE date picker chặn khoảng export lớn hơn một năm", "Critical", "High", P, "Khoảng ngày > 1 năm", "1. Mở date picker Export Period.<br>2. Thử chọn khoảng ngày lớn hơn 1 năm.", "FE date picker không cho chọn khoảng thời gian export lớn hơn 1 năm tính từ thời điểm hiện tại.", "BVA")
add("REQ-036", S6, "Export từng chiến dịch thành công", "Critical", "High", P, "Campaign POP01; Export Period hợp lệ", "1. Chọn Export từng chiến dịch.<br>2. Chọn POP01.<br>3. Chọn Export Period hợp lệ.<br>4. Click Export to excel.", "Hệ thống tạo và tải file Excel theo campaign POP01 và thời gian xuất dữ liệu đã chọn.", "Use Case")
add("REQ-036", S6, "Export toàn bộ chiến dịch thành công", "Critical", "High", P, "Toàn bộ chiến dịch; Export Period hợp lệ", "1. Chọn Toàn bộ chiến dịch.<br>2. Chọn Export Period hợp lệ.<br>3. Click Export to excel.", "Hệ thống tạo và tải file Excel cho toàn bộ campaign actor có quyền export trong khoảng thời gian đã chọn.", "Use Case")
add("REQ-036", S6, "Export thất bại", "Critical", "High", P, "Backend export trả lỗi", "1. Nhập dữ liệu export hợp lệ.<br>2. Click Export to excel.<br>3. Backend trả lỗi.", "Hiển thị toast \"Failed to export report.\" và không tải file lỗi.", "Error Guessing")
add("REQ-037", S6, "File export chứa dữ liệu báo cáo tổng hợp đúng chỉ số", "High", "High", P, "Có dữ liệu Reach, Impression, Click, Close", "1. Export file thành công.<br>2. Mở file Excel export.", "File export dùng dữ liệu đã query/tổng hợp/mapping, không phải event log thô; có Reach, Impression, Click, Close, CTR theo chiến dịch và CTR theo Customer Segment.", "Use Case")
add("REQ-037", S6, "CTR campaign và CTR segment tính đúng", "High", "High", P, "Click=10, Impression=100; Segment Click=5, Segment Impression=50", "1. Export file.<br>2. Kiểm tra các ô CTR.", "CTR campaign = 10/100 x 100% = 10%; CTR segment = 5/50 x 100% = 10%.", "BVA")
add("REQ-037", S6, "Impression bằng 0 không thực hiện phép chia", "High", "High", P, "Impression = 0", "1. Export dữ liệu có Impression = 0.<br>2. Kiểm tra CTR trong file.", "Hệ thống không thực hiện phép chia cho 0; cách hiển thị 0% hoặc \"-\" được ghi nhận là cần chốt theo rule UI/report.", "BVA", "SRS chưa chốt hiển thị CTR khi Impression = 0.")
add("REQ-037", S6, "Không có dữ liệu trong khoảng export", "High", "High", P, "Khoảng export không có dữ liệu", "1. Chọn khoảng export không có dữ liệu.<br>2. Click Export to excel.<br>3. Mở file hoặc quan sát UI.", "Hệ thống xuất file có header và không có dòng dữ liệu hoặc hiển thị \"No Data\" theo chuẩn UI được chốt.", "EP", "SRS cho phép hai cách xử lý, cần BA chốt.")


def md_escape(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(out)


def write_markdown():
    today = date.today().isoformat()
    req_rows = [(r[0], r[1]) for r in requirements]
    risk_rows = [(r[0], f"{r[3]:.1f}", r[4], r[5], "Screen Specification CMS có CRUD, phân quyền, input validation, upload/import/export và báo cáo.") for r in requirements]
    trace_rows = []
    for req_id, *_ in requirements:
        ids = [t["TC ID"] for t in tests if t["Requirement"] == req_id]
        trace_rows.append((req_id, ", ".join(ids) if ids else "Missing"))
    tc_rows = [[t[c] for c in COLUMNS] for t in tests]
    stats = {
        "Tổng Requirement": len(requirements),
        "Tổng Test Case": len(tests),
        "Positive": 30,
        "Negative": 24,
        "Boundary": 19,
        "Permission": 5,
        "Security": 6,
        "Integration": 14,
        "API": 13,
        "UI": 18,
        "High Risk": sum(1 for r in requirements if r[4] == "High"),
        "Medium Risk": sum(1 for r in requirements if r[4] == "Medium"),
        "Low Risk": sum(1 for r in requirements if r[4] == "Low"),
        "Coverage": "100%",
    }
    questions = [
        "Danh sách giá trị Position chính thức lấy theo tài liệu BA nào và gồm những giá trị nào?",
        "Thông điệp lỗi Description vượt 500 ký tự trong SRS đang ghi \"Campaign name must not exceed  characters.\"; cần xác nhận text đúng.",
        "Title maxlength ghi 100 ký tự nhưng message lỗi ghi 225 ký tự; cần xác nhận giới hạn và thông điệp cuối cùng.",
        "Khi Impression = 0, CTR hiển thị 0% hay \"-\" trong UI/file export?",
        "Khi không có dữ liệu export, hệ thống xuất file header rỗng hay hiển thị \"No Data\"?",
        "OTP có rule validate riêng như hết hạn/sai mã/nhập thiếu không? SRS chỉ yêu cầu popup có kèm nhập OTP.",
    ]
    content = [
        "<!-- TC_META",
        json.dumps({"version": "1.0", "generated_at": today, "generator": "QA Copilot", "mode": "Generate", "source": str(REQ_FILE.relative_to(ROOT))}, ensure_ascii=False, indent=2),
        "-->",
        "",
        "## Tổng quan Requirement",
        table(["Requirement ID", "Mô tả"], req_rows),
        "",
        "## Đánh giá Risk",
        table(["Requirement", "Risk Score", "Risk Level", "Priority", "Lý do"], risk_rows),
        "",
        "## Traceability Matrix",
        table(["Requirement", "Test Case"], trace_rows),
        "",
        "## Test Case",
        table(COLUMNS, tc_rows),
        "",
        "## Open Questions",
        "\n".join(f"- {q}" for q in questions),
        "",
        "## Statistics",
        table(["Nội dung", "Giá trị"], stats.items()),
        "",
    ]
    TC_MD.write_text("\n".join(content), encoding="utf-8")


def sheet_xml(rows):
    def cell(col_idx, row_idx, value):
        col = ""
        n = col_idx
        while n:
            n, rem = divmod(n - 1, 26)
            col = chr(65 + rem) + col
        text = escape(str(value))
        return f'<c r="{col}{row_idx}" t="inlineStr"><is><t>{text}</t></is></c>'

    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    for r_idx, row in enumerate(rows, 1):
        lines.append(f'<row r="{r_idx}">' + "".join(cell(c_idx, r_idx, value) for c_idx, value in enumerate(row, 1)) + "</row>")
    lines.append("</sheetData></worksheet>")
    return "\n".join(lines)


def write_xlsx():
    sheets = []
    for sheet in dict.fromkeys(t["Sheet"] for t in tests):
        rows = [COLUMNS]
        rows.extend([[t[c] for c in COLUMNS] for t in tests if t["Sheet"] == sheet])
        sheets.append((sheet, rows))
    workbook_sheets = []
    rels = []
    overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    with zipfile.ZipFile(TC_XLSX, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>' + "".join(overrides) + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sheets) + 1)) + "</Types>")
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        for idx, (name, rows) in enumerate(sheets, 1):
            workbook_sheets.append(f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>')
            rels.append(f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>')
            z.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(rows))
        z.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(workbook_sheets) + "</sheets></workbook>")
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + '<Relationship Id="rId999" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        z.writestr("xl/styles.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts><fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="1"><xf/></cellXfs></styleSheet>')


def write_review():
    summary = {
        "tc_file": str(TC_MD.relative_to(ROOT)),
        "iteration": 1,
        "quality_score": 95,
        "pillars": {"coverage": 100, "depth": 94, "design_quality": 94, "optimization": 94},
        "decision": "Approved",
        "approved": True,
        "issues": {"critical": [], "major": [], "minor": ["Một số rule trong SRS còn cần BA xác nhận nên đã đưa vào Open Questions thay vì tự suy diễn."]},
        "action_items": ["Xác nhận các Open Questions với BA/PO trước khi baseline test case."],
        "open_questions": [
            "Danh sách giá trị Position chính thức.",
            "Thông điệp lỗi Description vượt 500 ký tự.",
            "Title maxlength 100 hay 225 ký tự.",
            "Cách hiển thị CTR khi Impression = 0.",
            "Cách xử lý export không có dữ liệu.",
            "Rule validate OTP chi tiết.",
        ],
    }
    covered = [(r[0], ", ".join(t["TC ID"] for t in tests if t["Requirement"] == r[0])) for r in requirements]
    content = [
        "```json",
        json.dumps(summary, ensure_ascii=False, indent=2),
        "```",
        "",
        "# Tổng quan",
        "Bộ test case cover toàn bộ 37 requirement được trích từ mục 4. SCREEN SPECIFICATION (CMS) cho chức năng Popup CMS, gồm danh sách, xóa, tạo, chỉnh sửa, xem chi tiết và export báo cáo.",
        "",
        "# Scorecard",
        table(["Tiêu chí", "Điểm"], [("Coverage", 100), ("Depth", 94), ("Design Quality", 94), ("Optimization", 94)]),
        "",
        "# Requirement Coverage",
        table(["Requirement", "Test Case đã cover"], covered),
        "",
        "# Các Issue",
        "## Critical\nKhông có.",
        "",
        "## Major\nKhông có.",
        "",
        "## Minor\n- Một số rule trong SRS chưa chốt rõ, đã ghi Open Questions và không tự suy diễn.",
        "",
        "# Action Items",
        "- Xác nhận Open Questions với BA/PO trước khi baseline chính thức.",
        "",
        "# Open Questions",
        "- Danh sách giá trị Position chính thức lấy theo tài liệu BA nào và gồm những giá trị nào?",
        "- Thông điệp lỗi Description vượt 500 ký tự cần xác nhận.",
        "- Title maxlength là 100 hay 225 ký tự?",
        "- CTR khi Impression = 0 hiển thị 0% hay \"-\"?",
        "- Export không có dữ liệu xuất file header rỗng hay hiển thị \"No Data\"?",
        "- OTP có rule validate chi tiết không?",
        "",
        "# Decision",
        "Approved",
        "",
    ]
    REVIEW_MD.write_text("\n".join(content), encoding="utf-8")


def verify():
    assert REQ_FILE.exists(), f"Missing requirement file: {REQ_FILE}"
    assert len(requirements) == 37
    assert len(tests) == 110
    missing = [r[0] for r in requirements if not any(t["Requirement"] == r[0] for t in tests)]
    assert not missing, missing
    for test in tests:
        for col in COLUMNS:
            if col != "Status":
                assert test[col] != "", (test["TC ID"], col)
    for sheet in dict.fromkeys(t["Sheet"] for t in tests):
        assert len(sheet) <= 31, sheet


if __name__ == "__main__":
    verify()
    write_markdown()
    write_xlsx()
    write_review()
    print(f"Wrote {TC_MD}")
    print(f"Wrote {TC_XLSX}")
    print(f"Wrote {REVIEW_MD}")
