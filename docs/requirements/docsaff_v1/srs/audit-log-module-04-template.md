# SRS - Audit Log Management

## Changes Record

Note: A - Add/Create new, M - Modify, D - Delete

| Date of change | Reason (A, M, D) | Updated by | Old version | Description of change | New version |
|---|---|---|---|---|---|
| 2026-07-24 | A | Product/BA | -- | Create SRS Audit Log Management following module-04 template. | 1.0.0 |

## Table of Contents

- I. Introduction
- II. Overall Description
- III. Overview
- IV. Description of Functions
- V. Data Requirements
- VI. Consolidated Business Rules Summary
- VII. Non-functional Requirements
- VIII. Consolidated Acceptance Criteria Summary
- IX. Open Questions

# I. Introduction

## 1. Purpose of Document

Tài liệu này mô tả yêu cầu phần mềm cho module **Audit Log Management** thuộc White-label Affiliate Marketplace Platform. Module này ghi nhận, lưu trữ và cho phép tra cứu lịch sử thao tác quan trọng trên Admin CMS và Tenant Portal.

Audit Log phục vụ các mục tiêu chính:

- Traceability cho thay đổi cấu hình nghiệp vụ.
- Hỗ trợ điều tra sự cố vận hành.
- Hỗ trợ kiểm soát phân quyền và trách nhiệm thao tác.
- Hỗ trợ đối soát khi có sai lệch về visibility, commission, revenue share, earn display hoặc transaction.

## 2. Document Conventions

| Convention | Description |
|---|---|
| Actor | Người hoặc hệ thống thực hiện hành động. |
| Entity | Đối tượng bị tác động, ví dụ Tenant, Brand, Offer, Commission Rule. |
| Before/After value | Giá trị trước và sau khi thay đổi. Có thể mask/redact theo policy. |
| Tenant scope | Audit event phát sinh từ Tenant Portal phải có `tenant_id`; trong MVP1 chỉ Admin CMS/Ops được phân quyền tra cứu trên CMS. Giao diện Tenant tự xem log thuộc Deferred/Phase 2. |
| Admin scope | Admin/Ops có thể xem audit log toàn hệ thống theo quyền. |
| Sensitive data | Password, credential, API key, token, secret, PII hoặc dữ liệu cần mask. |
| R/O | Required/Optional, dùng trong screen description của các màn nhập/filter. |

## 3. Project Scope

### 3.1 In Scope

| Module | Features |
|---|---|
| Audit Capture | Ghi audit log cho thao tác tạo/sửa/xóa mềm/đổi trạng thái/cấu hình/export quan trọng. |
| Admin CMS Audit Log | Admin/Ops xem, tìm kiếm, lọc audit log toàn hệ thống theo quyền. |
| Tenant Portal Audit Capture | Ghi Audit Log cho thao tác phát sinh từ Tenant Portal, gắn `tenant_id`, `source_app`, actor và dữ liệu before/after đã mask; Admin CMS/Ops tra cứu tại CMS Audit Log. |
| Audit Detail | Xem chi tiết một audit event, bao gồm actor, action, entity, before/after value đã mask. |
| Security & Masking | Mask sensitive data, không lưu password/secret plain text. |

### 3.2 Out of Scope

| Item | Reason |
|---|---|
| Security event monitoring/SIEM chuyên sâu | Có thể tích hợp sau MVP1; tài liệu này chỉ mô tả audit nghiệp vụ ứng dụng. |
| Full system/application log | Log kỹ thuật/debug không thuộc Audit Log Management. |
| Legal/compliance archive dài hạn | Retention dài hạn cần chốt với policy bảo mật/tuân thủ. |
| User activity analytics | Audit log không thay thế analytics/reporting. |
| Tenant Portal Audit Log UI | Deferred/Phase 2: chưa có menu, màn danh sách/chi tiết, bộ lọc, export hoặc permission Audit Log trên Tenant Portal trong MVP1. |

## 4. Expected Results After Finishing This Document

