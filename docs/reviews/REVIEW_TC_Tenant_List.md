{
  "tc_file": "docs/testcases/TC_Tenant_List.md",
  "iteration": 1,
  "quality_score": 96,
  "pillars": {
    "coverage": 100,
    "depth": 94,
    "design_quality": 92,
    "optimization": 92
  },
  "decision": "Approved",
  "approved": true,
  "issues": {
    "critical": [],
    "major": [],
    "minor": [
      "Một số test case phụ thuộc policy chưa được chốt và đã được đánh dấu Remark/Open Questions.",
      "TC-019 và TC-023 cần cập nhật endpoint, HTTP status và schema sau khi có API contract.",
      "TC-031 cần cập nhật version trình duyệt sau khi browser matrix được phê duyệt."
    ]
  },
  "action_items": [
    "BA/PO xác nhận hành vi Keyword vượt 100 ký tự.",
    "Engineering/BA cung cấp API contract Tenant List.",
    "Product xác nhận pagination, filter thời gian và browser matrix."
  ],
  "open_questions": [
    "Keyword vượt 100 ký tự được trim hay báo lỗi?",
    "Keyword matching có phân biệt chữ hoa/thường và hỗ trợ partial match không?",
    "Updated period, timezone và boundary chính thức là gì?",
    "Page size và API pagination contract là gì?",
    "HTTP status/error code cho access denied và service error là gì?"
  ]
}

# Tổng quan

Bộ Test Case bao phủ toàn bộ requirement được trích xuất cho màn hình Danh sách Tenant, gồm quyền truy cập, tải danh sách, sort mặc định, keyword/status/account owner/updated period, mapping cột, Tenant Inactive, dữ liệu không được hiển thị, empty/error state, action, read-only behavior, pagination và compatibility.

Risk-based depth phù hợp với chức năng có dữ liệu quản trị và input người dùng: đã có positive, negative, boundary, permission, security, API, integration, database/read-only và exception coverage. Không phát hiện Test Case suy diễn business rule; các policy chưa đủ thông tin được đánh dấu Blocked/Remark và đưa vào Open Questions.

# Scorecard

| Tiêu chí | Điểm |
|----------|------:|
| Coverage | 100 |
| Depth | 94 |
| Design Quality | 92 |
| Optimization | 92 |
| **Quality Score** | **96/100** |

# Requirement Coverage

| Requirement | Trạng thái | Test Case |
|---|---|---|
| REQ-001 | Covered | TC-001, TC-002 |
| REQ-002 | Covered | TC-003 |
| REQ-003 | Covered | TC-004 đến TC-009 |
| REQ-004 | Covered | TC-010, TC-011 |
| REQ-005 | Covered | TC-012 |
| REQ-006 | Covered | TC-013 |
| REQ-007 | Covered | TC-014 đến TC-016 |
| REQ-008 | Covered | TC-017 |
| REQ-009 | Covered | TC-018, TC-019 |
| REQ-010 | Covered | TC-020 |
| REQ-011 | Covered | TC-021 đến TC-023 |
| REQ-012 | Covered | TC-024 đến TC-026 |
| REQ-013 | Covered | TC-027 |
| REQ-014 | Covered | TC-028, TC-029 |
| REQ-015 | Covered | TC-030 |
| REQ-016 | Covered | TC-031 |

Requirement chưa cover: Không có.

# Các Issue

## Critical

Không có.

## Major

Không có.

## Minor

1. TC-008 chưa thể xác định một expected behavior duy nhất do requirement cho phép “trim hoặc hiển thị lỗi”.
2. TC-019 và TC-023 cần endpoint, HTTP status và schema cụ thể để thực thi API test.
3. TC-031 chưa có version trình duyệt cụ thể.
4. Page size và message text chưa được định nghĩa nên Expected Result chỉ kiểm tra hành vi, không kiểm tra literal text.

# Action Items

1. BA/PO chốt Keyword policy tại boundary 101 ký tự.
2. BA/Engineering bổ sung API contract Tenant List.
3. Product chốt page size, Updated period/timezone và browser matrix.
4. Cập nhật các TC bị ảnh hưởng, giữ nguyên TC ID sau khi requirement được làm rõ.

# Open Questions

1. Keyword vượt 100 ký tự được trim hay báo lỗi?
2. Keyword matching có phân biệt chữ hoa/thường, partial match và trim khoảng trắng không?
3. Updated period/timezone/boundary chính thức là gì?
4. Account owner và Updated period có bắt buộc trong MVP1 không?
5. Page size và pagination contract là gì?
6. Empty/error message chính thức là gì?
7. User thiếu `tenant.read` bị ẩn menu hay nhận access denied sau khi click?
8. Endpoint, HTTP status, response/error schema của Tenant List là gì?
9. Quy tắc tính Brand/Offer và Commission count là gì?
10. Browser version matrix cụ thể là gì?
