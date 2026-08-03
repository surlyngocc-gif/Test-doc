---
name: gen-testcase
description: >
  Sinh mới hoặc cập nhật Test Case từ tài liệu Requirement (User Story, Change Request, BRD, SRS...),
  sau đó tự động review chất lượng theo vòng lặp cho đến khi đạt tiêu chuẩn hoặc hết số lần cho phép.
  Skill này chỉ đóng vai trò điều phối quy trình. Mọi quy tắc sinh Test Case và Review được định nghĩa
  trong các tài liệu tham chiếu.
---

# Gen TestCase Skill

## Mục đích

Tự động sinh hoặc cập nhật bộ Test Case chuyên nghiệp từ tài liệu Requirement theo quy trình chuẩn của QA.

Skill này chịu trách nhiệm điều phối quy trình làm việc, không chứa các quy tắc nghiệp vụ chi tiết.

---

# Tài liệu tham chiếu

Trước khi thực hiện, bắt buộc đọc và tuân thủ CHÍNH XÁC đầy đủ các tài liệu sau:

- `references/generation-rules.md` 
- `references/review-rules.md`

Nếu có xung đột giữa các tài liệu, ưu tiên theo thứ tự:

1. Yêu cầu trực tiếp của người dùng
2. SKILL.md
3. generation-rules.md
4. review-rules.md

---

# Khi nào sử dụng

Sử dụng Skill này khi người dùng muốn:

- Sinh Test Case từ User Story.
- Sinh Test Case từ Change Request.
- Sinh Test Case từ BRD hoặc SRS.
- Cập nhật Test Case sau khi Requirement thay đổi.
- Kiểm tra chất lượng bộ Test Case.
- Đảm bảo Test Case đạt tiêu chuẩn trước khi Release.
- Muốn biết Test Case còn thiếu gì, cần xác nhận thông tin gì với BA/PO
---

# Input

Hỗ trợ các loại tài liệu:

- User Story
- Change Request
- BRD
- SRS
- Requirement dạng Markdown

Ví dụ:

```
US_Login.md
CR_Payment.md
SRS_UserManagement.md
```

---

# Output

Sinh hai file:

```
TC_<Tên requirement>.md

REVIEW_TC_<Tên requirement>.md
```

# Quy trình thực hiện
## Bước 0: Khởi tạo và đọc cấu hình - Xác định thư mục Output

Trước khi tạo bất kỳ file nào, bắt buộc đọc `config/project-config.md` để lấy cấu hình thư mục.

Sử dụng các giá trị cấu hình sau:

- Requirements Folder
- TestCases Folder
- Reviews Folder
- Automation Folder

Sau đó lưu file đúng thư mục tương ứng.

Ví dụ

Requirement

docs/requirements/US_Login.md

↓

Test Case

docs/testcases/TC_Login.md

↓

Review

docs/reviews/REVIEW_TC_Login.md

Không được lưu file ở thư mục gốc của dự án.

Nếu thư mục chưa tồn tại thì tạo mới.

Nếu người dùng chỉ định đường dẫn khác thì ưu tiên theo yêu cầu của người dùng.

---


## Bước 1. Xác định chế độ làm việc

Kiểm tra sự tồn tại của file Test Case.

- Nếu chưa có → **Chế độ Tạo mới**
- Nếu đã có → **Chế độ Cập nhật**

Quy tắc cập nhật được định nghĩa trong `generation-rules.md`.

---

## Bước 2. Sinh hoặc cập nhật Test Case

Đọc tài liệu Requirement.

Sau đó thực hiện theo toàn bộ quy tắc trong:

`references/generation-rules.md`

Bao gồm nhưng không giới hạn:

- Phân tích Requirement
- Risk-Based Planning
- Traceability Matrix
- Sinh Test Case
- Quy tắc đặt tên
- Security Applicability
- Assumption Control
- Self Review

Không được lặp lại các quy tắc này trong SKILL.

---

## Bước 3. Review Test Case

Sau khi hoàn thành Test Case, thực hiện Review theo:

`references/review-rules.md`

Bao gồm:

- Coverage
- Depth
- Design Quality
- Optimization
- Quality Score
- Issue Classification
- Decision

Sinh file:

```
REVIEW_TC_<Tên requirement>.md
```

---

## Bước 4. Vòng lặp cải thiện

Nếu kết quả Review chưa đạt tiêu chuẩn thì:

- Chỉ sửa các Test Case liên quan.
- Không sinh lại toàn bộ nếu không cần thiết.
- Không thay đổi TC ID của các Test Case không bị ảnh hưởng.
- Không tự suy diễn Requirement.

Sau mỗi lần sửa:

- Thực hiện Review lại.
- Cập nhật file Review.

---

# Điều kiện hoàn thành

Quy trình được xem là hoàn thành khi đồng thời thỏa mãn:

- Quality Score ≥ 90
- Không còn Critical Issue
- Không còn Major Issue

Hoặc

Đã thực hiện đủ 05 vòng Review.

Nếu vẫn chưa đạt:

- Dừng quy trình.
- Ghi rõ nguyên nhân.
- Liệt kê các vấn đề còn tồn tại.
- Liệt kê các câu hỏi cần xác nhận với BA/PO.

---

# Xử lý lỗi

Dừng quy trình nếu xảy ra một trong các trường hợp sau:

- Không đọc được Requirement.
- File Requirement không tồn tại.
- Thiếu file Rule.
- Requirement bị lỗi định dạng.
- Không xác định được nội dung Requirement.

Không được tự suy diễn dữ liệu để tiếp tục.

---

# Kết quả trả về

Sau khi hoàn thành, trả về:

- Đường dẫn file Test Case.
- Đường dẫn file Review.
- Quality Score cuối cùng.
- Quyết định Review.
- Số vòng lặp đã thực hiện.
- Danh sách Issue còn tồn tại (nếu có).

Ví dụ:

```
✅ Đã hoàn thành

📄 Test Case:
TC_Login.md

📊 Review:
REVIEW_TC_Login.md

Quality Score: 95/100

Decision:
Approved

Iterations:
2/5
```

---

# Lưu ý

- Không được tự tạo Requirement.
- Không được bỏ qua bước Review.
- Không được bỏ qua Risk Assessment.
- Không được bỏ qua Traceability.
- Chỉ sinh Test Case dựa trên Requirement.
- Nếu Requirement chưa rõ, ghi nhận vào Open Questions thay vì tự suy diễn.

Mọi quy tắc chi tiết về sinh Test Case và Review đều được định nghĩa trong các tài liệu tham chiếu.
