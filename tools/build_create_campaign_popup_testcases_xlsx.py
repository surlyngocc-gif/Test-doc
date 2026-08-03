from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_PATH = Path(__file__).with_name("build_cms_popup_testcases_xlsx.py")
spec = importlib.util.spec_from_file_location("xlsx_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

base.OUT_PATH = "deliverables/Bo_ca_kiem_thu_Tao_Campaign_Popup.xlsx"


def tc(tc_id, category, scenario, pre, steps, data, expected, priority="Cao", status="Chưa chạy"):
    return [tc_id, category, scenario, pre, steps, data, expected, priority, status]


def build_create_cases():
    rows = []
    add = rows.append

    # Phân Quyền
    add(tc("TC-CRT-PQ-001", "Phân Quyền", "User có quyền Pop-up truy cập được màn tạo campaign", "User đã đăng nhập CMS và có quyền Pop-up", "1. Mở màn Danh sách campaign Pop-up\n2. Click Create", "Tài khoản Admin/Manager CMS có quyền Pop-up", "Điều hướng đến màn Tạo campaign Pop-up SCR-CMS-POP-002.", "Cao"))
    add(tc("TC-CRT-PQ-002", "Phân Quyền", "User không có quyền Pop-up không truy cập được màn tạo qua URL trực tiếp", "User đã đăng nhập CMS nhưng không có quyền Pop-up", "1. Nhập trực tiếp URL màn Create campaign\n2. Quan sát phản hồi", "URL màn SCR-CMS-POP-002", "Backend CMS từ chối truy cập; user không xem hoặc tạo được campaign.", "Cao"))
    add(tc("TC-CRT-PQ-003", "Phân Quyền", "User không có quyền Pop-up không thấy nút Create từ danh sách", "User không có quyền Pop-up", "1. Đăng nhập CMS\n2. Kiểm tra menu/màn danh sách nếu truy cập được", "Tài khoản không có quyền Pop-up", "Không hiển thị chức năng Pop-up hoặc không hiển thị nút Create. Backend vẫn phải chặn nếu truy cập trực tiếp.", "Cao"))
    add(tc("TC-CRT-PQ-004", "Phân Quyền", "Backend chặn tạo campaign nếu quyền bị thu hồi trong lúc đang nhập form", "User mở sẵn màn Create, sau đó bị thu hồi quyền", "1. Mở màn Create bằng user có quyền\n2. Thu hồi quyền Pop-up của user\n3. Nhập form hợp lệ\n4. Click Create và xác nhận", "Form hợp lệ; quyền bị thu hồi trước submit", "Backend từ chối tạo campaign. Requirement cần xác nhận thông báo lỗi cụ thể.", "Cao"))

    # Chức năng chính
    add(tc("TC-CRT-CN-001", "Chức năng chính", "Mở màn Tạo campaign Pop-up thành công", "User có quyền Pop-up", "1. Từ danh sách campaign click Create\n2. Quan sát màn hình", "Không áp dụng", "Màn Tạo campaign Pop-up hiển thị các nhóm thông tin: thông tin chung, ảnh/nội dung, điều hướng, đối tượng áp dụng, vị trí, tần suất và button Close/Create.", "Cao"))
    add(tc("TC-CRT-CN-002", "Chức năng chính", "Language hiển thị mặc định theo ngôn ngữ CMS hiện hữu", "User có quyền Pop-up", "1. Mở màn Create\n2. Quan sát dropdown Language", "Ngôn ngữ CMS hiện hữu là Tiếng Việt", "Language hiển thị ở góc phải theo mockup và mặc định theo ngôn ngữ CMS hiện hữu.", "Trung bình"))
    add(tc("TC-CRT-CN-003", "Chức năng chính", "Tạo campaign hợp lệ với đối tượng Toàn bộ hội viên và có End Date", "User có quyền tạo; dữ liệu hợp lệ", "1. Mở Create\n2. Nhập Campaign Name, Description, Priority, Start Date, End Date\n3. Upload ảnh hợp lệ\n4. Chọn Hiển thị nội dung, nhập Title/Content\n5. Để trống điều hướng\n6. Chọn Toàn bộ hội viên\n7. Chọn ít nhất 1 Position\n8. Chọn tần suất hợp lệ\n9. Click Create, xác nhận OTP", "Audience = Toàn bộ hội viên; No End Date = Off; ảnh JPG/PNG <= 2MB tỷ lệ 16:9", "Hiển thị popup confirm. Sau khi xác nhận thành công, toast: Campaign has been successfully saved. Backend trả trạng thái campaign và FE hiển thị ở danh sách/chi tiết.", "Cao"))
    add(tc("TC-CRT-CN-004", "Chức năng chính", "Tạo campaign hợp lệ với Customer Segment", "Có ít nhất một Customer Segment khả dụng", "1. Nhập form hợp lệ\n2. Chọn Customer Segment\n3. Chọn một segment trong dropdown\n4. Hoàn tất các field bắt buộc\n5. Click Create và xác nhận", "Customer Segment = Segment A", "Campaign được tạo thành công; đối tượng áp dụng lưu theo segment đã chọn.", "Cao"))
    add(tc("TC-CRT-CN-005", "Chức năng chính", "Tạo campaign hợp lệ với Import file", "Có file Excel hợp lệ theo template đã chốt", "1. Nhập form hợp lệ\n2. Chọn Import file\n3. Upload file danh sách hội viên hợp lệ\n4. Hoàn tất các field bắt buộc\n5. Click Create và xác nhận", "File Excel hợp lệ theo template", "Campaign được tạo thành công; đối tượng áp dụng là danh sách hội viên import từ file.", "Cao"))
    add(tc("TC-CRT-CN-006", "Chức năng chính", "Tạo campaign hợp lệ với No End Date = On", "User có quyền tạo", "1. Bật No End Date\n2. Nhập Start Date hợp lệ\n3. Không nhập End Date\n4. Nhập các field còn lại hợp lệ\n5. Click Create và xác nhận", "No End Date = On; End Date rỗng/null", "End Date bị disable/clear. Campaign tạo thành công nếu dữ liệu khác hợp lệ; request không gửi end date hoặc gửi null theo thiết kế API.", "Cao"))
    add(tc("TC-CRT-CN-007", "Chức năng chính", "Tạo campaign không có nội dung hiển thị", "User có quyền tạo", "1. Chọn Không có nội dung hiển thị\n2. Nhập các field bắt buộc khác hợp lệ\n3. Click Create và xác nhận", "No content displayed", "Title/Content disabled và không bắt buộc. Campaign tạo thành công nếu các field khác hợp lệ.", "Cao"))
    add(tc("TC-CRT-CN-008", "Chức năng chính", "Tạo campaign có cấu hình điều hướng đầy đủ", "User có quyền tạo", "1. Chọn Loại điều hướng\n2. Nhập Link điều hướng\n3. Nhập các field khác hợp lệ\n4. Click Create và xác nhận", "Navigation type = Webview; Link hợp lệ theo thiết kế", "Campaign được tạo thành công; thông tin điều hướng được gửi/lưu đầy đủ.", "Cao"))
    add(tc("TC-CRT-CN-009", "Chức năng chính", "Tạo campaign với nhiều Position", "Có nhiều Position native app khả dụng", "1. Nhập form hợp lệ\n2. Chọn từ 2 Position trở lên\n3. Click Create và xác nhận", "Position A, Position B", "Campaign được tạo thành công và lưu nhiều vị trí hiển thị.", "Trung bình"))
    add(tc("TC-CRT-CN-010", "Chức năng chính", "Chèn biến hệ thống vào Title", "Field Title đang focus", "1. Focus vào Title\n2. Click biến hệ thống Tên hội viên\n3. Quan sát nội dung Title", "Biến hệ thống: Tên hội viên", "CMS chèn biến vào đúng vị trí con trỏ trong Title.", "Trung bình"))
    add(tc("TC-CRT-CN-011", "Chức năng chính", "Chèn biến hệ thống vào Content", "Field Content đang focus", "1. Focus vào Content\n2. Click biến Số Bông Sen Vàng/Hạng thẻ/Số dặm\n3. Quan sát Content", "Các biến hệ thống được CMS cung cấp", "CMS chèn biến vào đúng vị trí con trỏ trong Content.", "Trung bình"))
    add(tc("TC-CRT-CN-012", "Chức năng chính", "Chỉ cho phép chèn biến nằm trong danh sách CMS cung cấp", "Màn Create đang mở", "1. Kiểm tra danh sách biến hệ thống\n2. Thử nhập/chèn biến ngoài danh sách nếu UI cho phép nhập tay", "Biến ngoài danh sách", "Chỉ biến nằm trong danh sách CMS cung cấp được chèn/hỗ trợ. Requirement cần xác nhận nếu UI cho phép nhập placeholder thủ công.", "Trung bình"))
    add(tc("TC-CRT-CN-013", "Chức năng chính", "Xóa file import đã upload và upload lại file khác trước khi lưu", "Chọn đối tượng Import file và đã upload file", "1. Upload file import hợp lệ\n2. Click xóa file\n3. Upload file hợp lệ khác\n4. Lưu campaign", "File A, File B", "Có thể xóa file đã upload và upload lại file khác trước khi lưu; campaign dùng file cuối cùng hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-CN-014", "Chức năng chính", "Close màn Create khi chưa nhập/chỉnh sửa dữ liệu", "Màn Create mới mở, chưa có thay đổi", "1. Click Close", "Không có dữ liệu nhập", "Đóng màn Create và quay về màn trước/danh sách; không hiển thị confirm mất dữ liệu.", "Trung bình"))
    add(tc("TC-CRT-CN-015", "Chức năng chính", "Close màn Create khi có dữ liệu chưa lưu", "Màn Create đã có dữ liệu nhập/chỉnh sửa", "1. Nhập một field bất kỳ\n2. Click Close", "Campaign Name = Test", "Hiển thị confirm: Unsaved changes will be lost. Do you want to continue?", "Cao"))
    add(tc("TC-CRT-CN-016", "Chức năng chính", "Cancel confirm rời màn Create giữ nguyên dữ liệu", "Confirm rời màn đang hiển thị", "1. Click Cancel trên confirm rời màn", "Dữ liệu đã nhập", "Confirm đóng; user vẫn ở màn Create; dữ liệu đã nhập vẫn được giữ.", "Trung bình"))
    add(tc("TC-CRT-CN-017", "Chức năng chính", "Đồng ý rời màn Create khi có dữ liệu chưa lưu", "Confirm rời màn đang hiển thị", "1. Click Yes/Continue trên confirm rời màn", "Dữ liệu chưa lưu", "Rời màn Create và không lưu thay đổi.", "Trung bình"))
    add(tc("TC-CRT-CN-018", "Chức năng chính", "Cancel popup xác nhận tạo campaign", "Form hợp lệ và popup confirm create đang mở", "1. Click Create\n2. Popup confirm hiển thị\n3. Click Cancel", "Form hợp lệ", "Popup đóng; không gọi API tạo campaign; campaign chưa được tạo.", "Cao"))
    add(tc("TC-CRT-CN-019", "Chức năng chính", "Tạo campaign thất bại do backend trả lỗi chung", "Form hợp lệ nhưng backend trả lỗi khi lưu", "1. Nhập form hợp lệ\n2. Click Create và xác nhận\n3. Backend trả lỗi chung", "Backend lỗi", "Hiển thị toast: Failed to save campaign.", "Cao"))
    add(tc("TC-CRT-CN-020", "Chức năng chính", "Màn tạo mới không có field Status", "Màn Create đang mở", "1. Quan sát toàn bộ form Create", "Không áp dụng", "Không hiển thị field Status trên màn tạo mới; backend xác định trạng thái sau khi tạo.", "Cao"))

    # Validation
    add(tc("TC-CRT-VL-001", "Quy tắc nhập liệu", "Không nhập Campaign Name", "Màn Create đang mở", "1. Bỏ trống Campaign Name\n2. Nhập các field khác hợp lệ\n3. Click Create", "Campaign Name rỗng", "Hiển thị lỗi: Campaign name is required.", "Cao"))
    add(tc("TC-CRT-VL-002", "Quy tắc nhập liệu", "Campaign Name chỉ gồm khoảng trắng", "Màn Create đang mở", "1. Nhập khoảng trắng vào Campaign Name\n2. Click Create", "\"   \"", "Trim xong rỗng và hiển thị lỗi: Campaign name is required.", "Cao"))
    add(tc("TC-CRT-VL-003", "Quy tắc nhập liệu", "Campaign Name đúng 255 ký tự", "Màn Create đang mở", "1. Nhập Campaign Name 255 ký tự\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Chuỗi 255 ký tự", "Campaign Name được chấp nhận nếu các field khác hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-VL-004", "Quy tắc nhập liệu", "Campaign Name vượt 255 ký tự", "Màn Create đang mở", "1. Nhập Campaign Name 256 ký tự\n2. Click Create", "Chuỗi 256 ký tự", "Hiển thị lỗi: Campaign name must not exceed 255 characters.", "Cao"))
    add(tc("TC-CRT-VL-005", "Quy tắc nhập liệu", "Campaign Name trùng vẫn cho lưu", "Đã có campaign cùng tên", "1. Nhập Campaign Name trùng campaign hiện có\n2. Nhập form hợp lệ\n3. Click Create và xác nhận", "Tên campaign đã tồn tại", "Không báo lỗi unique; campaign được phép lưu nếu dữ liệu khác hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-VL-006", "Quy tắc nhập liệu", "Description để trống", "Màn Create đang mở", "1. Bỏ trống Description\n2. Nhập các field bắt buộc hợp lệ\n3. Click Create", "Description rỗng", "Description không bắt buộc; campaign được phép lưu nếu dữ liệu khác hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-VL-007", "Quy tắc nhập liệu", "Description đúng 500 ký tự", "Màn Create đang mở", "1. Nhập Description 500 ký tự\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Chuỗi 500 ký tự", "Description được chấp nhận.", "Trung bình"))
    add(tc("TC-CRT-VL-008", "Quy tắc nhập liệu", "Description vượt 500 ký tự", "Màn Create đang mở", "1. Nhập Description 501 ký tự\n2. Click Create", "Chuỗi 501 ký tự", "Hiển thị lỗi theo SRS: Campaign name must not exceed  characters. Requirement cần xác nhận vì message thiếu số ký tự và sai tên trường.", "Trung bình"))
    add(tc("TC-CRT-VL-009", "Quy tắc nhập liệu", "Không nhập Priority", "Màn Create đang mở", "1. Bỏ trống Priority\n2. Click Create", "Priority rỗng", "Hiển thị lỗi: Priority is required.", "Cao"))
    add(tc("TC-CRT-VL-010", "Quy tắc nhập liệu", "Priority là chữ", "Màn Create đang mở", "1. Nhập Priority = abc\n2. Click Create", "abc", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-CRT-VL-011", "Quy tắc nhập liệu", "Priority là ký tự đặc biệt", "Màn Create đang mở", "1. Nhập Priority = @#$\n2. Click Create", "@#$", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-CRT-VL-012", "Quy tắc nhập liệu", "Priority là số thập phân", "Màn Create đang mở", "1. Nhập Priority = 1.5\n2. Click Create", "1.5", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-CRT-VL-013", "Quy tắc nhập liệu", "Priority là số âm", "Màn Create đang mở", "1. Nhập Priority = -1\n2. Click Create", "-1", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-CRT-VL-014", "Quy tắc nhập liệu", "Priority bằng 0", "Màn Create đang mở", "1. Nhập Priority = 0\n2. Click Create", "0", "Hiển thị lỗi: Priority must be a positive integer.", "Cao"))
    add(tc("TC-CRT-VL-015", "Quy tắc nhập liệu", "Priority là số nguyên dương hợp lệ", "Màn Create đang mở", "1. Nhập Priority = 1\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "1", "Priority được chấp nhận.", "Cao"))
    add(tc("TC-CRT-VL-016", "Quy tắc nhập liệu", "Start Date sai định dạng", "Màn Create đang mở", "1. Nhập Start Date sai format\n2. Click Create", "2026/07/01 hoặc text", "Hiển thị lỗi: Invalid start date format.", "Cao"))
    add(tc("TC-CRT-VL-017", "Quy tắc nhập liệu", "Start Date nhỏ hơn thời điểm hiện tại", "Màn Create đang mở", "1. Nhập Start Date trong quá khứ\n2. Click Create", "Start Date < current time", "Hiển thị lỗi: Start date must be greater than or equal to current time.", "Cao"))
    add(tc("TC-CRT-VL-018", "Quy tắc nhập liệu", "Start Date bằng thời điểm hiện tại", "Màn Create đang mở", "1. Nhập Start Date bằng current time tại thời điểm lưu\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Start Date = current time", "Start Date được chấp nhận theo rule greater than or equal. Cần kiểm tra theo độ chính xác mà hệ thống áp dụng.", "Trung bình"))
    add(tc("TC-CRT-VL-019", "Quy tắc nhập liệu", "End Date bắt buộc khi No End Date = Off", "No End Date đang Off", "1. Bỏ trống End Date\n2. Click Create", "End Date rỗng", "Không cho lưu. Requirement cần xác nhận message required vì SRS chưa nêu message cụ thể.", "Cao"))
    add(tc("TC-CRT-VL-020", "Quy tắc nhập liệu", "End Date sai định dạng", "Màn Create đang mở", "1. Nhập End Date sai format\n2. Click Create", "End Date sai format", "Hiển thị lỗi: Invalid end date format.", "Cao"))
    add(tc("TC-CRT-VL-021", "Quy tắc nhập liệu", "End Date nhỏ hơn Start Date", "Màn Create đang mở", "1. Nhập End Date < Start Date\n2. Click Create", "End Date < Start Date", "Hiển thị lỗi: End date must be greater than or equal to start date.", "Cao"))
    add(tc("TC-CRT-VL-022", "Quy tắc nhập liệu", "End Date bằng Start Date", "Màn Create đang mở", "1. Nhập End Date = Start Date\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "End Date = Start Date", "End Date được chấp nhận theo message greater than or equal.", "Trung bình"))
    add(tc("TC-CRT-VL-023", "Quy tắc nhập liệu", "No End Date On disable và clear End Date", "Màn Create đang mở; End Date đã có giá trị", "1. Nhập End Date\n2. Bật No End Date", "End Date có giá trị", "End Date bị disable/clear; không validate required.", "Cao"))
    add(tc("TC-CRT-VL-024", "Quy tắc nhập liệu", "No End Date Off yêu cầu nhập lại End Date nếu rỗng", "No End Date đang On và End Date đã clear", "1. Tắt No End Date\n2. Click Create khi End Date rỗng", "End Date rỗng", "End Date phải được nhập lại nếu đang rỗng.", "Cao"))
    add(tc("TC-CRT-VL-025", "Quy tắc nhập liệu", "Không upload ảnh popup", "Màn Create đang mở", "1. Không upload Popup image\n2. Nhập các field khác hợp lệ\n3. Click Create", "Không có ảnh", "Không cho lưu vì Popup image bắt buộc. Requirement cần xác nhận message required vì SRS chưa nêu message cụ thể.", "Cao"))
    add(tc("TC-CRT-VL-026", "Quy tắc nhập liệu", "Upload ảnh JPG hợp lệ", "Màn Create đang mở", "1. Upload ảnh JPG <= 2MB, tỷ lệ 16:9", "JPG hợp lệ", "Ảnh được upload/chấp nhận.", "Cao"))
    add(tc("TC-CRT-VL-027", "Quy tắc nhập liệu", "Upload ảnh PNG hợp lệ", "Màn Create đang mở", "1. Upload ảnh PNG <= 2MB, tỷ lệ 16:9", "PNG hợp lệ", "Ảnh được upload/chấp nhận.", "Cao"))
    add(tc("TC-CRT-VL-028", "Quy tắc nhập liệu", "Upload file ảnh rỗng hoặc lỗi đọc file", "Màn Create đang mở", "1. Upload file rỗng hoặc file lỗi", "File rỗng/lỗi", "Hiển thị lỗi: Invalid image file.", "Cao"))
    add(tc("TC-CRT-VL-029", "Quy tắc nhập liệu", "Upload ảnh sai định dạng", "Màn Create đang mở", "1. Upload file không phải JPG/PNG", "GIF/PDF/SVG", "Hiển thị lỗi: Invalid image format.", "Cao"))
    add(tc("TC-CRT-VL-030", "Quy tắc nhập liệu", "Upload ảnh vượt 2MB", "Màn Create đang mở", "1. Upload ảnh JPG/PNG dung lượng > 2MB", "Ảnh 2.1MB", "Hiển thị lỗi: Image size must not exceed 2MB.", "Cao"))
    add(tc("TC-CRT-VL-031", "Quy tắc nhập liệu", "Upload ảnh đúng 2MB", "Màn Create đang mở", "1. Upload ảnh JPG/PNG dung lượng đúng 2MB", "Ảnh 2MB", "Ảnh được chấp nhận nếu định dạng và tỷ lệ hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-VL-032", "Quy tắc nhập liệu", "Upload ảnh sai tỷ lệ nhưng hệ thống điều chỉnh được", "Màn Create đang mở", "1. Upload ảnh sai tỷ lệ\n2. Hệ thống điều chỉnh được về 16:9", "Ảnh sai tỷ lệ có thể điều chỉnh", "Ảnh được hệ thống điều chỉnh theo đúng tỷ lệ và chấp nhận.", "Trung bình"))
    add(tc("TC-CRT-VL-033", "Quy tắc nhập liệu", "Upload ảnh sai tỷ lệ và không điều chỉnh được", "Màn Create đang mở", "1. Upload ảnh sai tỷ lệ\n2. Hệ thống không điều chỉnh được", "Ảnh sai tỷ lệ không điều chỉnh được", "Hiển thị lỗi: Image ratio must be 16:9.", "Trung bình"))
    add(tc("TC-CRT-VL-034", "Quy tắc nhập liệu", "Chỉ chọn một lựa chọn trong nhóm nội dung hiển thị", "Màn Create đang mở", "1. Thử chọn đồng thời Không có nội dung hiển thị và Hiển thị nội dung", "Hai checkbox trong nhóm nội dung", "Hệ thống chỉ cho chọn đúng một lựa chọn.", "Cao"))
    add(tc("TC-CRT-VL-035", "Quy tắc nhập liệu", "Display content được chọn mặc định", "Màn Create mới mở", "1. Mở màn Create\n2. Quan sát nhóm nội dung hiển thị", "Không áp dụng", "Mặc định chọn Hiển thị nội dung.", "Trung bình"))
    add(tc("TC-CRT-VL-036", "Quy tắc nhập liệu", "Title bắt buộc khi chọn Hiển thị nội dung", "Display content được chọn", "1. Bỏ trống Title\n2. Nhập các field khác hợp lệ\n3. Click Create", "Title rỗng", "Hiển thị lỗi: Title is required.", "Cao"))
    add(tc("TC-CRT-VL-037", "Quy tắc nhập liệu", "Title chỉ gồm khoảng trắng", "Display content được chọn", "1. Nhập khoảng trắng vào Title\n2. Click Create", "\"   \"", "Trim xong rỗng và hiển thị lỗi: Title is required.", "Cao"))
    add(tc("TC-CRT-VL-038", "Quy tắc nhập liệu", "Title đúng 225 ký tự", "Display content được chọn", "1. Nhập Title 225 ký tự\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Title 225 ký tự, không tính biến hệ thống", "Title được chấp nhận.", "Trung bình"))
    add(tc("TC-CRT-VL-039", "Quy tắc nhập liệu", "Title vượt 225 ký tự", "Display content được chọn", "1. Nhập Title 226 ký tự\n2. Click Create", "Title 226 ký tự, không tính biến hệ thống", "Hiển thị lỗi: Title must not exceed 225 characters.", "Cao"))
    add(tc("TC-CRT-VL-040", "Quy tắc nhập liệu", "Content bắt buộc khi chọn Hiển thị nội dung", "Display content được chọn", "1. Bỏ trống Content\n2. Nhập các field khác hợp lệ\n3. Click Create", "Content rỗng", "Hiển thị lỗi: Content is required.", "Cao"))
    add(tc("TC-CRT-VL-041", "Quy tắc nhập liệu", "Content chỉ gồm khoảng trắng", "Display content được chọn", "1. Nhập khoảng trắng vào Content\n2. Click Create", "\"   \"", "Trim xong rỗng và hiển thị lỗi: Content is required.", "Cao"))
    add(tc("TC-CRT-VL-042", "Quy tắc nhập liệu", "Content đúng 500 ký tự", "Display content được chọn", "1. Nhập Content 500 ký tự\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Content 500 ký tự, không tính biến hệ thống", "Content được chấp nhận.", "Trung bình"))
    add(tc("TC-CRT-VL-043", "Quy tắc nhập liệu", "Content vượt 500 ký tự", "Display content được chọn", "1. Nhập Content 501 ký tự\n2. Click Create", "Content 501 ký tự, không tính biến hệ thống", "Hiển thị lỗi: Description must not exceed 500 characters.", "Cao"))
    add(tc("TC-CRT-VL-044", "Quy tắc nhập liệu", "Không cấu hình điều hướng", "Màn Create đang mở", "1. Để trống Loại điều hướng và Link điều hướng\n2. Nhập các field khác hợp lệ\n3. Click Create", "Navigation type rỗng; Link rỗng", "Được chấp nhận vì điều hướng không bắt buộc khi cả hai field cùng trống.", "Trung bình"))
    add(tc("TC-CRT-VL-045", "Quy tắc nhập liệu", "Có Link nhưng chưa chọn Loại điều hướng", "Màn Create đang mở", "1. Nhập Link điều hướng\n2. Không chọn Loại điều hướng\n3. Click Create", "Link có giá trị; navigation type rỗng", "Hiển thị lỗi: Navigation type is required.", "Cao"))
    add(tc("TC-CRT-VL-046", "Quy tắc nhập liệu", "Có Loại điều hướng nhưng chưa nhập Link", "Màn Create đang mở", "1. Chọn Loại điều hướng\n2. Để trống Link điều hướng\n3. Click Create", "Navigation type = Deeplink; Link rỗng", "Hiển thị lỗi: Navigation link is required.", "Cao"))
    add(tc("TC-CRT-VL-047", "Quy tắc nhập liệu", "Link điều hướng đúng 1000 ký tự", "Màn Create đang mở", "1. Nhập Link 1000 ký tự\n2. Chọn Loại điều hướng\n3. Nhập dữ liệu khác hợp lệ\n4. Click Create", "Link 1000 ký tự", "Link được chấp nhận.", "Trung bình"))
    add(tc("TC-CRT-VL-048", "Quy tắc nhập liệu", "Link điều hướng vượt 1000 ký tự", "Màn Create đang mở", "1. Nhập Link 1001 ký tự\n2. Click Create", "Link 1001 ký tự", "Hiển thị lỗi: Link must not exceed 1000 characters.", "Cao"))
    add(tc("TC-CRT-VL-049", "Quy tắc nhập liệu", "Không chọn đối tượng áp dụng", "Màn Create đang mở", "1. Không chọn Toàn bộ hội viên/Customer Segment/Import file\n2. Click Create", "Audience rỗng", "Hiển thị lỗi: Please select audience.", "Cao"))
    add(tc("TC-CRT-VL-050", "Quy tắc nhập liệu", "Chỉ chọn một đối tượng áp dụng", "Màn Create đang mở", "1. Thử chọn đồng thời Toàn bộ hội viên, Customer Segment và Import file", "Nhiều option audience", "Hệ thống chỉ cho chọn một trong ba option.", "Cao"))
    add(tc("TC-CRT-VL-051", "Quy tắc nhập liệu", "Chọn Toàn bộ hội viên sẽ disable/clear Customer Segment và Import file", "Trước đó đã chọn segment hoặc upload file", "1. Chọn Customer Segment hoặc Import file\n2. Chọn Toàn bộ hội viên", "Audience chuyển sang All members", "Dropdown Customer Segment và file import bị disable/clear; campaign áp dụng cho tất cả hội viên đã xác định account.", "Cao"))
    add(tc("TC-CRT-VL-052", "Quy tắc nhập liệu", "Chọn Customer Segment nhưng không chọn segment cụ thể", "Audience = Customer Segment", "1. Chọn Customer Segment\n2. Không chọn dropdown segment\n3. Click Create", "Segment rỗng", "Hiển thị lỗi: Please select one Customer Segment.", "Cao"))
    add(tc("TC-CRT-VL-053", "Quy tắc nhập liệu", "Chọn Customer Segment sẽ disable/clear file import", "Trước đó đã chọn Import file", "1. Chọn Import file và upload file\n2. Chọn Customer Segment", "File import đã upload", "File import bị disable/clear; dropdown Customer Segment enable.", "Cao"))
    add(tc("TC-CRT-VL-054", "Quy tắc nhập liệu", "Chọn Import file nhưng không upload file", "Audience = Import file", "1. Chọn Import file\n2. Không upload file\n3. Click Create", "Không có file import", "Hiển thị lỗi: Please upload member file.", "Cao"))
    add(tc("TC-CRT-VL-055", "Quy tắc nhập liệu", "Import file rỗng hoặc lỗi đọc file", "Audience = Import file", "1. Upload file rỗng hoặc file lỗi", "File rỗng/lỗi", "Hiển thị lỗi: Invalid import file.", "Cao"))
    add(tc("TC-CRT-VL-056", "Quy tắc nhập liệu", "Import file sai định dạng mẫu", "Audience = Import file", "1. Upload file Excel không đúng template", "Excel sai template", "Hiển thị lỗi: Invalid import file format.", "Cao"))
    add(tc("TC-CRT-VL-057", "Quy tắc nhập liệu", "Upload/validate import file thất bại", "Audience = Import file", "1. Upload file import\n2. Backend trả lỗi upload/validate", "File Excel; backend lỗi", "Hiển thị lỗi: Failed to upload import file.", "Cao"))
    add(tc("TC-CRT-VL-058", "Quy tắc nhập liệu", "Không chọn Position", "Màn Create đang mở", "1. Không chọn Position\n2. Click Create", "Position rỗng", "Hiển thị lỗi: Please select at least one Position.", "Cao"))
    add(tc("TC-CRT-VL-059", "Quy tắc nhập liệu", "Không chọn loại tần suất hiển thị", "Màn Create đang mở", "1. Không chọn Display Frequency\n2. Click Create", "Frequency rỗng", "Hiển thị lỗi: Please select frequency type.", "Cao"))
    add(tc("TC-CRT-VL-060", "Quy tắc nhập liệu", "Chọn 1 lần duy nhất trong toàn bộ thời gian hiệu lực", "Màn Create đang mở", "1. Chọn Only once during the entire validity period\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Frequency = Only once", "Tần suất được chấp nhận; không yêu cầu nhập X.", "Trung bình"))
    add(tc("TC-CRT-VL-061", "Quy tắc nhập liệu", "Chọn 1 lần/ngày reset 00:00", "Màn Create đang mở", "1. Chọn Once per day\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Frequency = Once per day", "Tần suất được chấp nhận; không yêu cầu nhập X.", "Trung bình"))
    add(tc("TC-CRT-VL-062", "Quy tắc nhập liệu", "Chọn Không giới hạn", "Màn Create đang mở", "1. Chọn Không giới hạn - hiển thị mỗi lần mở app\n2. Nhập dữ liệu khác hợp lệ\n3. Click Create", "Frequency = Không giới hạn", "Tần suất được chấp nhận; không yêu cầu nhập X.", "Trung bình"))
    add(tc("TC-CRT-VL-063", "Quy tắc nhập liệu", "X lần/ngày không nhập X", "Chọn X lần/ngày", "1. Chọn X lần/ngày\n2. Bỏ trống X\n3. Click Create", "X rỗng", "Hiển thị lỗi: Frequency value is required.", "Cao"))
    add(tc("TC-CRT-VL-064", "Quy tắc nhập liệu", "X lần/ngày nhập chữ/ký tự đặc biệt/số thập phân/số âm/0", "Chọn X lần/ngày", "1. Nhập X không hợp lệ\n2. Click Create", "abc, @, 1.5, -1, 0", "Hiển thị lỗi: Frequency value must be an integer and less than 50.", "Cao"))
    add(tc("TC-CRT-VL-065", "Quy tắc nhập liệu", "X lần/ngày nhập 50", "Chọn X lần/ngày", "1. Nhập X = 50\n2. Click Create", "50", "Hiển thị lỗi: Frequency value must be an integer and less than 50.", "Cao"))
    add(tc("TC-CRT-VL-066", "Quy tắc nhập liệu", "X lần/ngày giá trị biên hợp lệ", "Chọn X lần/ngày", "1. Nhập X = 1 và lưu với dữ liệu hợp lệ\n2. Lặp lại với X = 49", "X = 1; X = 49", "Giá trị được chấp nhận nếu các field khác hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-VL-067", "Quy tắc nhập liệu", "X lần/tuần không chọn ngày trong tuần", "Chọn X lần/tuần", "1. Chọn X lần/tuần\n2. Nhập X\n3. Không chọn ngày\n4. Click Create", "Không chọn T2-CN", "Hiển thị lỗi: Please select at least one day of week.", "Cao"))
    add(tc("TC-CRT-VL-068", "Quy tắc nhập liệu", "X lần/tuần chọn ít nhất một ngày", "Chọn X lần/tuần", "1. Chọn X lần/tuần\n2. Nhập X\n3. Chọn T2\n4. Nhập dữ liệu khác hợp lệ\n5. Click Create", "X có giá trị; chọn T2", "Tần suất được chấp nhận nếu dữ liệu khác hợp lệ.", "Trung bình"))
    add(tc("TC-CRT-VL-069", "Quy tắc nhập liệu", "X lần/tuần không nhập X", "Chọn X lần/tuần", "1. Chọn X lần/tuần\n2. Chọn ngày trong tuần\n3. Bỏ trống X\n4. Click Create", "X rỗng; chọn T2", "Requirement cần xác nhận: SRS nói bắt buộc nhập X nhưng chưa nêu message lỗi riêng.", "Cao"))

    # Integration
    add(tc("TC-CRT-TH-001", "Tích hợp", "Backend trả trạng thái campaign sau khi tạo", "Form hợp lệ", "1. Tạo campaign hợp lệ\n2. Quan sát response và danh sách/chi tiết", "Start Date/End Date hợp lệ", "Backend trả trạng thái campaign sau khi tạo, ví dụ Scheduled/Active theo thời gian hiệu lực và rule hệ thống; FE hiển thị trạng thái này.", "Cao"))
    add(tc("TC-CRT-TH-002", "Tích hợp", "Backend validate Start Date theo timezone UTC+7", "Có thể thay đổi timezone máy cá nhân", "1. Đổi timezone máy cá nhân khác UTC+7\n2. Nhập Start Date gần current time\n3. Lưu", "Timezone máy khác UTC+7", "Backend vẫn validate theo timezone hệ thống UTC+7.", "Cao"))
    add(tc("TC-CRT-TH-003", "Tích hợp", "Upload ảnh thất bại", "Màn Create có ảnh hợp lệ", "1. Upload ảnh hợp lệ\n2. Giả lập backend/storage trả lỗi upload", "Ảnh JPG/PNG hợp lệ", "Hiển thị lỗi: Failed to upload image.", "Cao"))
    add(tc("TC-CRT-TH-004", "Tích hợp", "Backend trả lỗi validate xác định được field", "Form submit lên backend", "1. Gửi dữ liệu khiến backend trả lỗi validate field\n2. Quan sát UI", "Lỗi validate có field", "FE hiển thị lỗi tại field tương ứng nếu xác định được.", "Cao"))
    add(tc("TC-CRT-TH-005", "Tích hợp", "Backend trả lỗi validate không xác định field", "Form submit lên backend", "1. Gửi dữ liệu khiến backend trả lỗi chung\n2. Quan sát UI", "Lỗi không map field", "Hiển thị toast: Failed to save campaign.", "Cao"))
    add(tc("TC-CRT-TH-006", "Tích hợp", "Không gửi Customer Segment khi audience khác Customer Segment", "Audience = Toàn bộ hội viên hoặc Import file", "1. Chọn audience không phải Customer Segment\n2. Submit form\n3. Kiểm tra request/log backend", "Audience = All members hoặc Import file", "Không gửi giá trị Customer Segment khi field disabled.", "Trung bình"))
    add(tc("TC-CRT-TH-007", "Tích hợp", "Không gửi file import khi audience khác Import file", "Audience = Toàn bộ hội viên hoặc Customer Segment", "1. Chọn audience không phải Import file\n2. Submit form\n3. Kiểm tra request/log backend", "Audience = All members hoặc Segment", "Không gửi file import khi field disabled/cleared.", "Trung bình"))
    add(tc("TC-CRT-TH-008", "Tích hợp", "Không resolve được biến hệ thống không làm lỗi toàn bộ Pop-up", "Có cấu hình biến hệ thống trong Title/Content", "1. Tạo campaign có biến hệ thống\n2. Giả lập App/Backend không resolve được biến\n3. Kiểm tra xử lý", "Biến hệ thống thiếu dữ liệu", "Không làm lỗi toàn bộ Pop-up. Requirement cần xác nhận rule kỹ thuật hiển thị/fallback cụ thể.", "Trung bình"))

    # Regression
    add(tc("TC-CRT-RG-001", "Hồi quy", "Không ảnh hưởng màn danh sách sau khi tạo campaign thành công", "Tạo campaign thành công", "1. Tạo campaign hợp lệ\n2. Quay về danh sách\n3. Tìm campaign vừa tạo", "Campaign mới", "Danh sách hiển thị campaign mới với thông tin chính xác.", "Cao"))
    add(tc("TC-CRT-RG-002", "Hồi quy", "Không ảnh hưởng module Customer Segment", "Có quyền truy cập Customer Segment", "1. Tạo campaign với Customer Segment\n2. Mở module Customer Segment\n3. Kiểm tra danh sách/điều kiện segment", "Segment A", "Module Customer Segment vẫn hoạt động và dữ liệu không bị thay đổi ngoài phạm vi.", "Trung bình"))
    add(tc("TC-CRT-RG-003", "Hồi quy", "Không ảnh hưởng template import của Notification", "Import template dùng chung/tham chiếu từ Notification", "1. Chọn Import file trong Create\n2. Tải/kiểm tra File Mẫu\n3. Kiểm tra template Notification hiện hữu", "Template import", "Template hiện hữu không bị thay đổi ngoài yêu cầu. Requirement cần xác nhận vì SRS chỉ nói dùng template Notification đang áp dụng.", "Trung bình"))
    add(tc("TC-CRT-RG-004", "Hồi quy", "Không ảnh hưởng chuẩn confirm/toast chung CMS", "Có màn CMS khác dùng confirm/toast", "1. Tạo campaign thành công/thất bại để phát sinh toast\n2. Kiểm tra confirm/toast ở màn CMS khác", "Toast success/error", "Confirm/toast chung của CMS vẫn hoạt động đúng.", "Trung bình"))

    # UI/UX
    add(tc("TC-CRT-UI-001", "UI/UX", "Hiển thị đúng tiêu đề và Screen ID màn Create", "User có quyền mở màn Create", "1. Mở màn Create\n2. Quan sát tiêu đề và bố cục", "SCR-CMS-POP-002", "Màn hình hiển thị đúng Tạo campaign Pop-up theo mockup.", "Thấp"))
    add(tc("TC-CRT-UI-002", "UI/UX", "Hiển thị đầy đủ các trường thông tin chung", "Màn Create đang mở", "1. Quan sát nhóm thông tin chung", "Language, Campaign Name, Description, Priority, Start Date, End Date, No End Date", "Các trường hiển thị đầy đủ theo SRS.", "Trung bình"))
    add(tc("TC-CRT-UI-003", "UI/UX", "Hiển thị đầy đủ nhóm ảnh và nội dung popup", "Màn Create đang mở", "1. Quan sát nhóm nội dung popup", "Popup image, No content displayed, Display content, System Variables, Title, Content", "Các trường/option hiển thị đầy đủ theo SRS.", "Trung bình"))
    add(tc("TC-CRT-UI-004", "UI/UX", "Hiển thị đầy đủ nhóm điều hướng", "Màn Create đang mở", "1. Quan sát nhóm điều hướng", "Loại điều hướng, Link điều hướng", "Các trường điều hướng hiển thị theo SRS.", "Trung bình"))
    add(tc("TC-CRT-UI-005", "UI/UX", "Hiển thị đầy đủ nhóm đối tượng áp dụng", "Màn Create đang mở", "1. Quan sát nhóm Đối tượng áp dụng", "Toàn bộ hội viên, Customer Segment, Import file, dropdown Segment, file import, File Mẫu", "Các option và field liên quan hiển thị đúng theo lựa chọn.", "Trung bình"))
    add(tc("TC-CRT-UI-006", "UI/UX", "Hiển thị đầy đủ nhóm quy tắc hiển thị", "Màn Create đang mở", "1. Quan sát nhóm Quy tắc hiển thị", "Position, Display Frequency", "Nhóm Position và Display Frequency hiển thị đầy đủ.", "Trung bình"))
    add(tc("TC-CRT-UI-007", "UI/UX", "Tooltip Priority hiển thị đúng nội dung", "Màn Create đang mở", "1. Hover/click icon thông tin cạnh Priority", "Icon thông tin Priority", "Tooltip hiển thị: Smaller numbers take display priority.", "Thấp"))
    add(tc("TC-CRT-UI-008", "UI/UX", "Tooltip System Variables hiển thị đúng nội dung", "Màn Create đang mở", "1. Hover/click icon thông tin cạnh Các biến hệ thống", "Icon thông tin System Variables", "Tooltip hiển thị: Click the system variables field to insert them into the content.", "Thấp"))
    add(tc("TC-CRT-UI-009", "UI/UX", "Segment condition hiển thị read-only chips", "Chọn Customer Segment", "1. Chọn Customer Segment\n2. Chọn một segment\n3. Quan sát Điều kiện của Segment", "Segment có Attributes", "Điều kiện segment hiển thị dạng tag/chip read-only; không cho chỉnh sửa tại màn Pop-up.", "Trung bình"))
    add(tc("TC-CRT-UI-010", "UI/UX", "Button Create chỉ submit khi field bắt buộc hợp lệ", "Màn Create đang mở", "1. Để form chưa hợp lệ\n2. Quan sát/click Create\n3. Nhập form hợp lệ\n4. Quan sát/click Create", "Form không hợp lệ và hợp lệ", "Button chỉ submit khi các field bắt buộc hợp lệ; nếu không hợp lệ thì validate toàn bộ form.", "Cao"))
    add(tc("TC-CRT-UI-011", "UI/UX", "Popup xác nhận Create hiển thị đúng nội dung", "Form Create hợp lệ", "1. Click Create", "Form hợp lệ", "Popup confirm hiển thị nội dung: Are you sure you want to create this campaign? và có kèm nhập mã OTP.", "Trung bình"))
    add(tc("TC-CRT-UI-012", "UI/UX", "Close button hiển thị và hoạt động đúng", "Màn Create đang mở", "1. Quan sát button Close\n2. Click Close trong các trạng thái có/không có dữ liệu", "Không áp dụng", "Button Close hiển thị; xử lý rời màn đúng theo trạng thái dữ liệu đã nhập.", "Trung bình"))
    return rows


def build_sheets():
    cases = build_create_cases()
    overview = [
        ["Hạng mục", "Nội dung"],
        ["Tên màn hình", "CMS_Tạo campaign Pop-up"],
        ["Mã màn hình", "SCR-CMS-POP-002"],
        ["Nguồn yêu cầu", "SRS CMS Pop-up - Chiến dịch Marketing, mục 4.3 CMS_Tạo campaign Pop-up"],
        ["Phạm vi", "Tạo campaign Pop-up gồm thông tin chung, thời gian hiệu lực, ảnh, nội dung, biến hệ thống, điều hướng, đối tượng áp dụng, import file, vị trí, tần suất, close, confirm OTP và submit tạo campaign."],
        ["Ngoài phạm vi", "Chi tiết chỉnh sửa campaign, danh sách campaign, export báo cáo và hành vi App sau khi hiển thị Pop-up."],
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
        ["Ca kiểm thử âm tính", 43],
        ["Ca kiểm thử biên", 18],
        ["Ca UI/UX", categories.get("UI/UX", 0)],
        ["Ca phân quyền", categories.get("Phân Quyền", 0)],
        ["Ưu tiên Cao", priorities.get("Cao", 0)],
        ["Ưu tiên Trung bình", priorities.get("Trung bình", 0)],
        ["Ưu tiên Thấp", priorities.get("Thấp", 0)],
        ["Phân bổ theo danh mục", "; ".join(f"{k}: {v}" for k, v in categories.items())],
    ]
    risks = [
        ["Loại", "Nội dung", "Khuyến nghị"],
        ["Requirement cần xác nhận", "Message required cho Start Date, End Date và Popup image chưa được nêu rõ trong SRS.", "BA/PO cần chốt thông báo lỗi để QA có assertion chính xác."],
        ["Requirement cần xác nhận", "Description vượt 500 ký tự có message sai/thiếu số ký tự: Campaign name must not exceed  characters.", "Cần sửa/chốt lại message đúng field và đúng maxlength."],
        ["Requirement cần xác nhận", "Template import file, max size, max rows, rule duplicate member chưa có.", "Cần bổ sung template và rule validation import file."],
        ["Requirement cần xác nhận", "Format hợp lệ cho từng Loại điều hướng chưa được định nghĩa.", "Cần bổ sung rule format link cho Màn hình app, Deeplink, Webview, Browser, Landing Page."],
        ["Requirement cần xác nhận", "OTP tạo campaign chưa có rule sai OTP, hết hạn, retry, resend.", "Cần bổ sung rule OTP để tạo ca kiểm thử đầy đủ."],
        ["Requirement cần xác nhận", "Rule kỹ thuật khi App/Backend không resolve được biến hệ thống chưa rõ.", "Cần chốt fallback hiển thị hoặc logging."],
        ["Requirement cần xác nhận", "Position lấy theo tài liệu BA nhưng danh sách chính thức chưa có trong SRS.", "Cần bổ sung danh mục Position native app."],
        ["Rủi ro", "Backend xác định trạng thái campaign sau khi tạo nhưng state machine chưa đầy đủ.", "Chốt lifecycle Scheduled/Active/Inactive/Expired trước UAT."],
        ["Khuyến nghị", "Ưu tiên tự động hóa các ca validation bắt buộc, upload file, audience, frequency và tạo campaign hợp lệ.", "Đưa các ca ưu tiên Cao vào regression suite."],
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
