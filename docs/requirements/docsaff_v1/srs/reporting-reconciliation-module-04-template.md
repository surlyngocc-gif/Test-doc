# SRS - Reporting & Reconciliation Management

## Changes Record

Note: A - Add/Create new, M - Modify, D - Delete

| Date of change | Reason (A, M, D) | Updated by | Old version | Description of change | New version |
|---|---|---|---|---|---|
| 2026-07-24 | A | Product/BA | -- | Create SRS Reporting & Reconciliation Management following module-04 template. | 1.0.0 |

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

Tài liệu này mô tả yêu cầu phần mềm cho module **Reporting & Reconciliation Management** thuộc White-label Affiliate Marketplace Platform.

Module này phục vụ các mục tiêu chính:

- Cung cấp báo cáo vận hành cho Admin/Ops/Finance.
- Cung cấp số liệu báo cáo trong phạm vi Tenant.
- Tổng hợp dữ liệu đối soát commission giữa Brand, Affiliate Platform và Tenant.
- Theo dõi settlement record theo chu kỳ hợp đồng.
- Phân biệt rõ số liệu tạm tính và số liệu chính thức.
- Hỗ trợ xử lý điều chỉnh thủ công cho các trường hợp hoàn/hủy sau khi transaction đã được chốt.

## 2. Document Conventions

| Convention | Description |
|---|---|
| R/O | Required/Optional, dùng trong mô tả màn hình và data field. |
| Pending/Provisional | Số liệu tạm tính trước ngày chốt commission chính thức. Không dùng để thanh toán. |
| Official | Số liệu đã được chốt chính thức sau khi order đủ điều kiện. |
| Settlement | Bản ghi tổng hợp số tiền phải thu/phải trả theo chu kỳ đối soát. |
| Adjustment | Bản ghi điều chỉnh thủ công khi có sai lệch, refund sau chốt hoặc yêu cầu Finance. |
| Tenant scope | Tenant chỉ xem dữ liệu thuộc Tenant của mình. |
| Admin scope | Admin/Ops/Finance có thể xem dữ liệu toàn hệ thống theo quyền. |
| Currency | MVP1 mặc định `VND`, trừ khi có quyết định mở rộng multi-currency. |

## 3. Project Scope

### 3.1 In Scope

| Module | Features |
|---|---|
| Admin Reporting | Dashboard báo cáo toàn hệ thống theo Tenant/Brand/Offer/Category/time range/status. |
| Tenant Reporting | Báo cáo trong phạm vi Tenant, không hiển thị commission Brand trả Affiliate. |
| Report Export | Export CSV/XLSX theo bộ lọc và quyền truy cập. |
| Reconciliation | Tạo kỳ đối soát, tổng hợp transaction đủ điều kiện, rà soát sai lệch. |
| Settlement Tracking | Theo dõi settlement record theo cycle cấu hình theo từng hợp đồng Brand/Tenant. |
| Manual Adjustment | Ghi nhận điều chỉnh do Admin/Finance thực hiện sau khi Cancel/Refund API của Order Confirmed/Settled bị từ chối và ghi Exception, hoặc khi có sai lệch Finance; không phải cập nhật tự động từ API. |

### 3.2 Out of Scope

| Item | Reason |
|---|---|
| Tính/cộng điểm cashback cho End user | Pending sau MVP1. |
| Báo cáo cashback/point posting status | MVP1 chưa có luồng post điểm. |
| CPC billing | MVP1 chỉ tracking click, không tính tiền CPC. |
| Listing fee billing | Listing fee chỉ xử lý commercial, không đưa vào hệ thống. |
| Payment gateway/accounting integration | MVP1 chỉ tracking settlement status, chưa tích hợp hệ thống kế toán/thanh toán. |
| Tự động invoice | Có thể bổ sung sau khi chốt quy trình Finance. |

## 4. Expected Results After Finishing This Document

- Xác định danh sách use case cho báo cáo, đối soát và settlement.
- Làm rõ số liệu nào là tạm tính, số liệu nào là chính thức.
- Làm rõ quyền nhìn dữ liệu tài chính giữa Admin CMS và Tenant Portal.
- Mô tả field dữ liệu, filter, validation, business rule và acceptance criteria.
- Làm cơ sở để UI/UX vẽ mockup và QA viết test case.

## 5. References

| Document | Location |
|---|---|
| Function List / SOW | [affiliate-marketplace-platform-function-list.md](../function-list/affiliate-marketplace-platform-function-list.md) |
| Order & Transaction SRS | [order-transaction-management-module-04-template.md](order-transaction-management-module-04-template.md) |
| Tenant Portal SRS | [tenant-portal-module-04-template.md](tenant-portal-module-04-template.md) |
| Audit Log SRS | [audit-log-module-04-template.md](audit-log-module-04-template.md) |
| Brand & Offer SRS | [brand-offer-management-module-04-template.md](brand-offer-management-module-04-template.md) |
| Tenant Management SRS | [tenant-management-module-04-template.md](tenant-management-module-04-template.md) |

# II. Overall Description

## 1. Definition

| Name | Description |
|---|---|
| GMV tracked | Tổng giá trị giao dịch/order được Platform ghi nhận từ Brand. |
| Click | Lượt End user click từ landing page sang Brand/Offer URL qua tracking link của Platform. |
| Conversion | Order success được Brand gửi về và Platform ghi nhận thành transaction. |
| Provisional revenue amount | Doanh thu/order amount tạm tính khi order chưa tới ngày chốt chính thức. |
| Provisional gross commission amount | Hoa hồng Brand trả Affiliate tạm tính. |
| Provisional tenant share amount | Phần Affiliate dự kiến chia cho Tenant trước khi chốt chính thức. |
| Gross commission amount | Hoa hồng Brand trả Affiliate chính thức sau khi order đủ điều kiện. |
| Tenant share amount | Phần Affiliate chia cho Tenant chính thức. |
| Affiliate keep amount | Phần Affiliate giữ lại chính thức. |
| Reconciliation period | Kỳ đối soát dữ liệu theo time range và contract/cycle tương ứng. |
| Settlement record | Bản ghi tổng hợp phải thu/phải trả cho một Brand/Tenant/cycle. |
| Adjustment record | Bản ghi điều chỉnh cộng/trừ vào kỳ đối soát/settlement. |

## 2. Operation Environment

| Item | Description |
|---|---|
| Application type | Admin CMS và Tenant Portal web application. |
| Primary users | Admin/Ops, Finance, Tenant Admin, Tenant Finance, Tenant Viewer. |
| Data source | Click Tracking, Order/Transaction, Commission Calculation, Tenant Revenue Share, Adjustment, Audit Log. |
| Device | Desktop/laptop là chính; responsive cơ bản cho tablet nếu UI framework hỗ trợ. |
| Locale | Giao diện hỗ trợ `vi-VN`, `en-US`; default/fallback là `vi-VN`. |
| Security | RBAC và tenant isolation bắt buộc. |

## 3. Actors and User Classes