- Xác định rõ use case Audit Log trong MVP1.
- Làm rõ các action cần ghi audit.
- Mô tả màn danh sách, chi tiết, filter và quyền xem Audit Log trên CMS; giao diện Tenant Portal được lưu làm đặc tả tham khảo cho Phase 2.
- Định nghĩa data fields, business rule, validation và acceptance criteria.

## 5. References

| Document | Location |
|---|---|
| Function List / SOW | [affiliate-marketplace-platform-function-list.md](../function-list/affiliate-marketplace-platform-function-list.md) |
| Tenant Management SRS | [tenant-management-module-04-template.md](tenant-management-module-04-template.md) |
| Tenant Portal SRS | [tenant-portal-module-04-template.md](tenant-portal-module-04-template.md) |
| Brand & Offer SRS | [brand-offer-management-module-04-template.md](brand-offer-management-module-04-template.md) |
| Category Management SRS | [category-management-module-04-template.md](category-management-module-04-template.md) |
| Order & Transaction SRS | [order-transaction-management-module-04-template.md](order-transaction-management-module-04-template.md) |

# II. Overall Description

## 1. Definition

| Name | Description |
|---|---|
| Audit Event | Một bản ghi lịch sử cho một thao tác nghiệp vụ hoặc cấu hình. |
| Actor | User hoặc service thực hiện thao tác. |
| Action | Loại hành động, ví dụ `CREATE`, `UPDATE`, `DEACTIVATE`, `EXPORT`. |
| Entity | Đối tượng bị tác động. |
| Entity ID | ID của đối tượng bị tác động. |
| Before value | Snapshot field thay đổi trước thao tác. |
| After value | Snapshot field thay đổi sau thao tác. |
| Masking | Ẩn một phần/toàn bộ giá trị nhạy cảm. |
| Admin Audit Log | Audit log toàn hệ thống cho Admin/Ops. |
| Tenant Audit Log | Audit event có `tenant_id` và phát sinh từ thao tác Tenant Portal. MVP1 được xem qua CMS Audit Log; giao diện Tenant Portal thuộc Deferred/Phase 2. |

## 2. Operation Environment

| Item | Description |
|---|---|
| Application type | MVP1: Admin CMS web app tra cứu Audit Log; Tenant Portal chỉ phát sinh Audit Event. Tenant Audit Log UI thuộc Phase 2. |
| Primary users | MVP1: Admin/Ops hoặc role CMS được phân quyền xem Audit Log. Tenant Admin tự xem log thuộc Phase 2. |
| Data source | Audit Log Service/Repository. |
| Security | Enforce RBAC và tenant isolation. |
| Locale | Giao diện hỗ trợ `vi-VN`, `en-US`; dữ liệu audit action/entity dùng enum kỹ thuật nhưng label hiển thị có thể localize. |

## 3. Actors and User Classes

| Actor | Description | Permission scope |
|---|---|---|
| Admin/Ops | Người vận hành Platform. | Xem audit log toàn hệ thống nếu có quyền `audit.read`. |
| Finance | Người xem lịch sử thay đổi liên quan transaction, revenue share, settlement nếu có quyền. | Xem các audit event tài chính theo quyền. |
| Tenant Admin | Người quản trị phía Tenant. | Thực hiện thao tác được ghi Audit Log; chưa được cung cấp giao diện hoặc permission `tenant_audit.read` trong MVP1. |
| System Service | Backend service ghi audit event tự động. | Write-only theo internal service permission. |

# III. Overview

## 1. Module Summary

| Module | Description |
|---|---|
| Audit Capture | Ghi nhận event khi thao tác quan trọng hoàn tất. |
| Audit Query | Tìm kiếm/lọc audit event theo actor, action, entity, time range, Tenant, Brand. |
| Audit Detail | Xem chi tiết before/after value, metadata và trace id. |
| Tenant Audit View | Deferred/Phase 2. MVP1 chỉ ghi log và cho Admin CMS/Ops được phân quyền tra cứu trên CMS theo Tenant. |

