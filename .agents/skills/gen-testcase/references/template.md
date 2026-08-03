# Test Case Output Template

Phiên bản: 1.0

Tài liệu này định nghĩa cấu trúc chuẩn của file Test Case.

Mọi AI Agent sinh Test Case đều PHẢI tuân thủ đúng định dạng dưới đây.

---

# 1. Metadata

Dòng đầu tiên của file phải là Metadata.

Ví dụ

```html
<!-- TC_META
{
  "version":"1.0",
  "generated_at":"2026-07-07",
  "generator":"QA Copilot",
  "mode":"Generate",
  "source":"US_Login.md"
}
-->
```

---

# 2. Requirement Summary

## Tổng quan Requirement

| Requirement ID | Mô tả |
|---------------|--------|
| REQ-001 | Người dùng đăng nhập bằng Email |
| REQ-002 | Password là bắt buộc |
| REQ-003 | Có nút Quên mật khẩu |

---

# 3. Risk Assessment

## Đánh giá Risk

| Requirement | Risk Score | Risk Level | Priority | Lý do |
|-------------|-----------|-----------|----------|--------|
|REQ-001|4.8|High|Critical|Liên quan xác thực người dùng|
|REQ-002|3.6|Medium|High|Validation dữ liệu|
|REQ-003|2.0|Low|Medium|Chức năng phụ|

---

# 4. Traceability Matrix

| Requirement | Test Case |
|-------------|-----------|
|REQ-001|TC-001, TC-002, TC-003|
|REQ-002|TC-004|
|REQ-003|TC-005|

Nếu Requirement chưa được cover.

Hiển thị

❌ Missing

---

# 5. Test Case

Sử dụng bảng Markdown.

| TC ID | Requirement | Category | Priority | Risk | Test Case Name | Preconditions | Test Data | Steps | Expected Result | Technique | Status | Remark |
|------|-------------|--------|----------|------|---------------|--------------|-----------|-------|----------------|-----------|--------|--------|

Ví dụ

|TC-001|REQ-001|Login|Critical|High|Đăng nhập thành công bằng Email hợp lệ|Đã mở màn hình Login|Email hợp lệ, Password hợp lệ|1. Nhập Email<br>2. Nhập Password<br>3. Click Login|Điều hướng tới Dashboard và hiển thị tên người dùng|EP| | |

---

# 6. Open Questions

Nếu Requirement thiếu thông tin.

Liệt kê.

Ví dụ

- Session timeout bao lâu?
- Có giới hạn số lần Login sai không?
- Password phân biệt chữ hoa chữ thường không?

Nếu không có.

Ghi

Không có.

---

# 7. Statistics

Thống kê cuối tài liệu.

| Nội dung | Giá trị |
|----------|---------|
|Tổng Requirement|3|
|Tổng Test Case|15|
|Positive|5|
|Negative|4|
|Boundary|2|
|Permission|1|
|Security|1|
|Integration|1|
|High Risk|1|
|Medium Risk|1|
|Low Risk|1|
|Coverage|100%|

---

# 8. Quy tắc đánh số

Requirement

```
REQ-001
REQ-002
REQ-003
```

---

Test Case

```
TC-001
TC-002
TC-003
```

Không reset TC ID giữa các Category.

---

# 9. Quy tắc Status

Khi sinh mới.

Để trống.

Ví dụ

```
Status:
```

Không tự điền

Pass

Fail

Blocked

---

# 10. Quy tắc Technique

Technique là bắt buộc.

Giá trị hợp lệ

- EP
- BVA
- Decision Table
- State Transition
- Pairwise
- Error Guessing
- Experience Based
- Use Case

---

# 11. Quy tắc Expected Result

Expected Result phải:

- Có thể kiểm chứng.
- Có thể đo lường.
- Không mơ hồ.
- Với test case  có nhiều Expected Result cần tách ra thành các dòng riêng và có gạch đầu dòng cho từng Expected

Ví dụ

✓ Hiển thị thông báo: "Password là bắt buộc"

✓ Điều hướng tới Dashboard.

✓ Database cập nhật trạng thái ACTIVE.

Không được viết

✗ Thành công, ✗ Hiển thị đúng;✗ Hoạt động bình thường

---

# 12. Quy tắc Preconditions

Mỗi Precondition phải
- Có thể đo lường
- Chỉ ghi điều kiện bắt buộc
- Không thể bị lặp lại trong Test Step
- Sử dụng cùng một cấu trúc trong toàn bộ dự án
Ví dụ
✓ User đã đăng nhập bằng tài khoản Merchant Admin.
✓ User có quyền Admin
✓ Merchant "ABC" đã tồn tại.
✓ Loyalty Program "Gold" đang Active.
✓ Point Balance của User = 500 điểm.
✓ Feature "Redeem Point" đã được bật.

# 13. Quy tắc Test Steps

Mỗi Step phải:

- Có hành động.
- Có dữ liệu đầu vào (nếu có).
- Theo đúng trình tự thực hiện.

Ví dụ

1. Nhập Email hợp lệ.
2. Nhập Password hợp lệ.
3. Click nút Login.

Không được viết tắt.

---

# 14. Quy tắc Test Data

Nếu có dữ liệu kiểm thử.

Phải ghi rõ.

Ví dụ

Email

```
qa@test.com
```

Password

```
123456Aa@
```

Nếu không yêu cầu.

Để trống.

---

# 15. Quy tắc Remark

Remark chỉ dùng cho:

- Lưu ý nghiệp vụ.
- Điều kiện đặc biệt.
- Dependency.
- Giới hạn của Test Case.

Không ghi thông tin dư thừa.

---

# 16. Output Format

Output phải theo đúng thứ tự.

1. Metadata

2. Requirement Summary

3. Risk Assessment

4. Traceability Matrix

5. Test Case

6. Open Questions

7. Statistics

Không được thay đổi thứ tự.

---

# 17. Các hành vi bị cấm

Không được:

- Bỏ Metadata.
- Thiếu Requirement Summary.
- Thiếu Risk Assessment.
- Thiếu Traceability Matrix.
- Thiếu Statistics.
- Thay đổi tên cột.
- Thay đổi thứ tự Output.
- Xuất dưới dạng HTML.
- Xuất dưới dạng CSV.

Output chuẩn là Markdown. Sau khi tạo file Markdown hãy dùng openpyxl để chuyển file Markdown vừa tạo thành Excel nếu người dùng yêu cầu.