| Actor | Description | Permission scope |
|---|---|---|
| Admin/Ops | Người vận hành Platform. | Xem báo cáo toàn hệ thống, lọc dữ liệu, export theo quyền. |
| Finance | Người phụ trách đối soát/thanh toán. | Tạo/xem/chốt settlement, tạo adjustment, export báo cáo tài chính. |
| Tenant Admin | Người quản trị phía Tenant. | Xem báo cáo/transaction trong phạm vi Tenant. |
| Tenant Finance | Người theo dõi doanh thu chia sẻ của Tenant. | Xem/export doanh thu chia sẻ trong phạm vi Tenant. |
| Tenant Viewer | Người xem chỉ đọc. | Xem dashboard/transaction cơ bản nếu được cấp quyền. |
| System Job | Job hệ thống tổng hợp dữ liệu, tạo report snapshot hoặc cập nhật settlement status nếu có cấu hình. | Chạy theo lịch hoặc theo thao tác user. |

## 4. Dependencies

| Dependency | Description |
|---|---|
| Order & Transaction | Cung cấp transaction, order status, số tạm tính và số chính thức. |
| Commission Calculation | Cung cấp gross commission, tenant share, affiliate keep chính thức. |
| Tenant Revenue Share | Cung cấp rule chia sẻ Affiliate -> Tenant theo Brand/Category/Offer. |
| Brand/Offer/Category | Cung cấp master data phục vụ filter và grouping. |
| Tenant Management | Cung cấp tenant scope, visibility và contract/cycle settlement nếu có. |
| Audit Log | Ghi nhận thao tác export, tạo/chốt settlement, tạo adjustment. |

# III. Overview

## 1. Scope by User Group

| User group | Can view | Cannot view |
|---|---|---|
| Admin/Ops | Click, conversion, GMV, provisional/official commission, tenant share, affiliate keep, exception count. | Dữ liệu bị hạn chế bởi RBAC hoặc field sensitive. |
| Finance | Số liệu đối soát, settlement, adjustment, export tài chính. | Credential/API secret, password, raw sensitive payload nếu không có quyền. |
| Tenant Admin/Finance | Click/order/GMV và doanh thu chia sẻ của Tenant. | Commission Brand -> Affiliate, affiliate keep, dữ liệu Tenant khác. |
| Tenant Viewer | Dashboard/transaction read-only theo quyền. | Export hoặc số tài chính nếu không được cấp quyền. |

## 2. Use Case List

| Use case ID | Use case name | Actor | Priority |
|---|---|---|---|
| RPT-001 | Xem dashboard báo cáo Admin | Admin/Ops, Finance | Must |
| RPT-002 | Export báo cáo Admin | Admin/Ops, Finance | Must |
| RPT-003 | Xem dashboard báo cáo Tenant | Tenant Admin, Tenant Finance, Tenant Viewer | Must |
| RPT-004 | Export báo cáo Tenant | Tenant Admin, Tenant Finance | Should |
| REC-001 | Xem danh sách kỳ đối soát/settlement | Admin/Ops, Finance | Must |
| REC-002 | Tạo kỳ đối soát/settlement | Finance | Must |
| REC-003 | Xem chi tiết kỳ đối soát/settlement | Admin/Ops, Finance | Must |
| REC-004 | Cập nhật trạng thái settlement | Finance | Must |
| REC-005 | Tạo adjustment thủ công | Finance | Should |
| REC-006 | Export dữ liệu đối soát/settlement | Finance | Must |

## 3. High-level Processing Flow

1. End user click Brand/Offer trên landing page.
2. Platform ghi nhận click tracking.
3. Brand gửi order success/cancel/refund event về Platform.
4. Platform ghi nhận transaction và số tạm tính.
5. Đến ngày chốt, Platform tính commission chính thức nếu order không bị cancel/refund.
6. Báo cáo Admin/Tenant đọc dữ liệu transaction theo quyền.
7. Finance tạo kỳ đối soát theo Brand/Tenant/cycle.
8. Hệ thống tổng hợp transaction đủ điều kiện và adjustment nếu có.
9. Finance rà soát số liệu, export file đối soát nếu cần.
10. Finance cập nhật trạng thái settlement theo quy trình vận hành.

# IV. Description of Functions

## 1. RPT-001 - Xem dashboard báo cáo Admin

### 1.1 Summary

Admin/Ops/Finance xem dashboard tổng quan toàn hệ thống để theo dõi hiệu quả vận hành marketplace, gồm click, conversion, GMV tracked, doanh thu/hoa hồng tạm tính, hoa hồng chính thức, phần chia Tenant và phần Affiliate giữ lại.

### 1.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Xem dashboard báo cáo Admin |
| Description | Cho phép người dùng CMS xem báo cáo tổng hợp theo khoảng thời gian, Tenant, Brand, Category, Offer và trạng thái order. |
| Actor | Admin/Ops, Finance |
| Role/Permission | `report.admin.read` |
| Precondition | User đã đăng nhập CMS và có quyền xem báo cáo Admin. Dữ liệu click/transaction đã được ghi nhận. |
| Postcondition | Dashboard hiển thị số liệu đúng theo filter và quyền truy cập. |

### 1.3 Main Flow

1. User mở màn hình Admin Reporting.
2. Hệ thống hiển thị filter mặc định theo ngày hiện tại hoặc khoảng thời gian mặc định.
3. User chọn filter cần xem.
4. Hệ thống validate filter.
5. Hệ thống truy vấn dữ liệu click, transaction, commission và exception.
6. Hệ thống hiển thị KPI, biểu đồ xu hướng và bảng top Brand/Offer/Tenant.
7. User có thể drill-down sang danh sách transaction hoặc settlement liên quan nếu có quyền.

### 1.4 Exception Flow

| Case | System behavior |
|---|---|
| Khoảng ngày không hợp lệ | Báo lỗi `Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc`. |
| Khoảng ngày vượt giới hạn truy vấn | Báo lỗi `Khoảng thời gian báo cáo vượt quá giới hạn cho phép`. |
| User không có quyền tài chính | Ẩn các field commission, tenant share, affiliate keep theo RBAC. |
| Không có dữ liệu | Hiển thị empty state, không hiển thị lỗi hệ thống. |
| Query timeout | Báo lỗi `Không tải được dữ liệu báo cáo. Vui lòng thử lại hoặc thu hẹp bộ lọc`. |

### 1.5 Screen Description