## 2. Use Case List

| Use case ID | Use case name | Actor | Priority |
|---|---|---|---|
| AUD-001 | Ghi nhận audit event | System Service | Must |
| AUD-002 | Admin xem danh sách audit log | Admin/Ops, Finance | Must |
| AUD-003 | Admin xem chi tiết audit log | Admin/Ops, Finance | Must |
| AUD-004 | Tenant xem danh sách audit log — Deferred/Phase 2 | Tenant Admin | Deferred |
| AUD-005 | Tenant xem chi tiết audit log — Deferred/Phase 2 | Tenant Admin | Deferred |
| AUD-006 | Export audit log | Admin/Ops | Should |

## 3. Audit Scope Matrix

| Domain | Events cần ghi audit |
|---|---|
| Tenant Management | Create/update/deactivate Tenant, tạo/sửa/inactive Tenant Portal user, đổi role/status user. |
| Brand Management | Create/update/deactivate Brand, đổi status Brand. |
| Brand Category & Commission | Thêm/sửa/inactive category mapping, đổi default category, đổi commission type/value/status. |
| Offer Management | Create/update/deactivate Offer, đổi status Offer, sửa Offer commission. |
| Category Management | Create/update/inactive category, sửa icon/sort/localized content/status. |
| Admin Assignment Pool | Assign/unassign Brand/Offer cho Tenant, sửa custom Offer assignment. |
| Tenant Revenue Share | Create/update/inactive Brand-level rule, Category override, Offer override. |
| Tenant Portal Visibility | Tenant bật/tắt Brand/Offer visibility trong pool. |
| Tenant Earn Display | Create/update/inactive Brand-level display, Category/Offer override. |
| Integration Config | Create/update credential metadata, endpoint, auth type, allowed IPs, integration status; không log secret plain text. |
| Transaction/Exception | Manual resolve exception, retry, ignore, export transaction/report nếu có quyền. |
| Export | Export report/transaction/audit log gồm actor, filter, export type, timestamp. |

# IV. Description of Functions

## 1. AUD-001 - Ghi nhận audit event

### a. Introduction

Hệ thống tự động ghi audit event khi một thao tác nghiệp vụ/cấu hình quan trọng được thực hiện thành công hoặc khi có thao tác export dữ liệu nhạy cảm.

### b. Actors/Objects

| Actor/Object | Role |
|---|---|
| Application Service | Thực hiện nghiệp vụ và gửi audit event. |
| Audit Service | Validate, mask và lưu audit event. |
| Audit Repository | Lưu trữ audit event. |

### c. Pre-conditions

- Actor đã được xác thực hoặc service có internal credential hợp lệ.
- Action thuộc danh sách cần audit.
- Entity bị tác động xác định được `entity_type` và `entity_id`.

### d. Expected Result

- Audit event được lưu đầy đủ actor, action, entity, tenant scope, timestamp và change detail.
- Sensitive data được mask hoặc không ghi vào audit log.
- Nếu thao tác nghiệp vụ thành công nhưng ghi audit thất bại, hệ thống xử lý theo policy đã chốt trong business rule.

### e. Screen Description

Không có màn hình. Đây là backend behavior.

### f. Logic Description

| # | Step | Actor/Object | Logic |
|---:|---|---|---|
| 1 | Business action completed | Application Service | Hoàn tất thao tác tạo/sửa/xóa mềm/đổi trạng thái/export. |
| 2 | Build event | Application Service | Tạo audit payload gồm actor, action, entity, before/after value, trace id. |
| 3 | Mask sensitive fields | Audit Service | Loại bỏ hoặc mask password, token, secret, credential, PII theo policy. |
| 4 | Validate event | Audit Service | Kiểm tra field bắt buộc và enum action/entity. |
| 5 | Persist | Audit Repository | Lưu audit event immutable. |

### g. Business Rules

