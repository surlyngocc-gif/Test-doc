<!-- TC_META
{
  "version":"1.0",
  "generated_at":"2026-07-31",
  "generator":"QA Copilot",
  "mode":"Generate",
  "source":"docs/requirements/docsaff_v1/srs/tenant-management-module-04-template.md"
}
-->

# Tổng quan Requirement

| Requirement ID | Mô tả |
|---------------|--------|
| REQ-001 | Admin/Ops đã đăng nhập và có quyền `tenant.read` được mở màn hình Tenant List. |
| REQ-002 | Danh sách truy vấn Tenant theo filter và mặc định sắp xếp `updated_at` giảm dần. |
| REQ-003 | Keyword tìm theo Tenant ID, Tenant code hoặc Tenant name; giới hạn tối đa 100 ký tự. |
| REQ-004 | Status filter gồm Tất cả, Draft, Active, Inactive; mặc định Tất cả. |
| REQ-005 | Account owner filter được hỗ trợ khi hệ thống có dữ liệu owner. |
| REQ-006 | Updated period filter được hỗ trợ khi UI có chức năng này. |
| REQ-007 | Bảng hiển thị Tenant ID, Tenant code, Tenant name, Status, Contact, Brand/Offer, Commission, Updated và Actions. |
| REQ-008 | Tenant Inactive vẫn xuất hiện trong CMS khi filter cho phép. |
| REQ-009 | Danh sách không hiển thị domain, branding hoặc locale configuration. |
| REQ-010 | Khi truy vấn không có kết quả, UI hiển thị empty state. |
| REQ-011 | User không có `tenant.read` nhận access denied ở UI và API. |
| REQ-012 | Action Chi tiết/Sửa hiển thị theo quyền và điều hướng đến màn tương ứng. |
| REQ-013 | Thao tác chỉ xem/lọc không làm thay đổi dữ liệu Tenant. |
| REQ-014 | Danh sách hỗ trợ pagination khi dữ liệu lớn. |
| REQ-015 | Khi Tenant Service lỗi, UI hiển thị lỗi rõ ràng và không hiển thị dữ liệu sai như kết quả mới. |
| REQ-016 | CMS hỗ trợ Chrome, Edge và Firefox bản hiện đại trên desktop/laptop. |

# Đánh giá Risk

| Requirement | Risk Score | Risk Level | Priority | Lý do |
|-------------|-----------|-----------|----------|--------|
| REQ-001 | 4.4 | High | Critical | Là cổng truy cập dữ liệu quản trị Tenant. |
| REQ-002 | 3.6 | Medium | High | Thứ tự dữ liệu ảnh hưởng vận hành hằng ngày. |
| REQ-003 | 4.0 | High | High | Input người dùng và ba trường tìm kiếm, dễ sai coverage hoặc injection. |
| REQ-004 | 3.4 | Medium | High | Trạng thái quyết định tập Tenant hiển thị. |
| REQ-005 | 2.8 | Medium | Medium | Filter phụ thuộc dữ liệu owner và UI. |
| REQ-006 | 2.8 | Medium | Medium | Filter thời gian có boundary và phụ thuộc UI. |
| REQ-007 | 3.8 | Medium | High | Dữ liệu tổng hợp từ nhiều nguồn trên bảng. |
| REQ-008 | 3.8 | Medium | High | Thiếu Tenant Inactive gây mất khả năng quản trị. |
| REQ-009 | 4.0 | High | High | Ngăn lộ cấu hình nội bộ ngoài phạm vi màn hình. |
| REQ-010 | 2.6 | Medium | Medium | Empty state cần phân biệt với lỗi hệ thống. |
| REQ-011 | 4.8 | High | Critical | Kiểm soát truy cập ở cả UI và API. |
| REQ-012 | 4.2 | High | High | Action phải khớp permission và điều hướng. |
| REQ-013 | 4.0 | High | High | Truy vấn read-only không được gây side effect. |
| REQ-014 | 3.6 | Medium | High | Dữ liệu lớn cần phân trang không thiếu/trùng bản ghi. |
| REQ-015 | 4.0 | High | High | Lỗi integration không được gây hiểu sai dữ liệu. |
| REQ-016 | 2.4 | Low | Medium | Yêu cầu tương thích trình duyệt quản trị. |

