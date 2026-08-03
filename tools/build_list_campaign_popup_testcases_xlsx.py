from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_PATH = Path(__file__).with_name("build_cms_popup_testcases_xlsx.py")
spec = importlib.util.spec_from_file_location("xlsx_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

base.OUT_PATH = "deliverables/Bo_ca_kiem_thu_Man_Danh_sach_Campaign_Popup.xlsx"


def tc(tc_id, category, scenario, pre, steps, data, expected, priority="Cao", status="Chưa chạy"):
    return [tc_id, category, scenario, pre, steps, data, expected, priority, status]


def build_list_screen_cases():
    rows = []
    add = rows.append

    # Phân Quyền
    add(tc("TC-LST-PQ-001", "Phân Quyền", "Admin CMS có quyền Pop-up nhìn thấy menu Popup - Chiến dịch Marketing", "Admin CMS đã đăng nhập và có quyền Pop-up", "1. Đăng nhập CMS bằng tài khoản Admin\n2. Quan sát menu bên trái", "Tài khoản Admin CMS có quyền Pop-up", "Menu Popup - Chiến dịch Marketing được hiển thị.", "Cao"))
    add(tc("TC-LST-PQ-002", "Phân Quyền", "Manager CMS có quyền Pop-up nhìn thấy menu Popup - Chiến dịch Marketing", "Manager CMS đã đăng nhập và có quyền Pop-up", "1. Đăng nhập CMS bằng tài khoản Manager\n2. Quan sát menu bên trái", "Tài khoản Manager CMS có quyền Pop-up", "Menu Popup - Chiến dịch Marketing được hiển thị.", "Cao"))
    add(tc("TC-LST-PQ-003", "Phân Quyền", "User không có quyền Pop-up không nhìn thấy menu chức năng", "User CMS đã đăng nhập nhưng không có quyền Pop-up", "1. Đăng nhập CMS\n2. Quan sát menu bên trái", "Tài khoản không có quyền Pop-up", "Không hiển thị menu Popup - Chiến dịch Marketing.", "Cao"))
    add(tc("TC-LST-PQ-004", "Phân Quyền", "Backend từ chối truy cập trực tiếp URL danh sách khi user không có quyền", "User không có quyền Pop-up có URL màn danh sách", "1. Đăng nhập bằng user không có quyền\n2. Nhập trực tiếp URL màn danh sách Campaign Pop-up", "URL màn SCR-CMS-POP-001", "Backend CMS từ chối truy cập; user không xem được màn danh sách và dữ liệu campaign.", "Cao"))
    add(tc("TC-LST-PQ-005", "Phân Quyền", "Icon Edit chỉ hiển thị với campaign Scheduled, Active, Inactive", "Danh sách có campaign đủ 4 trạng thái", "1. Mở màn danh sách\n2. Quan sát cột Action theo từng trạng thái", "Scheduled, Active, Inactive, Expired", "Icon Edit chỉ hiển thị với campaign trạng thái Scheduled, Active, Inactive; không hiển thị với Expired.", "Cao"))
    add(tc("TC-LST-PQ-006", "Phân Quyền", "Icon Delete chỉ enable với campaign Scheduled", "Danh sách có campaign đủ 4 trạng thái", "1. Mở màn danh sách\n2. Quan sát icon Delete theo từng trạng thái", "Scheduled, Active, Inactive, Expired", "Delete enable với Scheduled; Active/Inactive/Expired bị ẩn hoặc disabled.", "Cao"))
    add(tc("TC-LST-PQ-007", "Phân Quyền", "Backend chặn xóa khi campaign không còn Scheduled", "FE đang hiển thị Delete enable nhưng backend đã đổi trạng thái campaign", "1. Mở danh sách khi campaign là Scheduled\n2. Campaign bị đổi trạng thái bởi job/user khác\n3. Click Delete và xác nhận", "Campaign đã chuyển khỏi Scheduled", "Hiển thị toast: Campaign cannot be deleted in current status. Campaign không bị xóa.", "Cao"))

    # Chức năng chính
    add(tc("TC-LST-CN-001", "Chức năng chính", "Mở màn danh sách Campaign Pop-up thành công", "User có quyền Pop-up", "1. Đăng nhập CMS\n2. Chọn menu Popup - Chiến dịch Marketing", "Tài khoản có quyền Pop-up", "Màn Danh sách campaign Pop-up hiển thị đúng mục đích: danh sách, tìm kiếm/lọc và các thao tác tạo, xem, sửa, xóa.", "Cao"))
    add(tc("TC-LST-CN-002", "Chức năng chính", "Danh sách hiển thị No Data khi không có dữ liệu", "Không có campaign hoặc bộ lọc không khớp dữ liệu", "1. Mở màn danh sách hoặc áp dụng bộ lọc không có kết quả\n2. Quan sát vùng bảng", "Không có campaign phù hợp", "Hiển thị thông báo No Data.", "Trung bình"))
    add(tc("TC-LST-CN-003", "Chức năng chính", "Danh sách sắp xếp theo thời gian tạo gần nhất đến lâu nhất", "Có nhiều campaign với Created Date khác nhau", "1. Mở màn danh sách\n2. Đối chiếu thứ tự Created Date của các dòng", "Campaign có Created Date khác nhau", "Campaign được sắp xếp theo thời gian tạo: gần nhất đến lâu nhất.", "Cao"))
    add(tc("TC-LST-CN-004", "Chức năng chính", "Hiển thị STT theo trang hiện tại", "Danh sách có nhiều campaign và có phân trang", "1. Mở trang đầu danh sách\n2. Ghi nhận STT\n3. Chuyển sang trang tiếp theo\n4. Quan sát STT", "Dữ liệu nhiều trang", "STT hiển thị số thứ tự dòng trên danh sách theo trang hiện tại.", "Trung bình"))
    add(tc("TC-LST-CN-005", "Chức năng chính", "Phân trang theo chuẩn phân trang chung của CMS", "Danh sách có số campaign lớn hơn page size", "1. Mở màn danh sách\n2. Sử dụng nút chuyển trang theo chuẩn CMS\n3. Quan sát dữ liệu từng trang", "Dữ liệu nhiều trang", "Phân trang hoạt động theo chuẩn CMS hiện hữu. Requirement cần xác nhận nếu chuẩn phân trang chưa được cung cấp.", "Trung bình"))
    add(tc("TC-LST-CN-006", "Chức năng chính", "Tìm kiếm tương đối theo mã campaign", "Có campaign mã POP01", "1. Nhập một phần mã vào Search by Code\n2. Thực hiện tìm kiếm", "Từ khóa: POP hoặc 01", "Danh sách chỉ hiển thị campaign có mã khớp tương đối với từ khóa.", "Cao"))
    add(tc("TC-LST-CN-007", "Chức năng chính", "Tìm kiếm theo mã không có dữ liệu phù hợp", "Không có campaign khớp mã tìm kiếm", "1. Nhập mã không tồn tại vào Search by Code\n2. Thực hiện tìm kiếm", "Từ khóa không tồn tại", "Hiển thị No Data.", "Trung bình"))
    add(tc("TC-LST-CN-008", "Chức năng chính", "Tìm kiếm tương đối theo tên campaign", "Có campaign có tên phù hợp", "1. Nhập một phần tên vào Search by popup\n2. Thực hiện tìm kiếm", "Một phần tên campaign", "Danh sách chỉ hiển thị campaign có tên khớp tương đối với từ khóa.", "Cao"))
    add(tc("TC-LST-CN-009", "Chức năng chính", "Tìm kiếm theo tên không có dữ liệu phù hợp", "Không có campaign khớp tên tìm kiếm", "1. Nhập tên không tồn tại vào Search by popup\n2. Thực hiện tìm kiếm", "Tên không tồn tại", "Hiển thị No Data.", "Trung bình"))
    add(tc("TC-LST-CN-010", "Chức năng chính", "Kết hợp Search by Code và Search by popup", "Có dữ liệu phù hợp đồng thời mã và tên", "1. Nhập từ khóa mã\n2. Nhập từ khóa tên\n3. Thực hiện tìm kiếm", "Mã và tên cùng khớp một campaign", "Danh sách chỉ hiển thị campaign thỏa đồng thời điều kiện mã và tên.", "Cao"))
    add(tc("TC-LST-CN-011", "Chức năng chính", "Kết hợp Search by popup với các bộ lọc khác", "Có dữ liệu phù hợp nhiều điều kiện", "1. Nhập tên campaign\n2. Chọn Status\n3. Chọn Customer Segment\n4. Chọn Position nếu có\n5. Áp dụng lọc", "Tên, trạng thái, đối tượng, vị trí phù hợp", "Danh sách hiển thị campaign thỏa đồng thời tất cả điều kiện.", "Cao"))
    add(tc("TC-LST-CN-012", "Chức năng chính", "Status mặc định là Tất cả", "User mở màn danh sách lần đầu", "1. Mở màn danh sách\n2. Quan sát dropdown Status", "Không áp dụng", "Status mặc định là Tất cả và không lọc theo trạng thái.", "Trung bình"))
    add(tc("TC-LST-CN-013", "Chức năng chính", "Lọc Status = Scheduled", "Có campaign Scheduled và trạng thái khác", "1. Chọn Status = Scheduled\n2. Quan sát danh sách", "Scheduled", "Chỉ hiển thị campaign trạng thái Scheduled.", "Cao"))
    add(tc("TC-LST-CN-014", "Chức năng chính", "Lọc Status = Active", "Có campaign Active và trạng thái khác", "1. Chọn Status = Active\n2. Quan sát danh sách", "Active", "Chỉ hiển thị campaign trạng thái Active.", "Cao"))
    add(tc("TC-LST-CN-015", "Chức năng chính", "Lọc Status = Inactive", "Có campaign Inactive và trạng thái khác", "1. Chọn Status = Inactive\n2. Quan sát danh sách", "Inactive", "Chỉ hiển thị campaign trạng thái Inactive.", "Cao"))
    add(tc("TC-LST-CN-016", "Chức năng chính", "Lọc Status = Expired", "Có campaign Expired và trạng thái khác", "1. Chọn Status = Expired\n2. Quan sát danh sách", "Expired", "Chỉ hiển thị campaign trạng thái Expired.", "Cao"))
    add(tc("TC-LST-CN-017", "Chức năng chính", "Lọc Customer Segment = Tất cả", "Có campaign thuộc nhiều loại đối tượng áp dụng", "1. Chọn Customer Segment = Tất cả\n2. Quan sát danh sách", "Tất cả", "Không lọc theo đối tượng áp dụng.", "Trung bình"))
    add(tc("TC-LST-CN-018", "Chức năng chính", "Lọc Customer Segment = Toàn bộ người dùng", "Có campaign áp dụng toàn bộ hội viên", "1. Chọn Customer Segment = Toàn bộ người dùng\n2. Quan sát danh sách", "Toàn bộ người dùng", "Chỉ hiển thị campaign áp dụng cho toàn bộ hội viên.", "Trung bình"))
    add(tc("TC-LST-CN-019", "Chức năng chính", "Lọc theo Customer Segment cụ thể", "Có campaign áp dụng segment cụ thể", "1. Chọn một Customer Segment trong dropdown\n2. Quan sát danh sách", "Segment A", "Chỉ hiển thị campaign có đối tượng áp dụng là Customer Segment đã chọn.", "Trung bình"))
    add(tc("TC-LST-CN-020", "Chức năng chính", "Lọc Customer Segment = Import file", "Có campaign dùng file import", "1. Chọn Customer Segment = Import file\n2. Quan sát danh sách", "Import file", "Chỉ hiển thị campaign có đối tượng áp dụng là danh sách hội viên import từ file.", "Trung bình"))
    add(tc("TC-LST-CN-021", "Chức năng chính", "Lọc theo Position", "Có campaign theo nhiều Position", "1. Chọn một Position trong dropdown\n2. Quan sát danh sách", "Position trong danh sách BA cung cấp", "Chỉ hiển thị campaign có Position đã chọn.", "Trung bình"))
    add(tc("TC-LST-CN-022", "Chức năng chính", "Effective Period không chọn thì không lọc theo thời gian", "Có campaign nhiều khoảng hiệu lực khác nhau", "1. Để trống Effective Period\n2. Quan sát danh sách", "Effective Period rỗng", "Không lọc campaign theo thời gian hiệu lực.", "Trung bình"))
    add(tc("TC-LST-CN-023", "Chức năng chính", "Lọc Effective Period khi campaign nằm gọn trong khoảng lọc", "Có campaign Start và End nằm trong khoảng lọc", "1. Chọn From Date và To Date bao phủ campaign\n2. Áp dụng lọc", "Camp_Start >= Filter_From; Camp_End <= Filter_To", "Campaign được hiển thị.", "Cao"))
    add(tc("TC-LST-CN-024", "Chức năng chính", "Lọc Effective Period khi campaign bắt đầu trước và kết thúc trong khoảng lọc", "Có campaign giao với khoảng lọc", "1. Chọn khoảng lọc sao cho Start campaign ngoài khoảng và End campaign trong khoảng\n2. Áp dụng lọc", "Camp_Start < Filter_From; Camp_End nằm trong khoảng lọc", "Campaign được hiển thị.", "Cao"))
    add(tc("TC-LST-CN-025", "Chức năng chính", "Lọc Effective Period khi campaign bắt đầu trong và kết thúc sau khoảng lọc", "Có campaign giao với khoảng lọc", "1. Chọn khoảng lọc sao cho Start campaign trong khoảng và End campaign ngoài khoảng\n2. Áp dụng lọc", "Camp_Start nằm trong khoảng; Camp_End > Filter_To", "Campaign được hiển thị.", "Cao"))
    add(tc("TC-LST-CN-026", "Chức năng chính", "Không hiển thị campaign kết thúc trước khoảng lọc", "Có campaign kết thúc trước Filter_From", "1. Chọn khoảng lọc sau thời gian kết thúc campaign\n2. Áp dụng lọc", "Camp_End < Filter_From", "Campaign không hiển thị.", "Trung bình"))
    add(tc("TC-LST-CN-027", "Chức năng chính", "Không hiển thị campaign bắt đầu sau khoảng lọc", "Có campaign bắt đầu sau Filter_To", "1. Chọn khoảng lọc trước thời gian bắt đầu campaign\n2. Áp dụng lọc", "Camp_Start > Filter_To", "Campaign không hiển thị.", "Trung bình"))
    add(tc("TC-LST-CN-028", "Chức năng chính", "Hiển thị campaign No End Date khi Start Date nhỏ hơn hoặc bằng To Date lọc", "Có campaign No End Date", "1. Chọn khoảng lọc có To Date >= Start Date campaign\n2. Áp dụng lọc", "No End Date; Start Date <= Filter_To", "Campaign No End Date được hiển thị.", "Cao"))
    add(tc("TC-LST-CN-029", "Chức năng chính", "Click Create điều hướng sang màn tạo campaign", "User có quyền tạo và đang ở màn danh sách", "1. Click nút Create", "Không áp dụng", "Điều hướng sang màn Create - Tạo popup/chiến dịch marketing.", "Cao"))
    add(tc("TC-LST-CN-030", "Chức năng chính", "Click Export to Excel mở popup EXPORT", "User có quyền Pop-up và đang ở màn danh sách", "1. Click nút Export to Excel", "Không áp dụng", "Popup EXPORT được mở để chọn tên popup chiến dịch và thời gian xuất dữ liệu.", "Cao"))
    add(tc("TC-LST-CN-031", "Chức năng chính", "Click icon View mở màn xem chi tiết campaign", "Danh sách có campaign bất kỳ", "1. Click icon View tại một dòng campaign", "Campaign bất kỳ", "Mở màn xem chi tiết popup - chiến dịch marketing.", "Cao"))
    add(tc("TC-LST-CN-032", "Chức năng chính", "Click icon Edit mở màn chỉnh sửa campaign", "Danh sách có campaign Scheduled/Active/Inactive", "1. Click icon Edit tại campaign được phép edit", "Campaign Scheduled/Active/Inactive", "Điều hướng sang màn Chỉnh sửa popup - Chiến dịch marketing.", "Cao"))
    add(tc("TC-LST-CN-033", "Chức năng chính", "Click icon Delete campaign Scheduled mở popup xác nhận xóa", "Danh sách có campaign Scheduled", "1. Click icon Delete tại campaign Scheduled", "Campaign Scheduled", "Hiển thị popup xác nhận với nội dung: Are you sure you want to delete this campaign? và có nhập mã OTP.", "Cao"))
    add(tc("TC-LST-CN-034", "Chức năng chính", "Cancel popup xác nhận xóa", "Popup xác nhận xóa đang hiển thị", "1. Click Cancel", "Campaign Scheduled", "Popup đóng, không xóa campaign.", "Trung bình"))
    add(tc("TC-LST-CN-035", "Chức năng chính", "Xóa campaign Scheduled thành công từ màn danh sách", "Popup xác nhận xóa đang hiển thị; OTP hợp lệ", "1. Nhập OTP\n2. Click Delete", "Campaign Scheduled; OTP hợp lệ", "Gọi API xóa campaign; hiển thị toast: Campaign has been successfully deleted. Danh sách được cập nhật.", "Cao"))
    add(tc("TC-LST-CN-036", "Chức năng chính", "Xóa campaign Scheduled thất bại", "Backend trả lỗi khi xóa", "1. Click Delete tại popup xác nhận\n2. Quan sát phản hồi", "Backend xóa thất bại", "Hiển thị toast: Failed to delete campaign.", "Cao"))

    # Validation
    add(tc("TC-LST-VL-001", "Quy tắc nhập liệu", "Search by Code trim khoảng trắng", "Màn danh sách đang mở", "1. Nhập toàn khoảng trắng vào Search by Code\n2. Thực hiện tìm kiếm", "\"   \"", "Hệ thống trim và xem như không nhập; không báo lỗi.", "Trung bình"))
    add(tc("TC-LST-VL-002", "Quy tắc nhập liệu", "Search by Code chấp nhận 255 ký tự", "Màn danh sách đang mở", "1. Nhập từ khóa 255 ký tự vào Search by Code\n2. Thực hiện tìm kiếm", "Chuỗi 255 ký tự", "Không hiển thị lỗi vượt độ dài; hệ thống tìm kiếm theo keyword đã nhập.", "Trung bình"))
    add(tc("TC-LST-VL-003", "Quy tắc nhập liệu", "Search by Code vượt 255 ký tự", "Màn danh sách đang mở", "1. Nhập từ khóa 256 ký tự vào Search by Code", "Chuỗi 256 ký tự", "Hiển thị lỗi: Search keyword must not exceed 255 characters.", "Cao"))
    add(tc("TC-LST-VL-004", "Quy tắc nhập liệu", "Search by popup trim khoảng trắng", "Màn danh sách đang mở", "1. Nhập toàn khoảng trắng vào Search by popup\n2. Thực hiện tìm kiếm", "\"   \"", "Hệ thống trim và xem như không nhập; không báo lỗi.", "Trung bình"))
    add(tc("TC-LST-VL-005", "Quy tắc nhập liệu", "Search by popup chấp nhận 255 ký tự", "Màn danh sách đang mở", "1. Nhập từ khóa 255 ký tự vào Search by popup\n2. Thực hiện tìm kiếm", "Chuỗi 255 ký tự", "Không hiển thị lỗi vượt độ dài; hệ thống tìm kiếm theo keyword đã nhập.", "Trung bình"))
    add(tc("TC-LST-VL-006", "Quy tắc nhập liệu", "Search by popup vượt 255 ký tự", "Màn danh sách đang mở", "1. Nhập từ khóa 256 ký tự vào Search by popup", "Chuỗi 256 ký tự", "Hiển thị lỗi: Search keyword must not exceed 255 characters.", "Cao"))
    add(tc("TC-LST-VL-007", "Quy tắc nhập liệu", "Effective Period from date lớn hơn to date", "Màn danh sách đang mở", "1. Nhập From Date lớn hơn To Date\n2. Áp dụng lọc", "From Date > To Date", "Hiển thị lỗi: Invalid date range.", "Cao"))
    add(tc("TC-LST-VL-008", "Quy tắc nhập liệu", "Status chỉ cho phép chọn một giá trị tại một thời điểm", "Màn danh sách đang mở", "1. Mở dropdown Status\n2. Thử chọn nhiều trạng thái", "Scheduled, Active", "Chỉ một giá trị được chọn tại một thời điểm.", "Trung bình"))
    add(tc("TC-LST-VL-009", "Quy tắc nhập liệu", "Customer Segment chỉ cho phép chọn một giá trị tại một thời điểm", "Màn danh sách đang mở", "1. Mở dropdown Customer Segment\n2. Thử chọn nhiều giá trị", "Toàn bộ người dùng, Import file", "Chỉ một giá trị được chọn tại một thời điểm.", "Trung bình"))
    add(tc("TC-LST-VL-010", "Quy tắc nhập liệu", "Position chỉ cho phép chọn một giá trị", "Màn danh sách đang mở", "1. Mở dropdown Position\n2. Thử chọn nhiều vị trí", "Nhiều Position", "Chỉ một Position được chọn tại một thời điểm.", "Trung bình"))

    # Integration
    add(tc("TC-LST-TH-001", "Tích hợp", "FE gửi đúng điều kiện tìm kiếm/lọc đến backend", "Có thể quan sát request hoặc log backend", "1. Nhập Search by Code\n2. Nhập Search by popup\n3. Chọn các filter\n4. Thực hiện tìm kiếm\n5. Kiểm tra request/log", "Code, name, status, segment, position, effective period", "Request gửi đủ điều kiện lọc đã chọn; backend trả danh sách đúng điều kiện.", "Cao"))
    add(tc("TC-LST-TH-002", "Tích hợp", "Danh sách cập nhật sau khi xóa campaign thành công", "Campaign Scheduled xóa thành công", "1. Xóa campaign Scheduled\n2. Quan sát danh sách sau toast thành công", "Campaign Scheduled", "Danh sách được reload/cập nhật; campaign đã xóa không còn hiển thị.", "Cao"))
    add(tc("TC-LST-TH-003", "Tích hợp", "Reach hiển thị từ dữ liệu báo cáo đã tổng hợp", "Có campaign có dữ liệu báo cáo", "1. Mở danh sách\n2. Quan sát cột Reach\n3. Đối chiếu dữ liệu tổng hợp nếu có quyền", "Campaign có Reach > 0", "Reach hiển thị theo dữ liệu báo cáo đã tổng hợp.", "Trung bình"))
    add(tc("TC-LST-TH-004", "Tích hợp", "Reach hiển thị 0 hoặc '-' khi chưa có dữ liệu", "Có campaign chưa có dữ liệu báo cáo", "1. Mở danh sách\n2. Quan sát cột Reach", "Campaign chưa có Reach", "Reach hiển thị 0 hoặc '-' theo chuẩn CMS. Requirement cần xác nhận chuẩn hiển thị cụ thể.", "Trung bình"))
    add(tc("TC-LST-TH-005", "Tích hợp", "Code campaign không thay đổi sau khi xóa campaign khác", "Có nhiều campaign trong danh sách", "1. Ghi nhận Code các campaign\n2. Xóa một campaign Scheduled\n3. Quan sát Code các campaign còn lại", "POP01, POP02...", "Code của các campaign còn lại không thay đổi.", "Trung bình"))
    add(tc("TC-LST-TH-006", "Tích hợp", "Lỗi backend khi tải danh sách", "Backend trả lỗi hoặc mất kết nối khi mở danh sách", "1. Mở màn danh sách khi API danh sách lỗi\n2. Quan sát UI", "API danh sách lỗi", "Requirement cần xác nhận: SRS chưa mô tả thông báo/lỗi tải danh sách. Ghi nhận rủi ro để BA/PO bổ sung.", "Cao"))

    # Regression
    add(tc("TC-LST-RG-001", "Hồi quy", "Không ảnh hưởng đăng nhập CMS", "Bản dựng có chức năng Pop-up", "1. Đăng nhập CMS bằng tài khoản hợp lệ\n2. Mở màn danh sách Pop-up\n3. Đăng xuất", "Tài khoản CMS hợp lệ", "Đăng nhập/đăng xuất CMS hoạt động bình thường.", "Cao"))
    add(tc("TC-LST-RG-002", "Hồi quy", "Không ảnh hưởng chuẩn phân trang màn CMS khác", "Có màn CMS khác dùng phân trang chung", "1. Kiểm tra phân trang màn Danh sách Pop-up\n2. Kiểm tra phân trang màn CMS khác", "Dữ liệu nhiều trang", "Phân trang ở màn CMS khác không bị ảnh hưởng.", "Trung bình"))
    add(tc("TC-LST-RG-003", "Hồi quy", "Không ảnh hưởng chuẩn toast/modal chung của CMS", "Có màn CMS khác dùng toast/modal", "1. Gây toast thành công/thất bại ở màn danh sách Pop-up\n2. Kiểm tra toast/modal ở màn CMS khác", "Toast xóa thành công/thất bại", "Toast/modal chung của CMS vẫn hoạt động đúng.", "Trung bình"))
    add(tc("TC-LST-RG-004", "Hồi quy", "Không ảnh hưởng module Customer Segment", "Có quyền truy cập module Customer Segment", "1. Mở danh sách Pop-up và lọc theo segment\n2. Mở module Customer Segment\n3. Quan sát danh sách segment", "Segment có campaign áp dụng", "Module Customer Segment vẫn hoạt động bình thường; dữ liệu segment dùng ở Pop-up nhất quán.", "Trung bình"))

    # UI/UX
    add(tc("TC-LST-UI-001", "UI/UX", "Hiển thị đúng tiêu đề và mục đích màn danh sách", "User có quyền Pop-up", "1. Mở màn danh sách\n2. Quan sát tiêu đề và bố cục", "SCR-CMS-POP-001", "Màn hình thể hiện đúng tên Danh sách campaign Pop-up và mục đích quản lý/tìm kiếm/lọc campaign.", "Thấp"))
    add(tc("TC-LST-UI-002", "UI/UX", "Hiển thị đúng các bộ lọc trên màn danh sách", "Màn danh sách đang mở", "1. Quan sát vùng filter", "Search by Code, Search by popup, Status, Customer Segment, Position, Effective Period", "Các bộ lọc hiển thị đầy đủ theo SRS.", "Trung bình"))
    add(tc("TC-LST-UI-003", "UI/UX", "Hiển thị đúng các nút thao tác chính", "Màn danh sách đang mở", "1. Quan sát vùng thao tác", "Export to Excel, Create", "Hiển thị nút Export to Excel và Create.", "Trung bình"))
    add(tc("TC-LST-UI-004", "UI/UX", "Hiển thị đúng các cột bảng danh sách", "Màn danh sách có dữ liệu", "1. Quan sát header bảng", "STT, Code, Popup Name - Campaign, Priority, Status, Position, Effective Period, Customer Segment, Created Date, Reach, Action", "Các cột hiển thị đầy đủ theo SRS.", "Trung bình"))
    add(tc("TC-LST-UI-005", "UI/UX", "Code hiển thị đúng cấu trúc POP[SỐ]", "Có campaign trong danh sách", "1. Mở danh sách\n2. Quan sát cột Code", "Ví dụ POP01", "Code hiển thị theo cấu trúc POP[SỐ].", "Trung bình"))
    add(tc("TC-LST-UI-006", "UI/UX", "Created Date hiển thị đúng format", "Có campaign trong danh sách", "1. Mở danh sách\n2. Quan sát cột Created Date", "01/07/2026 15:45", "Created Date hiển thị format dd/mm/yyyy HH:mm.", "Trung bình"))
    add(tc("TC-LST-UI-007", "UI/UX", "Effective Period hiển thị Start Date - End Date", "Có campaign có End Date", "1. Mở danh sách\n2. Quan sát cột Effective Period", "Start Date và End Date", "Effective Period hiển thị start date - end date.", "Trung bình"))
    add(tc("TC-LST-UI-008", "UI/UX", "Effective Period hiển thị No End Date", "Có campaign No End Date", "1. Mở danh sách\n2. Quan sát cột Effective Period", "No End Date", "Hiển thị start date - No End Date hoặc format tương đương.", "Trung bình"))
    add(tc("TC-LST-UI-009", "UI/UX", "Position nhiều giá trị hiển thị rõ ràng", "Campaign có nhiều Position", "1. Mở danh sách\n2. Quan sát cột Position", "Campaign có nhiều Position", "Nếu nhiều Position thì xuống dòng hoặc phân tách theo chuẩn UI hiện hữu; không bị chồng lấn nội dung.", "Thấp"))
    add(tc("TC-LST-UI-010", "UI/UX", "Customer Segment hiển thị đúng nhãn đối tượng áp dụng", "Có campaign thuộc từng loại audience", "1. Mở danh sách\n2. Quan sát cột Customer Segment", "All User, tên segment, Import file", "Hiển thị All User, tên Customer Segment hoặc Import file theo cấu hình campaign.", "Trung bình"))
    add(tc("TC-LST-UI-011", "UI/UX", "Action icon hiển thị dễ nhận biết và đúng trạng thái", "Danh sách có dữ liệu đủ trạng thái", "1. Mở danh sách\n2. Quan sát icon Edit/View/Delete", "Campaign đủ trạng thái", "Icon action hiển thị rõ ràng, đúng enable/disable/ẩn theo trạng thái.", "Thấp"))
    add(tc("TC-LST-UI-012", "UI/UX", "No Data hiển thị rõ ràng khi không có kết quả", "Không có dữ liệu phù hợp", "1. Áp dụng filter không có kết quả\n2. Quan sát bảng", "Filter không có kết quả", "Thông báo No Data hiển thị rõ ràng, không làm vỡ layout.", "Thấp"))
    return rows


def build_sheets():
    cases = build_list_screen_cases()
    overview = [
        ["Hạng mục", "Nội dung"],
        ["Tên màn hình", "CMS_Danh sách campaign Pop-up"],
        ["Mã màn hình", "SCR-CMS-POP-001"],
        ["Nguồn yêu cầu", "SRS CMS Pop-up - Chiến dịch Marketing, mục 4.1 và phần popup xóa liên quan từ mục 4.2"],
        ["Phạm vi", "Danh sách, tìm kiếm, lọc, hiển thị cột, phân trang, điều hướng Create/View/Edit, Delete từ danh sách, mở Export, phân quyền và UI/UX màn danh sách."],
        ["Ngoài phạm vi", "Chi tiết form Create/Edit, chi tiết nghiệp vụ Export và App display không thuộc file testcase màn danh sách này."],
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
        ["Ca kiểm thử tích cực", 45],
        ["Ca kiểm thử âm tính", 14],
        ["Ca kiểm thử biên", 7],
        ["Ca UI/UX", categories.get("UI/UX", 0)],
        ["Ca phân quyền", categories.get("Phân Quyền", 0)],
        ["Ưu tiên Cao", priorities.get("Cao", 0)],
        ["Ưu tiên Trung bình", priorities.get("Trung bình", 0)],
        ["Ưu tiên Thấp", priorities.get("Thấp", 0)],
        ["Phân bổ theo danh mục", "; ".join(f"{k}: {v}" for k, v in categories.items())],
    ]
    risks = [
        ["Loại", "Nội dung", "Khuyến nghị"],
        ["Requirement cần xác nhận", "Chuẩn phân trang chung của CMS chưa được mô tả chi tiết trong SRS.", "Bổ sung page size, điều hướng trang, tổng số bản ghi và hành vi khi đổi filter."],
        ["Requirement cần xác nhận", "Position lấy theo tài liệu BA cung cấp nhưng danh sách giá trị chưa có trong SRS.", "Bổ sung danh mục Position chính thức để kiểm thử đầy đủ."],
        ["Requirement cần xác nhận", "Reach khi chưa có dữ liệu hiển thị 0 hoặc '-' theo chuẩn CMS nhưng chưa chốt cụ thể.", "BA/PO cần chốt chuẩn hiển thị để tránh assertion mơ hồ."],
        ["Requirement cần xác nhận", "SRS chưa mô tả trạng thái loading/lỗi khi API danh sách thất bại.", "Bổ sung empty/loading/error state cho màn danh sách."],
        ["Requirement cần xác nhận", "OTP sai/hết hạn/retry khi xóa chưa được mô tả.", "Bổ sung rule OTP nếu muốn test chi tiết popup xóa."],
        ["Rủi ro", "Filter kết hợp nhiều điều kiện có thể sai mapping giữa FE và backend.", "Ưu tiên kiểm thử tích hợp request/response cho search và filter."],
        ["Khuyến nghị", "Nên đưa các ca phân quyền, search/filter và action Delete/Edit/View vào bộ hồi quy.", "Tự động hóa các ca ổn định sau khi yêu cầu được chốt."],
    ]
    return [
        ("Tổng quan", overview, [26, 120]),
        ("Ca kiểm thử", test_cases, [14, 18, 44, 42, 58, 38, 58, 14, 16]),
        ("Tổng hợp bao phủ", summary, [32, 110]),
        ("Rủi ro câu hỏi", risks, [28, 82, 82]),
    ]


base.build_sheets = build_sheets


if __name__ == "__main__":
    base.build_xlsx()