| BR ID | Rule |
|---|---|
| BR-AUD-001-01 | Mọi thao tác thay đổi cấu hình quan trọng phải ghi audit log. |
| BR-AUD-001-02 | Audit event sau khi ghi không cho sửa/xóa bằng chức năng thông thường. Nếu cần correction phải tạo audit event mới. |
| BR-AUD-001-03 | Không ghi password, API secret, token hoặc credential plain text vào audit log. |
| BR-AUD-001-04 | Before/after value chỉ lưu field thay đổi thay vì snapshot toàn bộ entity nếu không cần thiết. |
| BR-AUD-001-05 | Audit log phải gắn `tenant_id` nếu event thuộc một Tenant cụ thể. |
| BR-AUD-001-06 | Nếu ghi audit thất bại với action bắt buộc audit, action nghiệp vụ không được coi là hoàn tất hoặc phải được đưa vào audit retry/error queue theo policy Engineering. |

### h. Acceptance Criteria

| AC ID | Criteria |
|---|---|
| AC-AUD-001-01 | Khi tạo/sửa/inactive một entity quan trọng, hệ thống tạo audit event tương ứng. |
| AC-AUD-001-02 | Audit event không chứa password/secret plain text. |
| AC-AUD-001-03 | Audit event có đủ actor, action, entity, timestamp và trace id nếu có. |
| AC-AUD-001-04 | Event thuộc Tenant có `tenant_id` để enforce tenant isolation. |

## 2. AUD-002 - Admin xem danh sách audit log

### a. Introduction

Admin/Ops xem danh sách audit log toàn hệ thống để tra cứu lịch sử thay đổi cấu hình và thao tác vận hành.

### b. Actors/Objects

| Actor/Object | Role |
|---|---|
| Admin/Ops | Xem và lọc audit log. |
| Finance | Xem audit log liên quan tài chính nếu có quyền. |
| Audit Query Service | Query audit event theo filter và RBAC. |
| Permission Service | Enforce quyền `audit.read`. |

### c. Pre-conditions

- User đã đăng nhập Admin CMS.
- User có quyền `audit.read`.

### d. Expected Result

- Admin/Ops xem được audit log theo quyền.
- Có thể lọc theo keyword, time range, actor, action, entity, tenant, brand/module.
- Không xem được field đã bị mask hoặc ngoài quyền.

### e. Screen Description - Admin Audit Log List

| # | Items | Control type | Data type | R/O | Description / Validation / Error handling |
|---:|---|---|---|---|---|
| 1 | Keyword | Textbox | Text | O | Tìm theo audit_id, actor username, entity_id, request_id/trace_id. Tối đa 100 ký tự; trim khoảng trắng. |
| 2 | Time range | DateTime range | Datetime | O | Lọc theo `event_at`. Nếu from > to, hiển thị lỗi `Khoảng thời gian không hợp lệ`. |
| 3 | Actor | Dropdown/Search | User ref | O | Lọc theo người thực hiện. |
| 4 | Tenant | Dropdown/Search | Tenant ref | O | Lọc theo Tenant nếu event có tenant_id. |
| 5 | Entity type | Dropdown | Enum | O | Tenant, Brand, Offer, Category, Commission Rule, Revenue Share Rule, Earn Display, Integration, Transaction, Exception, Export. |
| 6 | Action | Dropdown | Enum | O | CREATE, UPDATE, DEACTIVATE, ACTIVATE, ASSIGN, UNASSIGN, EXPORT, RESOLVE, RETRY, IGNORE. |
| 7 | Audit table | Table | ReadOnly | ReadOnly | Hiển thị event_at, actor, action, entity_type, entity_id/name, tenant, summary, source app. |
| 8 | View detail | Icon/Button | Action | O | Mở màn chi tiết audit event. |
| 9 | Export | Button | Action | O | Export audit log theo filter nếu có quyền `audit.export`. |

### f. Business Rules