| STT | Field/Control | Type | R/O | Description, validation/rule |
|---:|---|---|---|---|
| 1 | Date range | Date range picker | R | Ngày bắt đầu/kết thúc báo cáo. `from_date <= to_date`. Có thể giới hạn tối đa theo cấu hình hệ thống. |
| 2 | Tenant | Dropdown multi-select | O | Lọc theo Tenant. Nếu để trống, hiển thị tất cả Tenant user có quyền xem. |
| 3 | Brand | Dropdown multi-select | O | Lọc theo Brand. Chỉ hiển thị Brand active hoặc có dữ liệu trong kỳ. |
| 4 | Category | Dropdown multi-select | O | Lọc theo Affiliate category. |
| 5 | Offer | Dropdown multi-select | O | Lọc theo Offer. |
| 6 | Order status | Dropdown multi-select | O | `Pending`, `Confirmed`, `Cancelled`. |
| 7 | Click count | KPI card | ReadOnly | Tổng click hợp lệ theo filter. |
| 8 | Conversion count | KPI card | ReadOnly | Tổng order success/transaction theo filter. |
| 9 | GMV tracked | KPI card | ReadOnly | Tổng order amount được ghi nhận. |
| 10 | Commission dự tính | KPI card | ReadOnly | Tổng `provisional_gross_commission_amount` của order chưa chốt. |
| 11 | Tenant share dự tính | KPI card | ReadOnly | Tổng `provisional_tenant_share_amount` của order chưa chốt. |
| 12 | Commission chính thức | KPI card | ReadOnly | Tổng `gross_commission_amount` của order đã Confirmed. |
| 13 | Tenant share chính thức | KPI card | ReadOnly | Tổng `tenant_share_amount` đã Confirmed. |
| 14 | Affiliate keep | KPI card | ReadOnly | Tổng `affiliate_keep_amount` đã Confirmed. |
| 15 | Exception count | KPI card | ReadOnly | Số exception liên quan missing rule/mapping/invalid event nếu có. |
| 16 | Apply filter | Button | O | Áp dụng bộ lọc. |
| 17 | Reset | Button | O | Đặt lại filter về mặc định. |

### 1.6 Business Rules

| Rule ID | Description |
|---|---|
| BR-RPT-001-01 | Dashboard Admin phải phân biệt rõ số tạm tính và số chính thức. |
| BR-RPT-001-02 | Số tạm tính không được cộng vào settlement/payable chính thức. |
| BR-RPT-001-03 | Order `Cancelled` không được tính vào commission/tenant share chính thức. |
| BR-RPT-001-04 | Admin/Ops chỉ xem field tài chính nếu có quyền tương ứng. |
| BR-RPT-001-05 | Dữ liệu report phải tính theo timezone cấu hình của Platform, MVP1 mặc định `Asia/Ho_Chi_Minh` nếu chưa cấu hình khác. |

### 1.7 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-RPT-001-01 | User có quyền mở dashboard và xem số liệu theo filter. |
| AC-RPT-001-02 | KPI tạm tính và chính thức hiển thị thành các nhóm/cột riêng. |
| AC-RPT-001-03 | User không có quyền tài chính không nhìn thấy commission/tenant share/affiliate keep. |
| AC-RPT-001-04 | Filter ngày sai hiển thị validation message rõ ràng. |
| AC-RPT-001-05 | Empty state hiển thị đúng khi không có dữ liệu. |

## 2. RPT-002 - Export báo cáo Admin

### 2.1 Summary

Admin/Ops/Finance export báo cáo theo bộ lọc hiện tại để phục vụ phân tích, vận hành hoặc chuẩn bị đối soát.

### 2.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Export báo cáo Admin |
| Description | Cho phép export CSV/XLSX dữ liệu dashboard hoặc transaction/report detail theo filter và quyền truy cập. |
| Actor | Admin/Ops, Finance |
| Role/Permission | `report.admin.export` |
| Precondition | User có quyền export. Filter hợp lệ. |
| Postcondition | File export được tạo/tải về; audit log ghi nhận thao tác export. |

### 2.3 Main Flow

1. User chọn filter báo cáo.
2. User bấm `Export`.
3. Hệ thống kiểm tra quyền export.
4. Hệ thống validate filter và giới hạn số dòng.
5. Hệ thống tạo file export.
6. User tải file về hoặc nhận link tải nội bộ nếu export chạy background.
7. Hệ thống ghi audit log.

### 2.4 Exception Flow

| Case | System behavior |
|---|---|
| Không có quyền export | Báo lỗi `Bạn không có quyền export báo cáo`. |
| Quá số dòng cho phép | Báo lỗi yêu cầu thu hẹp filter hoặc chuyển sang export background nếu hỗ trợ. |
| Không tạo được file | Báo lỗi và ghi system log để kỹ thuật kiểm tra. |

### 2.5 Export Fields

| STT | Field | R/O | Description |
|---:|---|---|---|
| 1 | report_period_from | R | Ngày bắt đầu báo cáo. |
| 2 | report_period_to | R | Ngày kết thúc báo cáo. |
| 3 | tenant_id | O | Tenant ID nếu dữ liệu có Tenant. |
| 4 | tenant_name | O | Tên Tenant. |
| 5 | brand_id | O | Brand ID. |
| 6 | brand_name | O | Tên Brand. |
| 7 | category_id | O | Affiliate category ID nếu có. |
| 8 | category_name | O | Tên category. |
| 9 | offer_id | O | Offer ID nếu transaction phát sinh từ Offer. |
| 10 | offer_title | O | Tên Offer. |
| 11 | click_count | O | Tổng click. |
| 12 | conversion_count | O | Tổng conversion/order. |
| 13 | gmv_tracked | O | Tổng GMV tracked. |
| 14 | provisional_gross_commission_amount | O | Commission dự tính. |
| 15 | provisional_tenant_share_amount | O | Tenant share dự tính. |
| 16 | gross_commission_amount | O | Commission chính thức. |
| 17 | tenant_share_amount | O | Tenant share chính thức. |
| 18 | affiliate_keep_amount | O | Affiliate keep chính thức. |
| 19 | cancelled_order_count | O | Số order Cancelled. |
| 20 | exception_count | O | Số exception. |

### 2.6 Business Rules

| Rule ID | Description |
|---|---|
| BR-RPT-002-01 | File export phải tuân theo cùng filter và quyền dữ liệu với màn hình. |
| BR-RPT-002-02 | Export Admin có thể bao gồm commission Brand -> Affiliate nếu user có quyền tài chính. |
| BR-RPT-002-03 | Mọi thao tác export phải ghi audit log. |
| BR-RPT-002-04 | Không export credential, API secret, raw sensitive payload. |

### 2.7 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-RPT-002-01 | User có quyền export được file theo đúng filter. |
| AC-RPT-002-02 | User không có quyền tài chính không export được field tài chính bị hạn chế. |
| AC-RPT-002-03 | File export phân biệt rõ cột tạm tính và chính thức. |
| AC-RPT-002-04 | Audit log ghi nhận actor, filter summary, file type và timestamp. |

## 3. RPT-003 - Xem dashboard báo cáo Tenant

### 3.1 Summary

Tenant user xem dashboard báo cáo trong phạm vi Tenant của mình. Tenant không được nhìn thấy commission Brand trả Affiliate hoặc phần Affiliate giữ lại.

### 3.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Xem dashboard báo cáo Tenant |
| Description | Cho phép Tenant xem click, order/conversion, GMV tracked và doanh thu chia sẻ của Tenant theo Brand/Offer/time range/status. |
| Actor | Tenant Admin, Tenant Finance, Tenant Viewer |
| Role/Permission | `tenant_report.read` |
| Precondition | User đăng nhập Tenant Portal và thuộc Tenant hợp lệ. |
| Postcondition | Dashboard chỉ hiển thị dữ liệu thuộc Tenant hiện tại. |

### 3.3 Main Flow