# Traceability Matrix

| Requirement | Test Case |
|-------------|-----------|
| REQ-001 | TC-001, TC-002 |
| REQ-002 | TC-003 |
| REQ-003 | TC-004, TC-005, TC-006, TC-007, TC-008, TC-009 |
| REQ-004 | TC-010, TC-011 |
| REQ-005 | TC-012 |
| REQ-006 | TC-013 |
| REQ-007 | TC-014, TC-015, TC-016 |
| REQ-008 | TC-017 |
| REQ-009 | TC-018, TC-019 |
| REQ-010 | TC-020 |
| REQ-011 | TC-021, TC-022, TC-023 |
| REQ-012 | TC-024, TC-025, TC-026 |
| REQ-013 | TC-027 |
| REQ-014 | TC-028, TC-029 |
| REQ-015 | TC-030 |
| REQ-016 | TC-031 |

# Test Case

| TC ID | Requirement | Category | Priority | Risk | Test Case Name | Preconditions | Test Data | Steps | Expected Result | Technique | Status | Remark |
|------|-------------|--------|----------|------|---------------|--------------|-----------|-------|----------------|-----------|--------|--------|
| TC-001 | REQ-001 | Functional | Critical | High | Mở Tenant List bằng tài khoản có quyền tenant.read | User đã đăng nhập CMS.<br>User có quyền `tenant.read`. |  | 1. Chọn menu Tenant Management.<br>2. Quan sát màn hình được tải. | - Tenant List được mở.<br>- Khu vực filter và bảng Tenant được hiển thị.<br>- Hệ thống gửi truy vấn đọc danh sách Tenant. | Use Case |  |  |
| TC-002 | REQ-001 | Navigation | High | High | Mở Tenant List từ menu Tenant Management | User đã đăng nhập CMS.<br>User có quyền `tenant.read`. |  | 1. Mở một module CMS khác.<br>2. Chọn Tenant Management từ menu. | - URL/màn hình chuyển sang Tenant List.<br>- Menu Tenant Management thể hiện trạng thái đang được chọn. | Use Case |  |  |
| TC-003 | REQ-002 | Business Rule | High | Medium | Kiểm tra thứ tự mặc định theo updated_at giảm dần | User đã đăng nhập CMS và có `tenant.read`.<br>Có ít nhất 3 Tenant với `updated_at` khác nhau. | T1: 30/07/2026 10:00<br>T2: 31/07/2026 09:00<br>T3: 29/07/2026 15:00 | 1. Mở Tenant List với filter mặc định.<br>2. Ghi nhận thứ tự ba Tenant. | - T2 đứng trước T1.<br>- T1 đứng trước T3.<br>- Thứ tự tuân theo `updated_at` giảm dần. | Decision Table |  |  |
| TC-004 | REQ-003 | Functional | High | High | Tìm Tenant bằng Tenant ID | User có `tenant.read`.<br>Tenant có ID xác định đã tồn tại. | Tenant ID: `TEN-0001` | 1. Nhập `TEN-0001` vào Keyword.<br>2. Áp dụng filter. | - Kết quả chứa Tenant có ID `TEN-0001`.<br>- Không có bản ghi không thỏa keyword trong tập kết quả. | EP |  |  |
| TC-005 | REQ-003 | Functional | High | High | Tìm Tenant bằng Tenant code | User có `tenant.read`.<br>Tenant có code xác định đã tồn tại. | Tenant code: `VNA_LOYALTY` | 1. Nhập `VNA_LOYALTY` vào Keyword.<br>2. Áp dụng filter. | - Kết quả chứa Tenant có code `VNA_LOYALTY`.<br>- Không có bản ghi không thỏa keyword trong tập kết quả. | EP |  |  |
| TC-006 | REQ-003 | Functional | High | High | Tìm Tenant bằng Tenant name | User có `tenant.read`.<br>Tenant có name xác định đã tồn tại. | Tenant name: `Vietnam Airlines Loyalty` | 1. Nhập `Vietnam Airlines Loyalty` vào Keyword.<br>2. Áp dụng filter. | - Kết quả chứa Tenant có name `Vietnam Airlines Loyalty`.<br>- Không có bản ghi không thỏa keyword trong tập kết quả. | EP |  |  |
| TC-007 | REQ-003 | Boundary | High | High | Tìm kiếm với Keyword dài đúng 100 ký tự | User có `tenant.read`. | Chuỗi Keyword dài đúng 100 ký tự | 1. Nhập chuỗi 100 ký tự vào Keyword.<br>2. Áp dụng filter. | - UI chấp nhận đủ 100 ký tự.<br>- Request filter được xử lý.<br>- UI hiển thị danh sách kết quả hoặc empty state theo dữ liệu. | BVA |  |  |
| TC-008 | REQ-003 | Boundary | High | High | Nhập Keyword dài 101 ký tự | User có `tenant.read`. | Chuỗi Keyword dài 101 ký tự | 1. Nhập chuỗi 101 ký tự vào Keyword.<br>2. Áp dụng filter. | - Hệ thống không xử lý quá 100 ký tự như một keyword hợp lệ không kiểm soát.<br>- Hành vi trim hoặc thông báo lỗi cần tuân theo policy được BA/PO xác nhận. | BVA |  | Blocked bởi OQ-01. |
| TC-009 | REQ-003 | Security | Critical | High | Keyword chứa payload injection không làm thay đổi câu truy vấn | User có `tenant.read`. | `' OR 1=1 --`<br>`<script>alert(1)</script>` | 1. Nhập lần lượt từng payload vào Keyword.<br>2. Áp dụng filter.<br>3. Quan sát response và UI. | - Không trả toàn bộ dữ liệu do điều kiện injection.<br>- Không thực thi script trên trình duyệt.<br>- Không hiển thị stack trace, câu SQL hoặc thông tin kỹ thuật nhạy cảm. | Error Guessing |  | Security áp dụng vì có input người dùng. |
| TC-010 | REQ-004 | Functional | High | Medium | Kiểm tra giá trị mặc định và danh mục Status | User có `tenant.read`. |  | 1. Mở Tenant List.<br>2. Mở dropdown Status. | - Giá trị mặc định là `Tất cả`.<br>- Dropdown có đúng bốn lựa chọn: Tất cả, Draft, Active, Inactive. | EP |  |  |
| TC-011 | REQ-004, REQ-008 | Functional | High | Medium | Lọc danh sách theo từng Status | User có `tenant.read`.<br>Có Tenant Draft, Active và Inactive. | Draft, Active, Inactive | 1. Chọn lần lượt từng Status.<br>2. Áp dụng filter sau mỗi lần chọn.<br>3. Kiểm tra status của mọi dòng kết quả. | - Khi chọn Draft, mọi dòng có Status Draft.<br>- Khi chọn Active, mọi dòng có Status Active.<br>- Khi chọn Inactive, mọi dòng có Status Inactive. | EP |  |  |
| TC-012 | REQ-005 | Functional | Medium | Medium | Lọc theo Account owner khi có dữ liệu owner | User có `tenant.read`.<br>UI có Account owner filter.<br>Có Tenant thuộc owner xác định. | Account owner: `Minh Nguyen` | 1. Chọn `Minh Nguyen` tại Account owner.<br>2. Áp dụng filter. | - Mọi Tenant trả về có account owner `Minh Nguyen`.<br>- Tenant thuộc owner khác không xuất hiện. | EP |  | Chỉ thực thi nếu hệ thống có dữ liệu owner. |
| TC-013 | REQ-006 | Functional | Medium | Medium | Lọc theo Updated period khi UI hỗ trợ | User có `tenant.read`.<br>UI có Updated period filter.<br>Có dữ liệu trong và ngoài kỳ chọn. | Updated period: 7 ngày | 1. Chọn kỳ `7 ngày`.<br>2. Áp dụng filter.<br>3. Đối chiếu `updated_at` của kết quả với kỳ chọn. | - Mọi bản ghi trả về nằm trong kỳ đã chọn theo policy thời gian của hệ thống.<br>- Bản ghi ngoài kỳ không xuất hiện. | BVA |  | Boundary thời gian/timezone cần OQ-03. |
| TC-014 | REQ-007 | UI | High | Medium | Kiểm tra header bảng Tenant List | User có `tenant.read`. |  | 1. Mở Tenant List.<br>2. Quan sát header bảng. | - Header có Tenant ID, Tenant code, Tenant name, Status, Contact, Brand/Offer, Commission, Updated và Actions.<br>- Không thiếu hoặc lặp cột. | Experience Based |  |  |
| TC-015 | REQ-007 | Integration | High | Medium | Kiểm tra mapping dữ liệu từng dòng Tenant | User có `tenant.read`.<br>Có Tenant với dữ liệu đã biết. | Tenant có ID, code, name, status, contact, số Brand/Offer, số Brand có revenue share, updated_at/by | 1. Mở Tenant List.<br>2. Tìm Tenant dữ liệu mẫu.<br>3. Đối chiếu từng cột với nguồn dữ liệu. | - Tenant ID/code/name/status/contact khớp bản ghi nguồn.<br>- Brand/Offer và Commission khớp dữ liệu tổng hợp.<br>- Updated hiển thị ngày và người cập nhật cuối. | Use Case |  |  |
| TC-016 | REQ-007 | UI | Medium | Medium | Hiển thị Commission là dấu gạch khi chưa cấu hình | User có `tenant.read`.<br>Có Tenant chưa có Brand cấu hình revenue share. | Tenant chưa cấu hình revenue share | 1. Mở Tenant List.<br>2. Tìm Tenant dữ liệu mẫu.<br>3. Quan sát cột Commission. | - Cột Commission hiển thị `-` cho Tenant chưa có cấu hình revenue share. | EP |  |  |
| TC-017 | REQ-008 | Business Rule | High | Medium | Tenant Inactive vẫn xuất hiện trong CMS | User có `tenant.read`.<br>Có Tenant Inactive. | Status filter: Tất cả và Inactive | 1. Mở danh sách với Status = Tất cả.<br>2. Xác nhận Tenant Inactive xuất hiện.<br>3. Lọc Status = Inactive. | - Tenant Inactive xuất hiện khi Status = Tất cả.<br>- Tenant Inactive xuất hiện khi Status = Inactive.<br>- Badge của dòng là Inactive. | Decision Table |  |  |
| TC-018 | REQ-009 | Security | Critical | High | Không hiển thị domain, branding và locale config trên bảng | User có `tenant.read`.<br>Tenant có domain/branding/locale đã cấu hình. | Domain, logo/theme và locale của Tenant mẫu | 1. Mở Tenant List.<br>2. Quan sát header và dữ liệu từng dòng. | - Không có cột/field domain.<br>- Không có logo/theme/branding config.<br>- Không có locale config. | Risk Based |  |  |
| TC-019 | REQ-009 | API | Critical | High | API Tenant List không trả field ngoài phạm vi màn hình | User có session hợp lệ và `tenant.read`. | Request danh sách Tenant hợp lệ | 1. Gửi request tải Tenant List.<br>2. Kiểm tra payload response. | - Response không chứa secret hoặc API key.<br>- Domain/branding/locale config không được trả nếu endpoint chỉ phục vụ contract của Tenant List. | Risk Based |  | Endpoint/schema chưa được nêu; kiểm tra theo contract triển khai. |
| TC-020 | REQ-010 | Exception | High | Medium | Hiển thị empty state khi filter không có kết quả | User có `tenant.read`. | Keyword không khớp Tenant nào | 1. Nhập keyword không tồn tại.<br>2. Áp dụng filter. | - Bảng không hiển thị dòng Tenant.<br>- UI hiển thị empty state.<br>- Empty state không bị hiển thị như lỗi hệ thống. | EP |  | Nội dung message chưa được requirement quy định. |
| TC-021 | REQ-011 | Permission | Critical | High | User không có tenant.read không mở được Tenant List từ menu | User đã đăng nhập CMS.<br>User không có `tenant.read`. |  | 1. Quan sát menu CMS.<br>2. Thử mở Tenant Management nếu menu vẫn hiển thị. | - User không truy cập được Tenant List.<br>- UI hiển thị access denied khi có yêu cầu truy cập. | Decision Table |  | Việc ẩn menu hay giữ menu chưa được chốt. |
| TC-022 | REQ-011 | Permission | Critical | High | Truy cập trực tiếp URL Tenant List khi không có quyền | User đã đăng nhập CMS.<br>User không có `tenant.read`.<br>Biết URL Tenant List. | URL Tenant List | 1. Nhập trực tiếp URL Tenant List trên trình duyệt. | - Tenant List và dữ liệu Tenant không được hiển thị.<br>- User nhận access denied. | Error Guessing |  |  |
| TC-023 | REQ-011 | API | Critical | High | Gọi API Tenant List khi không có tenant.read | User có session hợp lệ nhưng không có `tenant.read`. | Request Tenant List hợp lệ | 1. Gửi request tải Tenant List bằng session không có quyền.<br>2. Kiểm tra response. | - Backend từ chối request.<br>- Response không chứa bản ghi Tenant.<br>- Mã HTTP/error phải theo security policy đã phê duyệt. | Decision Table |  | HTTP status chưa được requirement quy định. |
| TC-024 | REQ-012 | Permission | High | High | Hiển thị action Chi tiết cho user có tenant.read | User có `tenant.read`.<br>Có ít nhất một Tenant. |  | 1. Mở Tenant List.<br>2. Mở Actions của một Tenant. | - Action Chi tiết được hiển thị.<br>- Action không được cấp quyền không được cung cấp để thực thi. | Decision Table |  |  |
| TC-025 | REQ-012 | Navigation | High | High | Điều hướng từ action Chi tiết đến Tenant Detail | User có `tenant.read`.<br>Có Tenant xác định. | Tenant ID: `TEN-0001` | 1. Mở Actions của `TEN-0001`.<br>2. Chọn Chi tiết. | - Màn Tenant Detail của `TEN-0001` được mở.<br>- Không mở dữ liệu của Tenant khác. | Use Case |  |  |
| TC-026 | REQ-012 | Permission | High | High | Action Sửa tuân theo quyền update | User A có `tenant.read` và `tenant.update`.<br>User B chỉ có `tenant.read`.<br>Có Tenant xác định. |  | 1. Đăng nhập bằng User A và mở Actions.<br>2. Ghi nhận action Sửa.<br>3. Đăng nhập bằng User B và mở Actions.<br>4. Thử truy cập trực tiếp URL sửa bằng User B. | - User A nhìn thấy và mở được action Sửa.<br>- User B không thực thi được action Sửa từ UI.<br>- User B truy cập trực tiếp URL/API sửa bị từ chối. | Decision Table |  |  |
| TC-027 | REQ-013 | Database | High | High | Xem và lọc không làm thay đổi dữ liệu Tenant | User có `tenant.read`.<br>Có snapshot dữ liệu Tenant trước kiểm thử. | Bộ filter hợp lệ | 1. Mở Tenant List.<br>2. Áp dụng nhiều filter và chuyển trang.<br>3. Đối chiếu dữ liệu Tenant trước/sau. | - Không có field Tenant nào thay đổi do thao tác xem/lọc.<br>- Không phát sinh create/update/deactivate Tenant.<br>- `updated_at` không đổi chỉ vì đọc danh sách. | Risk Based |  |  |
| TC-028 | REQ-014 | Functional | High | Medium | Chuyển trang khi dữ liệu vượt page size | User có `tenant.read`.<br>Số Tenant lớn hơn page size cấu hình. | Dữ liệu ít nhất 2 trang | 1. Mở Tenant List.<br>2. Ghi nhận bản ghi trang 1.<br>3. Chuyển sang trang 2. | - Trang 2 được tải.<br>- Không lặp bản ghi giữa trang 1 và trang 2 trong cùng snapshot/sort.<br>- Thứ tự `updated_at` giảm dần được duy trì. | BVA |  | Page size chưa được quy định. |
| TC-029 | REQ-014 | Boundary | High | Medium | Điều hướng tại trang đầu và trang cuối | User có `tenant.read`.<br>Dữ liệu có nhiều trang. |  | 1. Mở trang đầu.<br>2. Thử điều hướng về trang trước.<br>3. Đi đến trang cuối.<br>4. Thử điều hướng sang trang sau. | - Không điều hướng tới số trang nhỏ hơn trang đầu.<br>- Không điều hướng tới số trang lớn hơn trang cuối.<br>- Danh sách hiện tại không bị mất do thao tác ngoài biên. | BVA |  |  |
| TC-030 | REQ-015 | Integration | Critical | High | Tenant Service lỗi khi tải danh sách | User có `tenant.read`.<br>Tenant Service được mô phỏng trả lỗi. | Lỗi/timeout từ Tenant Service | 1. Mở Tenant List khi Tenant Service lỗi.<br>2. Quan sát UI và dữ liệu. | - UI hiển thị trạng thái lỗi rõ ràng.<br>- UI không hiển thị empty state thay cho lỗi.<br>- UI không trình bày dữ liệu cũ như kết quả vừa tải.<br>- Không lộ stack trace hoặc chi tiết kỹ thuật nhạy cảm. | Error Guessing |  | Message/retry behavior chưa được quy định. |
| TC-031 | REQ-016 | Compatibility | Medium | Low | Hiển thị Tenant List trên các trình duyệt được hỗ trợ | Có Chrome, Edge và Firefox bản hiện đại trên desktop/laptop.<br>User có `tenant.read`. | Cùng một bộ dữ liệu Tenant | 1. Mở Tenant List trên Chrome.<br>2. Lặp lại trên Edge.<br>3. Lặp lại trên Firefox.<br>4. Thực hiện keyword/status filter trên từng trình duyệt. | - Filter, bảng, badge, action và pagination hiển thị đầy đủ trên cả ba trình duyệt.<br>- Không có control bị che khuất hoặc không thao tác được. | Experience Based |  | Chưa có version/browser matrix cụ thể. |