| BR ID | Rule |
|---|---|
| BR-AUD-002-01 | Admin/Ops chỉ xem audit log theo quyền RBAC. |
| BR-AUD-002-02 | Danh sách audit log phải hỗ trợ pagination/sorting theo `event_at` giảm dần. |
| BR-AUD-002-03 | Field nhạy cảm luôn hiển thị masked kể cả với Admin/Ops. |
| BR-AUD-002-04 | Export audit log phải tự ghi thêm một audit event `EXPORT_AUDIT_LOG`. |

### g. Acceptance Criteria

| AC ID | Criteria |
|---|---|
| AC-AUD-002-01 | Admin/Ops có quyền xem được audit log list. |
| AC-AUD-002-02 | Filter theo time range, actor, action, entity, tenant trả đúng dữ liệu. |
| AC-AUD-002-03 | User không có quyền `audit.read` bị access denied. |
| AC-AUD-002-04 | Field secret/password không hiển thị plain text trên danh sách. |

## 3. AUD-003 - Admin xem chi tiết audit log

### a. Introduction

Admin/Ops xem chi tiết một audit event để biết thao tác nào đã xảy ra, ai thực hiện, trước/sau thay đổi ra sao và liên quan đến request/trace nào.

### b. Pre-conditions

- User có quyền xem audit log.
- Audit event tồn tại.

### c. Expected Result

- Hiển thị đầy đủ thông tin audit event theo quyền.
- Before/after value hiển thị rõ field changed.
- Sensitive fields được mask.

### d. Screen Description - Admin Audit Log Detail

| # | Items | Control type | Data type | R/O | Description / Validation / Error handling |
|---:|---|---|---|---|---|
| 1 | Audit summary | Section | ReadOnly | ReadOnly | audit_id, event_at, source_app, actor, action, entity_type, entity_id, entity_name nếu có. |
| 2 | Scope | Section | ReadOnly | ReadOnly | tenant_id/name, brand_id/name, module, request_id, trace_id, IP/device nếu policy cho phép. |
| 3 | Change detail | Table/JSON viewer | Object | ReadOnly | Hiển thị field_name, before_value, after_value. Không hiển thị field không đổi. |
| 4 | Metadata | Section | Object | ReadOnly | reason/note nếu action có nhập lý do, filter export nếu là export event, result status. |
| 5 | Back | Button | Action | O | Quay lại danh sách với filter hiện tại. |

### e. Business Rules

| BR ID | Rule |
|---|---|
| BR-AUD-003-01 | Audit detail không được expose secret/plain credential. |
| BR-AUD-003-02 | Nếu user không có quyền xem financial fields, before/after của field tài chính phải bị mask hoặc ẩn theo RBAC. |
| BR-AUD-003-03 | JSON/raw metadata nếu hiển thị phải được sanitize và không chứa dữ liệu nhạy cảm. |

### f. Acceptance Criteria

| AC ID | Criteria |
|---|---|
| AC-AUD-003-01 | Admin/Ops mở được audit detail từ danh sách. |
| AC-AUD-003-02 | Audit detail hiển thị old/new value cho các field thay đổi. |
| AC-AUD-003-03 | Field nhạy cảm được mask/ẩn theo policy. |

## 4. AUD-004 - Tenant xem danh sách audit log — Deferred/Phase 2

### a. Introduction

Không triển khai giao diện này trong MVP1. Hệ thống vẫn ghi lịch sử thao tác do Tenant User/System thực hiện trong Tenant Portal, ví dụ quản lý User/Role, bật/tắt Brand/Offer visibility và cấu hình Earn Display. Audit event phải gắn `tenant_id` và `source_app = Tenant Portal`; Admin CMS/Ops được phân quyền xem tại CMS Audit Log. Tenant Admin tự xem log được dự kiến cho Phase 2.

### b. Actors/Objects