1. Tenant user mở dashboard.
2. Hệ thống tự xác định `tenant_id` từ session.
3. User chọn filter ngày, Brand, Offer, order status.
4. Hệ thống truy vấn dữ liệu trong tenant scope.
5. Hệ thống hiển thị KPI và bảng top Brand/Offer.

### 3.4 Exception Flow

| Case | System behavior |
|---|---|
| User không thuộc Tenant hợp lệ | Không cho truy cập dashboard. |
| User không có quyền xem số tài chính | Ẩn doanh thu chia sẻ dự tính/chính thức. |
| Không có dữ liệu | Hiển thị empty state. |

### 3.5 Screen Description

| STT | Field/Control | Type | R/O | Description, validation/rule |
|---:|---|---|---|---|
| 1 | Date range | Date range picker | R | Khoảng thời gian cần xem. |
| 2 | Brand | Dropdown multi-select | O | Chỉ hiển thị Brand được assign và đang visible với Tenant. |
| 3 | Offer | Dropdown multi-select | O | Chỉ hiển thị Offer thuộc Brand được assign/visible. |
| 4 | Order status | Dropdown multi-select | O | `Pending`, `Confirmed`, `Cancelled`. |
| 5 | Click count | KPI card | ReadOnly | Tổng click trong Tenant scope. |
| 6 | Conversion count | KPI card | ReadOnly | Tổng order/conversion trong Tenant scope. |
| 7 | GMV tracked | KPI card | ReadOnly | Tổng order amount được ghi nhận trong Tenant scope. |
| 8 | Doanh thu chia sẻ dự tính | KPI card | ReadOnly | Tổng `provisional_tenant_share_amount`; chỉ hiển thị với role tài chính. |
| 9 | Doanh thu chia sẻ chính thức | KPI card | ReadOnly | Tổng `tenant_share_amount`; chỉ hiển thị với role tài chính. |

### 3.6 Business Rules

| Rule ID | Description |
|---|---|
| BR-RPT-003-01 | Tenant Portal không được hiển thị `gross_commission_amount`, `provisional_gross_commission_amount`, `affiliate_keep_amount`. |
| BR-RPT-003-02 | Tenant chỉ xem dữ liệu thuộc `tenant_id` hiện tại. |
| BR-RPT-003-03 | Label dùng cho Tenant là `Doanh thu chia sẻ dự tính` và `Doanh thu chia sẻ chính thức`. |
| BR-RPT-003-04 | Dashboard Tenant không hiển thị dữ liệu cashback/point posting trong MVP1. |

### 3.7 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-RPT-003-01 | Tenant chỉ xem được dữ liệu của Tenant mình. |
| AC-RPT-003-02 | Tenant không thấy commission Brand -> Affiliate ở UI, API response và export. |
| AC-RPT-003-03 | Dashboard phân biệt rõ doanh thu chia sẻ dự tính và chính thức. |

## 4. RPT-004 - Export báo cáo Tenant

### 4.1 Summary

Tenant Admin/Finance export báo cáo thuộc phạm vi Tenant để phục vụ vận hành nội bộ.

### 4.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Export báo cáo Tenant |
| Description | Export CSV/XLSX dashboard hoặc transaction report trong phạm vi Tenant. |
| Actor | Tenant Admin, Tenant Finance |
| Role/Permission | `tenant_report.export` |
| Precondition | User có quyền export và filter hợp lệ. |
| Postcondition | File export được tạo; audit log Tenant ghi nhận thao tác. |

### 4.3 Export Fields

| STT | Field | R/O | Description |
|---:|---|---|---|
| 1 | report_period_from | R | Ngày bắt đầu. |
| 2 | report_period_to | R | Ngày kết thúc. |
| 3 | brand_id | O | Brand ID. |
| 4 | brand_name | O | Tên Brand. |
| 5 | offer_id | O | Offer ID nếu có. |
| 6 | offer_title | O | Tên Offer. |
| 7 | click_count | O | Tổng click. |
| 8 | conversion_count | O | Tổng conversion/order. |
| 9 | gmv_tracked | O | Tổng GMV tracked. |
| 10 | provisional_tenant_share_amount | O | Doanh thu chia sẻ dự tính. |
| 11 | tenant_share_amount | O | Doanh thu chia sẻ chính thức. |
| 12 | cancelled_order_count | O | Số order Cancelled. |

### 4.4 Business Rules

| Rule ID | Description |
|---|---|
| BR-RPT-004-01 | Export Tenant không bao gồm commission Brand -> Affiliate hoặc Affiliate keep. |
| BR-RPT-004-02 | Export Tenant luôn bị giới hạn bởi `tenant_id` trong session. |
| BR-RPT-004-03 | Mọi thao tác export Tenant phải ghi Tenant audit log. |

### 4.5 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-RPT-004-01 | Tenant Finance export được file đúng dữ liệu theo filter. |
| AC-RPT-004-02 | File export không chứa field tài chính nội bộ của Platform. |
| AC-RPT-004-03 | User không có quyền export không thấy hoặc không dùng được action export. |

## 5. REC-001 - Xem danh sách kỳ đối soát/settlement

### 5.1 Summary

Admin/Ops/Finance xem danh sách settlement record đã tạo để theo dõi trạng thái đối soát với Brand và Tenant.

### 5.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Xem danh sách kỳ đối soát/settlement |
| Description | Hiển thị danh sách settlement record theo Brand, Tenant, cycle, period, status và số tiền tổng hợp. |
| Actor | Admin/Ops, Finance |
| Role/Permission | `settlement.read` |
| Precondition | User đăng nhập CMS và có quyền xem settlement. |
| Postcondition | Danh sách settlement hiển thị theo filter. |

### 5.3 Main Flow

1. User mở màn Settlement Tracking.
2. Hệ thống hiển thị filter và danh sách settlement record.
3. User lọc theo Brand, Tenant, period, cycle, status.
4. Hệ thống trả kết quả theo filter.
5. User click vào một record để xem chi tiết.

### 5.4 Screen Description

| STT | Field/Control | Type | R/O | Description, validation/rule |
|---:|---|---|---|---|
| 1 | Keyword | Text input | O | Tìm theo settlement_id, Brand name, Tenant name. Không tìm theo credential/raw payload. |
| 2 | Brand | Dropdown | O | Lọc theo Brand. |
| 3 | Tenant | Dropdown | O | Lọc theo Tenant. |
| 4 | Period from/to | Date range picker | O | Kỳ đối soát. `from <= to`. |
| 5 | Status | Dropdown | O | `Draft`, `In Review`, `Confirmed`, `Settled`, `Cancelled`. |
| 6 | Settlement ID | Table column | ReadOnly | Mã settlement record. |
| 7 | Brand | Table column | ReadOnly | Brand liên quan. |
| 8 | Tenant | Table column | ReadOnly | Tenant liên quan. |
| 9 | Period | Table column | ReadOnly | Kỳ đối soát. |
| 10 | Gross commission | Table column | ReadOnly | Tổng Brand commission chính thức trong kỳ. |
| 11 | Tenant share | Table column | ReadOnly | Tổng phần chia Tenant chính thức trong kỳ. |
| 12 | Affiliate keep | Table column | ReadOnly | Tổng phần Affiliate giữ lại trong kỳ. |
| 13 | Adjustment amount | Table column | ReadOnly | Tổng điều chỉnh cộng/trừ nếu có. |
| 14 | Status | Table column | ReadOnly | Trạng thái settlement. |
| 15 | Action | Button/menu | O | Xem chi tiết/cập nhật trạng thái theo quyền. |