# Open Questions

1. Với Keyword dài hơn 100 ký tự, hệ thống trim về 100 ký tự hay hiển thị lỗi? Nội dung lỗi là gì?
2. Keyword search có phân biệt chữ hoa/thường, hỗ trợ partial match, trim khoảng trắng và Unicode normalization như thế nào?
3. Updated period có các lựa chọn chính thức nào, timezone nào và boundary ngày được tính inclusive hay exclusive?
4. Account owner và Updated period là bắt buộc trong MVP1 hay chỉ triển khai “nếu UI hỗ trợ”?
5. Page size mặc định, danh sách page-size option và hành vi giữ filter khi chuyển trang là gì?
6. Empty-state message và service-error message chính thức là gì?
7. User không có `tenant.read` bị ẩn menu hay nhìn thấy menu và nhận access denied khi click?
8. API Tenant List dùng endpoint, HTTP status, response schema, pagination contract và error code nào?
9. Contact hiển thị thế nào khi thiếu contact name hoặc contact email?
10. Số Brand/Offer và Commission được tính theo assigned, active hay toàn bộ lịch sử?
11. Các version Chrome, Edge, Firefox cụ thể nào thuộc browser matrix hỗ trợ?
12. Có yêu cầu SLA cho Tenant List/filter không? NFR 3 giây hiện chỉ nêu rõ cho Tenant Portal User filter.

# Statistics

| Nội dung | Giá trị |
|----------|---------|
| Tổng Requirement | 16 |
| Tổng Test Case | 31 |
| Positive | 15 |
| Negative | 8 |
| Boundary | 5 |
| Permission | 6 |
| Security | 4 |
| Integration | 4 |
| High Risk | 8 |
| Medium Risk | 7 |
| Low Risk | 1 |
| Coverage | 100% |
