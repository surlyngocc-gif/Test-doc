from __future__ import annotations

import importlib.util
from pathlib import Path


BASE_PATH = Path(__file__).with_name("build_cms_popup_testcases_xlsx.py")
spec = importlib.util.spec_from_file_location("xlsx_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

base.OUT_PATH = "deliverables/Bo_ca_kiem_thu_Xoa_Campaign_Popup.xlsx"


def tc(tc_id, category, scenario, pre, steps, data, expected, priority="Cao", status="Chưa chạy"):
    return [tc_id, category, scenario, pre, steps, data, expected, priority, status]


def build_delete_cases():
    rows = []
    add = rows.append

    # Phân Quyền
    add(tc("TC-DEL-PQ-001", "Phân Quyền", "Admin CMS có quyền Pop-up nhìn thấy icon Delete cho campaign Scheduled", "Admin CMS đã đăng nhập; màn danh sách có campaign Scheduled", "1. Mở menu Pop-up - Chiến dịch Marketing\n2. Quan sát cột Action của campaign Scheduled", "Campaign trạng thái Scheduled", "Icon Delete hiển thị và enable tại dòng campaign Scheduled.", "Cao"))
    add(tc("TC-DEL-PQ-002", "Phân Quyền", "Manager CMS có quyền Pop-up nhìn thấy icon Delete cho campaign Scheduled", "Manager CMS đã đăng nhập; có quyền Pop-up; có campaign Scheduled", "1. Mở danh sách campaign Pop-up\n2. Quan sát cột Action của campaign Scheduled", "Campaign trạng thái Scheduled", "Icon Delete hiển thị và enable theo quyền Pop-up.", "Cao"))
    add(tc("TC-DEL-PQ-003", "Phân Quyền", "User không có quyền Pop-up không truy cập được màn danh sách để xoá campaign", "User CMS không có quyền Pop-up", "1. Đăng nhập CMS bằng user không có quyền\n2. Quan sát menu\n3. Truy cập trực tiếp URL danh sách Pop-up", "Tài khoản không có quyền Pop-up", "Menu Pop-up không hiển thị; nếu truy cập URL trực tiếp thì Backend CMS từ chối truy cập, user không xoá được campaign.", "Cao"))
    add(tc("TC-DEL-PQ-004", "Phân Quyền", "Không hiển thị hoặc disable icon Delete với campaign Active", "Màn danh sách có campaign Active", "1. Mở danh sách campaign Pop-up\n2. Quan sát cột Action của campaign Active", "Campaign trạng thái Active", "Icon Delete bị ẩn hoặc disabled; user không mở được popup xác nhận xoá.", "Cao"))
    add(tc("TC-DEL-PQ-005", "Phân Quyền", "Không hiển thị hoặc disable icon Delete với campaign Inactive", "Màn danh sách có campaign Inactive", "1. Mở danh sách campaign Pop-up\n2. Quan sát cột Action của campaign Inactive", "Campaign trạng thái Inactive", "Icon Delete bị ẩn hoặc disabled; user không mở được popup xác nhận xoá.", "Cao"))
    add(tc("TC-DEL-PQ-006", "Phân Quyền", "Không hiển thị hoặc disable icon Delete với campaign Expired", "Màn danh sách có campaign Expired", "1. Mở danh sách campaign Pop-up\n2. Quan sát cột Action của campaign Expired", "Campaign trạng thái Expired", "Icon Delete bị ẩn hoặc disabled; user không mở được popup xác nhận xoá.", "Cao"))
    add(tc("TC-DEL-PQ-007", "Phân Quyền", "Backend từ chối xoá khi campaign không còn trạng thái Scheduled", "FE đang hiển thị Delete enable; campaign vừa bị đổi trạng thái bởi job/user khác", "1. Mở danh sách khi campaign còn Scheduled\n2. Đổi trạng thái campaign ở backend sang Active/Inactive/Expired\n3. Click Delete\n4. Xác nhận xoá", "Campaign không còn Scheduled tại thời điểm gọi API", "Không xoá campaign; hiển thị toast: Campaign cannot be deleted in current status.", "Cao"))
    add(tc("TC-DEL-PQ-008", "Phân Quyền", "Không cho xoá campaign bằng API trực tiếp khi không có quyền", "User không có quyền Pop-up nhưng có thông tin campaign Scheduled", "1. Gửi request xoá campaign bằng API/client ngoài UI\n2. Kiểm tra phản hồi và dữ liệu", "Campaign Scheduled", "Backend từ chối request; campaign không bị xoá. Requirement cần xác nhận mã lỗi/thông báo cụ thể.", "Cao"))

    # Chức năng chính
    add(tc("TC-DEL-CN-001", "Chức năng chính", "Click Delete ở campaign Scheduled mở popup xác nhận xoá", "User có quyền Pop-up; có campaign Scheduled", "1. Mở danh sách campaign Pop-up\n2. Click icon Delete tại campaign Scheduled", "Campaign Scheduled", "Popup xác nhận xoá hiển thị.", "Cao"))
    add(tc("TC-DEL-CN-002", "Chức năng chính", "Popup xác nhận xoá hiển thị đúng nội dung và OTP", "Popup xác nhận xoá đang mở", "1. Quan sát nội dung popup\n2. Quan sát trường nhập OTP", "Không áp dụng", "Popup hiển thị nội dung: Are you sure you want to delete this campaign? và có mã/trường OTP theo SRS.", "Cao"))
    add(tc("TC-DEL-CN-003", "Chức năng chính", "Cancel popup xác nhận xoá", "Popup xác nhận xoá đang mở", "1. Click Cancel\n2. Kiểm tra popup\n3. Kiểm tra danh sách", "Không áp dụng", "Popup đóng; không gọi API xoá; campaign vẫn còn trên danh sách.", "Cao"))
    add(tc("TC-DEL-CN-004", "Chức năng chính", "Đóng popup xác nhận bằng icon Close hoặc click ngoài vùng popup nếu hệ thống hỗ trợ", "Popup xác nhận xoá đang mở", "1. Click icon Close hoặc thao tác đóng popup theo chuẩn CMS\n2. Kiểm tra danh sách", "Không áp dụng", "Popup đóng; không xoá campaign. Requirement cần xác nhận nếu popup không hỗ trợ click ngoài vùng.", "Trung bình"))
    add(tc("TC-DEL-CN-005", "Chức năng chính", "Click Delete trong popup gọi API xoá campaign", "Popup xác nhận xoá đang mở; OTP hợp lệ", "1. Nhập OTP hợp lệ\n2. Click Delete\n3. Kiểm tra request gửi lên backend", "Campaign Scheduled; OTP hợp lệ", "FE gọi API xoá campaign với đúng campaign ID/code đã chọn.", "Cao"))
    add(tc("TC-DEL-CN-006", "Chức năng chính", "Xoá campaign Scheduled thành công", "Campaign Scheduled tồn tại; API xoá trả thành công", "1. Click Delete tại campaign Scheduled\n2. Nhập OTP hợp lệ\n3. Click Delete trong popup", "Campaign Scheduled", "Hiển thị toast: Campaign has been successfully deleted. Danh sách được cập nhật lại.", "Cao"))
    add(tc("TC-DEL-CN-007", "Chức năng chính", "Campaign đã xoá không còn hiển thị trên danh sách sau khi reload", "Đã xoá campaign thành công", "1. Sau toast thành công, quan sát danh sách\n2. Reload trang\n3. Tìm kiếm theo code campaign đã xoá", "Code campaign vừa xoá", "Campaign đã xoá không còn hiển thị trên danh sách.", "Cao"))
    add(tc("TC-DEL-CN-008", "Chức năng chính", "Xoá campaign Scheduled thất bại do API trả lỗi chung", "Campaign Scheduled tồn tại; backend trả lỗi", "1. Click Delete tại campaign Scheduled\n2. Nhập OTP hợp lệ\n3. Click Delete trong popup\n4. Backend trả lỗi", "Lỗi backend chung", "Hiển thị toast: Failed to delete campaign. Campaign không bị xoá khỏi danh sách.", "Cao"))
    add(tc("TC-DEL-CN-009", "Chức năng chính", "Không xoá nhầm campaign khi thao tác trên nhiều dòng", "Danh sách có nhiều campaign Scheduled", "1. Chọn Delete tại campaign A\n2. Xác nhận xoá\n3. Kiểm tra campaign A và campaign B", "Campaign A, Campaign B", "Chỉ campaign A bị xoá; các campaign khác không bị ảnh hưởng.", "Cao"))
    add(tc("TC-DEL-CN-010", "Chức năng chính", "Popup xác nhận xoá đúng campaign được chọn sau khi lọc danh sách", "Danh sách đang áp dụng filter/search; có campaign Scheduled", "1. Lọc danh sách\n2. Click Delete tại campaign Scheduled trong kết quả lọc\n3. Kiểm tra thông tin request/API", "Campaign Scheduled trong kết quả lọc", "API xoá đúng campaign được chọn trong danh sách đã lọc.", "Cao"))
    add(tc("TC-DEL-CN-011", "Chức năng chính", "Xoá campaign ở trang phân trang khác cập nhật đúng trang hiện tại", "Danh sách có nhiều trang; campaign Scheduled nằm ở trang bất kỳ", "1. Chuyển sang trang chứa campaign Scheduled\n2. Xoá campaign thành công\n3. Quan sát phân trang và dữ liệu", "Campaign Scheduled ở trang 2 trở đi", "Danh sách refresh đúng; số dòng/trang được cập nhật theo chuẩn phân trang CMS.", "Trung bình"))
    add(tc("TC-DEL-CN-012", "Chức năng chính", "Xoá campaign cuối cùng của trang hiện tại", "Trang hiện tại chỉ còn một campaign Scheduled", "1. Mở trang chỉ còn một dòng\n2. Xoá campaign thành công\n3. Quan sát danh sách", "Campaign Scheduled cuối trang", "Danh sách cập nhật hợp lý: chuyển về trang còn dữ liệu hoặc hiển thị No Data theo chuẩn CMS.", "Trung bình"))
    add(tc("TC-DEL-CN-013", "Chức năng chính", "Xoá campaign khi danh sách đang có một bản ghi duy nhất", "Danh sách chỉ có một campaign Scheduled phù hợp filter", "1. Mở danh sách\n2. Xoá campaign duy nhất\n3. Quan sát màn hình", "Một campaign Scheduled", "Sau khi xoá thành công, danh sách hiển thị No Data.", "Cao"))
    add(tc("TC-DEL-CN-014", "Chức năng chính", "Không thay đổi Code của các campaign còn lại sau khi xoá", "Có nhiều campaign với code khác nhau", "1. Ghi nhận code các campaign trước khi xoá\n2. Xoá một campaign Scheduled\n3. Kiểm tra code các campaign còn lại", "POP01, POP02, POP03", "Code của các campaign còn lại không thay đổi theo SRS.", "Cao"))
    add(tc("TC-DEL-CN-015", "Chức năng chính", "Có thể tiếp tục thao tác xem/sửa campaign khác sau khi xoá thành công", "Xoá campaign thành công; danh sách còn campaign khác", "1. Sau khi danh sách refresh\n2. Click View hoặc Edit campaign khác", "Campaign khác còn tồn tại", "Các action khác vẫn hoạt động bình thường.", "Trung bình"))
    add(tc("TC-DEL-CN-016", "Chức năng chính", "Không gọi API xoá nhiều lần khi người dùng bấm Delete liên tục trong popup", "Popup xác nhận xoá đang mở; mạng phản hồi chậm", "1. Nhập OTP hợp lệ\n2. Bấm Delete nhiều lần liên tiếp\n3. Kiểm tra request/API", "Campaign Scheduled", "Chỉ một request xoá hợp lệ được xử lý hoặc button chuyển trạng thái loading/disabled để tránh duplicate request.", "Cao"))
    add(tc("TC-DEL-CN-017", "Chức năng chính", "Giữ nguyên filter/search sau khi xoá và refresh danh sách", "Danh sách đang áp dụng search/filter", "1. Áp dụng filter/search\n2. Xoá campaign Scheduled trong kết quả\n3. Quan sát filter/search và danh sách sau refresh", "Filter trạng thái Scheduled hoặc search theo tên/code", "Danh sách được cập nhật theo điều kiện search/filter hiện tại. Requirement cần xác nhận nếu hệ thống reset filter sau thao tác xoá.", "Trung bình"))
    add(tc("TC-DEL-CN-018", "Chức năng chính", "Không cho mở popup xoá với campaign Active/Inactive/Expired bằng thao tác bất thường trên UI", "Có campaign không phải Scheduled", "1. Dùng keyboard/devtool cố kích hoạt action Delete bị disabled\n2. Quan sát UI/API", "Campaign Active/Inactive/Expired", "Không mở popup xác nhận xoá; không gọi API xoá.", "Cao"))

    # Quy tắc nhập liệu
    add(tc("TC-DEL-VL-001", "Quy tắc nhập liệu", "Không cho xác nhận xoá khi OTP rỗng", "Popup xác nhận xoá đang mở", "1. Để trống OTP\n2. Click Delete", "OTP rỗng", "Không xoá campaign; hiển thị lỗi validate OTP. Requirement cần xác nhận message cụ thể.", "Cao"))
    add(tc("TC-DEL-VL-002", "Quy tắc nhập liệu", "Không cho xác nhận xoá khi OTP sai", "Popup xác nhận xoá đang mở", "1. Nhập OTP sai\n2. Click Delete", "OTP không hợp lệ", "Không xoá campaign; backend/FE báo OTP không hợp lệ. Requirement cần xác nhận message cụ thể.", "Cao"))
    add(tc("TC-DEL-VL-003", "Quy tắc nhập liệu", "Không cho xác nhận xoá khi OTP hết hạn", "Popup xác nhận xoá đang mở; OTP đã hết hạn", "1. Nhập OTP hết hạn\n2. Click Delete", "OTP hết hạn", "Không xoá campaign; hiển thị lỗi OTP hết hạn. Requirement cần xác nhận thời gian hết hạn và message.", "Cao"))
    add(tc("TC-DEL-VL-004", "Quy tắc nhập liệu", "Trim khoảng trắng khi nhập OTP nếu hệ thống hỗ trợ", "Popup xác nhận xoá đang mở", "1. Nhập OTP hợp lệ kèm khoảng trắng đầu/cuối\n2. Click Delete", "OTP có khoảng trắng", "Hệ thống xử lý theo rule OTP chung. Requirement cần xác nhận có trim OTP hay không.", "Trung bình"))
    add(tc("TC-DEL-VL-005", "Quy tắc nhập liệu", "Không cho nhập ký tự không hợp lệ vào OTP nếu OTP chỉ cho số", "Popup xác nhận xoá đang mở", "1. Nhập chữ hoặc ký tự đặc biệt vào OTP\n2. Quan sát field và click Delete", "abc, @#$", "Hệ thống chặn nhập hoặc hiển thị lỗi validate. Requirement cần xác nhận định dạng OTP.", "Trung bình"))
    add(tc("TC-DEL-VL-006", "Quy tắc nhập liệu", "Không cho gửi request xoá khi thiếu campaign ID/code", "Có thể giả lập request thiếu định danh campaign", "1. Gửi request xoá thiếu campaign ID/code\n2. Kiểm tra phản hồi backend", "Request thiếu campaign ID/code", "Backend từ chối request; không xoá dữ liệu. Requirement cần xác nhận mã lỗi/thông báo cụ thể.", "Cao"))
    add(tc("TC-DEL-VL-007", "Quy tắc nhập liệu", "Không xoá khi campaign ID không tồn tại", "Có thể gọi API với ID không tồn tại", "1. Gửi request xoá với campaign ID không tồn tại\n2. Kiểm tra dữ liệu", "Campaign ID không tồn tại", "Backend trả lỗi; không ảnh hưởng dữ liệu campaign khác. Requirement cần xác nhận message hiển thị ở FE.", "Cao"))
    add(tc("TC-DEL-VL-008", "Quy tắc nhập liệu", "Không cho xoá lại campaign đã bị xoá trước đó", "Campaign đã bị xoá bởi user/session khác", "1. Mở popup xoá campaign Scheduled\n2. Campaign bị xoá bởi user khác\n3. Click Delete xác nhận", "Campaign đã không còn tồn tại", "Không phát sinh xoá trùng; FE hiển thị lỗi phù hợp hoặc toast thất bại. Requirement cần xác nhận message.", "Cao"))

    # Tích hợp
    add(tc("TC-DEL-TH-001", "Tích hợp", "FE gửi đúng định danh campaign khi gọi API xoá", "Có thể kiểm tra network/log; campaign Scheduled", "1. Click Delete tại campaign Scheduled\n2. Xác nhận xoá\n3. Kiểm tra request", "Campaign ID/code", "Request xoá chứa đúng định danh campaign đã chọn.", "Cao"))
    add(tc("TC-DEL-TH-002", "Tích hợp", "FE hiển thị toast thành công khi API xoá trả thành công", "API xoá trả success", "1. Xoá campaign Scheduled\n2. Quan sát toast", "Response thành công", "Hiển thị toast: Campaign has been successfully deleted.", "Cao"))
    add(tc("TC-DEL-TH-003", "Tích hợp", "FE hiển thị toast thất bại khi API xoá trả lỗi", "API xoá trả lỗi", "1. Xoá campaign Scheduled\n2. Backend trả lỗi\n3. Quan sát toast", "Response lỗi", "Hiển thị toast: Failed to delete campaign.", "Cao"))
    add(tc("TC-DEL-TH-004", "Tích hợp", "FE hiển thị toast trạng thái không hợp lệ khi backend báo campaign không còn Scheduled", "Campaign chuyển trạng thái trong lúc thao tác", "1. Mở danh sách khi campaign Scheduled\n2. Backend đổi trạng thái\n3. Xác nhận xoá", "Response trạng thái không hợp lệ", "Hiển thị toast: Campaign cannot be deleted in current status.", "Cao"))
    add(tc("TC-DEL-TH-005", "Tích hợp", "Danh sách refresh sau khi xoá thành công", "API xoá trả thành công", "1. Xoá campaign Scheduled\n2. Kiểm tra request tải lại danh sách hoặc dữ liệu UI", "Campaign vừa xoá", "Danh sách được cập nhật lại; campaign vừa xoá biến mất.", "Cao"))
    add(tc("TC-DEL-TH-006", "Tích hợp", "Dữ liệu database đánh dấu/xoá campaign đúng bản ghi", "Có quyền kiểm tra database/log backend", "1. Xoá campaign Scheduled thành công\n2. Kiểm tra database/log", "Campaign ID", "Bản ghi campaign tương ứng được xoá hoặc đánh dấu xoá theo thiết kế; không ảnh hưởng bản ghi khác. Requirement cần xác nhận hard delete hay soft delete.", "Cao"))
    add(tc("TC-DEL-TH-007", "Tích hợp", "Rollback dữ liệu khi API xoá thất bại giữa chừng", "Có thể giả lập lỗi backend/database", "1. Gửi request xoá campaign Scheduled\n2. Giả lập lỗi trong quá trình xử lý\n3. Kiểm tra danh sách/database", "Lỗi transaction", "Campaign không bị xoá dở dang; dữ liệu nhất quán. Requirement cần xác nhận cơ chế transaction.", "Cao"))
    add(tc("TC-DEL-TH-008", "Tích hợp", "Xử lý lỗi mất kết nối khi xác nhận xoá", "Popup xác nhận xoá đang mở; có thể giả lập mất mạng", "1. Nhập OTP hợp lệ\n2. Ngắt mạng hoặc giả lập timeout\n3. Click Delete", "Network timeout", "Không xoá nếu request chưa thành công; UI hiển thị lỗi thất bại hoặc trạng thái retry theo chuẩn CMS. Requirement cần xác nhận message.", "Cao"))
    add(tc("TC-DEL-TH-009", "Tích hợp", "Không còn dữ liệu campaign đã xoá trong kết quả search/filter", "Campaign đã xoá thành công", "1. Search theo Code campaign đã xoá\n2. Search theo tên campaign đã xoá\n3. Lọc trạng thái Scheduled", "Code/tên campaign đã xoá", "Campaign đã xoá không xuất hiện trong mọi kết quả tìm kiếm/lọc.", "Cao"))

    # Hồi quy
    add(tc("TC-DEL-RG-001", "Hồi quy", "Không ảnh hưởng chức năng tạo campaign sau khi xoá", "Sau khi xoá một campaign thành công", "1. Mở màn Create\n2. Tạo campaign Scheduled hợp lệ\n3. Kiểm tra danh sách", "Dữ liệu tạo hợp lệ", "Tạo campaign vẫn hoạt động đúng; campaign mới hiển thị trên danh sách.", "Cao"))
    add(tc("TC-DEL-RG-002", "Hồi quy", "Không ảnh hưởng chức năng chỉnh sửa campaign còn lại", "Danh sách còn campaign Scheduled/Active/Inactive", "1. Xoá một campaign Scheduled\n2. Click Edit campaign khác\n3. Lưu thay đổi hợp lệ", "Campaign khác", "Chức năng chỉnh sửa campaign khác vẫn hoạt động đúng.", "Cao"))
    add(tc("TC-DEL-RG-003", "Hồi quy", "Không ảnh hưởng chức năng xem chi tiết campaign còn lại", "Danh sách còn campaign khác sau khi xoá", "1. Xoá campaign Scheduled\n2. Click View campaign khác", "Campaign khác", "Màn xem chi tiết mở đúng dữ liệu campaign được chọn.", "Trung bình"))
    add(tc("TC-DEL-RG-004", "Hồi quy", "Không ảnh hưởng search/filter danh sách sau khi xoá", "Đã xoá campaign thành công", "1. Thực hiện search theo code/tên\n2. Lọc theo Status, Customer Segment, Position, Effective Period", "Điều kiện lọc hợp lệ", "Search/filter vẫn trả kết quả đúng theo SRS danh sách.", "Cao"))
    add(tc("TC-DEL-RG-005", "Hồi quy", "Không ảnh hưởng export danh sách/report sau khi xoá", "Đã xoá campaign thành công; có quyền Export", "1. Mở popup Export\n2. Chọn điều kiện export\n3. Xuất file", "Điều kiện export hợp lệ", "Export vẫn hoạt động; campaign đã xoá không xuất hiện nếu rule export loại trừ campaign đã xoá.", "Trung bình"))
    add(tc("TC-DEL-RG-006", "Hồi quy", "Không ảnh hưởng rule hiển thị campaign trên App", "Có campaign Active khác đang hiển thị trên App", "1. Xoá campaign Scheduled trên CMS\n2. Kiểm tra campaign Active khác trên App/API hiển thị", "Campaign Active khác", "Campaign Active khác không bị ảnh hưởng bởi thao tác xoá campaign Scheduled.", "Cao"))
    add(tc("TC-DEL-RG-007", "Hồi quy", "Không ảnh hưởng chuẩn toast/confirm chung của CMS", "Có các màn CMS khác dùng toast/confirm", "1. Xoá campaign thành công/thất bại\n2. Kiểm tra toast/confirm ở màn liên quan khác", "Toast success/error", "Cơ chế toast/confirm chung vẫn hoạt động ổn định.", "Trung bình"))

    # UI/UX
    add(tc("TC-DEL-UI-001", "UI/UX", "Icon Delete hiển thị đúng vị trí trong cột Action", "Danh sách có campaign Scheduled", "1. Mở danh sách campaign\n2. Quan sát cột Action", "Campaign Scheduled", "Icon Delete hiển thị rõ ràng, cùng hàng với campaign tương ứng, không lệch layout.", "Thấp"))
    add(tc("TC-DEL-UI-002", "UI/UX", "Icon Delete disabled/ẩn dễ phân biệt với trạng thái không được xoá", "Danh sách có Active/Inactive/Expired", "1. Mở danh sách\n2. Quan sát icon Delete ở từng trạng thái", "Campaign Active, Inactive, Expired", "Icon Delete bị ẩn hoặc disabled theo thiết kế; không gây hiểu nhầm là có thể xoá.", "Trung bình"))
    add(tc("TC-DEL-UI-003", "UI/UX", "Popup xác nhận xoá căn chỉnh đúng và không che khuất nội dung quan trọng", "Click Delete campaign Scheduled", "1. Mở popup xác nhận xoá\n2. Quan sát layout popup", "Không áp dụng", "Popup hiển thị ở vị trí phù hợp, nội dung dễ đọc, không bị tràn/chồng lấn.", "Thấp"))
    add(tc("TC-DEL-UI-004", "UI/UX", "Nút Cancel và Delete trong popup hiển thị đúng trạng thái", "Popup xác nhận xoá đang mở", "1. Quan sát hai nút trong popup\n2. Hover/focus nếu có", "Không áp dụng", "Nút Cancel và Delete hiển thị rõ vai trò; trạng thái hover/focus/loading đúng chuẩn UI CMS.", "Thấp"))
    add(tc("TC-DEL-UI-005", "UI/UX", "Nút Delete trong popup chuyển loading/disabled khi đang gọi API", "API xoá phản hồi chậm", "1. Nhập OTP hợp lệ\n2. Click Delete\n3. Quan sát button trong lúc chờ phản hồi", "Network chậm", "Button Delete chuyển trạng thái loading hoặc disabled để người dùng biết đang xử lý và tránh bấm lặp.", "Trung bình"))
    add(tc("TC-DEL-UI-006", "UI/UX", "Toast thành công hiển thị đúng vị trí và tự đóng theo chuẩn CMS", "Xoá campaign thành công", "1. Xác nhận xoá thành công\n2. Quan sát toast", "Toast success", "Toast success hiển thị đúng nội dung, đúng vị trí và tự đóng theo chuẩn CMS.", "Thấp"))
    add(tc("TC-DEL-UI-007", "UI/UX", "Toast thất bại hiển thị đúng vị trí và không làm mất dữ liệu đang xem", "Xoá campaign thất bại", "1. Xác nhận xoá nhưng API trả lỗi\n2. Quan sát toast và danh sách", "Toast error", "Toast error hiển thị đúng nội dung; danh sách vẫn hiển thị campaign chưa xoá.", "Trung bình"))
    add(tc("TC-DEL-UI-008", "UI/UX", "Responsive màn danh sách vẫn thao tác xoá được theo chuẩn CMS", "Truy cập CMS ở kích thước màn hình được hỗ trợ", "1. Thu nhỏ/phóng to viewport theo chuẩn dự án\n2. Mở danh sách\n3. Click Delete campaign Scheduled", "Viewport desktop/tablet nếu CMS hỗ trợ", "Cột Action và popup xác nhận xoá vẫn hiển thị dùng được, không tràn màn hình.", "Thấp"))
    add(tc("TC-DEL-UI-009", "UI/UX", "Điều hướng bàn phím trong popup xác nhận xoá", "Popup xác nhận xoá đang mở", "1. Dùng Tab/Shift+Tab di chuyển focus\n2. Dùng Enter/Escape theo chuẩn CMS", "Keyboard navigation", "Focus di chuyển hợp lý giữa OTP, Cancel, Delete; thao tác bàn phím không gây xoá ngoài ý muốn.", "Thấp"))
    add(tc("TC-DEL-UI-010", "UI/UX", "Nội dung popup xác nhận xoá không bị sai chính tả so với SRS", "Popup xác nhận xoá đang mở", "1. Mở popup xác nhận\n2. Đối chiếu nội dung hiển thị", "Không áp dụng", "Nội dung hiển thị đúng: Are you sure you want to delete this campaign?", "Thấp"))
    return rows


def build_sheets():
    cases = build_delete_cases()
    overview = [
        ["Hạng mục", "Nội dung"],
        ["Tên chức năng", "CMS_Popup Xoá campaign"],
        ["Nguồn yêu cầu", "SRS CMS Pop-up - Chiến dịch Marketing, mục 4.2 CMS_Popup Xoá campaign"],
        ["Phạm vi", "Xoá campaign từ màn danh sách, chỉ cho phép trạng thái Scheduled, popup xác nhận có OTP, Cancel/Delete, gọi API, toast thành công/thất bại, refresh danh sách và kiểm soát trạng thái thay đổi."],
        ["Ngoài phạm vi", "Tạo campaign, chỉnh sửa campaign, export báo cáo chi tiết và logic hiển thị popup trên App ngoài kiểm tra hồi quy liên quan."],
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
        ["Ca kiểm thử tích cực", 18],
        ["Ca kiểm thử âm tính", 26],
        ["Ca kiểm thử biên/cạnh tranh dữ liệu", 8],
        ["Ca UI/UX", categories.get("UI/UX", 0)],
        ["Ca phân quyền", categories.get("Phân Quyền", 0)],
        ["Ưu tiên Cao", priorities.get("Cao", 0)],
        ["Ưu tiên Trung bình", priorities.get("Trung bình", 0)],
        ["Ưu tiên Thấp", priorities.get("Thấp", 0)],
        ["Phân bổ theo danh mục", "; ".join(f"{k}: {v}" for k, v in categories.items())],
    ]
    risks = [
        ["Loại", "Nội dung", "Khuyến nghị"],
        ["Requirement cần xác nhận", "SRS chưa nêu rule OTP chi tiết: bắt buộc/rỗng/sai/hết hạn/resend/retry/định dạng.", "BA/PO cần chốt rule OTP để bổ sung expected result và message cụ thể."],
        ["Requirement cần xác nhận", "SRS chưa nêu hard delete hay soft delete trong database.", "Xác nhận cơ chế lưu vết xoá, audit log và khả năng khôi phục nếu có."],
        ["Requirement cần xác nhận", "SRS chưa nêu message khi xoá campaign không tồn tại hoặc đã bị user khác xoá.", "Bổ sung mã lỗi/message để FE xử lý nhất quán."],
        ["Requirement cần xác nhận", "Sau khi xoá thành công, danh sách giữ nguyên search/filter hay reset filter chưa được mô tả rõ.", "Chốt hành vi refresh danh sách sau thao tác xoá."],
        ["Requirement cần xác nhận", "Icon Delete với Active/Inactive/Expired được phép ẩn hoặc disabled, chưa chốt một phương án UI duy nhất.", "Chốt theo mockup/design system để testcase UI có expected cố định."],
        ["Rủi ro", "Điều kiện chỉ xoá Scheduled phụ thuộc trạng thái thời gian thực; dễ xảy ra race condition khi job đổi trạng thái.", "Ưu tiên test đồng thời FE, API và backend state check."],
        ["Khuyến nghị", "Nên tự động hoá smoke test xoá thành công, cancel popup, trạng thái không hợp lệ và duplicate click.", "Đưa các ca ưu tiên Cao vào regression suite."],
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