| Actor/Object | Role |
|---|---|
| Tenant Admin | Phase 2 mới xem Audit Log trực tiếp trên Tenant Portal; MVP1 chỉ là actor phát sinh thao tác được audit. |
| Audit Query Service | Query audit event scoped theo Tenant. |
| Permission Service | Phase 2 mới cung cấp/enforce quyền `tenant_audit.read`; permission này không nằm trong Tenant Portal permission matrix MVP1. |

### c. Pre-conditions

- Không áp dụng trong MVP1.
- Phase 2 yêu cầu Tenant Admin đăng nhập và có quyền `tenant_audit.read`.

### d. Expected Result

- MVP1: Audit event Tenant Portal được ghi thành công và Admin CMS/Ops có thể tra cứu theo `tenant_id`/`source_app`.
- Phase 2: Tenant Admin chỉ xem log thuộc Tenant hiện tại và không thấy log nội bộ Platform không được expose.

### e. Screen Description - Tenant Audit Log List — Phase 2 reference

| # | Items | Control type | Data type | R/O | Description / Validation / Error handling |
|---:|---|---|---|---|---|
| 1 | Keyword | Textbox | Text | O | Tìm theo actor, entity_id/name, audit_id. |
| 2 | Time range | DateTime range | Datetime | O | Lọc theo thời gian phát sinh. |
| 3 | Actor | Dropdown/Search | Tenant user ref | O | Chỉ gồm user thuộc Tenant hiện tại. |
| 4 | Module | Dropdown | Enum | O | User management, Brand visibility, Offer visibility, Earn display, Transaction export, Report export. |
| 5 | Action | Dropdown | Enum | O | CREATE, UPDATE, ACTIVATE, INACTIVE, SHOW, HIDE, EXPORT. |
| 6 | Audit table | Table | ReadOnly | ReadOnly | event_at, actor, action, module, entity, summary. |
| 7 | View detail | Icon/Button | Action | O | Mở audit detail nếu có quyền. |

### f. Business Rules

| BR ID | Rule |
|---|---|
| BR-AUD-004-01 | Tenant user chỉ xem audit event có `tenant_id` bằng Tenant trong session/token. |
| BR-AUD-004-02 | Tenant user không được xem audit event Admin/Ops nội bộ nếu event không thuộc phạm vi Tenant Portal hoặc không được expose. |
| BR-AUD-004-03 | Tenant Audit Log không hiển thị commission Brand trả Affiliate hoặc secret nội bộ Platform. |

### g. Acceptance Criteria

| AC ID | Criteria |
|---|---|
| AC-AUD-004-01 | Tenant Admin xem được audit log của Tenant mình. |
| AC-AUD-004-02 | Tenant Admin không xem được log Tenant khác khi đổi filter/url/API param. |
| AC-AUD-004-03 | Tenant user không có quyền audit nhận access denied. |

## 5. AUD-005 - Tenant xem chi tiết audit log — Deferred/Phase 2

### a. Introduction

Không triển khai trong MVP1. Phần dưới là đặc tả tham khảo cho Phase 2, khi Tenant Admin được phép xem chi tiết Audit Event trong phạm vi Tenant.

### b. Screen Description - Tenant Audit Log Detail — Phase 2 reference

| # | Items | Control type | Data type | R/O | Description / Validation / Error handling |
|---:|---|---|---|---|---|
| 1 | Audit summary | Section | ReadOnly | ReadOnly | audit_id, event_at, actor, action, module, entity. |
| 2 | Change detail | Table | ReadOnly | ReadOnly | Field changed, before value, after value đã mask theo policy. |
| 3 | Context | Section | ReadOnly | ReadOnly | Brand/Offer/Category liên quan nếu có; không hiển thị internal secret. |
| 4 | Back | Button | Action | O | Quay lại danh sách. |

### c. Business Rules

| BR ID | Rule |
|---|---|
| BR-AUD-005-01 | Tenant audit detail phải enforce tenant scope giống audit list. |
| BR-AUD-005-02 | Không hiển thị dữ liệu ngoài quyền của Tenant user. |

### d. Acceptance Criteria