### 5.5 Business Rules

| Rule ID | Description |
|---|---|
| BR-REC-001-01 | Settlement list chỉ dùng số chính thức và adjustment đã được ghi nhận. |
| BR-REC-001-02 | Không đưa transaction `Pending` hoặc `Cancelled` vào settlement payable. |
| BR-REC-001-03 | Settlement cycle theo từng hợp đồng Brand/Tenant, không hard-code theo tháng/quý. |

### 5.6 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-REC-001-01 | User xem được danh sách settlement theo filter. |
| AC-REC-001-02 | Bảng hiển thị tổng gross commission, tenant share, affiliate keep và adjustment. |
| AC-REC-001-03 | Pending/Cancelled transaction không xuất hiện trong số settlement chính thức. |

## 6. REC-002 - Tạo kỳ đối soát/settlement

### 6.1 Summary

Finance tạo settlement record theo Brand/Tenant và kỳ đối soát. Hệ thống tổng hợp transaction đủ điều kiện, áp dụng adjustment nếu có và tạo bản ghi ở trạng thái ban đầu.

### 6.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Tạo kỳ đối soát/settlement |
| Description | Tạo settlement record cho một Brand/Tenant/cycle/period để phục vụ đối soát. |
| Actor | Finance |
| Role/Permission | `settlement.create` |
| Precondition | Có transaction `Confirmed` trong kỳ hoặc có adjustment cần đối soát. Brand/Tenant có contract/cycle hợp lệ. |
| Postcondition | Settlement record được tạo ở trạng thái `Draft` hoặc `In Review` theo cấu hình workflow. |

### 6.3 Main Flow

1. Finance chọn tạo settlement mới.
2. User chọn Brand, Tenant và kỳ đối soát.
3. Hệ thống validate Brand/Tenant/cycle.
4. Hệ thống lấy transaction `Confirmed` đủ điều kiện trong kỳ.
5. Hệ thống lấy adjustment chưa được đưa vào settlement nếu thuộc kỳ.
6. Hệ thống tính tổng gross commission, tenant share, affiliate keep và adjustment.
7. User xem preview số liệu.
8. User xác nhận tạo settlement.
9. Hệ thống tạo settlement record và settlement lines.
10. Hệ thống ghi audit log.

### 6.4 Exception Flow

| Case | System behavior |
|---|---|
| Brand/Tenant chưa có cycle hợp lệ | Báo lỗi `Chưa có cấu hình cycle đối soát cho Brand/Tenant này`. |
| Kỳ bị trùng với settlement đã tồn tại | Báo lỗi `Kỳ đối soát đã tồn tại`. |
| Không có transaction đủ điều kiện | Cho phép tạo settlement rỗng nếu có quyền/policy cho phép, hoặc báo `Không có dữ liệu đủ điều kiện`. |
| Có transaction exception chưa xử lý | Cảnh báo và cho phép Finance quyết định loại trừ hoặc dừng tạo theo policy. |

### 6.5 Screen Description

| STT | Field/Control | Type | R/O | Description, validation/rule |
|---:|---|---|---|---|
| 1 | Brand | Dropdown | R | Chọn Brand cần đối soát. |
| 2 | Tenant | Dropdown | R | Chọn Tenant cần đối soát. Chỉ hiển thị Tenant đã được assign Brand. |
| 3 | Settlement cycle | Label/Dropdown | R | Lấy theo hợp đồng Brand/Tenant. Có thể là monthly, quarterly hoặc custom theo hợp đồng. |
| 4 | Period from | Date picker | R | Ngày bắt đầu kỳ. |
| 5 | Period to | Date picker | R | Ngày kết thúc kỳ. `period_from <= period_to`. |
| 6 | Include adjustments | Checkbox | O | Mặc định bật nếu có adjustment chưa settle trong kỳ. |
| 7 | Preview totals | Summary section | ReadOnly | Hiển thị transaction count, gross commission, tenant share, affiliate keep, adjustment. |
| 8 | Create settlement | Button | O | Tạo settlement nếu dữ liệu hợp lệ. |

### 6.6 Business Rules

| Rule ID | Description |
|---|---|
| BR-REC-002-01 | Một Brand/Tenant/period không được tạo trùng settlement active. |
| BR-REC-002-02 | Chỉ transaction `Confirmed` chưa thuộc settlement khác mới được đưa vào settlement. |
| BR-REC-002-03 | Transaction `Pending` chỉ xuất hiện ở báo cáo forecast, không đưa vào settlement. |
| BR-REC-002-04 | Adjustment đã được settle không được đưa lại vào settlement khác. |
| BR-REC-002-05 | Settlement tạo mới phải lưu snapshot số liệu tại thời điểm tạo. |

### 6.7 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-REC-002-01 | Finance tạo settlement thành công khi Brand/Tenant/period hợp lệ. |
| AC-REC-002-02 | Hệ thống không cho tạo settlement trùng kỳ. |
| AC-REC-002-03 | Settlement line chỉ gồm transaction Confirmed đủ điều kiện và adjustment hợp lệ. |
| AC-REC-002-04 | Audit log ghi nhận thao tác tạo settlement. |

## 7. REC-003 - Xem chi tiết kỳ đối soát/settlement

### 7.1 Summary

Admin/Ops/Finance xem chi tiết settlement gồm thông tin kỳ, tổng tiền, danh sách transaction, adjustment và lịch sử trạng thái.

### 7.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Xem chi tiết kỳ đối soát/settlement |
| Description | Hiển thị thông tin settlement record và các line item phục vụ đối soát. |
| Actor | Admin/Ops, Finance |
| Role/Permission | `settlement.read` |
| Precondition | Settlement record tồn tại. |
| Postcondition | User xem được chi tiết theo quyền. |

### 7.3 Screen Description

| STT | Field/Control | Type | R/O | Description, validation/rule |
|---:|---|---|---|---|
| 1 | Settlement ID | Label | ReadOnly | Mã settlement. |
| 2 | Brand | Label | ReadOnly | Brand liên quan. |
| 3 | Tenant | Label | ReadOnly | Tenant liên quan. |
| 4 | Period | Label | ReadOnly | Kỳ đối soát. |
| 5 | Status | Badge | ReadOnly | `Draft`, `In Review`, `Confirmed`, `Settled`, `Cancelled`. |
| 6 | Transaction count | Summary | ReadOnly | Số transaction trong settlement. |
| 7 | Gross commission | Summary | ReadOnly | Tổng Brand commission chính thức. |
| 8 | Tenant share | Summary | ReadOnly | Tổng chia sẻ Tenant chính thức. |
| 9 | Affiliate keep | Summary | ReadOnly | Tổng Affiliate giữ lại. |
| 10 | Adjustment amount | Summary | ReadOnly | Tổng điều chỉnh cộng/trừ. |
| 11 | Settlement lines | Table | ReadOnly | Danh sách transaction/adjustment line. |
| 12 | Status history | Timeline | ReadOnly | Lịch sử thay đổi trạng thái settlement. |
| 13 | Export | Button | O | Export chi tiết settlement theo quyền. |

