from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_PATH = Path(__file__).with_name("build_cms_popup_testcases_xlsx.py")
spec = importlib.util.spec_from_file_location("xlsx_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

base.OUT_PATH = "deliverables/Bo_ca_kiem_thu_Chinh_sua_Campaign_Popup.xlsx"


def tc(tc_id, category, scenario, pre, steps, data, expected, priority="Cao", status="Chưa chạy"):
    return [tc_id, category, scenario, pre, steps, data, expected, priority, status]


def build_edit_cases():
    rows = []
    add = rows.append

    # Phân Quyền
    add(tc("TC-EDT-PQ-001", "Phân Quyền", "User có quyền Pop-up mở được màn chỉnh sửa campaign Scheduled", "User có quyền Pop-up; có campaign Scheduled", "1. Mở danh sách campaign\n2. Click icon Edit tại campaign Scheduled", "Campaign trạng thái Scheduled", "Điều hướng đến màn Chỉnh sửa campaign Pop-up SCR-CMS-POP-003.", "Cao"))
    add(tc("TC-EDT-PQ-002", "Phân Quyền", "User có quyền Pop-up mở được màn chỉnh sửa campaign Active", "User có quyền Pop-up; có campaign Active", "1. Mở danh sách campaign\n2. Click icon Edit tại campaign Active", "Campaign trạng thái Active", "Điều hướng đến màn Chỉnh sửa campaign Pop-up.", "Cao"))
    add(tc("TC-EDT-PQ-003", "Phân Quyền", "User có quyền Pop-up mở được màn chỉnh sửa campaign Inactive", "User có quyền Pop-up; có campaign Inactive", "1. Mở danh sách campaign\n2. Click icon Edit tại campaign Inactive", "Campaign trạng thái Inactive", "Điều hướng đến màn Chỉnh sửa campaign Pop-up.", "Cao"))
    add(tc("TC-EDT-PQ-004", "Phân Quyền", "Không cho chỉnh sửa campaign Expired", "Có campaign Expired", "1. Mở danh sách campaign\n2. Quan sát icon Edit hoặc truy cập URL edit của campaign Expired", "Campaign trạng thái Expired", "Icon Edit không hiển thị/không enable; nếu truy cập trực tiếp thì màn chỉ xem, toàn bộ field read-only/disabled và không cho lưu.", "Cao"))
    add(tc("TC-EDT-PQ-005", "Phân Quyền", "User không có quyền Pop-up không truy cập được màn Edit qua URL trực tiếp", "User không có quyền Pop-up", "1. Đăng nhập CMS bằng user không có quyền\n2. Nhập URL màn Edit campaign", "URL Edit campaign", "Backend CMS từ chối truy cập; user không xem/sửa được campaign.", "Cao"))
    add(tc("TC-EDT-PQ-006", "Phân Quyền", "Nút Save chỉ enable khi có thay đổi hợp lệ trên field được phép sửa", "User có quyền edit; mở màn Edit", "1. Mở màn Edit\n2. Không thay đổi dữ liệu\n3. Quan sát Save\n4. Thay đổi field được phép bằng giá trị hợp lệ\n5. Quan sát Save", "Campaign Scheduled/Active/Inactive", "Save không enable khi chưa có thay đổi; Save enable khi có thay đổi hợp lệ trên field được phép sửa.", "Cao"))
    add(tc("TC-EDT-PQ-007", "Phân Quyền", "Không cho submit thay đổi field bị disabled bằng thao tác bất thường", "Mở màn Edit Active/Inactive có field disabled", "1. Dùng devtool/API client cố gửi thay đổi field không được phép\n2. Gửi request cập nhật", "Field không được phép sửa theo trạng thái", "Backend từ chối hoặc bỏ qua thay đổi trái phép. Requirement cần xác nhận mã lỗi/thông báo cụ thể.", "Cao"))

    # Chức năng chính
    add(tc("TC-EDT-CN-001", "Chức năng chính", "Mở màn Edit hiển thị dữ liệu campaign hiện tại", "Có campaign bất kỳ được phép edit", "1. Mở màn Edit\n2. Đối chiếu dữ liệu với màn danh sách/chi tiết", "Campaign Scheduled/Active/Inactive", "Màn Edit hiển thị đúng dữ liệu campaign hiện tại.", "Cao"))
    add(tc("TC-EDT-CN-002", "Chức năng chính", "Scheduled campaign cho phép chỉnh sửa đầy đủ field", "Có campaign Scheduled; user có quyền", "1. Mở Edit campaign Scheduled\n2. Quan sát trạng thái enable/disable của các field", "Campaign Scheduled", "Toàn bộ field theo màn Create được phép chỉnh sửa nếu actor có quyền.", "Cao"))
    add(tc("TC-EDT-CN-003", "Chức năng chính", "Lưu thành công campaign Scheduled sau khi sửa đầy đủ field", "Campaign Scheduled; dữ liệu sửa hợp lệ", "1. Mở Edit Scheduled\n2. Sửa nhiều field hợp lệ\n3. Click Save\n4. Xác nhận OTP", "Dữ liệu hợp lệ theo rule Create", "Hiển thị popup confirm; sau khi xác nhận thành công hiển thị toast: Campaign has been successfully edited. Dữ liệu cập nhật đúng.", "Cao"))
    add(tc("TC-EDT-CN-004", "Chức năng chính", "Active campaign chỉ cho sửa đúng nhóm field được phép", "Có campaign Active", "1. Mở Edit campaign Active\n2. Quan sát các field enable", "Campaign Active", "Chỉ enable: Tên chiến dịch popup, Mô tả chiến dịch, Trạng thái Active sang Inactive, Ảnh popup, Nội dung hiển thị cùng popup. Các field khác disabled.", "Cao"))
    add(tc("TC-EDT-CN-005", "Chức năng chính", "Lưu thành công Active campaign khi sửa Tên chiến dịch", "Có campaign Active", "1. Mở Edit Active\n2. Sửa Tên chiến dịch hợp lệ\n3. Click Save và xác nhận OTP", "Tên mới hợp lệ", "Lưu thành công; toast: Campaign has been successfully edited.", "Cao"))
    add(tc("TC-EDT-CN-006", "Chức năng chính", "Lưu thành công Active campaign khi sửa Mô tả", "Có campaign Active", "1. Mở Edit Active\n2. Sửa Mô tả hợp lệ\n3. Click Save và xác nhận OTP", "Description mới hợp lệ", "Lưu thành công; mô tả được cập nhật.", "Trung bình"))
    add(tc("TC-EDT-CN-007", "Chức năng chính", "Đổi trạng thái Active sang Inactive", "Có campaign Active", "1. Mở Edit Active\n2. Đổi trạng thái từ Active sang Inactive\n3. Click Save và xác nhận OTP", "Status: Active -> Inactive", "Lưu thành công; campaign chuyển sang Inactive và không hiển thị trên App theo rule trạng thái.", "Cao"))
    add(tc("TC-EDT-CN-008", "Chức năng chính", "Lưu thành công Active campaign khi sửa ảnh popup", "Có campaign Active", "1. Mở Edit Active\n2. Upload ảnh JPG/PNG hợp lệ\n3. Click Save và xác nhận OTP", "Ảnh JPG/PNG <= 2MB, tỷ lệ 16:9", "Lưu thành công; ảnh popup được cập nhật.", "Cao"))
    add(tc("TC-EDT-CN-009", "Chức năng chính", "Lưu thành công Active campaign khi sửa nội dung hiển thị", "Có campaign Active", "1. Mở Edit Active\n2. Sửa No content displayed/Display content, Title, Content hợp lệ\n3. Click Save và xác nhận OTP", "Title/Content hợp lệ", "Lưu thành công; cấu hình nội dung popup được cập nhật.", "Cao"))
    add(tc("TC-EDT-CN-010", "Chức năng chính", "Active campaign không cho sửa Priority", "Có campaign Active", "1. Mở Edit Active\n2. Quan sát field Priority", "Campaign Active", "Priority disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-011", "Chức năng chính", "Active campaign không cho sửa thời gian hiệu lực", "Có campaign Active", "1. Mở Edit Active\n2. Quan sát Start Date, End Date, No End Date", "Campaign Active", "Các field thời gian hiệu lực disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-012", "Chức năng chính", "Active campaign không cho sửa điều hướng", "Có campaign Active", "1. Mở Edit Active\n2. Quan sát Loại điều hướng và Link điều hướng", "Campaign Active", "Các field điều hướng disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-013", "Chức năng chính", "Active campaign không cho sửa đối tượng áp dụng", "Có campaign Active", "1. Mở Edit Active\n2. Quan sát nhóm Đối tượng áp dụng", "Campaign Active", "Nhóm đối tượng áp dụng disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-014", "Chức năng chính", "Active campaign không cho sửa Position", "Có campaign Active", "1. Mở Edit Active\n2. Quan sát nhóm Position", "Campaign Active", "Position disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-015", "Chức năng chính", "Active campaign không cho sửa tần suất hiển thị", "Có campaign Active", "1. Mở Edit Active\n2. Quan sát Display Frequency", "Campaign Active", "Display Frequency disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-016", "Chức năng chính", "Inactive campaign chỉ cho sửa đúng nhóm field được phép", "Có campaign Inactive", "1. Mở Edit campaign Inactive\n2. Quan sát các field enable", "Campaign Inactive", "Chỉ enable: Tên chiến dịch, Mô tả, Priority, Trạng thái Inactive sang Active, Ảnh popup, Nội dung hiển thị, Loại điều hướng, Link điều hướng, Vị trí hiển thị. Field khác disabled.", "Cao"))
    add(tc("TC-EDT-CN-017", "Chức năng chính", "Đổi trạng thái Inactive sang Active", "Có campaign Inactive", "1. Mở Edit Inactive\n2. Đổi trạng thái từ Inactive sang Active\n3. Click Save và xác nhận OTP", "Status: Inactive -> Active", "Lưu thành công; campaign chuyển sang Active nếu backend chấp nhận.", "Cao"))
    add(tc("TC-EDT-CN-018", "Chức năng chính", "Lưu thành công Inactive campaign khi sửa Priority", "Có campaign Inactive", "1. Mở Edit Inactive\n2. Sửa Priority hợp lệ\n3. Click Save và xác nhận OTP", "Priority = 1", "Lưu thành công; Priority được cập nhật.", "Cao"))
    add(tc("TC-EDT-CN-019", "Chức năng chính", "Lưu thành công Inactive campaign khi sửa điều hướng", "Có campaign Inactive", "1. Mở Edit Inactive\n2. Sửa Loại điều hướng và Link điều hướng hợp lệ\n3. Click Save và xác nhận OTP", "Navigation type + Link hợp lệ", "Lưu thành công; thông tin điều hướng được cập nhật.", "Cao"))
    add(tc("TC-EDT-CN-020", "Chức năng chính", "Lưu thành công Inactive campaign khi sửa Position", "Có campaign Inactive", "1. Mở Edit Inactive\n2. Chọn lại một hoặc nhiều Position\n3. Click Save và xác nhận OTP", "Position mới", "Lưu thành công; Position được cập nhật.", "Cao"))
    add(tc("TC-EDT-CN-021", "Chức năng chính", "Inactive campaign không cho sửa thời gian hiệu lực", "Có campaign Inactive", "1. Mở Edit Inactive\n2. Quan sát Start Date, End Date, No End Date", "Campaign Inactive", "Các field thời gian hiệu lực disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-022", "Chức năng chính", "Inactive campaign không cho sửa đối tượng áp dụng", "Có campaign Inactive", "1. Mở Edit Inactive\n2. Quan sát nhóm Đối tượng áp dụng", "Campaign Inactive", "Nhóm đối tượng áp dụng disabled và không thể chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-CN-023", "Chức năng chính", "Expired campaign chỉ xem, không cho kích hoạt lại", "Có campaign Expired", "1. Mở màn Edit/View campaign Expired\n2. Quan sát field trạng thái và Save", "Campaign Expired", "Toàn bộ field read-only/disabled; không hiển thị/không enable Save; không cho kích hoạt lại trực tiếp campaign Expired.", "Cao"))
    add(tc("TC-EDT-CN-024", "Chức năng chính", "Click Save hiển thị popup confirm edit", "Màn Edit có thay đổi hợp lệ", "1. Sửa field hợp lệ\n2. Click Save", "Dữ liệu sửa hợp lệ", "Hiển thị popup confirm: Are you sure you want to edit the campiagn ? và có nhập mã OTP.", "Cao"))
    add(tc("TC-EDT-CN-025", "Chức năng chính", "Cancel popup confirm edit", "Popup confirm edit đang mở", "1. Click Cancel", "Không áp dụng", "Popup đóng; không lưu thay đổi.", "Cao"))
    add(tc("TC-EDT-CN-026", "Chức năng chính", "Yes popup confirm gọi API cập nhật", "Popup confirm edit đang mở; OTP hợp lệ", "1. Nhập OTP\n2. Click Yes", "OTP hợp lệ", "Gọi API cập nhật campaign.", "Cao"))
    add(tc("TC-EDT-CN-027", "Chức năng chính", "Cập nhật campaign thành công", "API cập nhật trả thành công", "1. Sửa field hợp lệ\n2. Save và xác nhận", "Dữ liệu sửa hợp lệ", "Hiển thị toast: Campaign has been successfully edited. Dữ liệu mới hiển thị sau khi quay lại danh sách/chi tiết.", "Cao"))
    add(tc("TC-EDT-CN-028", "Chức năng chính", "Cập nhật campaign thất bại", "API cập nhật trả lỗi", "1. Sửa field hợp lệ\n2. Save và xác nhận\n3. Backend trả lỗi", "Backend lỗi", "Hiển thị toast: Failed to edit campaign.", "Cao"))
    add(tc("TC-EDT-CN-029", "Chức năng chính", "Close màn Edit khi không có thay đổi", "Màn Edit mở, chưa chỉnh sửa", "1. Click Close", "Không có thay đổi", "Đóng màn Edit và quay về màn trước đó/danh sách campaign; không hiển thị confirm mất dữ liệu.", "Trung bình"))
    add(tc("TC-EDT-CN-030", "Chức năng chính", "Close màn Edit khi có thay đổi chưa lưu", "Màn Edit có dữ liệu đã chỉnh sửa", "1. Sửa một field\n2. Click Close", "Dữ liệu đã thay đổi", "Hiển thị confirm: Unsaved changes will be lost. Do you want to continue?", "Cao"))
    add(tc("TC-EDT-CN-031", "Chức năng chính", "Cancel confirm rời màn Edit", "Confirm rời màn đang mở", "1. Click Cancel", "Không áp dụng", "Confirm đóng; giữ nguyên màn Edit và dữ liệu đã chỉnh sửa.", "Trung bình"))
    add(tc("TC-EDT-CN-032", "Chức năng chính", "Yes/Continue confirm rời màn Edit", "Confirm rời màn đang mở", "1. Click Yes/Continue", "Dữ liệu chưa lưu", "Rời màn Edit; không lưu thay đổi.", "Trung bình"))

    # Validation
    add(tc("TC-EDT-VL-001", "Quy tắc nhập liệu", "Scheduled campaign validate toàn bộ rule như màn Create", "Campaign Scheduled", "1. Mở Edit Scheduled\n2. Nhập dữ liệu không hợp lệ ở nhiều field\n3. Click Save", "Dữ liệu vi phạm rule Create", "Hệ thống validate toàn bộ rule tương ứng như màn Create và hiển thị lỗi phù hợp.", "Cao"))
    add(tc("TC-EDT-VL-002", "Quy tắc nhập liệu", "Scheduled - Campaign Name rỗng", "Campaign Scheduled", "1. Xóa Campaign Name\n2. Click Save", "Campaign Name rỗng", "Hiển thị lỗi: Campaign name is required.", "Cao"))
    add(tc("TC-EDT-VL-003", "Quy tắc nhập liệu", "Scheduled - Campaign Name vượt 255 ký tự", "Campaign Scheduled", "1. Nhập Campaign Name 256 ký tự\n2. Click Save", "Chuỗi 256 ký tự", "Hiển thị lỗi: Campaign name must not exceed 255 characters.", "Cao"))
    add(tc("TC-EDT-VL-004", "Quy tắc nhập liệu", "Scheduled - Priority không phải số nguyên dương", "Campaign Scheduled", "1. Nhập Priority = 0, -1, 1.5, abc\n2. Click Save", "0, -1, 1.5, abc", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-EDT-VL-005", "Quy tắc nhập liệu", "Scheduled - Start Date nhỏ hơn current time", "Campaign Scheduled", "1. Nhập Start Date trong quá khứ\n2. Click Save", "Start Date < current time", "Hiển thị lỗi: Start date must be greater than or equal to current time.", "Cao"))
    add(tc("TC-EDT-VL-006", "Quy tắc nhập liệu", "Scheduled - End Date nhỏ hơn Start Date", "Campaign Scheduled", "1. Nhập End Date < Start Date\n2. Click Save", "End Date < Start Date", "Hiển thị lỗi: End date must be greater than or equal to start date.", "Cao"))
    add(tc("TC-EDT-VL-007", "Quy tắc nhập liệu", "Scheduled - Popup image sai định dạng", "Campaign Scheduled", "1. Upload file không phải JPG/PNG\n2. Click Save", "GIF/PDF", "Hiển thị lỗi: Invalid image format.", "Cao"))
    add(tc("TC-EDT-VL-008", "Quy tắc nhập liệu", "Scheduled - Popup image vượt 2MB", "Campaign Scheduled", "1. Upload ảnh > 2MB\n2. Click Save", "Ảnh 2.1MB", "Hiển thị lỗi: Image size must not exceed 2MB.", "Cao"))
    add(tc("TC-EDT-VL-009", "Quy tắc nhập liệu", "Scheduled - Title bắt buộc khi Display content", "Campaign Scheduled; Display content được chọn", "1. Xóa Title\n2. Click Save", "Title rỗng", "Hiển thị lỗi: Title is required.", "Cao"))
    add(tc("TC-EDT-VL-010", "Quy tắc nhập liệu", "Scheduled - Content bắt buộc khi Display content", "Campaign Scheduled; Display content được chọn", "1. Xóa Content\n2. Click Save", "Content rỗng", "Hiển thị lỗi: Content is required.", "Cao"))
    add(tc("TC-EDT-VL-011", "Quy tắc nhập liệu", "Scheduled - Link có nhập nhưng thiếu Loại điều hướng", "Campaign Scheduled", "1. Nhập Link điều hướng\n2. Xóa Loại điều hướng\n3. Click Save", "Link có giá trị; Navigation type rỗng", "Hiển thị lỗi: Navigation type is required.", "Cao"))
    add(tc("TC-EDT-VL-012", "Quy tắc nhập liệu", "Scheduled - Loại điều hướng có chọn nhưng thiếu Link", "Campaign Scheduled", "1. Chọn Loại điều hướng\n2. Xóa Link điều hướng\n3. Click Save", "Navigation type có giá trị; Link rỗng", "Hiển thị lỗi: Navigation link is required.", "Cao"))
    add(tc("TC-EDT-VL-013", "Quy tắc nhập liệu", "Scheduled - không chọn đối tượng áp dụng", "Campaign Scheduled", "1. Bỏ chọn audience nếu UI cho phép\n2. Click Save", "Audience rỗng", "Hiển thị lỗi: Please select audience.", "Cao"))
    add(tc("TC-EDT-VL-014", "Quy tắc nhập liệu", "Scheduled - Customer Segment nhưng chưa chọn segment", "Campaign Scheduled", "1. Chọn Customer Segment\n2. Không chọn segment\n3. Click Save", "Segment rỗng", "Hiển thị lỗi: Please select one Customer Segment.", "Cao"))
    add(tc("TC-EDT-VL-015", "Quy tắc nhập liệu", "Scheduled - Import file nhưng chưa upload file", "Campaign Scheduled", "1. Chọn Import file\n2. Không upload file\n3. Click Save", "File import rỗng", "Hiển thị lỗi: Please upload member file.", "Cao"))
    add(tc("TC-EDT-VL-016", "Quy tắc nhập liệu", "Scheduled - không chọn Position", "Campaign Scheduled", "1. Bỏ chọn toàn bộ Position\n2. Click Save", "Position rỗng", "Hiển thị lỗi: Please select at least one Position.", "Cao"))
    add(tc("TC-EDT-VL-017", "Quy tắc nhập liệu", "Scheduled - không chọn tần suất hiển thị", "Campaign Scheduled", "1. Bỏ chọn Display Frequency\n2. Click Save", "Frequency rỗng", "Hiển thị lỗi: Please select frequency type.", "Cao"))
    add(tc("TC-EDT-VL-018", "Quy tắc nhập liệu", "Scheduled - X lần/ngày không hợp lệ", "Campaign Scheduled chọn X lần/ngày", "1. Nhập X = 0, 50, 1.5 hoặc chữ\n2. Click Save", "0, 50, 1.5, abc", "Hiển thị lỗi: Frequency value must be an integer and less than 50.", "Cao"))
    add(tc("TC-EDT-VL-019", "Quy tắc nhập liệu", "Scheduled - X lần/tuần không chọn ngày", "Campaign Scheduled chọn X lần/tuần", "1. Nhập X\n2. Không chọn ngày trong tuần\n3. Click Save", "Không chọn T2-CN", "Hiển thị lỗi: Please select at least one day of week.", "Cao"))
    add(tc("TC-EDT-VL-020", "Quy tắc nhập liệu", "Active - Campaign Name rỗng", "Campaign Active", "1. Xóa Campaign Name\n2. Click Save", "Campaign Name rỗng", "Hiển thị lỗi: Campaign name is required.", "Cao"))
    add(tc("TC-EDT-VL-021", "Quy tắc nhập liệu", "Active - Campaign Name vượt 255 ký tự", "Campaign Active", "1. Nhập Campaign Name 256 ký tự\n2. Click Save", "Chuỗi 256 ký tự", "Hiển thị lỗi: Campaign name must not exceed 255 characters.", "Cao"))
    add(tc("TC-EDT-VL-022", "Quy tắc nhập liệu", "Active - Title vượt 225 ký tự khi sửa nội dung", "Campaign Active; Display content được chọn", "1. Nhập Title 226 ký tự\n2. Click Save", "Title 226 ký tự", "Hiển thị lỗi: Title must not exceed 225 characters.", "Cao"))
    add(tc("TC-EDT-VL-023", "Quy tắc nhập liệu", "Active - Content vượt 500 ký tự khi sửa nội dung", "Campaign Active; Display content được chọn", "1. Nhập Content 501 ký tự\n2. Click Save", "Content 501 ký tự", "Hiển thị lỗi: Description must not exceed 500 characters.", "Cao"))
    add(tc("TC-EDT-VL-024", "Quy tắc nhập liệu", "Active - upload ảnh sai định dạng", "Campaign Active", "1. Upload file không phải JPG/PNG\n2. Click Save", "GIF/PDF", "Hiển thị lỗi: Invalid image format.", "Cao"))
    add(tc("TC-EDT-VL-025", "Quy tắc nhập liệu", "Inactive - Priority không hợp lệ", "Campaign Inactive", "1. Nhập Priority = 0, -1, 1.5 hoặc chữ\n2. Click Save", "0, -1, 1.5, abc", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-EDT-VL-026", "Quy tắc nhập liệu", "Inactive - Link điều hướng vượt 1000 ký tự", "Campaign Inactive", "1. Nhập Link điều hướng 1001 ký tự\n2. Click Save", "Link 1001 ký tự", "Hiển thị lỗi: Link must not exceed 1000 characters.", "Cao"))
    add(tc("TC-EDT-VL-027", "Quy tắc nhập liệu", "Inactive - có Link nhưng thiếu Loại điều hướng", "Campaign Inactive", "1. Nhập Link\n2. Xóa Loại điều hướng\n3. Click Save", "Link có giá trị; type rỗng", "Hiển thị lỗi: Navigation type is required.", "Cao"))
    add(tc("TC-EDT-VL-028", "Quy tắc nhập liệu", "Inactive - có Loại điều hướng nhưng thiếu Link", "Campaign Inactive", "1. Chọn Loại điều hướng\n2. Xóa Link\n3. Click Save", "Type có giá trị; Link rỗng", "Hiển thị lỗi: Navigation link is required.", "Cao"))
    add(tc("TC-EDT-VL-029", "Quy tắc nhập liệu", "Inactive - bỏ chọn toàn bộ Position", "Campaign Inactive", "1. Bỏ chọn toàn bộ Position\n2. Click Save", "Position rỗng", "Hiển thị lỗi: Please select at least one Position.", "Cao"))

    # Tích hợp
    add(tc("TC-EDT-TH-001", "Tích hợp", "Backend trả lỗi trạng thái khi campaign đổi trạng thái trong lúc edit", "User đang mở màn Edit; campaign bị job/người khác đổi trạng thái", "1. Mở Edit campaign\n2. Thay đổi campaign bởi job/user khác\n3. Click Save", "Campaign chuyển trạng thái trong lúc edit", "Backend trả lỗi trạng thái và FE reload dữ liệu mới nhất.", "Cao"))
    add(tc("TC-EDT-TH-002", "Tích hợp", "FE gửi đúng field được phép sửa với Active campaign", "Có thể kiểm tra request/log", "1. Mở Edit Active\n2. Sửa field được phép\n3. Save\n4. Kiểm tra request", "Active campaign", "Request chỉ chứa/áp dụng các field được phép sửa; field disabled không bị cập nhật.", "Cao"))
    add(tc("TC-EDT-TH-003", "Tích hợp", "FE gửi đúng field được phép sửa với Inactive campaign", "Có thể kiểm tra request/log", "1. Mở Edit Inactive\n2. Sửa field được phép\n3. Save\n4. Kiểm tra request", "Inactive campaign", "Request chỉ chứa/áp dụng các field được phép sửa; field disabled không bị cập nhật.", "Cao"))
    add(tc("TC-EDT-TH-004", "Tích hợp", "Backend trả lỗi validate field xác định được", "Màn Edit submit dữ liệu", "1. Gửi dữ liệu khiến backend trả lỗi validate có field\n2. Quan sát UI", "Lỗi validate có field", "FE hiển thị lỗi tại field tương ứng nếu xác định được.", "Cao"))
    add(tc("TC-EDT-TH-005", "Tích hợp", "Backend trả lỗi chung không xác định field", "Màn Edit submit dữ liệu", "1. Gửi dữ liệu khiến backend trả lỗi chung\n2. Quan sát UI", "Lỗi không map field", "FE hiển thị toast: Failed to edit campaign.", "Cao"))
    add(tc("TC-EDT-TH-006", "Tích hợp", "Upload ảnh thất bại khi edit", "Màn Edit Active/Inactive/Scheduled cho phép sửa ảnh", "1. Upload ảnh hợp lệ\n2. Giả lập upload thất bại", "Ảnh hợp lệ; backend/storage lỗi", "Hiển thị lỗi: Failed to upload image.", "Cao"))
    add(tc("TC-EDT-TH-007", "Tích hợp", "Dữ liệu cập nhật phản ánh ở màn danh sách sau edit", "Cập nhật campaign thành công", "1. Sửa field hiển thị ở danh sách như tên/priority/status/position\n2. Lưu thành công\n3. Quay lại danh sách", "Dữ liệu sửa hợp lệ", "Danh sách hiển thị dữ liệu mới đúng với cập nhật.", "Cao"))

    # Hồi quy
    add(tc("TC-EDT-RG-001", "Hồi quy", "Không ảnh hưởng màn tạo campaign", "Sau khi triển khai chỉnh sửa campaign", "1. Mở màn Create\n2. Tạo campaign hợp lệ", "Dữ liệu tạo hợp lệ", "Màn Create vẫn hoạt động đúng rule hiện có.", "Cao"))
    add(tc("TC-EDT-RG-002", "Hồi quy", "Không ảnh hưởng màn danh sách campaign", "Sau khi edit campaign", "1. Edit campaign thành công\n2. Mở danh sách\n3. Tìm/lọc campaign vừa sửa", "Campaign vừa sửa", "Danh sách, search/filter và cột dữ liệu vẫn hoạt động đúng.", "Cao"))
    add(tc("TC-EDT-RG-003", "Hồi quy", "Không ảnh hưởng màn xem chi tiết campaign", "Sau khi edit campaign", "1. Edit campaign thành công\n2. Mở View chi tiết campaign", "Campaign vừa sửa", "Màn View hiển thị dữ liệu cập nhật và toàn bộ field read-only.", "Trung bình"))
    add(tc("TC-EDT-RG-004", "Hồi quy", "Không ảnh hưởng module Customer Segment", "Campaign có Customer Segment", "1. Edit campaign không được phép sửa audience ở Active/Inactive\n2. Mở module Segment", "Segment đang dùng", "Dữ liệu segment không bị thay đổi ngoài phạm vi.", "Trung bình"))
    add(tc("TC-EDT-RG-005", "Hồi quy", "Không ảnh hưởng chuẩn confirm/toast chung CMS", "Có màn CMS khác dùng confirm/toast", "1. Save edit thành công/thất bại\n2. Kiểm tra confirm/toast ở màn khác", "Toast success/error", "Confirm/toast chung vẫn hoạt động đúng.", "Trung bình"))

    # UI/UX
    add(tc("TC-EDT-UI-001", "UI/UX", "Hiển thị đúng tiêu đề và Screen ID màn Edit", "User mở màn Edit", "1. Mở màn Edit\n2. Quan sát tiêu đề/bố cục", "SCR-CMS-POP-003", "Màn hiển thị đúng Chỉnh sửa campaign Pop-up theo mockup.", "Thấp"))
    add(tc("TC-EDT-UI-002", "UI/UX", "Field không được phép sửa disabled rõ ràng", "Mở Edit Active/Inactive/Expired", "1. Mở từng trạng thái\n2. Quan sát field không được phép sửa", "Active/Inactive/Expired", "Các field không thuộc phạm vi được phép chỉnh sửa disabled ngay trên FE, không gây nhầm lẫn.", "Cao"))
    add(tc("TC-EDT-UI-003", "UI/UX", "Save button disabled khi không có thay đổi", "Màn Edit mở dữ liệu ban đầu", "1. Mở Edit\n2. Không thay đổi dữ liệu\n3. Quan sát Save", "Không thay đổi", "Save không enable.", "Trung bình"))
    add(tc("TC-EDT-UI-004", "UI/UX", "Save button enable khi có thay đổi hợp lệ", "Màn Edit có field được phép sửa", "1. Sửa field hợp lệ\n2. Quan sát Save", "Dữ liệu hợp lệ", "Save enable.", "Trung bình"))
    add(tc("TC-EDT-UI-005", "UI/UX", "Popup confirm edit hiển thị đúng nội dung", "Có thay đổi hợp lệ", "1. Click Save", "Không áp dụng", "Popup confirm hiển thị text: Are you sure you want to edit the campiagn ? và có nhập mã OTP. Lưu ý typo campiagn theo SRS.", "Trung bình"))
    add(tc("TC-EDT-UI-006", "UI/UX", "Button Close hiển thị trên màn Edit", "Màn Edit đang mở", "1. Quan sát khu vực button", "Không áp dụng", "Button Close hiển thị và có thể click.", "Thấp"))
    add(tc("TC-EDT-UI-007", "UI/UX", "Confirm rời màn hiển thị khi có dữ liệu chưa lưu", "Màn Edit đã thay đổi dữ liệu", "1. Click Close", "Dữ liệu chưa lưu", "Confirm hiển thị đúng text: Unsaved changes will be lost. Do you want to continue?", "Trung bình"))
    add(tc("TC-EDT-UI-008", "UI/UX", "Expired campaign không hiển thị Save", "Campaign Expired", "1. Mở Edit/View Expired\n2. Quan sát button Save", "Campaign Expired", "Không hiển thị hoặc không enable Save vì không có field nào được phép chỉnh sửa.", "Cao"))
    add(tc("TC-EDT-UI-009", "UI/UX", "Tooltip Priority vẫn hiển thị khi field Priority được phép sửa", "Campaign Scheduled hoặc Inactive", "1. Hover/click icon thông tin cạnh Priority", "Campaign Scheduled/Inactive", "Tooltip hiển thị: Smaller numbers take display priority.", "Thấp"))
    add(tc("TC-EDT-UI-010", "UI/UX", "Tooltip System Variables vẫn hiển thị khi nội dung được phép sửa", "Campaign Scheduled/Active/Inactive", "1. Hover/click icon thông tin cạnh Các biến hệ thống", "Campaign có quyền sửa nội dung", "Tooltip hiển thị: Click the system variables field to insert them into the content.", "Thấp"))
    return rows


def build_sheets():
    cases = build_edit_cases()
    overview = [
        ["Hạng mục", "Nội dung"],
        ["Tên màn hình", "CMS — Chỉnh sửa campaign Pop-up"],
        ["Mã màn hình", "SCR-CMS-POP-003"],
        ["Nguồn yêu cầu", "SRS CMS Pop-up - Chiến dịch Marketing, mục 4.4 CMS — Chỉnh sửa campaign Pop-up"],
        ["Phạm vi", "Mở màn Edit, field enable/disable theo trạng thái Scheduled/Active/Inactive/Expired, Save, confirm OTP, Close, validation các field được phép sửa, xử lý backend lỗi/trạng thái thay đổi."],
        ["Ngoài phạm vi", "Tạo mới campaign, xóa campaign, export báo cáo và hành vi App sau khi campaign hiển thị."],
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
        ["Ca kiểm thử tích cực", 44],
        ["Ca kiểm thử âm tính", 29],
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
        ["Requirement cần xác nhận", "Thông báo lỗi khi backend từ chối field không được phép sửa chưa được nêu rõ.", "BA/PO cần chốt message/mã lỗi cho unauthorized field update."],
        ["Requirement cần xác nhận", "OTP edit chưa có rule sai OTP, hết hạn, retry, resend.", "Bổ sung rule OTP để tạo ca kiểm thử chi tiết hơn."],
        ["Requirement cần xác nhận", "Text confirm edit trong SRS có typo 'campiagn'.", "Xác nhận giữ nguyên theo mockup hay sửa thành 'campaign'."],
        ["Requirement cần xác nhận", "Inactive đổi sang Active có cần re-check thời gian hiệu lực hiện tại hay không chưa rõ.", "Bổ sung rule backend khi kích hoạt lại Inactive."],
        ["Requirement cần xác nhận", "Expired campaign mở từ Edit hay chỉ View chưa hoàn toàn rõ.", "Chốt navigation/action cho Expired."],
        ["Rủi ro", "Field matrix theo trạng thái là vùng rủi ro cao, dễ sai enable/disable giữa FE và backend.", "Ưu tiên kiểm thử FE và API/log backend cho từng trạng thái."],
        ["Khuyến nghị", "Nên tự động hóa smoke/regression cho Save theo Scheduled/Active/Inactive và Expired read-only.", "Đưa nhóm ca ưu tiên Cao vào regression suite."],
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
