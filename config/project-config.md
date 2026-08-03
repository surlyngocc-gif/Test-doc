# Project Configuration

Phiên bản: 1.0

Tài liệu này định nghĩa toàn bộ cấu hình mặc định của dự án.

Mọi AI Agent và Skill trong QA Copilot PHẢI đọc tài liệu này trước khi thực hiện bất kỳ tác vụ nào.

Không được hardcode đường dẫn, ngôn ngữ, định dạng hoặc quy ước trong từng Skill.

---

# 1. Thông tin dự án

Tên dự án

Loyalty Platform

Mô tả

Hệ thống quản lý khách hàng thân thiết, tích điểm và đổi thưởng.

---

# 2. Ngôn ngữ

Ngôn ngữ mặc định

Tiếng Việt

Ngôn ngữ Test Case

Tiếng Việt

Ngôn ngữ Review

Tiếng Việt

Ngôn ngữ Comment

Tiếng Việt

Nếu người dùng yêu cầu ngôn ngữ khác thì ưu tiên theo yêu cầu của người dùng.

---

# 3. Quy ước đặt tên

Requirement

```
US_<Tên>.md

CR_<Tên>.md

BRD_<Tên>.md

SRS_<Tên>.md
```

Test Case

```
TC_<Tên>.md
```

Review

```
REVIEW_TC_<Tên>.md
```

Automation

```
AUTO_<Tên>.spec.ts
```

---

# 4. Cấu trúc thư mục

Requirement

```
docs/requirements/
```

Test Case

```
docs/testcases/
```

Review

```
docs/reviews/
```

Automation

```
docs/automation/
```

Test Plan

```
docs/testplan/
```


Tài liệu thiết kế

```
docs/design/
```

Nếu thư mục chưa tồn tại.

Được phép tạo mới.

---

# 5. Quy tắc lưu file

Mặc định lưu:

Requirement

↓

docs/requirements/

Test Case

↓

docs/testcases/

Review

↓

docs/reviews/

Automation

↓

docs/automation/

Test Plan

↓

docs/testplan/

Không được ghi đè file nếu chưa được yêu cầu.

Nếu file đã tồn tại.

Thực hiện chế độ Update.

---

# 6. Định dạng Output

Test Case

Markdown (.md)

Review

Markdown (.md)

Test Plan

Mark down (.md)

Automation

TypeScript

Report

Markdown

Excel

Chỉ sinh khi người dùng yêu cầu.

---

# 7. Quy tắc ghi đè

Nếu file chưa tồn tại

→ Tạo mới.

Nếu file đã tồn tại

→ Cập nhật.

Không được xóa nội dung cũ nếu không có yêu cầu.

Phải giữ lịch sử thay đổi khi cập nhật.

---

# 8. Quy tắc đánh số

Requirement

```
REQ-001
REQ-002
REQ-003
```

Test Case

```
TC-001
TC-002
TC-003
```

Không reset TC ID khi cập nhật.

---

# 9. Framework Automation

Framework

Playwright

Ngôn ngữ

TypeScript

Pattern

Page Object Model (POM)

---

# 10. Chuẩn Review

Quality Score tối thiểu

90

Critical

0

Major

0

Minor

Không giới hạn

Nếu chưa đạt.

Thực hiện Review Loop.

---

# 11. Quy tắc sinh Automation

Chỉ sinh Automation cho các Test Case:

- Có Regression Scope
- Có khả năng tự động hóa
- Không phụ thuộc thao tác thủ công
- Không yêu cầu xác minh bằng mắt

---

# 12. Cấu hình AI

Mặc định sử dụng:

- Risk-Based Testing
- ISTQB Test Design
- Traceability Matrix
- Requirement Coverage
- Review Loop

Không được bỏ qua các bước trên.

---

# 13. Quy tắc ưu tiên

Khi có xung đột.

Ưu tiên theo thứ tự:

1. Yêu cầu trực tiếp của người dùng.

2. project-config.md

3. SKILL.md

4. generation-rules.md

5. review-rules.md

6. template.md

7. risk-model.md

---

# 14. Các hành vi bị cấm

Không được:

- Hardcode đường dẫn trong Skill.
- Hardcode tên dự án.
- Hardcode ngôn ngữ.
- Hardcode định dạng Output.
- Ghi đè file khi chưa được yêu cầu.
- Thay đổi cấu trúc thư mục nếu không có chỉ định.

---

# 15. Self Check

Trước khi thực hiện bất kỳ tác vụ nào.

Kiểm tra:

✓ Đã đọc project-config.md.

✓ Đã xác định đúng thư mục Output.

✓ Đã xác định đúng ngôn ngữ.

✓ Đã xác định đúng định dạng Output.

✓ Đã xác định đúng quy tắc đặt tên file.

Nếu chưa hoàn thành.

Không được tiếp tục thực hiện.