### 7.4 Settlement Line Fields

| STT | Field | R/O | Description |
|---:|---|---|---|
| 1 | line_id | R | Mã line item. |
| 2 | line_type | R | `Transaction` hoặc `Adjustment`. |
| 3 | transaction_id | O | Transaction liên quan nếu line type là Transaction. |
| 4 | brand_order_id | O | Mã order phía Brand. |
| 5 | order_success_at | O | Thời điểm Brand báo order success. |
| 6 | official_calculation_at | O | Thời điểm chốt commission chính thức. |
| 7 | gross_commission_amount | O | Commission Brand -> Affiliate. |
| 8 | tenant_share_amount | O | Phần chia Tenant. |
| 9 | affiliate_keep_amount | O | Phần Affiliate giữ lại. |
| 10 | adjustment_amount | O | Giá trị adjustment nếu có. |
| 11 | adjustment_reason | O | Lý do adjustment. |

### 7.5 Business Rules

| Rule ID | Description |
|---|---|
| BR-REC-003-01 | Settlement detail phải hiển thị snapshot tại thời điểm tạo/chốt settlement, không tự thay đổi ngầm theo rule mới. |
| BR-REC-003-02 | Nếu transaction bị điều chỉnh sau settlement, tạo adjustment record thay vì sửa trực tiếp line đã chốt. |
| BR-REC-003-03 | User không có quyền settlement finance không được xem field tiền nhạy cảm. |

### 7.6 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-REC-003-01 | User xem được tổng tiền và line item của settlement. |
| AC-REC-003-02 | Detail phân biệt rõ transaction line và adjustment line. |
| AC-REC-003-03 | Số liệu trong settlement đã Confirmed/Settled không bị thay đổi khi commission rule sau đó thay đổi. |

## 8. REC-004 - Cập nhật trạng thái settlement

### 8.1 Summary

Finance cập nhật trạng thái settlement theo quy trình vận hành đối soát.

### 8.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Cập nhật trạng thái settlement |
| Description | Cho phép Finance chuyển trạng thái settlement theo workflow được phép. |
| Actor | Finance |
| Role/Permission | `settlement.update_status` |
| Precondition | Settlement tồn tại và user có quyền cập nhật. |
| Postcondition | Settlement chuyển trạng thái hợp lệ và audit log được ghi nhận. |

### 8.3 Status Definition

| Status | Description |
|---|---|
| Draft | Settlement mới tạo, chưa gửi/khóa để đối soát. |
| In Review | Đang rà soát với Brand/Tenant/Finance. |
| Confirmed | Số liệu đối soát đã được xác nhận nội bộ hoặc với đối tác theo quy trình. |
| Settled | Đã hoàn tất thanh toán/ghi nhận settlement theo quy trình Finance. |
| Cancelled | Settlement bị hủy, không dùng để thanh toán. |

### 8.4 Main Flow

1. Finance mở settlement detail.
2. User chọn action cập nhật trạng thái.
3. Hệ thống kiểm tra workflow transition hợp lệ.
4. User nhập ghi chú nếu trạng thái yêu cầu.
5. Hệ thống cập nhật trạng thái.
6. Hệ thống ghi status history và audit log.

### 8.5 Business Rules

| Rule ID | Description |
|---|---|
| BR-REC-004-01 | Chỉ Finance có quyền mới được cập nhật settlement status. |
| BR-REC-004-02 | Không cho sửa line item trực tiếp khi settlement đã `Confirmed` hoặc `Settled`. |
| BR-REC-004-03 | Chuyển sang `Cancelled` phải yêu cầu lý do. |
| BR-REC-004-04 | Settlement đã `Settled` chỉ được điều chỉnh bằng adjustment kỳ sau, không sửa settlement gốc. |

### 8.6 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-REC-004-01 | Finance chuyển trạng thái theo workflow hợp lệ. |
| AC-REC-004-02 | Transition không hợp lệ bị chặn và hiển thị lỗi. |
| AC-REC-004-03 | Status history và audit log ghi nhận đầy đủ actor, thời gian, trạng thái trước/sau. |

## 9. REC-005 - Tạo adjustment thủ công

### 9.1 Summary

Finance tạo adjustment thủ công để xử lý sai lệch sau khi transaction đã Confirmed hoặc settlement đã chốt, ví dụ Brand báo refund muộn, sai số tiền order, sai commission hoặc quyết định Finance.

### 9.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Tạo adjustment thủ công |
| Description | Tạo bản ghi điều chỉnh cộng/trừ gắn với Brand/Tenant, transaction hoặc settlement liên quan. |
| Actor | Finance |
| Role/Permission | `settlement.adjustment.create` |
| Precondition | Có lý do điều chỉnh hợp lệ. Nếu gắn transaction, transaction phải tồn tại. |
| Postcondition | Adjustment được ghi nhận ở trạng thái chờ đưa vào settlement hoặc đã gắn với settlement hiện tại. |

### 9.3 Main Flow

1. Finance chọn tạo adjustment.
2. User nhập Brand, Tenant, adjustment type, amount, reason.
3. User có thể gắn transaction_id hoặc settlement_id liên quan.
4. Hệ thống validate dữ liệu.
5. Hệ thống lưu adjustment.
6. Hệ thống ghi audit log.
7. Adjustment được đưa vào kỳ settlement phù hợp theo policy.

### 9.4 Exception Flow

| Case | System behavior |
|---|---|
| Amount bằng 0 | Báo lỗi `Số tiền điều chỉnh phải khác 0`. |
| Thiếu reason | Báo lỗi `Vui lòng nhập lý do điều chỉnh`. |
| Transaction không thuộc Brand/Tenant đã chọn | Báo lỗi `Transaction không thuộc Brand/Tenant này`. |
| Settlement đã Settled | Không sửa settlement gốc; adjustment được đánh dấu đưa vào kỳ sau. |

### 9.5 Screen Description

| STT | Field/Control | Type | R/O | Description, validation/rule |
|---:|---|---|---|---|
| 1 | Brand | Dropdown | R | Brand liên quan đến adjustment. |
| 2 | Tenant | Dropdown | R | Tenant liên quan đến adjustment. |
| 3 | Adjustment type | Dropdown | R | `Increase`, `Decrease`. |
| 4 | Adjustment target | Dropdown | R | `Gross commission`, `Tenant share`, `Affiliate keep` hoặc combo theo policy Finance. |
| 5 | Amount | Money input | R | Số tiền điều chỉnh, > 0. MVP1 dùng VND. |
| 6 | Related transaction ID | Text/Lookup | O | Transaction liên quan nếu có. |
| 7 | Related settlement ID | Text/Lookup | O | Settlement liên quan nếu có. |
| 8 | Reason | Textarea | R | Lý do điều chỉnh, tối thiểu 10 ký tự, tối đa theo cấu hình UI. |
| 9 | Attachment reference | File/link | O | Tài liệu đối chiếu nếu hệ thống hỗ trợ upload/link. |
| 10 | Save | Button | O | Lưu adjustment nếu dữ liệu hợp lệ. |