| AC ID | Criteria |
|---|---|
| AC-AUD-005-01 | Tenant Admin mở được audit detail thuộc Tenant mình. |
| AC-AUD-005-02 | Tenant Admin không mở được audit detail của Tenant khác. |

## 6. AUD-006 - Export audit log

### a. Introduction

Admin/Ops export audit log theo filter để phục vụ kiểm tra, đối soát hoặc cung cấp bằng chứng vận hành. Tenant export audit log có thể đưa vào phase sau nếu cần.

### b. Business Rules

| BR ID | Rule |
|---|---|
| BR-AUD-006-01 | Export audit log chỉ dành cho user có quyền `audit.export`. |
| BR-AUD-006-02 | Export phải tuân theo filter hiện tại và RBAC. |
| BR-AUD-006-03 | File export không chứa secret/password plain text. |
| BR-AUD-006-04 | Mỗi lần export audit log phải ghi audit event mới. |
| BR-AUD-006-05 | Nếu số dòng vượt threshold hệ thống, export phải chạy async hoặc báo lỗi giới hạn theo policy. |

### c. Acceptance Criteria

| AC ID | Criteria |
|---|---|
| AC-AUD-006-01 | User có quyền export được audit log theo filter. |
| AC-AUD-006-02 | User không có quyền export không thấy hoặc không dùng được action export. |
| AC-AUD-006-03 | Export action được ghi lại trong audit log. |

# V. Data Requirements

## 1. Audit Event

| Field | Type | R/O | Description / Validation |
|---|---|---|---|
| audit_id | UUID/String | R | ID audit event do hệ thống sinh. |
| event_at | Datetime | R | Thời điểm phát sinh event theo timezone hệ thống. |
| source_app | Enum | R | `Admin CMS`, `Tenant Portal`, `Backend Job`, `API`. |
| actor_type | Enum | R | User, System, Service. |
| actor_user_id | UUID/String | O | User thực hiện nếu actor là User. |
| actor_username | String | O | Username/account hiển thị. |
| actor_role | String/Enum | O | Role tại thời điểm thao tác nếu có. |
| tenant_id | UUID/String | O | Tenant scope nếu event liên quan Tenant. Bắt buộc với Tenant Portal event. |
| brand_id | UUID/String | O | Brand liên quan nếu có. |
| action | Enum | R | CREATE, UPDATE, ACTIVATE, DEACTIVATE, ASSIGN, UNASSIGN, SHOW, HIDE, EXPORT, RESOLVE, RETRY, IGNORE. |
| entity_type | Enum | R | Tenant, User, Brand, Offer, Category, Commission Rule, Revenue Share Rule, Earn Display, Integration Config, Transaction, Exception, Report, Audit Log. |
| entity_id | UUID/String | R | ID entity bị tác động. |
| entity_name | String | O | Tên hiển thị để tra cứu nhanh. |
| change_summary | String | O | Tóm tắt thay đổi. |
| change_set | Object/JSON | O | Danh sách field changed với before/after đã mask. |
| reason | String | O | Lý do thao tác nếu form/action có nhập. |
| request_id | String | O | Request ID phục vụ trace. |
| trace_id | String | O | Trace/correlation ID. |
| ip_address | String | O | IP actor nếu policy cho phép lưu. |
| user_agent | String | O | User agent nếu policy cho phép lưu. |
| result_status | Enum | R | Success, Failed, Partial. MVP1 ưu tiên ghi action Success; Failed audit cho security/exception nếu cần. |
| created_at | Datetime | R | Thời điểm ghi vào repository. |

## 2. Change Set Item

| Field | Type | R/O | Description / Validation |
|---|---|---|---|
| field_name | String | R | Tên field thay đổi. |
| before_value | Mixed | O | Giá trị trước thay đổi, masked nếu sensitive. |
| after_value | Mixed | O | Giá trị sau thay đổi, masked nếu sensitive. |
| value_type | Enum | O | String, Number, Boolean, DateTime, Object, Array, Masked. |
| sensitivity | Enum | O | Public, Internal, Sensitive, Secret. |

