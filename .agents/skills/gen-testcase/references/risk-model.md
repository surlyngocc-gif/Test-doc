# Risk Model

Phiên bản: 1.0

Tài liệu này định nghĩa mô hình đánh giá rủi ro (Risk Assessment) để xác định mức độ ưu tiên kiểm thử cho từng Requirement trước khi sinh Test Case.

Mọi AI Agent đều PHẢI thực hiện bước đánh giá Risk trước khi tạo Test Case.

---

# 1. Mục tiêu

Risk Assessment giúp:

- Xác định Requirement nào cần kiểm thử kỹ hơn.
- Xác định số lượng Test Case tối thiểu cần sinh.
- Xác định phạm vi Regression Test.
- Tối ưu thời gian kiểm thử.
- Ưu tiên nguồn lực QA.

Không được sinh Test Case trước khi hoàn thành Risk Assessment.

---

# 2. Quy trình đánh giá

Đối với mỗi Requirement.

Thực hiện lần lượt:

1. Phân tích Requirement.
2. Chấm điểm Risk.
3. Xác định Risk Level.
4. Xác định phạm vi kiểm thử.
5. Xác định Regression Scope.

---

# 3. Các tiêu chí đánh giá

Mỗi Requirement được đánh giá theo 5 tiêu chí.

## 3.1 Business Impact

Mức độ ảnh hưởng tới nghiệp vụ.

| Điểm | Mô tả |
|------|-------|
|1|Ít ảnh hưởng|
|2|Ảnh hưởng nhỏ|
|3|Ảnh hưởng trung bình|
|4|Ảnh hưởng lớn|
|5|Ảnh hưởng nghiêm trọng hoặc ảnh hưởng doanh thu|

Ví dụ:

5

- Thanh toán
- Loyalty
- Đăng nhập
- Đặt hàng

1

- Banner
- Tooltip
- Nội dung tĩnh

---

## 3.2 Usage Frequency

Tần suất người dùng sử dụng.

|Điểm|Mô tả|
|----|------|
|1|Rất ít|
|2|Ít|
|3|Thỉnh thoảng|
|4|Thường xuyên|
|5|Mỗi ngày hoặc mọi người đều sử dụng|

---

## 3.3 Technical Complexity

Độ phức tạp kỹ thuật.

Đánh giá dựa trên:

- API
- Database
- Cache
- Queue
- Microservice
- Third-party
- Payment
- Authentication

|Điểm|Mô tả|
|----|------|
|1|Rất đơn giản|
|3|Có nhiều business rule|
|5|Nhiều service, transaction hoặc tích hợp|

---

## 3.4 Change Frequency

Mức độ thay đổi Requirement.

|Điểm|Mô tả|
|----|------|
|1|Hầu như không thay đổi|
|3|Thỉnh thoảng thay đổi|
|5|Thay đổi thường xuyên|

---

## 3.5 Historical Defect Rate

Tỷ lệ phát sinh Bug trong quá khứ.

Nếu có dữ liệu lịch sử.

|Điểm|Mô tả|
|----|------|
|1|Hầu như không có Bug|
|3|Bug mức trung bình|
|5|Thường xuyên có Bug hoặc nhiều Regression|

Nếu không có dữ liệu.

Mặc định:

3

Không được tự suy diễn.

---

# 4. Công thức tính Risk

```
Risk Score =
(
Business Impact
+
Usage Frequency
+
Technical Complexity
+
Change Frequency
+
Historical Defect Rate
)
/5
```

Làm tròn đến một chữ số thập phân.

---

# 5. Phân loại Risk

|Risk Score|Risk Level|
|-----------|----------|
|>=4.0|High|
|2.5 - 3.9|Medium|
|<2.5|Low|

---

# 6. Chiến lược sinh Test Case

## High Risk

Bắt buộc có:

- Positive
- Negative
- Boundary
- Validation
- Permission
- Business Rule
- State Transition
- API
- Database
- Integration
- Exception
- Security (nếu áp dụng)
- Concurrency (nếu áp dụng)
- Regression

Không được bỏ qua bất kỳ nhóm nào nếu phù hợp.

---

## Medium Risk

Bắt buộc có:

- Positive
- Negative
- Boundary
- Validation
- Permission
- Business Rule

Có thể thêm Integration nếu cần.

---

## Low Risk

Tối thiểu:

- Positive
- Negative

Boundary nếu có Validation.

---

# 7. Regression Scope

Sau khi đánh giá Risk.

AI phải đề xuất mức Regression.

## High

Regression đầy đủ.

Bao gồm:

- Functional
- API
- UI
- Integration
- Regression

---

## Medium

Regression theo module.

---

## Low

Smoke Test hoặc Sanity Test.

---

# 8. Priority

Risk Level quyết định Priority.

|Risk|Priority|
|----|---------|
|High|Critical|
|Medium|High|
|Low|Medium|

---

# 9. Kết quả Output

Sau khi đánh giá.

Sinh bảng.

|REQ ID|Risk Score|Risk Level|Priority|
|------|----------|----------|--------|

Ví dụ

|REQ-001|4.8|High|Critical|
|REQ-002|2.7|Medium|High|
|REQ-003|1.9|Low|Medium|

---

# 10. Quy tắc

Không được đánh giá Risk theo cảm tính.

Mọi điểm số phải có giải thích.

Ví dụ.

Business Impact = 5

Lý do:

Liên quan trực tiếp đến chức năng Thanh toán.

---

Technical Complexity = 4

Lý do:

Có nhiều API và Transaction Database.

---

# 11. Điều chỉnh Risk

Nếu Requirement có các yếu tố sau.

Tăng thêm 0.5 điểm.

- Thanh toán
- Loyalty Point
- Hoàn tiền
- Authentication
- Authorization
- Đối soát
- Đồng bộ dữ liệu
- Third-party
- File Upload
- Push Notification
- Scheduler

Tổng điểm tối đa không vượt quá 5.

---

# 12. Các hành vi bị cấm

Không được:

- Bỏ qua bước đánh giá Risk.
- Chấm điểm không có lý do.
- Tự nâng hoặc hạ Risk để giảm số lượng Test Case.
- Chấm tất cả Requirement cùng một mức Risk.
- Bỏ qua Business Impact.
- Bỏ qua Historical Defect khi có dữ liệu.

---

# 13. Self Review Checklist

Trước khi kết thúc.

Kiểm tra:

✓ Mọi Requirement đều có Risk Score.

✓ Có giải thích điểm số.

✓ Đã xác định Risk Level.

✓ Đã xác định Priority.

✓ Đã đề xuất Regression Scope.

✓ Đã xác định Strategy sinh Test Case.

Nếu còn Requirement chưa đánh giá Risk.

Không được tiếp tục sang bước sinh Test Case.