### 9.6 Business Rules

| Rule ID | Description |
|---|---|
| BR-REC-005-01 | Adjustment phải có reason rõ ràng. |
| BR-REC-005-02 | Cancel/Refund API cho transaction đã `Confirmed` hoặc settlement đã `Settled` bị từ chối và ghi Exception. Nếu cần điều chỉnh, Admin/Finance tạo adjustment thủ công; không đổi Order Status hoặc tự động ghi đè dữ liệu đã chốt trong MVP1. |
| BR-REC-005-03 | Adjustment đã đưa vào settlement thì không được xóa cứng; nếu sai phải tạo adjustment đảo chiều. |
| BR-REC-005-04 | Adjustment phải ghi audit log và lưu actor/timestamp. |

### 9.7 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-REC-005-01 | Finance tạo được adjustment hợp lệ. |
| AC-REC-005-02 | Amount = 0 hoặc thiếu reason bị chặn. |
| AC-REC-005-03 | Adjustment được đưa vào settlement đúng kỳ theo policy. |
| AC-REC-005-04 | Adjustment không sửa trực tiếp transaction/order status gốc. |

## 10. REC-006 - Export dữ liệu đối soát/settlement

### 10.1 Summary

Finance export settlement summary hoặc settlement line detail để gửi đối tác hoặc lưu hồ sơ đối soát.

### 10.2 Use Case Specification

| Item | Description |
|---|---|
| Title | Export dữ liệu đối soát/settlement |
| Description | Export settlement summary/detail theo quyền. |
| Actor | Finance |
| Role/Permission | `settlement.export` |
| Precondition | Settlement tồn tại và user có quyền export. |
| Postcondition | File export được tạo và audit log ghi nhận. |

### 10.3 Export Fields

| STT | Field | R/O | Description |
|---:|---|---|---|
| 1 | settlement_id | R | Mã settlement. |
| 2 | brand_id | R | Brand ID. |
| 3 | brand_name | R | Brand name. |
| 4 | tenant_id | R | Tenant ID. |
| 5 | tenant_name | R | Tenant name. |
| 6 | period_from | R | Ngày bắt đầu kỳ. |
| 7 | period_to | R | Ngày kết thúc kỳ. |
| 8 | status | R | Trạng thái settlement. |
| 9 | line_type | O | Transaction/Adjustment. |
| 10 | transaction_id | O | Transaction ID nếu có. |
| 11 | brand_order_id | O | Mã order phía Brand. |
| 12 | gross_commission_amount | O | Commission Brand -> Affiliate. |
| 13 | tenant_share_amount | O | Phần chia Tenant. |
| 14 | affiliate_keep_amount | O | Phần Affiliate giữ lại. |
| 15 | adjustment_amount | O | Số điều chỉnh. |
| 16 | adjustment_reason | O | Lý do điều chỉnh. |

### 10.4 Business Rules

| Rule ID | Description |
|---|---|
| BR-REC-006-01 | Export settlement chỉ dành cho role có quyền settlement export. |
| BR-REC-006-02 | Export cho Tenant nếu có sau này phải loại bỏ gross commission và affiliate keep. |
| BR-REC-006-03 | Export phải ghi audit log. |

### 10.5 Acceptance Criteria

| AC ID | Description |
|---|---|
| AC-REC-006-01 | Finance export được settlement summary/detail. |
| AC-REC-006-02 | File export chứa đầy đủ settlement line và adjustment. |
| AC-REC-006-03 | Audit log ghi nhận thao tác export settlement. |

# V. Data Requirements

## 1. Reporting Filter

| Field | Type | R/O | Description |
|---|---|---|---|
| date_from | Date | R | Ngày bắt đầu filter. |
| date_to | Date | R | Ngày kết thúc filter. |
| tenant_ids | Array | O | Danh sách Tenant cần lọc. |
| brand_ids | Array | O | Danh sách Brand cần lọc. |
| category_ids | Array | O | Danh sách Category cần lọc. |
| offer_ids | Array | O | Danh sách Offer cần lọc. |
| order_statuses | Array | O | `Pending`, `Confirmed`, `Cancelled`. |
| grouping | Enum | O | `Date`, `Tenant`, `Brand`, `Category`, `Offer`. |
| timezone | String | O | Timezone dùng tính kỳ báo cáo. |

## 2. Reporting Metric

| Field | Type | R/O | Description |
|---|---|---|---|
| click_count | Integer | O | Tổng click hợp lệ. |
| conversion_count | Integer | O | Tổng transaction/order success. |
| conversion_rate | Decimal | O | `conversion_count / click_count` nếu click_count > 0. |
| gmv_tracked | Money | O | Tổng order amount được ghi nhận. |
| provisional_revenue_amount | Money | O | Doanh thu/order amount tạm tính. |
| provisional_gross_commission_amount | Money | O | Commission Brand -> Affiliate tạm tính. Chỉ Admin/Finance xem. |
| provisional_tenant_share_amount | Money | O | Doanh thu chia sẻ Tenant dự tính. |
| gross_commission_amount | Money | O | Commission Brand -> Affiliate chính thức. Chỉ Admin/Finance xem. |
| tenant_share_amount | Money | O | Doanh thu chia sẻ Tenant chính thức. |
| affiliate_keep_amount | Money | O | Affiliate keep chính thức. Chỉ Admin/Finance xem. |
| cancelled_order_count | Integer | O | Số order Cancelled. |
| exception_count | Integer | O | Số exception liên quan dữ liệu/report. |

## 3. Settlement Record

| Field | Type | R/O | Description |
|---|---|---|---|
| settlement_id | String | R | Mã settlement unique. |
| brand_id | String | R | Brand liên quan. |
| tenant_id | String | R | Tenant liên quan. |
| contract_cycle_code | String | O | Cycle theo hợp đồng, ví dụ monthly/quarterly/custom. |
| period_from | Date | R | Ngày bắt đầu kỳ. |
| period_to | Date | R | Ngày kết thúc kỳ. |
| status | Enum | R | `Draft`, `In Review`, `Confirmed`, `Settled`, `Cancelled`. |
| transaction_count | Integer | O | Số transaction line. |
| gross_commission_amount | Money | O | Tổng gross commission. |
| tenant_share_amount | Money | O | Tổng tenant share. |
| affiliate_keep_amount | Money | O | Tổng affiliate keep. |
| adjustment_amount | Money | O | Tổng adjustment cộng/trừ. |
| final_gross_commission_amount | Money | O | Gross commission sau adjustment nếu policy áp dụng. |
| final_tenant_share_amount | Money | O | Tenant share sau adjustment nếu policy áp dụng. |
| final_affiliate_keep_amount | Money | O | Affiliate keep sau adjustment nếu policy áp dụng. |
| created_by | String | R | User tạo settlement. |
| created_at | Datetime | R | Thời điểm tạo. |
| confirmed_by | String | O | User xác nhận. |
| confirmed_at | Datetime | O | Thời điểm xác nhận. |
| settled_by | String | O | User đánh dấu settled. |
| settled_at | Datetime | O | Thời điểm settled. |