## 3. Sensitive Field Policy

| Field pattern/type | Policy |
|---|---|
| password, password_hash, confirm_password | Không lưu plain text; nếu cần chỉ ghi `changed: true`. |
| api_key, secret, token, credential, private_key | Không lưu plain text; hiển thị `******`. |
| email/phone | Có thể mask một phần theo privacy policy. |
| financial fields | Hiển thị theo RBAC; Tenant không thấy commission Brand trả Affiliate. |
| raw payload | Không lưu raw nếu chứa secret/PII; chỉ lưu metadata hoặc masked snapshot. |

# VI. Consolidated Business Rules Summary

| BR ID | Rule |
|---|---|
| BR-AUD-GEN-001 | Audit log là bắt buộc cho thay đổi cấu hình quan trọng. |
| BR-AUD-GEN-002 | Audit event phải immutable sau khi ghi. |
| BR-AUD-GEN-003 | Audit log không chứa password/secret/plain credential. |
| BR-AUD-GEN-004 | Tenant Portal audit log phải scope theo `tenant_id`. |
| BR-AUD-GEN-005 | Admin audit log phải enforce RBAC. |
| BR-AUD-GEN-006 | Export audit log phải tạo audit event mới. |
| BR-AUD-GEN-007 | Before/after value phải mask theo data sensitivity và quyền user. |
| BR-AUD-GEN-008 | Audit event phải có timestamp đáng tin cậy từ server, không tin timestamp client gửi. |

# VII. Non-functional Requirements

| NFR ID | Requirement |
|---|---|
| NFR-AUD-001 | Audit write phải có độ tin cậy cao; không được silently fail với action bắt buộc audit. |
| NFR-AUD-002 | Audit query phải hỗ trợ pagination khi dữ liệu lớn. |
| NFR-AUD-003 | Audit log phải có index theo event_at, actor, entity_type, entity_id, tenant_id. |
| NFR-AUD-004 | Audit log phải bảo vệ dữ liệu nhạy cảm bằng masking/redaction. |
| NFR-AUD-005 | Audit log phải giữ tenant isolation tuyệt đối trong Tenant Portal. |
| NFR-AUD-006 | Audit log list/detail không expose stack trace hoặc lỗi kỹ thuật nội bộ. |
| NFR-AUD-007 | Retention period cần cấu hình theo policy vận hành/compliance khi triển khai. |

# VIII. Consolidated Acceptance Criteria Summary

| AC ID | Criteria |
|---|---|
| AC-AUD-GEN-001 | Tạo/sửa/inactive Tenant, Brand, Offer, Category, visibility, commission, revenue share và earn display đều sinh audit event. |
| AC-AUD-GEN-002 | Audit log không chứa password/API secret/token plain text. |
| AC-AUD-GEN-003 | Admin/Ops lọc được audit log theo actor, action, entity, tenant và time range. |
| AC-AUD-GEN-004 | Tenant Admin chỉ xem được audit log thuộc Tenant mình. |
| AC-AUD-GEN-005 | Audit detail hiển thị before/after value theo policy. |
| AC-AUD-GEN-006 | Export audit log tuân theo RBAC và tự ghi lại audit event export. |

# IX. Open Questions

| # | Question | Current assumption |
|---:|---|---|
| 1 | Retention audit log bao lâu? | Tạm để theo policy vận hành/compliance khi triển khai. |
| 2 | Có cần export audit log cho Tenant Portal không? | MVP1 ưu tiên Admin export; Tenant export có thể bổ sung sau nếu Tenant yêu cầu. |
| 3 | Audit event failed action có cần lưu không? | MVP1 ưu tiên audit action thành công; failed/security event có thể thuộc security log riêng. |
| 4 | Có cần màn mockup riêng cho Admin/Tenant audit log không? | Chưa có mockup; có thể vẽ nếu cần làm UI chi tiết. |
