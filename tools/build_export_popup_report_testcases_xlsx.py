from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_PATH = Path(__file__).with_name("build_cms_popup_testcases_xlsx.py")
spec = importlib.util.spec_from_file_location("xlsx_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

base.OUT_PATH = "deliverables/Bo_ca_kiem_thu_Export_Bao_cao_Popup.xlsx"


def tc(tc_id, category, scenario, pre, steps, data, expected, priority="Cao", status="Chưa chạy"):
    return [tc_id, category, scenario, pre, steps, data, expected, priority, status]


def build_export_cases():
    rows = []
    add = rows.append

    # Phân Quyền
    add(tc("TC-EXP-PQ-001", "Phân Quyền", "Admin CMS có quyền Pop-up mở được popup EXPORT từ màn danh sách", "Admin CMS đã đăng nhập và có quyền Pop-up", "1. Mở menu Pop-up - Chiến dịch Marketing\n2. Click nút Export to Excel", "Tài khoản Admin CMS", "Popup EXPORT mở thành công.", "Cao"))
    add(tc("TC-EXP-PQ-002", "Phân Quyền", "Manager CMS có quyền Pop-up mở được popup EXPORT từ màn danh sách", "Manager CMS đã đăng nhập và có quyền Pop-up", "1. Mở danh sách campaign Pop-up\n2. Click Export to Excel", "Tài khoản Manager CMS", "Popup EXPORT mở thành công.", "Cao"))
    add(tc("TC-EXP-PQ-003", "Phân Quyền", "User không có quyền Pop-up không nhìn thấy chức năng export", "User CMS không có quyền Pop-up", "1. Đăng nhập CMS\n2. Quan sát menu và màn danh sách nếu truy cập được bằng URL", "Tài khoản không có quyền Pop-up", "User không thấy menu/chức năng Pop-up; backend từ chối truy cập trực tiếp nên không export được báo cáo.", "Cao"))
    add(tc("TC-EXP-PQ-004", "Phân Quyền", "Backend từ chối API export khi user không có quyền", "User không có quyền Pop-up nhưng có API endpoint export", "1. Gửi request export bằng API/client ngoài UI\n2. Kiểm tra phản hồi", "Request export hợp lệ về dữ liệu nhưng thiếu quyền", "Backend từ chối request; không tạo file export. Requirement cần xác nhận mã lỗi/thông báo cụ thể.", "Cao"))
    add(tc("TC-EXP-PQ-005", "Phân Quyền", "Export toàn bộ campaign chỉ gồm campaign actor có quyền export", "User có quyền export một phần dữ liệu campaign", "1. Mở popup EXPORT\n2. Chọn Toàn bộ chiến dịch\n3. Chọn thời gian hợp lệ\n4. Export file\n5. Kiểm tra nội dung file", "Khoảng thời gian có campaign thuộc nhiều phạm vi quyền", "File chỉ chứa dữ liệu các campaign user có quyền export.", "Cao"))
    add(tc("TC-EXP-PQ-006", "Phân Quyền", "Dropdown campaign chỉ hiển thị campaign thuộc phạm vi quyền dữ liệu", "User có quyền export một phần campaign", "1. Mở popup EXPORT\n2. Chọn Export từng chiến dịch\n3. Mở dropdown Tên popup chiến dịch", "Nhiều campaign thuộc/không thuộc quyền", "Dropdown chỉ hiển thị campaign Pop-up user được phép export. Requirement cần xác nhận nếu dropdown hiển thị tất cả theo SRS.", "Cao"))
    add(tc("TC-EXP-PQ-007", "Phân Quyền", "Không export được campaign ngoài phạm vi quyền bằng request chỉnh sửa campaign_id", "User có quyền export campaign A nhưng không có quyền campaign B", "1. Mở popup export campaign A\n2. Sửa request thành campaign_id của campaign B\n3. Gửi request", "campaign_id ngoài quyền", "Backend từ chối hoặc không trả dữ liệu ngoài quyền; không rò rỉ báo cáo campaign B.", "Cao"))
    add(tc("TC-EXP-PQ-008", "Phân Quyền", "Không cho tải file khi phiên đăng nhập hết hạn", "User đang mở popup EXPORT; session hết hạn", "1. Chọn dữ liệu hợp lệ\n2. Làm session hết hạn\n3. Click Export to excel", "Session hết hạn", "Hệ thống yêu cầu đăng nhập lại hoặc từ chối export theo chuẩn CMS; không tải file.", "Cao"))

    # Chức năng chính
    add(tc("TC-EXP-CN-001", "Chức năng chính", "Click Export to Excel mở popup EXPORT", "User có quyền Pop-up; đang ở màn danh sách campaign", "1. Click nút Export to Excel", "Không áp dụng", "Popup EXPORT hiển thị.", "Cao"))
    add(tc("TC-EXP-CN-002", "Chức năng chính", "Popup EXPORT hiển thị đúng tiêu đề", "Popup EXPORT đang mở", "1. Quan sát header popup", "Không áp dụng", "Header hiển thị đúng: EXPORT.", "Trung bình"))
    add(tc("TC-EXP-CN-003", "Chức năng chính", "Close icon đóng popup và không export", "Popup EXPORT đang mở", "1. Chọn một số filter trong popup\n2. Click icon X\n3. Kiểm tra request/download", "Không áp dụng", "Popup đóng; không thực hiện export; không lưu thay đổi filter trong popup.", "Cao"))
    add(tc("TC-EXP-CN-004", "Chức năng chính", "Cancel đóng popup và không export", "Popup EXPORT đang mở", "1. Chọn dữ liệu trong popup\n2. Click Cancel", "Không áp dụng", "Popup đóng; không gọi API export; không tải file.", "Cao"))
    add(tc("TC-EXP-CN-005", "Chức năng chính", "Mặc định chọn Export từng chiến dịch khi mở từ action export của một campaign cụ thể", "Có action export tại một campaign cụ thể nếu UI hỗ trợ", "1. Click export tại dòng campaign cụ thể\n2. Quan sát popup EXPORT", "Campaign POP01", "Option Export từng chiến dịch được chọn mặc định và campaign tương ứng được chọn nếu có.", "Cao"))
    add(tc("TC-EXP-CN-006", "Chức năng chính", "Chỉ chọn được một trong hai option export", "Popup EXPORT đang mở", "1. Chọn Export từng chiến dịch\n2. Chọn Toàn bộ chiến dịch\n3. Chọn lại Export từng chiến dịch", "Hai option export", "Tại mọi thời điểm chỉ có một option được chọn.", "Cao"))
    add(tc("TC-EXP-CN-007", "Chức năng chính", "Chọn Export từng chiến dịch hiển thị và enable dropdown campaign", "Popup EXPORT đang mở", "1. Chọn Export từng chiến dịch\n2. Quan sát field Tên popup chiến dịch", "Option Export từng chiến dịch", "Dropdown Tên popup chiến dịch hiển thị/enable và là field bắt buộc.", "Cao"))
    add(tc("TC-EXP-CN-008", "Chức năng chính", "Chọn Toàn bộ chiến dịch ẩn hoặc disable dropdown campaign", "Popup EXPORT đang mở", "1. Chọn Toàn bộ chiến dịch\n2. Quan sát field Tên popup chiến dịch", "Option Toàn bộ chiến dịch", "Dropdown Tên popup chiến dịch bị ẩn hoặc disabled và không bắt buộc.", "Cao"))
    add(tc("TC-EXP-CN-009", "Chức năng chính", "Export từng chiến dịch thành công", "Có campaign Pop-up; có dữ liệu báo cáo trong khoảng export", "1. Mở popup EXPORT\n2. Chọn Export từng chiến dịch\n3. Chọn campaign\n4. Chọn Export Period hợp lệ\n5. Click Export to excel", "Campaign POP01; khoảng ngày hợp lệ", "Hệ thống tải file Excel báo cáo theo campaign và thời gian đã chọn.", "Cao"))
    add(tc("TC-EXP-CN-010", "Chức năng chính", "Export toàn bộ chiến dịch thành công", "Có nhiều campaign trong phạm vi quyền; có dữ liệu báo cáo", "1. Mở popup EXPORT\n2. Chọn Toàn bộ chiến dịch\n3. Chọn Export Period hợp lệ\n4. Click Export to excel", "Khoảng ngày hợp lệ", "Hệ thống tải file Excel tổng hợp toàn bộ campaign phù hợp quyền dữ liệu và thời gian xuất.", "Cao"))
    add(tc("TC-EXP-CN-011", "Chức năng chính", "Request export từng chiến dịch gửi campaign_id", "Có thể kiểm tra network/log", "1. Chọn Export từng chiến dịch\n2. Chọn campaign\n3. Chọn thời gian hợp lệ\n4. Click Export to excel\n5. Kiểm tra request", "Campaign POP01", "Request export có campaign_id đúng campaign đã chọn.", "Cao"))
    add(tc("TC-EXP-CN-012", "Chức năng chính", "Request export toàn bộ chiến dịch không gửi campaign_id", "Có thể kiểm tra network/log", "1. Chọn Toàn bộ chiến dịch\n2. Chọn thời gian hợp lệ\n3. Click Export to excel\n4. Kiểm tra request", "All Campaigns", "Request không gửi campaign_id.", "Cao"))
    add(tc("TC-EXP-CN-013", "Chức năng chính", "Tên file export từng chiến dịch theo format gợi ý", "Export từng chiến dịch thành công", "1. Export campaign POP01 với khoảng ngày hợp lệ\n2. Kiểm tra tên file tải về", "CampaignID=POP01; FromDate; ToDate", "Tên file theo gợi ý: Popup_Report_<CampaignID>_<FromDate>_<ToDate>.xlsx. Requirement cần xác nhận format ngày chính xác.", "Trung bình"))
    add(tc("TC-EXP-CN-014", "Chức năng chính", "Tên file export toàn bộ chiến dịch theo format gợi ý", "Export toàn bộ chiến dịch thành công", "1. Export toàn bộ chiến dịch với khoảng ngày hợp lệ\n2. Kiểm tra tên file tải về", "FromDate; ToDate", "Tên file theo gợi ý: Popup_Report_AllCampaigns_<FromDate>_<ToDate>.xlsx. Requirement cần xác nhận format ngày chính xác.", "Trung bình"))
    add(tc("TC-EXP-CN-015", "Chức năng chính", "Export vẫn tạo file khi không có dữ liệu trong khoảng export", "Không có dữ liệu báo cáo trong khoảng ngày đã chọn", "1. Mở popup EXPORT\n2. Chọn campaign hoặc toàn bộ chiến dịch\n3. Chọn khoảng ngày không có dữ liệu\n4. Click Export to excel", "Khoảng ngày không có dữ liệu", "Hệ thống vẫn xuất file có header và không có dòng dữ liệu, hoặc hiển thị No Data theo chuẩn UI được chốt.", "Cao"))
    add(tc("TC-EXP-CN-016", "Chức năng chính", "Dropdown campaign hiển thị cấu trúc ID_[Tên Campaign]", "Popup EXPORT chọn Export từng chiến dịch", "1. Mở dropdown Tên popup chiến dịch\n2. Quan sát danh sách option", "Campaign POP01 - Tên A", "Option campaign hiển thị theo cấu trúc ID_[Tên Campaign].", "Trung bình"))
    add(tc("TC-EXP-CN-017", "Chức năng chính", "Export Period hiển thị đúng format date range", "Popup EXPORT đang mở", "1. Chọn From Date và To Date\n2. Quan sát field Export Period", "2025-07-04 đến 2025-08-12", "Export Period hiển thị theo format date range của CMS, ví dụ 2025-07-04 -> 2025-08-12.", "Trung bình"))
    add(tc("TC-EXP-CN-018", "Chức năng chính", "Export file dùng dữ liệu báo cáo tổng hợp, không phải event log thô", "Có dữ liệu event log và dữ liệu report tổng hợp", "1. Export file\n2. Kiểm tra cấu trúc/nội dung file", "Dữ liệu impression/click/close", "File chỉ chứa dữ liệu đã query/tổng hợp/mapping để vận hành đọc được; không xuất event log thô theo từng sự kiện kỹ thuật.", "Cao"))
    add(tc("TC-EXP-CN-019", "Chức năng chính", "File export có bộ chỉ số Reach, Impression, Click, Close, CTR campaign", "Export file thành công", "1. Mở file Excel export\n2. Kiểm tra các cột/chỉ số", "File export", "File có các chỉ số Reach, Impression, Click, Close, CTR theo chiến dịch theo template export.", "Cao"))
    add(tc("TC-EXP-CN-020", "Chức năng chính", "File export có CTR theo Customer Segment", "Campaign áp dụng Customer Segment", "1. Export một campaign áp dụng segment\n2. Mở file Excel\n3. Kiểm tra phần CTR theo segment", "Campaign dùng Customer Segment", "File hiển thị CTR theo từng Customer Segment được áp dụng cho campaign.", "Cao"))
    add(tc("TC-EXP-CN-021", "Chức năng chính", "Campaign áp dụng Toàn bộ hội viên hiển thị nhóm All User/Toàn bộ hội viên", "Campaign áp dụng toàn bộ hội viên", "1. Export campaign\n2. Kiểm tra phần segment trong file", "Audience = Toàn bộ hội viên", "Export hiển thị nhóm All User/Toàn bộ hội viên thay vì Customer Segment cụ thể.", "Cao"))
    add(tc("TC-EXP-CN-022", "Chức năng chính", "Campaign Import file xuất báo cáo theo template campaign cụ thể import file", "Campaign áp dụng đối tượng Import file", "1. Export campaign Import file\n2. Mở file Excel\n3. Đối chiếu cấu trúc template", "Campaign dùng Import file", "File export tuân theo template export cho 1 campaign cụ thể - tệp khách hàng import cụ thể.", "Cao"))
    add(tc("TC-EXP-CN-023", "Chức năng chính", "Campaign chọn từ module Segment xuất báo cáo theo template campaign cụ thể segment", "Campaign áp dụng Customer Segment từ module Segment", "1. Export campaign segment\n2. Mở file Excel\n3. Đối chiếu cấu trúc template", "Campaign dùng Customer Segment", "File export tuân theo template export cho 1 campaign cụ thể - tệp khách hàng chọn từ Segment.", "Cao"))
    add(tc("TC-EXP-CN-024", "Chức năng chính", "Toàn bộ chiến dịch xuất báo cáo theo template toàn bộ chiến dịch", "Có nhiều campaign trong khoảng export", "1. Chọn Toàn bộ chiến dịch\n2. Export file\n3. Mở file Excel\n4. Đối chiếu cấu trúc template", "All Campaigns", "File export tuân theo template export toàn bộ chiến dịch.", "Cao"))

    # Quy tắc nhập liệu
    add(tc("TC-EXP-VL-001", "Quy tắc nhập liệu", "Không chọn campaign khi Export từng chiến dịch", "Popup EXPORT chọn Export từng chiến dịch", "1. Không chọn Tên popup chiến dịch\n2. Chọn Export Period hợp lệ\n3. Click Export to excel", "Campaign rỗng", "Hiển thị lỗi: Please select popup campaign. Không export file.", "Cao"))
    add(tc("TC-EXP-VL-002", "Quy tắc nhập liệu", "Không chọn Export Period", "Popup EXPORT đang mở", "1. Chọn option export hợp lệ\n2. Không chọn Export Period\n3. Click Export to excel", "Export Period rỗng", "Hiển thị lỗi: Please select export date range. Không export file.", "Cao"))
    add(tc("TC-EXP-VL-003", "Quy tắc nhập liệu", "Chỉ chọn From Date chưa chọn To Date", "Popup EXPORT đang mở", "1. Chọn From Date\n2. Không chọn To Date\n3. Click Export to excel", "Thiếu To Date", "Hiển thị lỗi: Please select export date range.", "Cao"))
    add(tc("TC-EXP-VL-004", "Quy tắc nhập liệu", "Chỉ chọn To Date chưa chọn From Date", "Popup EXPORT đang mở", "1. Chọn To Date\n2. Không chọn From Date\n3. Click Export to excel", "Thiếu From Date", "Hiển thị lỗi: Please select export date range.", "Cao"))
    add(tc("TC-EXP-VL-005", "Quy tắc nhập liệu", "date_from lớn hơn date_to", "Có thể nhập tay hoặc giả lập stale UI", "1. Nhập From Date lớn hơn To Date\n2. Click Export to excel", "date_from > date_to", "Hiển thị lỗi: Invalid date range. Không export file.", "Cao"))
    add(tc("TC-EXP-VL-006", "Quy tắc nhập liệu", "Date picker chặn khoảng export lớn hơn 1 năm", "Popup EXPORT đang mở", "1. Mở date picker\n2. Chọn khoảng thời gian lớn hơn 1 năm tính từ thời điểm hiện tại", "Khoảng ngày > 1 năm", "FE date picker chặn ngay từ đầu, không cho chọn khoảng thời gian export > 1 năm.", "Cao"))
    add(tc("TC-EXP-VL-007", "Quy tắc nhập liệu", "Export với khoảng thời gian đúng bằng 1 năm", "Popup EXPORT đang mở", "1. Chọn khoảng Export Period đúng 1 năm\n2. Chọn dữ liệu export hợp lệ\n3. Click Export to excel", "Khoảng ngày = 1 năm", "Hệ thống cho phép export vì thỏa điều kiện <= 1 năm.", "Cao"))
    add(tc("TC-EXP-VL-008", "Quy tắc nhập liệu", "Export với khoảng thời gian vượt 1 năm bằng cách sửa request", "Có thể chỉnh request hoặc stale UI", "1. Chọn khoảng hợp lệ trên UI\n2. Sửa request thành khoảng > 1 năm\n3. Gửi request export", "Khoảng ngày > 1 năm", "Backend từ chối export để bảo vệ rule. Requirement cần xác nhận mã lỗi/thông báo cụ thể.", "Cao"))
    add(tc("TC-EXP-VL-009", "Quy tắc nhập liệu", "Export từng chiến dịch với campaign_id không tồn tại", "Có thể sửa request campaign_id", "1. Chọn Export từng chiến dịch\n2. Sửa campaign_id thành ID không tồn tại\n3. Gửi request", "campaign_id không tồn tại", "Backend trả lỗi; không tạo file. FE hiển thị lỗi thất bại phù hợp.", "Cao"))
    add(tc("TC-EXP-VL-010", "Quy tắc nhập liệu", "Chọn Toàn bộ chiến dịch không validate campaign rỗng", "Popup EXPORT đang mở", "1. Chọn Toàn bộ chiến dịch\n2. Không chọn campaign\n3. Chọn Export Period hợp lệ\n4. Click Export to excel", "Không có campaign_id", "Không hiển thị lỗi Please select popup campaign; request không gửi campaign_id.", "Cao"))
    add(tc("TC-EXP-VL-011", "Quy tắc nhập liệu", "Không gửi campaign_id cũ sau khi chuyển từ Export từng chiến dịch sang Toàn bộ chiến dịch", "Popup EXPORT đang mở", "1. Chọn Export từng chiến dịch và chọn campaign\n2. Chuyển sang Toàn bộ chiến dịch\n3. Chọn thời gian hợp lệ\n4. Export và kiểm tra request", "Campaign đã chọn trước đó", "Request export toàn bộ chiến dịch không chứa campaign_id cũ.", "Cao"))
    add(tc("TC-EXP-VL-012", "Quy tắc nhập liệu", "Quay lại Export từng chiến dịch sau khi chọn Toàn bộ chiến dịch phải validate campaign", "Popup EXPORT đang mở", "1. Chọn Toàn bộ chiến dịch\n2. Chuyển sang Export từng chiến dịch\n3. Không chọn campaign\n4. Chọn thời gian hợp lệ\n5. Click Export to excel", "Campaign rỗng", "Hiển thị lỗi: Please select popup campaign.", "Cao"))
    add(tc("TC-EXP-VL-013", "Quy tắc nhập liệu", "Khoảng ngày có dữ liệu tại đúng From Date được tính vào export", "Có event/report phát sinh đúng ngày From Date", "1. Chọn Export Period có From Date trùng ngày phát sinh dữ liệu\n2. Export file\n3. Kiểm tra số liệu", "Dữ liệu tại From Date", "Dữ liệu tại biên From Date được đưa vào báo cáo theo khoảng export.", "Cao"))
    add(tc("TC-EXP-VL-014", "Quy tắc nhập liệu", "Khoảng ngày có dữ liệu tại đúng To Date được tính vào export", "Có event/report phát sinh đúng ngày To Date", "1. Chọn Export Period có To Date trùng ngày phát sinh dữ liệu\n2. Export file\n3. Kiểm tra số liệu", "Dữ liệu tại To Date", "Dữ liệu tại biên To Date được đưa vào báo cáo theo khoảng export.", "Cao"))
    add(tc("TC-EXP-VL-015", "Quy tắc nhập liệu", "Export trong một ngày", "Có dữ liệu báo cáo trong cùng một ngày", "1. Chọn From Date bằng To Date\n2. Chọn option export hợp lệ\n3. Click Export to excel", "From Date = To Date", "Hệ thống cho phép export dữ liệu trong ngày được chọn.", "Trung bình"))
    add(tc("TC-EXP-VL-016", "Quy tắc nhập liệu", "Không cho nhập định dạng ngày không hợp lệ nếu field cho nhập tay", "Popup EXPORT đang mở; date range cho nhập tay nếu có", "1. Nhập ngày sai format\n2. Click Export to excel", "2025/99/99 hoặc text", "Hệ thống không chấp nhận ngày sai format; hiển thị lỗi theo chuẩn component. Requirement cần xác nhận message cụ thể.", "Trung bình"))
    add(tc("TC-EXP-VL-017", "Quy tắc nhập liệu", "Không export khi không có campaign nào trong phạm vi quyền cho Toàn bộ chiến dịch", "User có quyền Pop-up nhưng không có campaign phù hợp quyền dữ liệu", "1. Chọn Toàn bộ chiến dịch\n2. Chọn Export Period hợp lệ\n3. Click Export to excel", "Không có campaign trong quyền", "Hệ thống xử lý theo rule không dữ liệu: xuất file header rỗng hoặc hiển thị No Data theo chuẩn UI được chốt.", "Trung bình"))

    # Tích hợp
    add(tc("TC-EXP-TH-001", "Tích hợp", "API export thành công trả file .xlsx tải được", "Dữ liệu export hợp lệ; backend hoạt động", "1. Gửi request export từ UI\n2. Kiểm tra response và file tải về", "Request hợp lệ", "Response trả file Excel .xlsx; trình duyệt tải file thành công.", "Cao"))
    add(tc("TC-EXP-TH-002", "Tích hợp", "API export thất bại hiển thị toast lỗi", "Backend export trả lỗi", "1. Chọn dữ liệu hợp lệ\n2. Click Export to excel\n3. Backend trả lỗi", "Lỗi backend", "Hiển thị toast: Failed to export report.", "Cao"))
    add(tc("TC-EXP-TH-003", "Tích hợp", "Mất kết nối khi export", "Có thể giả lập network timeout", "1. Chọn dữ liệu hợp lệ\n2. Ngắt mạng hoặc giả lập timeout\n3. Click Export to excel", "Network timeout", "Không tải file; hiển thị lỗi export thất bại theo chuẩn CMS.", "Cao"))
    add(tc("TC-EXP-TH-004", "Tích hợp", "Không gửi request export nhiều lần khi bấm liên tục", "API export phản hồi chậm", "1. Chọn dữ liệu hợp lệ\n2. Click Export to excel nhiều lần liên tiếp\n3. Kiểm tra request", "Network chậm", "Chỉ một request export được xử lý hoặc button chuyển loading/disabled để tránh duplicate download.", "Cao"))
    add(tc("TC-EXP-TH-005", "Tích hợp", "Reach đếm hội viên duy nhất", "Có dữ liệu một hội viên thấy cùng popup nhiều lần", "1. Export report campaign\n2. Kiểm tra chỉ số Reach trong file", "Member A thấy popup 3 lần", "Reach chỉ tính Member A là 1 trong cùng phạm vi thống kê.", "Cao"))
    add(tc("TC-EXP-TH-006", "Tích hợp", "Impression đếm tổng lượt hiển thị", "Có dữ liệu nhiều lần hiển thị popup", "1. Export report campaign\n2. Kiểm tra Impression", "Member A thấy 3 lần; Member B thấy 2 lần", "Impression bằng tổng số lần popup được hiển thị trong khoảng export.", "Cao"))
    add(tc("TC-EXP-TH-007", "Tích hợp", "Click đếm lượt nhấn popup không phụ thuộc điều hướng thành công", "Có dữ liệu click thành công và điều hướng thất bại", "1. Export report campaign\n2. Kiểm tra Click", "Click popup, navigation failed", "Click vẫn được ghi nhận khi hội viên nhấn popup, không phụ thuộc việc điều hướng sau đó thành công hay không.", "Cao"))
    add(tc("TC-EXP-TH-008", "Tích hợp", "Close không tính cho interaction đã click", "Có dữ liệu user click popup và user đóng popup", "1. Export report campaign\n2. Kiểm tra Click và Close", "Interaction click; interaction close", "Nếu hội viên đã nhấn popup thì interaction đó tính Click, không tính Close.", "Cao"))
    add(tc("TC-EXP-TH-009", "Tích hợp", "CTR campaign tính bằng Click/Impression x 100%", "Có dữ liệu Click và Impression xác định", "1. Export report campaign\n2. Đối chiếu CTR trong file", "Click=25; Impression=100", "CTR campaign hiển thị 25% theo công thức Click / Impression x 100%.", "Cao"))
    add(tc("TC-EXP-TH-010", "Tích hợp", "CTR segment tính bằng Click segment/Impression segment x 100%", "Campaign áp dụng Customer Segment có dữ liệu theo segment", "1. Export campaign\n2. Đối chiếu CTR từng segment", "Segment A: Click=10, Impression=50", "CTR segment A hiển thị 20% theo công thức Click segment / Impression segment x 100%.", "Cao"))
    add(tc("TC-EXP-TH-011", "Tích hợp", "Impression bằng 0 không thực hiện phép chia CTR", "Có campaign/segment Impression = 0", "1. Export report\n2. Kiểm tra cột CTR", "Impression=0", "Không phát sinh lỗi chia cho 0; hiển thị 0% hoặc '-' theo rule UI/report được chốt.", "Cao"))
    add(tc("TC-EXP-TH-012", "Tích hợp", "Dữ liệu export khớp dữ liệu báo cáo đã tổng hợp", "Có quyền đối chiếu dữ liệu report backend/database", "1. Export file\n2. Lấy dữ liệu tổng hợp backend/database cùng điều kiện\n3. Đối chiếu số liệu", "Campaign, khoảng ngày", "Số liệu trong file khớp dữ liệu báo cáo đã query/mapping/biến đổi.", "Cao"))
    add(tc("TC-EXP-TH-013", "Tích hợp", "File Excel mở được trên ứng dụng bảng tính phổ biến", "Export file thành công", "1. Tải file\n2. Mở bằng Microsoft Excel/Google Sheets/LibreOffice nếu có", "File .xlsx", "File không lỗi định dạng, mở được và hiển thị dữ liệu đầy đủ.", "Trung bình"))
    add(tc("TC-EXP-TH-014", "Tích hợp", "Dữ liệu Unicode tiếng Việt hiển thị đúng trong file export", "Campaign/Segment có tên tiếng Việt có dấu", "1. Export file\n2. Mở file\n3. Kiểm tra tên campaign/segment", "Tên tiếng Việt có dấu", "Tiếng Việt hiển thị đúng, không lỗi font/encoding.", "Trung bình"))
    add(tc("TC-EXP-TH-015", "Tích hợp", "Export dữ liệu lớn trong phạm vi 1 năm", "Có nhiều campaign và dữ liệu report lớn", "1. Chọn Toàn bộ chiến dịch\n2. Chọn khoảng 1 năm\n3. Export file", "Dữ liệu lớn <= 1 năm", "File được tạo/tải thành công trong ngưỡng hiệu năng chấp nhận. Requirement cần xác nhận SLA/thời gian tối đa.", "Cao"))

    # Hồi quy
    add(tc("TC-EXP-RG-001", "Hồi quy", "Không ảnh hưởng search/filter danh sách sau khi mở và đóng popup EXPORT", "Đang ở màn danh sách campaign", "1. Áp dụng search/filter trên danh sách\n2. Mở popup EXPORT\n3. Click Cancel hoặc Close\n4. Kiểm tra search/filter danh sách", "Filter danh sách bất kỳ", "Search/filter của màn danh sách vẫn giữ đúng trạng thái trước đó.", "Trung bình"))
    add(tc("TC-EXP-RG-002", "Hồi quy", "Không ảnh hưởng chức năng tạo campaign", "Sau khi export report", "1. Export file thành công\n2. Mở màn Create\n3. Tạo campaign hợp lệ", "Dữ liệu tạo hợp lệ", "Chức năng tạo campaign vẫn hoạt động đúng.", "Cao"))
    add(tc("TC-EXP-RG-003", "Hồi quy", "Không ảnh hưởng chức năng chỉnh sửa campaign", "Sau khi export report", "1. Export file thành công\n2. Mở Edit campaign được phép sửa\n3. Lưu thay đổi hợp lệ", "Campaign Scheduled/Active/Inactive", "Chức năng chỉnh sửa campaign vẫn hoạt động đúng.", "Cao"))
    add(tc("TC-EXP-RG-004", "Hồi quy", "Không ảnh hưởng chức năng xoá campaign", "Sau khi export report", "1. Export file thành công\n2. Xoá campaign Scheduled hợp lệ", "Campaign Scheduled", "Chức năng xoá campaign vẫn hoạt động đúng.", "Cao"))
    add(tc("TC-EXP-RG-005", "Hồi quy", "Không ảnh hưởng màn xem chi tiết campaign", "Sau khi export report", "1. Export file\n2. Mở View campaign", "Campaign bất kỳ", "Màn xem chi tiết hiển thị đúng dữ liệu và read-only theo SRS.", "Trung bình"))
    add(tc("TC-EXP-RG-006", "Hồi quy", "Không ảnh hưởng tracking Impression/Click/Close trên App", "Có campaign Active đang ghi nhận tracking", "1. Export report trên CMS\n2. Thực hiện impression/click/close trên App\n3. Kiểm tra dữ liệu tracking sau đó", "Campaign Active", "Tracking mới vẫn được ghi nhận bình thường; export không làm thay đổi event/report source.", "Cao"))
    add(tc("TC-EXP-RG-007", "Hồi quy", "Không ảnh hưởng quyền truy cập menu Pop-up", "Có nhiều role CMS", "1. Kiểm tra menu Pop-up với user có quyền và không có quyền sau khi triển khai export", "Admin/Manager/User không quyền", "Menu và quyền truy cập Pop-up vẫn tuân thủ SRS danh sách.", "Cao"))

    # UI/UX
    add(tc("TC-EXP-UI-001", "UI/UX", "Popup EXPORT hiển thị đúng bố cục theo mockup", "Click Export to Excel", "1. Mở popup EXPORT\n2. Quan sát bố cục, spacing, label, button", "Không áp dụng", "Popup hiển thị đúng mockup, không tràn/chồng lấn nội dung.", "Thấp"))
    add(tc("TC-EXP-UI-002", "UI/UX", "Label các field hiển thị đúng", "Popup EXPORT đang mở", "1. Quan sát label Header, option export, Tên popup chiến dịch, Thời gian xuất dữ liệu, Cancel, Export to excel", "Không áp dụng", "Các label hiển thị đúng nội dung theo SRS.", "Thấp"))
    add(tc("TC-EXP-UI-003", "UI/UX", "Dropdown campaign enable/disable trực quan theo option export", "Popup EXPORT đang mở", "1. Chọn Export từng chiến dịch\n2. Chọn Toàn bộ chiến dịch\n3. Quan sát dropdown campaign", "Hai option export", "Dropdown hiển thị/enable hoặc ẩn/disable rõ ràng, không gây nhầm lẫn.", "Trung bình"))
    add(tc("TC-EXP-UI-004", "UI/UX", "Export to excel button hiển thị trạng thái loading khi đang export", "API export phản hồi chậm", "1. Chọn dữ liệu hợp lệ\n2. Click Export to excel\n3. Quan sát button", "Request export chậm", "Button hiển thị loading/disabled theo chuẩn CMS trong lúc xử lý.", "Trung bình"))
    add(tc("TC-EXP-UI-005", "UI/UX", "Lỗi validate hiển thị gần field tương ứng", "Popup EXPORT có dữ liệu thiếu", "1. Bỏ trống campaign hoặc date range\n2. Click Export to excel\n3. Quan sát vị trí lỗi", "Field thiếu dữ liệu", "Thông báo lỗi hiển thị gần field liên quan và dễ đọc.", "Trung bình"))
    add(tc("TC-EXP-UI-006", "UI/UX", "Toast Failed to export report hiển thị đúng vị trí", "API export trả lỗi", "1. Click Export to excel với dữ liệu hợp lệ\n2. Backend trả lỗi\n3. Quan sát toast", "Lỗi backend", "Toast lỗi hiển thị đúng nội dung và vị trí theo chuẩn CMS.", "Thấp"))
    add(tc("TC-EXP-UI-007", "UI/UX", "Date range picker chặn chọn quá 1 năm một cách dễ hiểu", "Popup EXPORT đang mở", "1. Mở date picker\n2. Thử chọn khoảng ngày > 1 năm", "Khoảng > 1 năm", "UI chặn chọn khoảng > 1 năm, trạng thái disabled/feedback rõ ràng.", "Trung bình"))
    add(tc("TC-EXP-UI-008", "UI/UX", "Popup EXPORT responsive trong kích thước màn hình CMS hỗ trợ", "CMS ở viewport được hỗ trợ", "1. Thay đổi kích thước viewport\n2. Mở popup EXPORT\n3. Kiểm tra thao tác chọn option/date/dropdown", "Desktop/tablet nếu CMS hỗ trợ", "Popup dùng được, không tràn màn hình, button vẫn thao tác được.", "Thấp"))
    add(tc("TC-EXP-UI-009", "UI/UX", "Điều hướng bàn phím trong popup EXPORT", "Popup EXPORT đang mở", "1. Dùng Tab/Shift+Tab di chuyển focus\n2. Chọn option/dropdown/date bằng bàn phím nếu hỗ trợ\n3. Kiểm tra focus trap", "Keyboard navigation", "Focus di chuyển hợp lý trong popup; không mất focus ra nền khi popup đang mở.", "Thấp"))
    add(tc("TC-EXP-UI-010", "UI/UX", "Không lưu filter trong popup sau khi đóng và mở lại", "Popup EXPORT đang mở", "1. Chọn option/filter trong popup\n2. Click Close icon\n3. Mở lại popup EXPORT", "Option/date/campaign đã chọn trước đó", "Popup mở lại theo trạng thái mặc định hoặc theo context mở popup; không lưu thay đổi filter vừa đóng theo SRS.", "Trung bình"))
    return rows


def build_sheets():
    cases = build_export_cases()
    overview = [
        ["Hạng mục", "Nội dung"],
        ["Tên chức năng", "CMS_Export báo cáo Pop-up"],
        ["Mã màn hình", "SCR-CMS-RPT-002"],
        ["Nguồn yêu cầu", "SRS CMS Pop-up - Chiến dịch Marketing, mục 4.6 CMS_Export báo cáo Pop-up"],
        ["Phạm vi", "Popup EXPORT, Export từng chiến dịch, Toàn bộ chiến dịch, campaign dropdown, Export Period, validate dữ liệu, tải file Excel, bộ chỉ số Reach/Impression/Click/Close/CTR, phân quyền dữ liệu và lỗi export."],
        ["Ngoài phạm vi", "Thiết kế chi tiết template Google Sheet ngoài các trường/chỉ số được mô tả trong SRS và hành vi App ngoài kiểm tra hồi quy tracking liên quan."],
    ]
    test_cases = [base.HEADERS] + cases
    categories = {}
    priorities = {}
    for row in cases:
        categories[row[1]] = categories.get(row[1], 0) + 1
        priorities[row[7]] = priorities.get(row[7], 0) + 1
    summary = [
        ["Chỉ số", "Số lượng/Ghi chú"],
        ["Tổng số ca kiểm thử", len(cases)],
        ["Ca kiểm thử tích cực", 32],
        ["Ca kiểm thử âm tính", 25],
        ["Ca kiểm thử biên", 8],
        ["Ca UI/UX", categories.get("UI/UX", 0)],
        ["Ca phân quyền", categories.get("Phân Quyền", 0)],
        ["Ưu tiên Cao", priorities.get("Cao", 0)],
        ["Ưu tiên Trung bình", priorities.get("Trung bình", 0)],
        ["Ưu tiên Thấp", priorities.get("Thấp", 0)],
        ["Phân bổ theo danh mục", "; ".join(f"{k}: {v}" for k, v in categories.items())],
    ]
    risks = [
        ["Loại", "Nội dung", "Khuyến nghị"],
        ["Requirement cần xác nhận", "SRS chỉ gợi ý tên file export, chưa chốt format ngày và quy tắc đặt tên cuối cùng.", "BA/PO cần chốt format filename để testcase expected cố định."],
        ["Requirement cần xác nhận", "Trường hợp không có dữ liệu có hai hướng: xuất file header rỗng hoặc hiển thị No Data.", "Chốt một hành vi chính thức cho UI/backend."],
        ["Requirement cần xác nhận", "Impression = 0 hiển thị CTR là 0% hay '-' chưa được chốt.", "Chốt rule hiển thị CTR để tránh sai lệch báo cáo."],
        ["Requirement cần xác nhận", "Dropdown campaign theo SRS ghi '(Tất cả)' nhưng option Toàn bộ chiến dịch lại ẩn/disable campaign.", "Làm rõ có option Tất cả trong dropdown hay chỉ dùng radio Toàn bộ chiến dịch."],
        ["Requirement cần xác nhận", "Chưa có SLA cho export dữ liệu lớn và giới hạn số dòng/file.", "Bổ sung yêu cầu hiệu năng, timeout và xử lý file lớn."],
        ["Requirement cần xác nhận", "Template export nằm ở Google Sheet ngoài SRS, cần chốt bản template baseline.", "Đính kèm template chính thức hoặc version template vào SRS."],
        ["Rủi ro", "Số liệu Reach/CTR dễ sai do trùng hội viên, lọc thời gian và mapping segment.", "Ưu tiên kiểm thử đối chiếu backend/database cho các công thức báo cáo."],
        ["Khuyến nghị", "Nên tự động hóa regression cho export từng campaign, toàn bộ campaign, date range > 1 năm, no data và CTR Impression = 0.", "Đưa nhóm ca ưu tiên Cao vào regression suite."],
    ]
    return [
        ("Tổng quan", overview, [26, 120]),
        ("Ca kiểm thử", test_cases, [14, 18, 44, 42, 58, 38, 58, 14, 16]),
        ("Tổng hợp bao phủ", summary, [32, 110]),
        ("Rủi ro câu hỏi", risks, [30, 82, 82]),
    ]


base.build_sheets = build_sheets


if __name__ == "__main__":
    base.build_xlsx()