## 4. Settlement Line

| Field | Type | R/O | Description |
|---|---|---|---|
| settlement_line_id | String | R | Mã line unique. |
| settlement_id | String | R | Settlement cha. |
| line_type | Enum | R | `Transaction`, `Adjustment`. |
| transaction_id | String | O | Transaction liên quan. |
| adjustment_id | String | O | Adjustment liên quan. |
| gross_commission_amount | Money | O | Gross commission line. |
| tenant_share_amount | Money | O | Tenant share line. |
| affiliate_keep_amount | Money | O | Affiliate keep line. |
| line_status | Enum | O | `Included`, `Excluded`, `Adjusted`. |
| note | Text | O | Ghi chú line. |

## 5. Adjustment Record

| Field | Type | R/O | Description |
|---|---|---|---|
| adjustment_id | String | R | Mã adjustment unique. |
| brand_id | String | R | Brand liên quan. |
| tenant_id | String | R | Tenant liên quan. |
| adjustment_type | Enum | R | `Increase`, `Decrease`. |
| adjustment_target | Enum | R | `Gross commission`, `Tenant share`, `Affiliate keep`. |
| amount | Money | R | Số tiền điều chỉnh, > 0. |
| currency | String | R | MVP1 mặc định `VND`. |
| related_transaction_id | String | O | Transaction liên quan. |
| related_settlement_id | String | O | Settlement liên quan. |
| reason | Text | R | Lý do điều chỉnh. |
| status | Enum | R | `Pending`, `Included`, `Cancelled`. |
| created_by | String | R | User tạo. |
| created_at | Datetime | R | Thời điểm tạo. |

## 6. Export Job

| Field | Type | R/O | Description |
|---|---|---|---|
| export_job_id | String | R | Mã job export. |
| export_type | Enum | R | `Admin Report`, `Tenant Report`, `Settlement Summary`, `Settlement Detail`. |
| requested_by | String | R | User yêu cầu export. |
| tenant_scope | String | O | Tenant scope nếu export Tenant. |
| filter_snapshot | JSON | R | Snapshot filter tại thời điểm export. |
| file_format | Enum | R | `CSV`, `XLSX`. |
| status | Enum | R | `Processing`, `Completed`, `Failed`, `Expired`. |
| file_url | String | O | Link tải nội bộ nếu có. |
| created_at | Datetime | R | Thời điểm tạo. |
| expired_at | Datetime | O | Thời điểm link/file hết hạn nếu có. |

# VI. Consolidated Business Rules Summary

| Rule ID | Description |
|---|---|
| BR-RR-GEN-001 | Báo cáo phải phân biệt rõ số tạm tính và số chính thức trên UI, API và export. |
| BR-RR-GEN-002 | Số tạm tính không được đưa vào settlement/payable chính thức. |
| BR-RR-GEN-003 | Settlement chỉ lấy transaction `Confirmed` chưa được settle và adjustment hợp lệ. |
| BR-RR-GEN-004 | Transaction `Cancelled` không được tính vào commission/tenant share chính thức. |
| BR-RR-GEN-005 | Cancel/Refund API sau `Confirmed`/`Settled` bị từ chối và ghi Exception. Adjustment chỉ được Admin/Finance thực hiện thủ công khi đối soát; không sửa Order Status gốc trong MVP1. |
| BR-RR-GEN-006 | Settlement cycle theo từng hợp đồng Brand/Tenant, không hard-code theo tháng/quý. |
| BR-RR-GEN-007 | Tenant Portal không được hiển thị commission Brand -> Affiliate hoặc Affiliate keep. |
| BR-RR-GEN-008 | Export phải tuân thủ RBAC, tenant isolation và masking policy. |
| BR-RR-GEN-009 | Tạo/chốt/hủy settlement, tạo adjustment và export phải ghi audit log. |
| BR-RR-GEN-010 | Settlement đã Confirmed/Settled phải giữ snapshot số liệu; không tự thay đổi theo rule mới. |

# VII. Non-functional Requirements

| ID | Requirement |
|---|---|
| NFR-RR-001 | Report query phải phản hồi trong thời gian chấp nhận được với filter thông thường; dữ liệu lớn có thể dùng export background. |
| NFR-RR-002 | Hệ thống phải enforce RBAC và tenant isolation ở backend, không chỉ ẩn UI. |
| NFR-RR-003 | File export phải có encoding phù hợp để mở được với Excel và giữ tiếng Việt. |
| NFR-RR-004 | Số tiền phải định dạng nhất quán theo currency và locale. |
| NFR-RR-005 | Các thao tác tài chính quan trọng phải có audit log. |
| NFR-RR-006 | Báo cáo cần tránh double count khi transaction hoặc adjustment được xử lý lại. |

# VIII. Consolidated Acceptance Criteria Summary

| AC ID | Description |
|---|---|
| AC-RR-GEN-001 | Admin xem được dashboard toàn hệ thống theo filter và quyền. |
| AC-RR-GEN-002 | Tenant xem được dashboard trong phạm vi Tenant và không thấy commission Brand -> Affiliate. |
| AC-RR-GEN-003 | Báo cáo/export có cột riêng cho số tạm tính và số chính thức. |
| AC-RR-GEN-004 | Finance tạo được settlement theo Brand/Tenant/period hợp lệ. |
| AC-RR-GEN-005 | Settlement không lấy order Pending/Cancelled vào số chính thức. |
| AC-RR-GEN-006 | Finance xem được settlement detail gồm transaction line và adjustment line. |
| AC-RR-GEN-007 | Finance cập nhật trạng thái settlement theo workflow hợp lệ. |
| AC-RR-GEN-008 | Finance tạo được adjustment cho refund/sai lệch sau chốt. |
| AC-RR-GEN-009 | Export report/settlement ghi audit log. |
| AC-RR-GEN-010 | Settlement đã Confirmed/Settled giữ snapshot số liệu, không bị thay đổi bởi rule mới. |

# IX. Open Questions

| STT | Question | Note |
|---:|---|---|
| 1 | Có cần attachment/upload file đối soát từ Brand trong MVP1 không? | Hiện tài liệu chỉ mô tả attachment reference optional. |
| 2 | Workflow settlement có cần bước Brand/Tenant xác nhận trên portal không? | MVP1 đang giả định Finance cập nhật trạng thái trên CMS. |
| 3 | Có cần tự động tạo settlement theo lịch không? | MVP1 có thể tạo thủ công; tự động hóa để mở rộng sau. |
| 4 | Multi-currency có nằm trong MVP1 không? | Hiện mặc định VND. |
| 5 | Quy tắc final amount sau adjustment áp vào gross commission/tenant share/affiliate keep chi tiết ra sao? | Cần Finance chốt khi triển khai nghiệp vụ thanh toán thực tế. |
