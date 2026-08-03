# SRS: White-label Affiliate Marketplace Platform

## Document control

- Status: Draft
- Owner: TBD
- Technical owner: TBD
- Stakeholders: Business, Partnership, Product, Operations, Tenant Success, Finance, Legal/Compliance, Engineering, QA
- Last updated: 2026-07-23
- Source BRD: [docs/brd/affiliate-marketplace-platform.md](../brd/affiliate-marketplace-platform.md)
- Source analysis: [docs/analysis/affiliate-marketplace-platform-analysis.md](../analysis/affiliate-marketplace-platform-analysis.md)
- Source use cases: [docs/usecases/affiliate-marketplace-platform-usecase-list.md](../usecases/affiliate-marketplace-platform-usecase-list.md)
- Source activity diagram: [docs/modeling/affiliate-marketplace-customer-journey-activity-diagram.md](../modeling/affiliate-marketplace-customer-journey-activity-diagram.md)
- Source mockup: [docs/mockups/affiliate-marketplace-landing-page-desktop.html](../mockups/affiliate-marketplace-landing-page-desktop.html)

## Document Revision History

| Ver. | Date | Changed by | Modifications |
|---|---|---|---|
| 0.1 | 2026-07-09 | Codex | Draft SRS theo use case list UC-001..UC-020. |
| 0.2 | 2026-07-09 | Codex | Cập nhật theo template SRS Quy Nguyen: bổ sung abbreviation, overall description, feature list, GUI elements, field-level data dictionary, rule catalog và integration payload fields. |
| 0.3 | 2026-07-09 | Codex | Bổ sung chi tiết tính năng CMS Brand Management: use case list, use case specification, màn danh sách/lọc, màn thêm/sửa/xem chi tiết/xóa và field-level requirements. |
| 0.4 | 2026-07-09 | Codex | Cập nhật CMS-BRAND-003: bỏ API credential reference, Order success API status, Cancel/refund integration status khỏi form thêm/sửa Brand; tạo mockup màn thêm mới Brand. |

## List of Abbreviations

| Abbreviation | Meaning |
|---|---|
| SRS | Software Requirement Specification |
| BRD | Business Requirement Document |
| UC | Use Case |
| SR | System Requirement |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| EU | End user |
| Tenant | Enterprise/partner sở hữu marketplace white-label và hệ thống loyalty |
| Brand | Brand/Merchant bán hàng hoặc cung cấp offer |
| B1 | Tỷ lệ cashback Tenant chia cho End user qua Platform nếu Tenant yêu cầu; deferred sau MVP1 theo CR-01 |
| gross_commission_amount | Commission Brand trả Affiliate sau khi tính theo rule Category/Offer |
| tenant_share_rate | Tỷ lệ % Affiliate chia cho Tenant, tính trên `gross_commission_amount` |
| tenant_share_amount | Số tiền Affiliate chia cho Tenant |
| affiliate_keep_amount | Số tiền Affiliate giữ lại sau khi chia Tenant |
| API | Application Programming Interface |
| SLA | Service Level Agreement |
| PII | Personally Identifiable Information |
| TBD | To Be Determined |

## Introduction

### Purpose

Tài liệu SRS này mô tả yêu cầu hệ thống cho Affiliate Marketplace Platform theo MVP1. Tài liệu được tổ chức theo use case, gồm use case list và use case detail để Product, Engineering và QA có thể chuyển thành backlog, API contract, test cases và acceptance criteria.

### Scope

SRS này đặc tả hệ thống Affiliate Marketplace Platform cho MVP1, bao gồm marketplace white-label, cấu hình Tenant/Brand/Offer, visibility theo Tenant, click tracking, order ingestion, commission/revenue share, reporting và settlement tracking. Theo CR-01, MVP1 không làm cashback B1, không tính/cộng điểm cho End user và không gọi Tenant Loyalty API.

### Out of Scope

Các nội dung không thuộc phạm vi SRS/MVP1 gồm CPC billing, listing fee billing/reporting, Brand portal tự cấu hình commission/cashback, checkout/payment của Brand trong Platform, native mobile app riêng, full accounting ledger, cashback B1, point conversion, Tenant Loyalty API posting, batch point posting và lịch sử order/cashback End user 3 tab.

### References

- IEEE SRS Standard: IEEE 830-1998, dùng như định hướng cấu trúc.
- [BRD: White-label Affiliate Marketplace Platform](../brd/affiliate-marketplace-platform.md)
- [Functional Analysis](../analysis/affiliate-marketplace-platform-analysis.md)
- [Use Case List](../usecases/affiliate-marketplace-platform-usecase-list.md)
- [PlantUML Customer Journey Activity Diagram](../modeling/affiliate-marketplace-customer-journey-activity-diagram.md)
- [Landing Page Desktop Mockup](../mockups/affiliate-marketplace-landing-page-desktop.html)

### Overview

Tài liệu bao gồm mô tả tổng quan hệ thống, feature list, user classes, use case specifications, GUI elements, functional requirements, non-functional requirements, data dictionary, rule catalog, API/interface requirements, validation/error handling, audit/observability, acceptance criteria, traceability, dependencies, risks và open questions.

### Product summary

Affiliate Marketplace Platform là hệ thống trung gian multi-tenant giữa Brand/Merchant và Tenant có hệ sinh thái loyalty. Mỗi Tenant có marketplace white-label riêng để End user xem Brand/Offer, click sang Brand mua hàng, Platform tracking click/order, tính commission/revenue share, chờ số ngày theo Brand để chốt chính thức sau giai đoạn tạm tính, báo cáo và đối soát. MVP1 không cộng điểm qua Tenant Loyalty API.

## System scope

### In scope

- Multi-tenant white-label marketplace theo subdomain/custom domain.
- Tenant setup: domain, branding, locale.
- Brand setup: profile, API credentials, commission Brand -> Affiliate theo Category/Offer, pending days.
- Offer/content management đa ngôn ngữ.
- Top brands, category và offer listing theo Tenant. Banner Management/banner slider thuộc Deferred/Phase 2.
- Cấu hình Brand/Offer visibility theo Tenant; mặc định hidden nếu chưa assign active.
- Click tracking phục vụ nối order theo `click_id` và reporting; không tính CPC billing.
- Brand order success API real-time.
- Brand Cancel/Refund API theo từng Order Item, chỉ tự động áp dụng cho Order `Pending`; contract chi tiết theo Order Transaction SRS.
- Commission/revenue share: Brand trả commission theo Category/Offer; Affiliate chia revenue share cho Tenant.
- Provisional → official calculation theo `pending_days` khi order không bị cancel/refund.
- Tenant reporting, Admin/Ops reporting, exception handling, reconciliation và settlement tracking.

### Out of scope

- Listing fee billing/reporting trong hệ thống.
- CPC billing hoặc tính phí CPC.
- Brand portal tự cấu hình commission/cashback trong MVP1.
- Checkout/payment của Brand bên trong Platform.
- Native mobile app riêng.
- Full accounting ledger.
- Batch loyalty posting/fallback chính thức trong MVP1.
- Cashback B1, point conversion, point posting và Tenant Loyalty API không thuộc MVP1.
- Cashback/Point History của End User gồm 3 tab; Basic My Orders vẫn thuộc MVP1.

## Overall Description

### Product Perspective

Affiliate Marketplace Platform là lớp trung gian nằm giữa Brand/Merchant và Tenant white-label marketplace. Platform không xử lý checkout/payment của Brand; Platform chỉ quản lý catalog, tracking click/order, commission/revenue share và reporting. Với mỗi Tenant, Platform render marketplace theo domain/branding riêng và enforce data isolation theo tenant_id. Tenant Loyalty System không được gọi trong MVP1 theo CR-01.

### Features list

| Feature ID | Name | Description | Related UC | Priority |
|---|---|---|---|---|
| FEAT-001 | Tenant Management | Tạo Tenant, domain, branding, locale | UC-001, UC-002 | Must |
| FEAT-002 | Brand Management | Tạo Brand/Merchant, credentials, commission, pending days | UC-004, UC-005, UC-006 | Must |
| FEAT-003 | Offer & Content Management | Tạo Offer, localized content, Top brands, category; Banner Management thuộc Deferred/Phase 2 | UC-007 | Must |
| FEAT-004 | Tenant Visibility Management | Assign/unassign Brand/Offer theo Tenant, default hidden | UC-008 | Must |
| FEAT-005 | White-label Marketplace | Landing page, search/filter, Top brands, earn/cashback display text; không có banner trong MVP1 | UC-010, UC-011 | Must |
| FEAT-006 | Click Tracking & Redirect | Tạo click_id, tracking outbound click, redirect sang Brand, không CPC billing | UC-012 | Must |
| FEAT-007 | Brand Order Integration | Nhận order success, cancel/refund, validate auth/schema/idempotency | UC-013, UC-014 | Must |
| FEAT-008 | Commission & Revenue Share Engine | Tính commission/revenue share, provisional amounts, pending_until và chốt số chính thức | UC-005, UC-016 | Must |
| FEAT-009 | Tenant Loyalty Posting | Gọi Tenant Loyalty API real-time, xử lý success/failure/retry | UC-017 | Deferred |
| FEAT-010 | Reporting & Settlement | Tenant/Admin reports, exception queue, reconciliation, settlement tracking | UC-018, UC-019, UC-020 | Must |

### User Classes and Characteristics

| User class / Actor | Quyền chính | Giới hạn |
|---|---|---|
| Admin/Ops | Quản lý Tenant, Brand, Offer, visibility, commission/revenue share, exception, reporting, settlement | Toàn hệ thống, theo phân quyền nội bộ |
| Tenant Admin | Xem dashboard/report, theo dõi click/conversion/doanh thu chia sẻ scoped theo Tenant | Không xem dữ liệu Tenant khác; không cấu hình commission Brand trong MVP1 |
| End user | Xem marketplace, tìm/lọc Brand/Offer, click sang Brand | Chỉ dữ liệu trong Tenant hiện tại |
| Brand System | Gửi order success và cancel/refund event theo API contract | Chỉ theo Brand credential và payload hợp lệ |
| Tenant Loyalty System | Không nhận request cộng điểm trong MVP1 | Tích hợp point posting là deferred |
| Affiliate Platform | Xử lý tracking click/order, commission/revenue share, reporting | Tuân thủ rule visibility và tenant isolation |

### Assumptions and Dependencies

| Type | Item | Impact |
|---|---|---|
| Assumption | App/hệ thống Tenant có thể truyền `member_ref/user_ref` hoặc session context sang Landing Page. MVP1 không cung cấp End-user Account/Login trên Landing Page. Nếu thiếu context, End user vẫn được xem/click/mua nhưng cần warning về quyền lợi. | Tracking/reporting có thể thiếu member_ref; quyền lợi/cashback/đối chiếu hội viên có thể không đảm bảo nếu chưa định danh. |
| Assumption | Admin/Ops là người cấu hình commission/revenue share rule trong MVP1. | Brand portal không thuộc MVP1. |
| Assumption | Cashback B1/point posting là deferred sau MVP1. | Platform không tự tính/cộng điểm trong MVP1. |
| Dependency | Brand order success API real-time. | Không có API thì không tạo conversion/transaction tự động. |
| Dependency | Brand triển khai Cancel/Refund API theo Order Transaction SRS. | Brand phải gửi đúng khóa Order/Item và idempotency key; event cho Order Confirmed bị từ chối. |
| Dependency | Tenant-Brand commercial/legal approval. | Quyết định Brand/Offer assignment theo Tenant. |
| Dependency | Locale list MVP1. | Ảnh hưởng localization test scope. |

## System context

### Target system behavior

1. Admin/Ops onboarding Tenant, Brand, Offer và cấu hình rule.
2. Admin/Ops assign Brand/Offer hiển thị theo từng Tenant.
3. End user mở marketplace của Tenant và chỉ thấy catalog hợp lệ của Tenant đó.
4. Landing page hiển thị Top brands, category có icon, offer cards và earn/cashback display text dạng `Nhận x điểm với mỗi 20,000đ chi tiêu`; đây chỉ là text hiển thị, không tự tính/cộng điểm. Banner slider thuộc Deferred/Phase 2.
5. Khi End user chọn Brand/Offer, Platform tạo click_id và redirect sang Brand. Click Banner thuộc Deferred/Phase 2.
6. Brand gửi order success real-time; Platform validate auth, schema, idempotency, click_id và visibility.
7. Order hợp lệ vào trạng thái pending/tạm tính.
8. Sau pending days theo Brand, nếu không có cancel/refund, Platform finalize commission/revenue share chính thức.
9. Không gọi Tenant Loyalty API và không tạo trạng thái `Rewarded/Đã hoàn điểm` trong MVP1.

### External systems

| System | Vai trò | Direction |
|---|---|---|
| DNS/SSL/domain provider | Hỗ trợ domain/subdomain white-label cho Tenant | Tenant/Admin -> Platform/DNS |
| Brand System | Nhận user redirect, ghi nhận mua hàng, gửi order success/cancel/refund | Brand -> Platform |
| Tenant Loyalty System | Không nhận API cộng điểm trong MVP1; phase sau mới tích hợp | Platform -> Tenant |
| Reporting/analytics store | Tổng hợp click, order, commission/revenue share, settlement | Platform internal |

## Models and diagrams

| Artifact | Location | Usage |
|---|---|---|
| Functional analysis | [analysis](../analysis/affiliate-marketplace-platform-analysis.md) | Nguồn FR, business rules, validation, data objects |
| Modeling | [modeling](../modeling/affiliate-marketplace-platform-modeling.md) | Use case model, process, state, data, integration context |
| Customer journey activity diagram | [PlantUML diagram](../modeling/affiliate-marketplace-customer-journey-activity-diagram.md) | Luồng End user từ landing page đến ghi nhận/chốt transaction; point posting deferred theo CR-01 |
| Use case list | [usecases](../usecases/affiliate-marketplace-platform-usecase-list.md) | Danh sách UC-001..UC-020 |
| Landing page mockup | [mockup](../mockups/affiliate-marketplace-landing-page-desktop.html) | Hành vi và nội dung landing page desktop mới nhất |

## Screen behavior summary

| Screen | Fields / content | Actions | States | Permission behavior |
|---|---|---|---|---|
| Landing page marketplace | Tenant logo, language, My Orders, Top brands, category icons, search, sort, offer cards và earn/cashback display text; MVP1 không có account entry hoặc banner slider | Search, filter category, select Brand/Offer, change language, open My Orders khi có End User context | Loading, empty, no result, domain error, catalog error, direct link blocked, missing End User context | Chỉ hiển thị Brand/Offer active thỏa `assignment_status = Active` và `tenant_visibility_status = Visible`; End-user Account/Login thuộc Deferred/Phase 2 |
| Basic My Orders | Danh sách Order cơ bản và chi tiết các Order Item phát sinh qua Platform; không hiển thị Cashback/Point | Open list, copy Brand Order ID, view detail | Loading, empty, missing End User context, order not found | Scope theo `tenant_id` và `member_ref/user_ref` từ app/hệ thống Tenant |
| Cashback/Point History | Deferred/Phase 2 | N/A | N/A | N/A |
| Admin setup screens | Tenant, Brand, Offer, visibility, commission/revenue share, integration configs | Create/update/activate/deactivate | Draft, active, inactive, validation error | Admin/Ops only |
| Tenant reporting portal | Click, conversion, doanh thu chia sẻ, transaction status | Filter/export/view details | Empty, loading, partial data, error | Tenant Admin chỉ xem Tenant của mình |
| Admin reporting/exception | Toàn hệ thống, exception queue, settlement records | Review, mark, retry, export | Open, processing, resolved, failed | Admin/Ops only |

### GUI elements - Landing page marketplace

| Field Name | Description | Control Type | Data Type | Default Value | Required(Y/N) | Rule |
|---|---|---|---|---|---|---|
| Tenant logo | Logo theo Tenant branding config | Image/display | URL/string | Fallback logo | Y | Render theo Tenant đã resolve; không dùng logo Tenant khác |
| Tenant name | Tên marketplace/Tenant hiển thị ở header | Text/display | String | Tenant name | Y | Lấy theo tenant_id từ domain |
| Language selector | Chọn ngôn ngữ marketplace | Select | Locale code | `vi-VN` | Y | MVP1 hỗ trợ `vi-VN` và `en-US`; thiếu bản dịch fallback `vi-VN` |
| End-user Account/Login | Deferred/Phase 2; không có account entry trên Landing Page MVP1 | N/A | N/A | N/A | N | `member_ref/user_ref` hoặc session context do app/hệ thống Tenant truyền sang nếu có; Landing Page không tự xác thực End User |
| Đơn hàng của tôi | Mở Basic My Orders | Button/link | URL/action | N/A | N | Thuộc MVP1; chỉ mở khi có đủ End User context để scope dữ liệu, không hiển thị Cashback/Point |
| Banner slider | Deferred/Phase 2; không hiển thị trong MVP1 | N/A | N/A | N/A | N | Không triển khai quản lý, hiển thị hoặc click Banner trong MVP1 |
| Top brands | Tối đa 3 Brand nổi bật do Tenant cấu hình tại màn hình `Assigned Brands` trên Tenant Portal | Card list | List/Brand | Empty | N | Tenant chọn tối đa 3 Brand từ danh sách Brand đã được Platform assign cho Tenant. Chỉ hiển thị Brand khi Tenant và Brand đều `Active`, Brand đang được bật hiển thị trên Landing Page và có ít nhất một Category mapping hoặc Offer hợp lệ để xác định Commission. |
| Search keyword | Tìm Brand/Offer | Text input | String | Empty | N | Trim whitespace; chỉ search trong catalog Tenant hiện tại |
| Category filter | Lọc theo danh mục có icon | Segmented control | Category code | `Tất cả` | N | Icon phải đi kèm text label; chỉ category có offer active/assigned |
| Sort | Sắp xếp catalog | Select | Enum | `Phổ biến` | N | MVP1 chỉ gồm `Phổ biến` và `Tên A - Z`. Brand Favourite và sắp xếp/lọc theo Brand yêu thích thuộc Deferred/Phase 2. |
| Brand/Offer card | Card hiển thị Brand/Offer | Card/display | Offer object | N/A | Y | Chỉ hiển thị khi Brand và Offer có status `Active`, đã được assign hợp lệ và thời điểm hiện tại nằm trong Start Date–End Date. Offer ngoài thời gian hiệu lực không hiển thị/click nhưng Offer Status không tự đổi thành `Expired` hoặc `Draft`. |
| Earn rate | Tỷ lệ tích điểm hiển thị trên card | Text/display | String | N/A | Conditional | Format: `Nhận x điểm với mỗi 20,000đ chi tiêu`; không hiển thị số điểm dự kiến cụ thể |
| Offer action area | Vùng card có thể chọn để redirect | Card action | Action | N/A | Y | Không dùng button `Xem ưu đãi`; click/select card vẫn phải tracking trước redirect |
| Empty state | Không có offer phù hợp | Message | String | N/A | Conditional | Hiển thị khi catalog rỗng hoặc filter không có kết quả |
| Error state | Domain/catalog/direct link error | Message + optional retry | String/action | N/A | Conditional | Không lộ thông tin nội bộ hoặc dữ liệu Tenant khác |

### GUI elements - Basic My Orders (MVP1)

| Field Name | Description | Control Type | Data Type | Default Value | Required(Y/N) | Rule |
|---|---|---|---|---|---|---|
| Brand Order ID | Mã Order tại hệ thống Brand | Text + copy action | String | N/A | Y | Lấy từ `brand_order_id`; cho phép sao chép |
| Brand | Brand phát sinh Order | Display | String | N/A | Y | Lấy từ Brand snapshot/reference trên Transaction |
| Order date | Thời điểm ghi nhận Order | Display | Datetime | N/A | Y | Hiển thị theo timezone/format của Landing Page |
| Amount | Tổng `Final amount` hiện tại của các item không bị hoàn toàn bộ | Display | Money | `0` | Y | Item `Refunded` có Final amount bằng `0` nên không được cộng vào Amount |
| Order Status | Trạng thái tổng hợp của Order | Badge | Enum | N/A | Y | `Pending`, `Confirmed`, `Cancelled`, tổng hợp từ trạng thái item theo Order Transaction SRS |
| Copy | Sao chép Brand Order ID | Icon/Button | Action | N/A | N | Không thay đổi dữ liệu Order |
| View | Mở chi tiết Order | Icon/Button | Action | N/A | Y | Hiển thị Brand Order ID, Brand, Amount, Order Status và danh sách item; không hiển thị commission, Tenant Share, Cashback hoặc Point |

### GUI elements - Cashback/Point History (Deferred/Phase 2)

| Field Name | Description | Control Type | Data Type | Default Value | Required(Y/N) | Rule |
|---|---|---|---|---|---|---|
| Status tabs | 3 tab lịch sử đơn | Tabs | Enum | `Chờ xử lý` | N | Deferred sau MVP1 theo CR-01 |
| Order item | Dòng/card đơn hàng | Card/list row | Order object | N/A | Y | Chỉ hiển thị order thuộc tenant_id và member_ref hiện tại |
| Brand name/logo | Brand của order | Display | String/URL | N/A | Y | Lấy từ Brand linked với click/order |
| Brand order ref | Mã đơn từ Brand hoặc mã tham chiếu | Text/display | String | Masked/TBD | Y | Không hiển thị dữ liệu nhạy cảm ngoài scope |
| Order status | Trạng thái order/cashback | Badge | Enum | N/A | Y | Deferred sau MVP1; nếu triển khai phase sau cần map lại trạng thái theo cashback/point posting |
| Earn/cashback info | Thông tin điểm/cashback nếu có | Text/display | Number/string | N/A | Conditional | Deferred sau MVP1; landing card MVP1 chỉ hiển thị display text, không hiển thị số điểm dự kiến |
| Empty state | Không có order trong tab | Message | String | N/A | Conditional | Theo từng tab |
| Retry/refresh | Tải lại dữ liệu | Button | Action | N/A | N | Không tạo order/cashback mới |

### GUI elements - Admin/Ops setup screens

| Field Name | Description | Control Type | Data Type | Default Value | Required(Y/N) | Rule |
|---|---|---|---|---|---|---|
| Tenant code | Mã Tenant duy nhất | Text input | String | Empty | Y | Unique; immutable nếu đã active trừ quy trình migration |
| Hostname/domain | Domain/subdomain Tenant | Text input | String/domain | Empty | Y | Unique; active khi DNS/SSL valid |
| Supported locales | Danh sách locale Tenant hỗ trợ | Multi-select | Locale list | `vi-VN`, `en-US` | Y | MVP1 chốt hỗ trợ tiếng Việt và tiếng Anh; default `vi-VN` |
| Brand code | Mã Brand duy nhất | Text input | String | Empty | Y | Unique trong Platform |
| Brand status | Trạng thái Brand | Select | Enum | Draft | Y | Active mới được active Offer/nhận order |
| Pending days | Số ngày chờ trước khi chốt commission/revenue share chính thức | Number input | Integer | TBD | Y | Số nguyên không âm hoặc theo ngưỡng vận hành |
| Brand commission type | Kiểu commission Brand trả Affiliate | Select | Enum: Percentage, Fixed | Percentage | Y | Offer rule là tùy chọn; nếu Offer không có commission rule thì fallback sang Category/default category |
| Brand commission value | Giá trị commission Brand trả Affiliate | Number input | Decimal/Money | Empty | Y | `%` nếu Percentage, VND nếu Fixed; > 0 |
| Tenant share rate | Tỷ lệ Affiliate chia Tenant | Number input | Decimal percent | Empty | Y | > 0 và <= 100; tính trên commission Brand trả Affiliate; có thể override theo Category/Offer |
| Cashback B1% | Deferred sau MVP1 | Number input | Decimal percent | Empty | N | Không cấu hình trong MVP1 theo CR-01 |
| Assignment status | Brand/Offer visibility theo Tenant | Toggle/select | Enum | Inactive | Y | Default hidden; active mới hiển thị |
| Loyalty endpoint | API cộng điểm Tenant | Text input | URL | Empty | N | Deferred sau MVP1 theo CR-01 |

## Functional requirements

| ID | Requirement | Actor | Trigger | Priority | Source |
|---|---|---|---|---|---|
| SR-001 | Hệ thống phải hỗ trợ tạo và quản lý Tenant multi-tenant. | Admin/Ops | Onboard Tenant | Must | UC-001 |
| SR-002 | Hệ thống phải cấu hình domain, branding, locale cho marketplace Tenant. | Admin/Ops | Tenant setup | Must | UC-002 |
| SR-003 | Hệ thống cấu hình Tenant loyalty real-time API. | Admin/Ops | Loyalty integration setup | Deferred | UC-003 |
| SR-004 | Hệ thống phải tạo và quản lý Brand/Merchant. | Admin/Ops | Onboard Brand | Must | UC-004 |
| SR-005 | Hệ thống phải cấu hình commission/revenue share theo mô hình MVP1 mới. | Admin/Ops | Commission setup | Must | UC-005 |
| SR-006 | Hệ thống phải cấu hình pending_days theo Brand để chốt commission/revenue share chính thức. | Admin/Ops | Rule setup | Must | UC-006 |
| SR-007 | Hệ thống phải tạo/active Offer/content đa ngôn ngữ, Top brands và category. Banner Management thuộc Deferred/Phase 2. | Admin/Ops | Campaign setup | Must | UC-007 |
| SR-008 | Hệ thống phải cấu hình Brand/Offer visibility theo Tenant theo mô hình 2 tầng: Admin assignment pool và Tenant visibility trong pool; mặc định hidden nếu chưa được Admin assign active. | Admin/Ops, Tenant Admin | Visibility setup | Must | UC-008 |
| SR-009 | Hệ thống cấu hình cashback B1 và point conversion khi Tenant yêu cầu. | Admin/Ops | Cashback setup | Deferred | UC-009 |
| SR-010 | Hệ thống phải render marketplace white-label theo Tenant. | End user/System | Open Tenant domain | Must | UC-010 |
| SR-011 | Hệ thống phải hỗ trợ tìm kiếm/lọc Brand/Offer trong phạm vi Tenant. | End user | Search/filter | Must | UC-011 |
| SR-012 | Hệ thống phải tracking click Brand/Offer và redirect sang Brand, không tính CPC. Click Banner thuộc Deferred/Phase 2. | End user/System | Select Offer/Brand | Must | UC-012 |
| SR-013 | Hệ thống phải nhận và validate Brand order success real-time. | Brand System | Purchase success | Must | UC-013 |
| SR-014 | Hệ thống phải xử lý Brand cancel/refund để ngăn chốt commission/revenue share sai. | Brand System/System | Cancel/refund event | Must | UC-014 |
| SR-015 | Hệ thống phải hiển thị Basic My Orders gồm danh sách Order và chi tiết item; không hiển thị Cashback/Point trong MVP1. Cashback/Point History ba tab thuộc Deferred/Phase 2. | End user | Open My Orders | Must | UC-015 |
| SR-016 | Hệ thống phải finalize order đủ điều kiện sau pending_until. | System Job | Scheduled check | Must | UC-016 |
| SR-017 | Hệ thống cộng điểm qua Tenant Loyalty API real-time khi đủ điều kiện. | Platform/Tenant Loyalty | Eligible order | Deferred | UC-017 |
| SR-018 | Hệ thống phải cung cấp Tenant reporting scoped theo Tenant. | Tenant Admin | Open report | Must | UC-018 |
| SR-019 | Hệ thống phải cung cấp Admin/Ops reporting và exception handling toàn hệ thống. | Admin/Ops | Open report/queue | Must | UC-019 |
| SR-020 | Hệ thống phải hỗ trợ reconciliation và settlement tracking. | Admin/Ops/Finance | Settlement cycle | Must | UC-020 |

## Feature Detail: CMS - Brand Management / Onboard Brand

### Feature summary

CMS Brand Management là nhóm chức năng dành cho Admin/Ops để quản lý Brand/Merchant trên Platform. Chức năng này là tiền đề cho Offer activation, Brand order success API, commission configuration, visibility assignment theo Tenant và reporting/settlement.

Trong MVP1, Brand portal không thuộc phạm vi. Brand profile, trạng thái Brand và pending days do Admin/Ops quản lý trên CMS. Cấu hình API integration của Brand được quản lý ở use case/integration screen riêng, không nằm trong form thêm/sửa Brand cơ bản.

### Feature scope

| Scope item | Description | In MVP1 |
|---|---|---|
| Xem danh sách Brand | Admin/Ops xem danh sách Brand/Merchant đã được tạo trên Platform. | Yes |
| Lọc/tìm kiếm Brand | Tìm theo keyword, status, category, integration status, created date. | Yes |
| Xem chi tiết Brand | Xem profile, trạng thái, integration, commission summary, offer count, tenant assignment summary. | Yes |
| Thêm mới Brand | Tạo Brand profile ở trạng thái Draft hoặc Active theo quyền. | Yes |
| Sửa Brand | Cập nhật profile, category, logo, website, contact, pending days, integration metadata. | Yes |
| Xóa/Ngưng hoạt động Brand | Soft delete/deactivate Brand nếu không thể hard delete do đã có Offer/Order/Settlement. | Yes |
| Hard delete Brand | Xóa vật lý Brand khỏi database. | No, trừ khi Brand chưa có dữ liệu liên kết và có policy riêng |
| Brand tự đăng nhập portal | Brand tự cấu hình profile/commission/cashback. | No |

### CMS navigation

```text
Admin CMS
  -> Brand Management
     -> Brand List
        -> Filter/Search
        -> View Brand Detail
        -> Create Brand
        -> Edit Brand
        -> Deactivate/Delete Brand
```

### Brand Management use case list

| Use Case ID | Use case | Actor | Goal | Trigger | Pre-condition | Post condition | Priority |
|---|---|---|---|---|---|---|---|
| BRAND-UC-001 | Xem danh sách Brand | Admin/Ops | Xem toàn bộ Brand đã tạo trên Platform | Mở menu Brand Management | Admin/Ops authorized | Danh sách Brand hiển thị theo quyền | Must |
| BRAND-UC-002 | Tìm kiếm/lọc Brand | Admin/Ops | Thu hẹp danh sách Brand theo tiêu chí | Nhập keyword/chọn filter | Brand list loaded | Danh sách Brand được lọc | Must |
| BRAND-UC-003 | Xem chi tiết Brand | Admin/Ops | Xem profile và dữ liệu liên quan của Brand | Chọn một Brand trong list | Brand tồn tại | Brand detail hiển thị | Must |
| BRAND-UC-004 | Thêm mới Brand | Admin/Ops | Tạo Brand/Merchant mới | Click `Thêm Brand` | Admin/Ops có quyền tạo | Brand Draft/Active được tạo | Must |
| BRAND-UC-005 | Sửa Brand | Admin/Ops | Cập nhật thông tin Brand | Click `Sửa` trong detail/list | Brand tồn tại; Admin/Ops có quyền sửa | Brand được cập nhật và audit log được ghi | Must |
| BRAND-UC-006 | Xóa/Ngưng hoạt động Brand | Admin/Ops | Gỡ Brand khỏi vận hành active | Click `Xóa`/`Ngưng hoạt động` | Brand tồn tại; Admin/Ops có quyền | Brand Inactive/Deleted theo rule | Must |

### Screen inventory - Brand CMS

| Screen ID | Screen name | Purpose | Actor | Related use case |
|---|---|---|---|---|
| CMS-BRAND-001 | Brand List | Xem, tìm kiếm, lọc Brand | Admin/Ops | BRAND-UC-001, BRAND-UC-002 |
| CMS-BRAND-002 | Brand Detail | Xem thông tin chi tiết Brand và dữ liệu liên quan | Admin/Ops | BRAND-UC-003 |
| CMS-BRAND-003 | Create/Edit Brand Form | Thêm mới hoặc cập nhật Brand | Admin/Ops | BRAND-UC-004, BRAND-UC-005 |
| CMS-BRAND-004 | Delete/Deactivate Confirmation | Xác nhận xóa/ngưng hoạt động Brand | Admin/Ops | BRAND-UC-006 |

### GUI elements - CMS-BRAND-001 Brand List

| Field Name | Description | Control Type | Data Type | Default Value | Required(Y/N) | Rule |
|---|---|---|---|---|---|---|
| Keyword | Tìm theo Brand name, code, website, contact email | Text input | String | Empty | N | Trim whitespace; min length TBD; search không phân biệt hoa/thường nếu DB hỗ trợ |
| Status filter | Lọc theo trạng thái Brand | Select/Multi-select | Enum | All | N | Values: Draft, Active, Inactive |
| Category filter | Lọc theo danh mục Brand | Select/Multi-select | Category code | All | N | Chỉ hiển thị category được cấu hình |
| Created date from/to | Lọc theo ngày tạo | Date range | Date | Empty | N | from <= to |
| Sort | Sắp xếp danh sách | Select | Enum | Updated newest | N | Sort fields: created_at, updated_at, name, status |
| Brand code column | Mã Brand | Text/display | String | N/A | Y | Clickable nếu user có quyền xem detail |
| Brand name column | Tên Brand | Text/display | String | N/A | Y | Hiển thị localized/display name nếu có |
| Category column | Danh mục chính | Text/display | String | Empty | N | N/A |
| Status column | Trạng thái Brand | Badge | Enum | N/A | Y | Draft/Active/Inactive |
| Pending days column | Số ngày chờ reward | Number/display | Integer | Empty | N | Empty nếu chưa cấu hình |
| Offer count column | Số offer thuộc Brand | Number/display | Integer | 0 | N | Tính cả Draft/Active/Inactive theo filter TBD |
| Tenant assignment count column | Số Tenant đang được assign Brand/Offer | Number/display | Integer | 0 | N | Chỉ count active assignment nếu không nêu rõ |
| Last updated column | Lần cập nhật gần nhất | Datetime/display | Datetime | N/A | Y | Theo timezone hệ thống/TBD |
| Actions | View/Edit/Deactivate | Icon/menu buttons | Action | N/A | Y | Action hiển thị theo permission và status |

### GUI elements - CMS-BRAND-003 Create/Edit Brand Form

| Field Name | Description | Control Type | Data Type | Default Value | Required(Y/N) | Rule |
|---|---|---|---|---|---|---|
| Brand code | Mã định danh Brand trong Platform | Text input | String | Empty | Y | Unique; allowed characters TBD; không đổi sau khi có order nếu không có migration policy |
| Brand name | Tên Brand hiển thị | Text input | String | Empty | Y | Required; max length TBD |
| Legal name | Tên pháp lý/đối tác hợp đồng | Text input | String | Empty | N | Dùng cho Ops/Finance nếu có |
| Category | Danh mục Brand chính | Select | Category code | Empty | N | Must reference configured category |
| Website URL | Website chính của Brand | Text input | URL | Empty | N | Must be valid URL if provided |
| Logo URL / Logo upload | Logo Brand | File upload / URL input | URL/String | Empty | N | Validate file type/size if upload; fallback initials if empty |
| Short description | Mô tả ngắn Brand | Textarea | Text | Empty | N | Có thể dùng ở marketplace/detail nếu Product cho phép |
| Contact name | Người liên hệ Brand | Text input | String | Empty | N | Confidential |
| Contact email | Email liên hệ Brand | Text input | Email | Empty | N | Must be valid email if provided |
| Contact phone | Số điện thoại liên hệ | Text input | String | Empty | N | Format validation TBD |
| Brand status | Trạng thái Brand | Select | Enum | Draft | Y | Active mới active Offer và nhận order success |
| Pending days | Số ngày chờ sau order success trước reward | Number input | Integer | Empty/TBD | Y | >= 0; nếu chưa cấu hình thì không auto reward |
| Notes | Ghi chú vận hành | Textarea | Text | Empty | N | Internal only |

### Data fields - Brand entity for CMS

| Field Name | Description | Data Type | Required | Create | Edit | List | Detail | Rule |
|---|---|---|---|---|---|---|---|---|
| brand_id | Khóa định danh Brand | UUID/String | Y | System generated | N | Hidden | Y | Unique, immutable |
| code | Mã Brand | String | Y | Y | Conditional | Y | Y | Unique; avoid edit after linked data exists |
| name | Tên Brand | String | Y | Y | Y | Y | Y | Required |
| legal_name | Tên pháp lý | String | N | Y | Y | N | Y | Optional |
| category | Danh mục chính | String/Enum | N | Y | Y | Y | Y | Must reference configured category |
| website_url | Website Brand | URL/String | N | Y | Y | N | Y | Valid URL |
| logo_url | Logo Brand | URL/String | N | Y | Y | N | Y | Valid asset URL |
| short_description | Mô tả ngắn | Text | N | Y | Y | N | Y | Internal/public usage TBD |
| contact_name | Người liên hệ | String | N | Y | Y | N | Y | Confidential |
| contact_email | Email liên hệ | Email | N | Y | Y | N | Y | Email format |
| contact_phone | SĐT liên hệ | String | N | Y | Y | N | Y | Format TBD |
| status | Trạng thái Brand | Enum | Y | Y | Y | Y | Y | Draft, Active, Inactive |
| pending_days | Số ngày chờ reward | Integer | Y | Y | Y | Y | Y | >= 0 |
| created_at | Ngày tạo | Datetime | Y | System generated | N | Y | Y | Audit |
| created_by | Người tạo | User ref | Y | System generated | N | N | Y | Audit |
| updated_at | Ngày cập nhật | Datetime | Y | System generated | N | Y | Y | Audit |
| updated_by | Người cập nhật | User ref | Y | System generated | N | N | Y | Audit |

### Business rules - Brand CMS

| Rule ID | Rule | Applies to | Error behavior |
|---|---|---|---|
| BRAND-RULE-001 | Brand code phải unique trên toàn Platform. | Create/Edit | Không cho lưu, hiển thị lỗi duplicate. |
| BRAND-RULE-002 | Brand Active mới được active Offer và nhận order success production. | Offer activation, Order API | Chặn active Offer hoặc reject order nếu Brand inactive. |
| BRAND-RULE-003 | Pending days là bắt buộc cho Brand trước khi auto reward. | Create/Edit, Reward job | Không auto reward nếu thiếu; form nên bắt buộc theo MVP1. |
| BRAND-RULE-004 | Không hard delete Brand đã có Offer, Click, Order, Commission Rule, Assignment hoặc Settlement. | Delete | Chỉ cho Inactive/soft delete. |
| BRAND-RULE-005 | Deactivate Brand phải làm Offer active không còn hiển thị/click trên marketplace. | Deactivate | Marketplace filter ẩn Offer thuộc Brand inactive. |
| BRAND-RULE-006 | Form thêm/sửa Brand cơ bản không quản lý API credential hoặc integration status. | Create/Edit | Các trường integration nằm ở use case/screen riêng. |
| BRAND-RULE-007 | Mọi thay đổi Brand quan trọng phải ghi audit log. | Create/Edit/Delete | Nếu audit log fail, action không được coi là hoàn tất. |

### Use case specification - BRAND-UC-001 Xem danh sách Brand

- Title: Xem danh sách Brand
- Description: Admin/Ops xem danh sách Brand/Merchant trên CMS để kiểm tra trạng thái onboarding và vận hành.
- Actor: Admin/Ops
- Pre-condition: Admin/Ops đã đăng nhập và có quyền `brand.view`.
- Post condition: Danh sách Brand hiển thị theo filter/sort/pagination.
- Main flow:
  1. Admin/Ops mở menu `Brand Management`.
  2. Hệ thống tải danh sách Brand mặc định, sort theo `updated_at` mới nhất.
  3. Hệ thống hiển thị các cột chính: code, name, category, status, pending_days, offer_count, tenant_assignment_count, updated_at, actions.
  4. Admin/Ops có thể chuyển trang hoặc thay đổi sort.
- Alternative Flow:
  - Không có Brand nào: hiển thị empty state và CTA `Thêm Brand` nếu có quyền tạo.
- Exception:
  - Không có quyền: hiển thị unauthorized/forbidden.
  - Lỗi tải dữ liệu: hiển thị error state và action retry.
- GUI: CMS-BRAND-001.
- Related data: Brand, Offer count, Tenant Brand/Offer Assignment count.
- Acceptance criteria:
  - Given Admin/Ops có quyền `brand.view`
  - When mở `Brand Management`
  - Then hệ thống hiển thị danh sách Brand với pagination và actions theo quyền

### Use case specification - BRAND-UC-002 Tìm kiếm/lọc Brand

- Title: Tìm kiếm/lọc Brand
- Description: Admin/Ops lọc Brand theo keyword, status, category, integration status và created date.
- Actor: Admin/Ops
- Pre-condition: Admin/Ops có quyền `brand.view`; Brand list screen đã mở.
- Post condition: Danh sách Brand được lọc đúng tiêu chí.
- Main flow:
  1. Admin/Ops nhập keyword hoặc chọn filter.
  2. Hệ thống validate filter date range nếu có.
  3. Hệ thống query Brand theo tiêu chí.
  4. Hệ thống hiển thị result count và danh sách kết quả.
- Alternative Flow:
  - Admin/Ops clear filter: hệ thống quay lại danh sách mặc định.
  - Không có kết quả: hiển thị no result state.
- Exception:
  - Date range không hợp lệ: không query, hiển thị lỗi `from date must be <= to date`.
- GUI: CMS-BRAND-001.
- Related data: Brand.
- Acceptance criteria:
  - Given có Brand Active và Draft
  - When Admin/Ops lọc status = Active
  - Then danh sách chỉ hiển thị Brand Active

### Use case specification - BRAND-UC-003 Xem chi tiết Brand

- Title: Xem chi tiết Brand
- Description: Admin/Ops xem thông tin chi tiết Brand và các thông tin liên quan phục vụ vận hành.
- Actor: Admin/Ops
- Pre-condition: Admin/Ops có quyền `brand.view`; Brand tồn tại.
- Post condition: Brand detail hiển thị.
- Main flow:
  1. Admin/Ops chọn Brand từ danh sách.
  2. Hệ thống tải Brand profile.
  3. Hệ thống hiển thị thông tin profile, status, pending_days, offer summary, tenant assignment summary, audit metadata.
  4. Hệ thống hiển thị actions `Sửa`, `Ngưng hoạt động` theo quyền/status.
- Alternative Flow:
  - Brand Inactive: hiển thị badge Inactive và không hiển thị action dùng cho Active nếu không hợp lệ.
- Exception:
  - Brand không tồn tại hoặc đã bị xóa: hiển thị not found.
  - Không có quyền: forbidden.
- GUI: CMS-BRAND-002.
- Related data: Brand, Offer, Assignment, Commission Rule summary.
- Acceptance criteria:
  - Given Brand tồn tại
  - When Admin/Ops mở Brand detail
  - Then hệ thống hiển thị profile và integration/status summary của Brand

### Use case specification - BRAND-UC-004 Thêm mới Brand

- Title: Thêm mới Brand
- Description: Admin/Ops tạo Brand/Merchant mới trên CMS.
- Actor: Admin/Ops
- Pre-condition: Admin/Ops có quyền `brand.create`.
- Post condition: Brand được tạo ở Draft hoặc Active theo input/quyền.
- Main flow:
  1. Admin/Ops click `Thêm Brand`.
  2. Hệ thống mở form Create Brand.
  3. Admin/Ops nhập các trường bắt buộc: Brand code, Brand name, Brand status, Pending days.
  4. Admin/Ops nhập các trường optional: legal name, category, website, logo, contact, notes.
  5. Admin/Ops click `Lưu`.
  6. Hệ thống validate field-level rules.
  7. Hệ thống tạo Brand record và audit log.
  8. Hệ thống điều hướng tới Brand detail hoặc hiển thị success message.
- Alternative Flow:
  - Admin/Ops chọn `Lưu nháp`: Brand ở Draft.
  - Admin/Ops hủy form: không lưu dữ liệu.
- Exception:
  - Brand code trùng: không cho lưu.
  - Pending days invalid: không cho lưu.
  - Integration chưa cấu hình: không chặn lưu Brand; xử lý ở use case/screen integration riêng trước khi nhận order success production.
- GUI: CMS-BRAND-003.
- Related data: Brand.
- Acceptance criteria:
  - Given Brand code chưa tồn tại và pending_days hợp lệ
  - When Admin/Ops tạo Brand
  - Then Brand record được tạo và audit log ghi nhận người tạo/thời điểm tạo

### Use case specification - BRAND-UC-005 Sửa Brand

- Title: Sửa Brand
- Description: Admin/Ops cập nhật thông tin Brand đã tồn tại.
- Actor: Admin/Ops
- Pre-condition: Admin/Ops có quyền `brand.edit`; Brand tồn tại.
- Post condition: Brand được cập nhật và audit log được ghi.
- Main flow:
  1. Admin/Ops mở Brand detail hoặc chọn action `Sửa`.
  2. Hệ thống mở form Edit Brand với dữ liệu hiện tại.
  3. Admin/Ops chỉnh sửa field được phép.
  4. Admin/Ops click `Lưu`.
  5. Hệ thống validate field-level rules và dependency rules.
  6. Hệ thống cập nhật Brand record.
  7. Hệ thống ghi audit log gồm field changed, old value/new value nếu policy cho phép.
- Alternative Flow:
  - Admin/Ops đổi status Draft -> Active: hệ thống kiểm tra required config trước khi active.
  - Admin/Ops đổi Active -> Inactive: hệ thống cảnh báo ảnh hưởng marketplace/offer.
- Exception:
  - Brand code không được sửa do đã có linked data: disable field hoặc hiển thị lỗi.
  - Dữ liệu stale/concurrent update: hiển thị conflict nếu có versioning.
- GUI: CMS-BRAND-003.
- Related data: Brand, Audit Log.
- Acceptance criteria:
  - Given Brand tồn tại và Admin/Ops có quyền sửa
  - When Admin/Ops cập nhật pending_days hợp lệ
  - Then Brand được cập nhật và reward job dùng pending_days mới cho order success sau thời điểm hiệu lực

### Use case specification - BRAND-UC-006 Xóa/Ngưng hoạt động Brand

- Title: Xóa/Ngưng hoạt động Brand
- Description: Admin/Ops gỡ Brand khỏi vận hành active. Với Brand đã có dữ liệu liên kết, hệ thống thực hiện deactivate/soft delete thay vì hard delete.
- Actor: Admin/Ops
- Pre-condition: Admin/Ops có quyền `brand.delete` hoặc `brand.deactivate`; Brand tồn tại.
- Post condition: Brand chuyển Inactive hoặc Deleted theo rule.
- Main flow:
  1. Admin/Ops chọn action `Ngưng hoạt động` hoặc `Xóa`.
  2. Hệ thống kiểm tra dữ liệu liên kết: Offer, Click, Order, Commission Rule, Assignment, Settlement.
  3. Hệ thống hiển thị confirmation và impact summary.
  4. Admin/Ops xác nhận.
  5. Nếu Brand có linked data, hệ thống chuyển Brand status sang Inactive.
  6. Nếu Brand chưa có linked data và policy cho phép, hệ thống hard delete hoặc soft delete theo cấu hình.
  7. Hệ thống ghi audit log.
- Alternative Flow:
  - Admin/Ops hủy confirmation: không thay đổi Brand.
- Exception:
  - Brand đang có active Offer/Assignment: hệ thống yêu cầu confirm impact hoặc chặn nếu policy yêu cầu inactive Offer/unassign trước.
  - Không có quyền: forbidden.
- GUI: CMS-BRAND-004.
- Related data: Brand, Offer, Assignment, Audit Log.
- Acceptance criteria:
  - Given Brand đã có Offer hoặc Order liên kết
  - When Admin/Ops xác nhận xóa
  - Then hệ thống không hard delete
  - And Brand chuyển Inactive/soft deleted theo rule
  - And Brand/Offer không còn hiển thị trên marketplace

## Use Case Specifications

### Use case summary

| Use Case ID | Title | Actor | Pre-condition | Post condition | Main flow summary | Alternative / Exception summary |
|---|---|---|---|---|---|---|
| UC-001 | Onboard Tenant | Admin/Ops | Admin authorized; Tenant partnership approved | Tenant Draft created | Nhập Tenant info, validate unique code, create Tenant | Duplicate code, missing required fields |
| UC-002 | Cấu hình domain và branding Tenant | Admin/Ops | Tenant exists | Domain/branding config saved; marketplace can resolve when active | Configure hostname, DNS/SSL, logo, theme, locale | DNS/SSL pending, fallback branding |
| UC-003 | Cấu hình loyalty integration Tenant | Admin/Ops | Deferred sau MVP1 | Không áp dụng MVP1 | Không cấu hình/call Tenant Loyalty API trong MVP1 | Đưa sang phase sau |
| UC-004 | Onboard Brand/Merchant | Admin/Ops | Brand partnership approved | Brand Draft/Active created | Enter Brand profile, validate code, create Brand | Duplicate Brand code, inactive Brand |
| UC-005 | Cấu hình commission Brand và revenue share Tenant | Admin/Ops | Tenant and Brand/Offer exist | Active Brand commission and Tenant revenue share rule | Configure Brand commission and `tenant_share_rate%`; validate scope/effective period | Invalid rate, missing category/offer scope, effective period invalid |
| UC-006 | Cấu hình pending_days theo Brand | Admin/Ops | Brand exists | Active pending rule | Configure pending_days | Missing required pending_days, invalid value |
| UC-007 | Tạo và active Offer/content đa ngôn ngữ | Admin/Ops | Brand active | Offer Draft/Active | Enter Offer/content/Top Brand/Category, validate locale, active nếu đủ điều kiện; Banner thuộc Deferred/Phase 2 | Missing translation; Offer status khác `Active`; hoặc thời điểm hiện tại nằm ngoài Start Date–End Date |
| UC-008 | Cấu hình Brand/Offer hiển thị theo Tenant | Admin/Ops, Tenant Admin | Tenant and Brand/Offer exist; commercial/legal approved | Assignment Active/Inactive; Tenant visibility Visible/Hidden | Admin assign Brand/Offer vào pool; Tenant bật/tắt trong pool | No assignment means hidden; Tenant hidden means not visible; direct link blocked |
| UC-009 | Cấu hình cashback tầng 2 cho Tenant | Admin/Ops | Deferred sau MVP1 | Không áp dụng MVP1 | Không cấu hình B1/point conversion trong MVP1 | Đưa sang phase sau |
| UC-010 | Xem marketplace white-label | End user | Tenant/domain active | Tenant catalog displayed | Resolve Tenant, load branding/catalog, show earn rate | Domain error, empty catalog |
| UC-011 | Tìm kiếm/lọc Brand/Offer | End user | Catalog loaded | Filtered catalog displayed | Search/filter within Tenant catalog | No result, invalid category |
| UC-012 | Click Offer/Brand và redirect sang Brand | End user | Tenant/Offer/Brand/Assignment active | click_id created; redirected to Brand | Validate click, show member warning if not identified, create tracking, redirect; click Banner thuộc Deferred/Phase 2 | Direct link blocked, tracking fail |
| UC-013 | Brand báo order success | Brand System | Credential valid; click/order data available | Pending order created or request rejected | Authenticate, validate schema/idempotency/click_id/visibility, create order | Auth fail, schema fail, duplicate, click_id invalid |
| UC-014 | Brand báo cancel/refund theo Order Item | Brand System | Order tồn tại, đang Pending và item match | Item chuyển Refunded; Order Status và dữ liệu tài chính được tổng hợp lại | Validate, match item, atomic update, recalculate, save Adjustment History | Unmatched/invalid event hoặc Order Confirmed: giữ nguyên dữ liệu và ghi Exception |
| UC-015 | Tra cứu Basic My Orders | End user | Có Tenant context và `member_ref/user_ref` hoặc session context hợp lệ từ app Tenant | Danh sách/chi tiết Order cơ bản được hiển thị đúng End User | Open My Orders, scope dữ liệu, hiển thị list, copy Brand Order ID, view item detail | Missing context, empty list, order not found; Cashback/Point History thuộc Phase 2 |
| UC-016 | Finalize order đủ điều kiện | Affiliate Platform/System Job | Pending order exists | Order Confirmed hoặc Cancelled | Check pending_until and cancel/refund, finalize | Not due, cancelled |
| UC-017 | Cộng điểm qua Tenant loyalty API | Platform/Tenant Loyalty | Deferred sau MVP1 | Không áp dụng MVP1 | Không tính/cộng điểm hoặc gọi Tenant Loyalty API trong MVP1 | Đưa sang phase sau |
| UC-018 | Xem Tenant reporting | Tenant Admin | Tenant Admin authorized | Tenant-scoped report displayed | Filter/report scoped by tenant_id | Unauthorized, partial data |
| UC-019 | Xem Admin reporting và exception | Admin/Ops | Admin authorized | System-wide report/queue displayed | Filter, review exceptions, retry if allowed | Retry fail, empty state |
| UC-020 | Reconciliation và settlement tracking | Admin/Ops, Finance | Eligible transactions exist | Settlement record/report updated | Aggregate commission/revenue share by cycle, review and update | Exceptions on hold, cycle TBD |

### Use case details

### UC-001 — Onboard Tenant

- Primary actor: Admin/Ops
- Goal: Tạo Tenant để có thể cấu hình marketplace white-label.
- Preconditions: Admin/Ops authorized; Tenant partnership approved.
- Trigger: Admin/Ops chọn tạo Tenant mới.
- Main flow:
  1. Admin/Ops nhập Tenant name, code, contact, status.
  2. Hệ thống validate Tenant code không trùng.
  3. Hệ thống tạo Tenant ở trạng thái Draft.
  4. Hệ thống cho phép tiếp tục cấu hình các thông tin vận hành cần thiết của Tenant.
- Alternate/exception:
  - Tenant code trùng: không cho lưu, hiển thị lỗi validation.
  - Thiếu field bắt buộc: không cho lưu.
- Data: Tenant.
- Business rules: BRULE-001.
- Acceptance criteria:
  - Given Admin/Ops có quyền và Tenant code chưa tồn tại
  - When Admin/Ops tạo Tenant
  - Then hệ thống tạo Tenant record ở trạng thái Draft

### UC-002 — Cấu hình domain và branding Tenant

- Primary actor: Admin/Ops
- Goal: Cấu hình domain, logo, theme và locale để marketplace render đúng Tenant.
- Preconditions: Tenant tồn tại.
- Trigger: Tenant cần public marketplace.
- Main flow:
  1. Admin/Ops nhập subdomain/custom domain, DNS/SSL status.
  2. Admin/Ops cấu hình logo, theme, default locale, supported locales.
  3. Hệ thống validate domain mapping và trạng thái SSL/DNS.
  4. Hệ thống lưu Tenant Domain và Tenant Branding Config.
  5. Khi domain active, marketplace request resolve đúng Tenant.
- Alternate/exception:
  - DNS/SSL chưa hợp lệ: domain ở trạng thái Pending Verification.
  - Branding asset thiếu optional fields: dùng fallback theme.
- Data: Tenant Domain, Tenant Branding Config.
- Business rules: BRULE-001, BRULE-002, BRULE-003, BRULE-021.
- Acceptance criteria:
  - Given domain đã verified
  - When End user mở domain Tenant
  - Then hệ thống render marketplace với branding của Tenant

### UC-003 — Cấu hình loyalty integration Tenant

> Deferred theo CR-01: MVP1 không cấu hình Tenant Loyalty API, không gọi API cộng điểm và không sinh Point Posting Log.

- Primary actor: Admin/Ops
- Goal: Không áp dụng trong MVP1.
- Preconditions: Không áp dụng MVP1.
- Trigger: Phase sau khi bật automatic cashback/point posting.
- Main flow: Không triển khai trong MVP1.
- Alternate/exception: Không áp dụng MVP1.
- Data: Deferred Tenant Loyalty Integration, Point Posting Log.
- Business rules: BRULE-005, BRULE-019.
- Acceptance criteria:
  - Given order đủ điều kiện chốt commission trong MVP1
  - When Platform xử lý finalization
  - Then hệ thống không gọi Tenant Loyalty API

### UC-004 — Onboard Brand/Merchant

- Primary actor: Admin/Ops
- Goal: Tạo Brand profile để quản lý offer, order API và commission.
- Preconditions: Brand partnership approved.
- Trigger: Admin/Ops tạo Brand mới.
- Main flow:
  1. Admin/Ops nhập Brand profile, code, category, status, contact.
  2. Hệ thống validate Brand code/order namespace không trùng.
  3. Hệ thống tạo Brand ở trạng thái Draft hoặc Active theo quyền.
  4. Hệ thống cho phép cấu hình commission, pending days, API credential.
- Alternate/exception:
  - Brand code trùng: không cho lưu.
  - Brand inactive: không được active Offer hoặc nhận order success.
- Data: Brand.
- Business rules: BRULE-006.
- Acceptance criteria:
  - Given Brand code chưa tồn tại
  - When Admin/Ops tạo Brand
  - Then Brand được lưu và có thể tiếp tục cấu hình rule

### UC-005 — Cấu hình commission Brand và revenue share cho Tenant

- Primary actor: Admin/Ops
- Goal: Cấu hình commission Brand trả Affiliate và phần Affiliate chia lại cho Tenant.
- Preconditions: Tenant, Brand/Offer tồn tại.
- Trigger: Có điều khoản commission với Brand/Tenant.
- Main flow:
  1. Admin/Ops cấu hình commission Brand trả Affiliate theo Category của từng Brand hoặc theo Offer.
  2. Admin/Ops cấu hình Tenant revenue share theo Brand default, hoặc override theo Category/Offer nếu cần.
  3. Hệ thống validate commission_type, commission_value và tenant_share_rate.
  4. Hệ thống lưu rule và effective period nếu có.
  5. Rule active được dùng khi order success hợp lệ; ưu tiên Offer -> Category -> Brand default cho revenue share.
- Alternate/exception:
  - Thiếu Category commission rule khi order success gửi category chưa được map: đưa exception hoặc không tính commission theo policy.
  - tenant_share_rate không hợp lệ: không cho active rule.
  - Effective period invalid: không cho lưu/active.
- Data: Brand Commission Rule, Tenant Revenue Share Rule.
- Business rules: BRULE-008, BRULE-009.
- Acceptance criteria:
  - Given Brand commission rule hợp lệ và Tenant revenue share rule có `tenant_share_rate%` hợp lệ
  - When Admin/Ops active rule
  - Then hệ thống sử dụng rule để tính commission/revenue share cho transaction hợp lệ

### UC-006 — Cấu hình pending_days theo Brand

- Primary actor: Admin/Ops
- Goal: Cấu hình số ngày chờ trước khi chốt commission/revenue share chính thức.
- Preconditions: Brand tồn tại.
- Trigger: Brand cần rule chốt commission.
- Main flow:
  1. Admin/Ops nhập pending_days theo Brand.
  2. Hệ thống validate pending_days là số hợp lệ theo policy.
  3. Hệ thống lưu rule effective.
- Alternate/exception:
  - pending_days thiếu nếu bắt buộc: không cho active rule chốt commission.
- Data: Brand reward delay rule.
- Business rules: BRULE-007.
- Acceptance criteria:
  - Given Brand có pending_days hợp lệ
  - When order success được ghi nhận
  - Then hệ thống tính được ngày dự kiến chốt chính thức theo `order_success_at + pending_days`

### UC-007 — Tạo và active Offer/content đa ngôn ngữ

- Primary actor: Admin/Ops
- Goal: Tạo Offer, Top brands, Category và localized content. Banner Management thuộc Deferred/Phase 2.
- Preconditions: Brand active.
- Trigger: Campaign/offer sẵn sàng.
- Main flow:
  1. Admin/Ops nhập offer title, description, terms, category, destination URL.
  2. Admin/Ops nhập localized content theo supported locales.
  3. Admin/Ops cấu hình Top Brand nếu áp dụng; không cấu hình Banner trong MVP1.
  4. Hệ thống validate Brand active, thời gian hiệu lực và required locales.
  5. Hệ thống active Offer hoặc lưu Draft.
- Alternate/exception:
  - Thiếu bản dịch bắt buộc: không cho Active hoặc fallback theo locale policy.
  - Offer hết hạn/tạm dừng: không hiển thị/click.
- Data: Offer, Localized Content.
- Business rules: BRULE-006, BRULE-012, BRULE-021.
- Acceptance criteria:
  - Given Brand active và content hợp lệ
  - When Admin/Ops active Offer
  - Then Offer có thể được assign cho Tenant marketplace

### UC-008 — Cấu hình Brand/Offer hiển thị theo Tenant

- Primary actor: Admin/Ops
- Goal: Quyết định Brand/Offer nào được phép hiển thị trên từng Tenant marketplace và Tenant có đang bật hiển thị hay không.
- Preconditions: Tenant và Brand/Offer tồn tại; có phê duyệt commercial/legal.
- Trigger: Setup tenant marketplace catalog.
- Main flow:
  1. Admin/Ops chọn Tenant.
  2. Admin/Ops assign Brand hoặc Offer cụ thể vào pool của Tenant.
  3. Admin/Ops cấu hình `assignment_status`.
  4. Hệ thống validate Tenant/Brand/Offer tồn tại.
  5. Hệ thống lưu Tenant Brand/Offer Assignment.
  6. Tenant có thể bật/tắt Brand/Offer trong Tenant Portal; nếu Tenant chưa thao tác thì assigned active mặc định visible.
  7. Marketplace chỉ hiển thị khi `assignment_status = Active` và `tenant_visibility_status = Visible`.
- Alternate/exception:
  - Không có assignment active: Brand/Offer hidden by default.
  - Tenant tắt visibility: Brand/Offer không hiển thị dù assignment active.
  - Direct link tới offer không thỏa visibility cuối cùng: chặn và hiển thị lỗi không khả dụng.
- Data: Tenant Brand/Offer Assignment.
- Business rules: BRULE-024, BRULE-012.
- Acceptance criteria:
  - Given Offer active nhưng chưa assigned cho Tenant A
  - When End user mở marketplace Tenant A
  - Then Offer không được hiển thị

### UC-009 — Cấu hình cashback tầng 2 cho Tenant

> Deferred theo CR-01: MVP1 không cấu hình cashback B1, không tính điểm/cashback cho End user và không thực hiện disbursement qua Platform.

- Primary actor: Admin/Ops
- Goal: Không áp dụng trong MVP1.
- Preconditions: Không áp dụng MVP1.
- Trigger: Phase sau khi Platform hỗ trợ automatic cashback cho End user.
- Main flow: Không triển khai trong MVP1.
- Alternate/exception: Không áp dụng MVP1.
- Data: Deferred Cashback Rule, Point Conversion Rule.
- Business rules: BRULE-004, BRULE-023.
- Acceptance criteria:
  - Given Tenant có cấu hình revenue share trong MVP1
  - When Admin/Ops vận hành transaction/order
  - Then hệ thống không yêu cầu nhập B1 hoặc point conversion rule

### UC-010 — Xem marketplace white-label

- Primary actor: End user
- Goal: Xem landing page marketplace đúng Tenant.
- Preconditions: Domain/Tenant active.
- Trigger: End user mở domain Tenant.
- Main flow:
  1. Hệ thống resolve Tenant theo domain.
  2. Hệ thống load branding, language, Top brands, category và catalog; không load Banner trong MVP1.
  3. Hệ thống filter Brand/Offer active, còn hiệu lực và thỏa visibility 2 tầng.
  4. Landing page hiển thị catalog theo Tenant.
  5. Offer card hiển thị earn rate dạng `Nhận x điểm với mỗi 20,000đ chi tiêu`.
- Alternate/exception:
  - Domain inactive: hiển thị lỗi domain/cấu hình.
  - Không có offer phù hợp: hiển thị empty state.
- Data: Tenant, Tenant Domain, Tenant Branding Config, Offer, Assignment.
- Business rules: BRULE-001, BRULE-002, BRULE-003, BRULE-012, BRULE-024.
- UI rules:
  - Landing page không hiển thị số điểm dự kiến trên card.
  - Landing page không hiển thị `Hiệu lực đến` hoặc `Còn ... ngày`.
  - Landing page không có button `Xem ưu đãi` trên offer card theo mockup mới nhất.
- Acceptance criteria:
  - Given Tenant domain active
  - When End user mở marketplace
  - Then hệ thống hiển thị branding Tenant và catalog chỉ gồm Brand/Offer thỏa `assignment_status = Active` và `tenant_visibility_status = Visible`

### UC-011 — Tìm kiếm/lọc Brand/Offer

- Primary actor: End user
- Goal: Tìm Brand/Offer bằng search, category hoặc Top brands. Banner không phải tiêu chí tìm kiếm trong MVP1.
- Preconditions: Catalog đã load.
- Trigger: End user nhập keyword hoặc chọn filter.
- Main flow:
  1. End user nhập keyword hoặc chọn category icon.
  2. Hệ thống lọc trong catalog của Tenant hiện tại.
  3. Hệ thống giữ nguyên rule active/assignment.
  4. Hệ thống hiển thị kết quả phù hợp.
- Alternate/exception:
  - Không có kết quả: hiển thị no result state.
  - Category không có offer active: không hiển thị category hoặc trả empty.
- Data: Offer, Brand, Category, Localized Content.
- Business rules: BRULE-012, BRULE-021, BRULE-024.
- Acceptance criteria:
  - Given Catalog có 10 offer assigned cho Tenant
  - When End user search theo keyword
  - Then kết quả chỉ gồm offer matching và vẫn thuộc Tenant đó

### UC-012 — Click Offer/Brand và redirect sang Brand

- Primary actor: End user
- Goal: Chọn Offer/Brand để sang Brand mua hàng. Click Banner thuộc Deferred/Phase 2.
- Preconditions: Tenant active, Offer/Brand active, visibility 2 tầng pass.
- Trigger: End user chọn Offer/Brand hợp lệ.
- Main flow:
  1. End user click/select item.
  2. Marketplace gửi request tracking.
  3. Platform validate Tenant, Offer/Brand và visibility. Nếu thiếu member_ref, UI hiển thị warning về quyền lợi hội viên/cashback/đối chiếu nhưng không chặn click.
  4. Platform tạo Click Tracking Record và click_id duy nhất.
  5. Platform redirect sang Brand destination URL kèm tracking parameter.
- Alternate/exception:
  - Thiếu member reference: hiển thị warning, cho phép tiếp tục click/mua; click record không có member_ref hoặc ghi nhận anonymous/user_ref theo context.
  - Offer không assigned/direct link cũ: chặn redirect.
  - Click double-submit: xử lý idempotent theo session/action window nếu triển khai.
- Data: Click Tracking Record.
- Business rules: BRULE-013, BRULE-022, BRULE-024.
- Acceptance criteria:
  - Given Offer active và assigned
  - When End user chọn Offer
  - Then Platform tạo click_id và redirect sang Brand
  - And không phát sinh CPC billing

### UC-013 — Brand báo order success

- Primary actor: Brand System
- Goal: Gửi order success về Platform để ghi nhận conversion.
- Preconditions: Brand active; API credential hợp lệ; click_id/order data có trong payload.
- Trigger: Purchase completed tại Brand.
- Main flow:
  1. Brand gọi API order success real-time.
  2. Platform authenticate request.
  3. Platform validate schema, click_id, brand_order_id, amount, currency, order_time.
  4. Platform kiểm tra duplicate/idempotency.
  5. Platform validate `click_id` và Tenant visibility.
  6. Platform accept order, tạo Order/Conversion trạng thái `Pending` và tính commission/revenue share tạm tính nếu đủ dữ liệu.
- Alternate/exception:
  - Auth fail/schema fail: reject và log.
  - Duplicate: trả response idempotent, không tạo order trùng.
  - Click_id invalid/visibility fail: reject hoặc đưa exception queue.
- Data: Order/Conversion, Click Tracking Record.
- Business rules: BRULE-013, BRULE-014, BRULE-015, BRULE-024.
- Acceptance criteria:
  - Given order success payload hợp lệ và click_id match được click tracking record
  - When Brand gửi API
  - Then Platform tạo order pending

### UC-014 — Brand báo cancel/refund theo Order Item

- Primary actor: Brand System
- Goal: Hoàn/hủy toàn bộ các Order Item được chỉ định trong Order `Pending` và tính lại dữ liệu tài chính.
- Preconditions: Order tồn tại và đang `Pending`; event có `request_id`, Brand + Brand Order ID và danh sách Item Code.
- Trigger: Item bị cancel/refund tại Brand.
- Main flow:
  1. Brand gửi Cancel/Refund event gồm một hoặc nhiều `items[].item_code`.
  2. Platform validate authentication, schema và idempotency theo `request_id`.
  3. Platform match Order bằng Brand + Brand Order ID và xác nhận Order đang `Pending`.
  4. Platform match từng item; không hỗ trợ hoàn một phần Qty của cùng item.
  5. Trong một atomic transaction, hệ thống chuyển item được hoàn/hủy sang `Refunded`, đặt Final amount/Gross Commission/Tenant Share của item về `0`, tính lại các giá trị tổng hợp và lưu Adjustment History.
  6. Hệ thống tổng hợp Order Status: tất cả item Refunded → `Cancelled`; còn Pending/Exception → `Pending`; các item còn lại đều Confirmed → `Confirmed`.
- Alternate/exception:
  - Không tìm thấy Order/item, payload không hợp lệ hoặc atomic update lỗi: giữ nguyên Transaction và ghi Exception.
  - Order đã `Confirmed`: từ chối event, giữ nguyên Order/item và dữ liệu tài chính đã chốt; ghi Exception để Admin xử lý đối soát thủ công.
- Data: Order, Order Item, Commission/Tenant Share snapshot, Adjustment History và Exception.
- Business rules: BRULE-018.
- Acceptance criteria:
  - Given order đang `Pending`
  - When Brand báo cancel/refund
  - Then các item trong event chuyển `Refunded`, dữ liệu tài chính được tính lại atomically và Order Status được tổng hợp từ toàn bộ item

### UC-015 — Tra cứu Basic My Orders

> Basic My Orders thuộc MVP1. Cashback/Point History ba tab, Cashback dự kiến/thực nhận và Point Posting thuộc Deferred/Phase 2.

- Primary actor: End user
- Goal: Tra cứu các Order cơ bản đã phát sinh qua Platform và xem danh sách item của từng Order.
- Preconditions: Tenant đang Active; runtime nhận được `member_ref/user_ref` hoặc session context hợp lệ từ app/hệ thống Tenant.
- Trigger: End user chọn `Đơn hàng của tôi`.
- Main flow:
  1. Hệ thống xác định `tenant_id` và End User context.
  2. Hệ thống tải các Order thuộc đúng Tenant và End User.
  3. Danh sách hiển thị Brand Order ID, Brand, Order Date, Amount, Order Status, Copy và View.
  4. End user có thể sao chép Brand Order ID.
  5. Khi chọn View, hệ thống hiển thị thông tin Order và danh sách item gồm mã/tên item, SKU nếu có, Qty, Amount, Final amount và Item Status.
  6. Item `Refunded` có Final amount bằng `0` và không được cộng vào Amount trên Order header.
- Alternate/exception:
  - Thiếu End User context: không trả dữ liệu Order và hiển thị thông báo không thể xác định người dùng.
  - Không có Order: hiển thị empty state.
  - Order không thuộc đúng Tenant/End User hoặc không tồn tại: từ chối truy cập.
- Data: Transaction/Order snapshot và Order Item; không đọc dữ liệu Cashback/Point Posting.
- Business rules: Luôn scope theo `tenant_id` và End User context; không hiển thị commission, Tenant Share, Cashback hoặc Point.
- Acceptance criteria:
  - Given runtime có Tenant và End User context hợp lệ
  - When End user mở My Orders
  - Then hệ thống hiển thị đúng danh sách và chi tiết Order thuộc End User đó, gồm Order/Item Status, và không hiển thị dữ liệu Cashback/Point

### UC-016 — Finalize order đủ điều kiện

- Primary actor: Affiliate Platform / Scheduler Job
- Goal: Chốt order sau pending_until nếu không bị hoàn/hủy.
- Preconditions: Pending order tồn tại.
- Trigger: Scheduled job đến pending_until.
- Main flow:
  1. Job lấy danh sách order pending đến hạn.
  2. Platform kiểm tra order chưa cancel/refund.
  3. Platform chốt commission Brand trả Affiliate chính thức.
  4. Platform chốt revenue share Affiliate chia Tenant chính thức.
  5. Platform đưa transaction vào reporting/reconciliation/settlement.
- Alternate/exception:
  - Chưa đến hạn: giữ `Pending`.
  - Có cancel/refund trước ngày chốt: chuyển `Cancelled`.
- Data: Order/Conversion, Commission Calculation, Revenue Share Calculation, Settlement Record.
- Business rules: BRULE-007, BRULE-018, BRULE-023.
- Acceptance criteria:
  - Given order pending đã đến pending_until và không cancel/refund
  - When scheduler chạy
  - Then commission/revenue share của order chuyển sang chính thức

### UC-017 — Cộng điểm qua Tenant loyalty API

> Deferred theo CR-01: MVP1 không gọi Tenant Loyalty API để cộng điểm.

- Primary actor: Affiliate Platform, Tenant Loyalty System.
- Goal: Không áp dụng trong MVP1.
- Preconditions: Không áp dụng MVP1.
- Trigger: Phase sau khi triển khai automatic point posting.
- Main flow: Không triển khai trong MVP1.
- Alternate/exception: Không áp dụng MVP1.
- Data: Deferred Cashback Transaction, Point Posting Log.
- Business rules: BRULE-005, BRULE-019, BRULE-023.
- Acceptance criteria:
  - Given order đã được chốt commission/revenue share trong MVP1
  - When Platform hoàn tất finalization
  - Then hệ thống không tạo Point Posting Log và không gọi Tenant Loyalty API

### UC-018 — Xem Tenant reporting

- Primary actor: Tenant Admin
- Goal: Theo dõi performance marketplace trong phạm vi Tenant.
- Preconditions: Tenant Admin authorized.
- Trigger: Tenant Admin mở portal/reporting.
- Main flow:
  1. Tenant Admin chọn date range/filter.
  2. Hệ thống query dữ liệu scoped theo tenant_id.
  3. Hệ thống hiển thị click, conversion/order, GMV, commission/revenue share tạm tính và chính thức trong phạm vi Tenant.
  4. Tenant Admin xem/export dữ liệu nếu được phân quyền.
- Alternate/exception:
  - Tenant Admin truy cập Tenant khác: unauthorized.
  - Pipeline/report delay: hiển thị partial data indicator nếu áp dụng.
- Data: Click Tracking Record, Order/Conversion, Revenue Share Calculation, Settlement Record.
- Business rules: BRULE-020.
- Acceptance criteria:
  - Given Tenant Admin thuộc Tenant A
  - When mở reporting
  - Then chỉ dữ liệu Tenant A được hiển thị

### UC-019 — Xem Admin reporting và exception

- Primary actor: Admin/Ops
- Goal: Theo dõi toàn hệ thống và xử lý exception.
- Preconditions: Admin/Ops authorized.
- Trigger: Admin/Ops mở dashboard/report hoặc exception queue.
- Main flow:
  1. Admin/Ops chọn filter Tenant/Brand/Offer/date/status.
  2. Hệ thống hiển thị click, conversion/order, commission, revenue share, settlement.
  3. Hệ thống hiển thị exception: invalid API, duplicate, click_id invalid, visibility fail, cancel/refund unmatched, missing commission rule.
  4. Admin/Ops review và cập nhật trạng thái xử lý exception theo quyền.
- Alternate/exception:
  - Không có dữ liệu: empty state.
  - Exception chưa xử lý: giữ trạng thái open/on hold và không đưa vào settlement chính thức.
- Data: Reporting aggregates, Exception records, Order/Conversion.
- Business rules: BRULE-020.
- Acceptance criteria:
  - Given có exception order/transaction
  - When Admin/Ops mở exception queue
  - Then item lỗi được hiển thị với Tenant, Brand, order và trạng thái xử lý

### UC-020 — Reconciliation và settlement tracking

- Primary actor: Admin/Ops, Finance
- Goal: Theo dõi đối soát commission và settlement với Brand/Tenant.
- Preconditions: Có transaction đủ điều kiện.
- Trigger: Đến settlement cycle.
- Main flow:
  1. Admin/Ops chọn settlement cycle.
  2. Hệ thống tổng hợp transaction theo Tenant/Brand/Offer.
  3. Hệ thống tính totals commission Brand trả Affiliate, Tenant revenue share và Affiliate keep.
  4. Admin/Ops/Finance review reconciliation.
  5. Hệ thống cập nhật Settlement Record status.
- Alternate/exception:
  - Có exception chưa xử lý: flag chưa sẵn sàng settle.
  - Settlement cycle được cấu hình theo từng hợp đồng Brand/Tenant; không hard-code tháng/quý.
- Data: Settlement Record, Order/Conversion, Commission Calculation, Revenue Share Calculation.
- Business rules: BRULE-009, BRULE-020.
- Acceptance criteria:
  - Given settlement cycle có transaction eligible
  - When Admin/Ops tạo settlement report
  - Then report hiển thị totals commission/revenue share theo Tenant/Brand

## Non-functional requirements

### Performance

- NFR-001: Landing page catalog response phải đủ nhanh để hỗ trợ trải nghiệm browse; target cụ thể TBD bởi Engineering/Product.
- NFR-002: Click tracking và redirect phải xử lý theo hướng near real-time; nếu tracking fail thì không được tạo click_id giả.
- NFR-003: Brand order success API phải hỗ trợ idempotency để xử lý retry.

### Reliability and availability

- NFR-004: Order success, commission/revenue share và settlement records phải không mất trace khi xảy ra retry hoặc timeout.
- NFR-005: Tenant Loyalty API failure/posting không áp dụng MVP1; các failure chính cần ghi exception gồm order API, click_id matching, visibility, category mapping, commission rule và cancel/refund unmatched.
- NFR-006: Reporting có thể chậm hơn transaction source, nhưng phải thể hiện trạng thái dữ liệu nếu chưa đồng bộ.

### Security and privacy

- NFR-007: Tenant Admin chỉ truy cập dữ liệu Tenant của mình.
- NFR-008: Brand API phải authentication bằng credential được cấp.
- NFR-009: Tenant Loyalty API request deferred sau MVP1; không phát sinh request trong MVP1.
- NFR-010: End user data phải scoped theo tenant_id và member reference.
- NFR-011: Audit log phải lưu thay đổi rule quan trọng: commission, revenue share, earn/cashback display text, visibility và integration credentials metadata của Brand.

### Accessibility

- NFR-012: Landing page phải có label cho search, language selector và actionable elements.
- NFR-013: Category icon không được là cách duy nhất truyền đạt ý nghĩa; phải có text label.
- NFR-014: Trạng thái loading/empty/error phải có text rõ ràng.

### Compatibility

- NFR-015: Marketplace phải responsive cho desktop/mobile; mockup hiện tại là desktop reference.
- NFR-016: MVP1 hỗ trợ đa ngôn ngữ gồm `vi-VN` và `en-US`; default locale `vi-VN`.

### Maintainability

- NFR-017: Business rules về commission, revenue share, earn/cashback display text, visibility và pending days phải cấu hình được, không hard-code theo Tenant/Brand.
- NFR-018: Integration logs phải đủ thông tin để Engineering/Ops debug nhưng không lộ secret.

## Data requirements

| Entity | Key fields | Lifecycle | Owner |
|---|---|---|---|
| Tenant | tenant_id, code, status, contact | Draft -> Active -> Inactive | Admin/Ops |
| Tenant Domain | domain_id, tenant_id, hostname, dns_status, ssl_status | Pending Verification -> Active -> Inactive | Admin/Ops |
| Tenant Branding Config | tenant_id, logo, theme, default_locale, supported_locales | Draft/Active version | Admin/Ops |
| Tenant Loyalty Integration | Deferred sau MVP1 | Không áp dụng MVP1 | N/A |
| Brand | brand_id, code, name, status | Draft -> Active -> Inactive | Admin/Ops |
| Offer | offer_id, brand_id, status, destination_url | Draft -> Active -> Inactive | Admin/Ops |
| Tenant Brand/Offer Assignment | assignment_id, tenant_id, brand_id, offer_id, assignment_status, assignment_scope | Unassigned -> Active -> Inactive | Admin/Ops |
| Tenant Brand/Offer Visibility | tenant_id, brand_id, offer_id optional, tenant_visibility_status, offer_visibility_mode | Visible -> Hidden | Tenant Admin |
| Tenant Revenue Share Rule | rule_id, tenant_id, brand_id, category_id/offer_id optional, tenant_share_rate | Draft -> Active -> Inactive; chỉ rule `Active` được dùng để resolve Tenant Share | Admin/Ops |
| Earn/Cashback Display Text | display_id, tenant_id, brand_id, category_id/offer_id optional, locale, display_text | Draft -> Active -> Inactive | Tenant Admin |
| Click Tracking Record | click_id, tenant_id, user_ref, brand_id, offer_id, clicked_at | Created -> Redirected | Platform |
| Order/Conversion | order_id, brand_order_id, click_id, amount, status, pending_until | Pending -> Confirmed/Cancelled | Brand/System |
| Cashback Transaction | Deferred sau MVP1 | Không áp dụng MVP1 | N/A |
| Point Posting Log | Deferred sau MVP1 | Không áp dụng MVP1 | N/A |
| Settlement Record | settlement_id, cycle, tenant_id, brand_id, totals, status | Open -> Settled | Admin/Ops |

### Data dictionary - Tenant and white-label setup

| Entity | Field Name | Description | Data Type | Required | Default | Source | Validation / Rule | Sensitivity |
|---|---|---|---|---|---|---|---|---|
| Tenant | tenant_id | Khóa định danh Tenant | UUID/String | Y | Generated | Platform | Unique, immutable | Internal |
| Tenant | code | Mã Tenant dùng trong config/reporting | String | Y | Empty | Admin/Ops | Unique, no whitespace-only | Internal |
| Tenant | name | Tên Tenant hiển thị/quản trị | String | Y | Empty | Admin/Ops | Max length TBD | Public/Internal |
| Tenant | status | Trạng thái Tenant | Enum: Draft, Active, Inactive | Y | Draft | Admin/Ops | Active mới render marketplace | Internal |
| Tenant | contact_name | Người liên hệ vận hành | String | N | Empty | Admin/Ops | Optional | Confidential |
| Tenant | contact_email | Email liên hệ | Email | N | Empty | Admin/Ops | Email format | Confidential |
| Tenant Domain | domain_id | Khóa domain config | UUID/String | Y | Generated | Platform | Unique | Internal |
| Tenant Domain | tenant_id | Tenant owner | UUID/String | Y | N/A | Platform | Must reference Tenant | Internal |
| Tenant Domain | hostname | Domain/subdomain white-label | String/domain | Y | Empty | Admin/Ops | Unique; valid hostname | Public |
| Tenant Domain | dns_status | Trạng thái DNS | Enum: Pending, Verified, Failed | Y | Pending | System/Admin | Active domain requires Verified | Internal |
| Tenant Domain | ssl_status | Trạng thái SSL | Enum: Pending, Issued, Failed | Y | Pending | System/Admin | Active domain requires Issued | Internal |
| Tenant Domain | status | Trạng thái domain | Enum: Pending Verification, Active, Inactive | Y | Pending Verification | System/Admin | Active only if DNS/SSL pass | Internal |
| Tenant Branding Config | tenant_id | Tenant owner | UUID/String | Y | N/A | Platform | Must reference Tenant | Internal |
| Tenant Branding Config | logo_url | Logo Tenant | URL/String | N | Fallback logo | Admin/Ops | Must be valid asset URL if provided | Public |
| Tenant Branding Config | primary_color | Màu chủ đạo | String/HEX | N | Default theme | Admin/Ops | HEX format | Public |
| Tenant Branding Config | default_locale | Locale mặc định | Locale code | Y | `vi-VN` | Admin/Ops | Must be in supported_locales | Public |
| Tenant Branding Config | supported_locales | Danh sách locale hỗ trợ | Array/Locale | Y | `vi-VN`, `en-US` | Admin/Ops | MVP1 gồm `vi-VN` và `en-US` | Public |
| Tenant Branding Config | status | Trạng thái config | Enum: Draft, Active, Inactive | Y | Draft | Admin/Ops | Active config used by marketplace | Internal |

### Data dictionary - Brand, Offer, content and visibility

| Entity | Field Name | Description | Data Type | Required | Default | Source | Validation / Rule | Sensitivity |
|---|---|---|---|---|---|---|---|---|
| Brand | brand_id | Khóa định danh Brand | UUID/String | Y | Generated | Platform | Unique | Internal |
| Brand | code | Mã Brand | String | Y | Empty | Admin/Ops | Unique | Internal |
| Brand | name | Tên Brand hiển thị | String | Y | Empty | Admin/Ops | Required for card/report | Public |
| Brand | status | Trạng thái Brand | Enum: Draft, Active, Inactive | Y | Draft | Admin/Ops | Active mới active Offer/nhận order | Internal |
| Brand | api_credential_ref | Tham chiếu credential API Brand | Secret reference | Conditional | Empty | Admin/Ops | Required for order success API | Secret reference |
| Brand | pending_days | Số ngày chờ trước khi chốt commission/revenue share chính thức | Integer | Y | TBD | Admin/Ops | >= 0; nếu thiếu không cho active rule chốt tự động | Internal |
| Offer | offer_id | Khóa định danh Offer | UUID/String | Y | Generated | Platform | Unique | Internal |
| Offer | brand_id | Brand owner | UUID/String | Y | N/A | Admin/Ops | Must reference active Brand to set Offer Active | Internal |
| Offer | status | Trạng thái offer | Enum: Draft, Active, Inactive | Y | Draft | Admin/Ops | Active mới hiển thị | Public/Internal |
| Offer | start_at | Thời điểm bắt đầu hiệu lực | Datetime | N | Empty | Admin/Ops | start_at <= end_at if both exist | Internal |
| Offer | end_at | Thời điểm kết thúc hiệu lực | Datetime | N | Empty | Admin/Ops | Expired offer không hiển thị/click | Internal |
| Offer | destination_url | URL redirect sang Brand | URL/String | Y | Empty | Admin/Ops/Brand | Valid URL; append tracking params | Confidential/Internal |
| Localized Content | content_id | Khóa content | UUID/String | Y | Generated | Platform | Unique | Internal |
| Localized Content | entity_type | Loại entity | MVP1: Offer, Category, Brand; Banner chỉ áp dụng từ Phase 2 | Y | N/A | Admin/Ops | Must match entity_id; không nhận Banner trong MVP1 | Internal |
| Localized Content | entity_id | ID entity được dịch | UUID/String | Y | N/A | Admin/Ops | Must exist | Internal |
| Localized Content | locale | Locale của nội dung | Locale code | Y | default_locale | Admin/Ops | Must be supported locale | Public |
| Localized Content | title | Tiêu đề hiển thị | String | Y | Empty | Admin/Ops | Required for Active | Public |
| Localized Content | description | Mô tả ngắn | Text | N | Empty | Admin/Ops | Optional by content type | Public |
| Localized Content | terms | Điều kiện/terms | Text | N | Empty | Admin/Ops | Required if compliance policy requires | Public |
| Tenant Brand/Offer Assignment | assignment_id | Khóa assignment | UUID/String | Y | Generated | Platform | Unique | Internal |
| Tenant Brand/Offer Assignment | tenant_id | Tenant được gán | UUID/String | Y | N/A | Admin/Ops | Must reference Tenant | Internal |
| Tenant Brand/Offer Assignment | brand_id | Brand được gán | UUID/String | Y | N/A | Admin/Ops | Must reference Brand | Internal |
| Tenant Brand/Offer Assignment | offer_id | Offer được gán, optional nếu gán cấp Brand | UUID/String | N | Empty | Admin/Ops | If empty, applies Brand-level per rule | Internal |
| Tenant Brand/Offer Assignment | assignment_status | Trạng thái assignment pool | Enum: Active, Inactive | Y | Inactive | Admin/Ops | Default hidden unless Active | Internal |
| Tenant Brand/Offer Assignment | assignment_scope | Phạm vi Offer được phép | Enum: All active offers, Custom offers | Y | All active offers | Admin/Ops | Custom offers phải có danh sách Offer hợp lệ | Internal |
| Tenant Brand/Offer Visibility | tenant_visibility_status | Trạng thái Tenant bật/tắt trong pool | Enum: Visible, Hidden | Y | Visible khi assignment mới Active | Tenant Portal | Chỉ có hiệu lực trong Admin assignment pool | Internal |

### Data dictionary - Rule configuration

| Entity | Field Name | Description | Data Type | Required | Default | Source | Validation / Rule | Sensitivity |
|---|---|---|---|---|---|---|---|---|
| Brand Commission Rule | rule_id | Khóa rule | UUID/String | Y | Generated | Platform | Unique | Internal |
| Brand Commission Rule | brand_id | Brand áp dụng | UUID/String | Y | N/A | Admin/Ops | Must reference Brand | Internal |
| Brand Commission Rule | affiliate_category_id | Category nội bộ Affiliate áp dụng | UUID/String | Conditional | Empty | Admin/Ops | Required for category-level rule | Internal |
| Brand Commission Rule | is_default | Nếu item có brand_offer_code, Platform resolve Offer Mapping theo brand_id + brand_offer_code và sử dụng Offer commission rule hợp lệ. Nếu không có code hoặc mapping/rule Offer không hợp lệ, hệ thống fallback sang Category rồi Category Default. | Boolean | Conditional | false | Admin/Ops | Exactly one active default category per Brand | Internal |
| Brand Commission Rule | brand_category_id/code | Category ID/code phía Brand để map order payload | String | Conditional | Empty | Admin/Ops/Brand | Required for category-level rule; nếu Brand không truyền field này trong order runtime thì dùng default category | Internal |
| Brand Commission Rule | offer_id | Offer áp dụng nếu rule cấp Offer | UUID/String | N | Empty | Admin/Ops | Offer-level là tùy chọn; nếu không có Offer commission rule active thì runtime fallback sang Category/default category | Internal |
| Brand Commission Rule | commission_type | Kiểu commission Brand trả Affiliate | Enum: Percentage, Fixed | Y | Percentage | Admin/Ops | Determines value unit | Confidential |
| Brand Commission Rule | commission_value | Giá trị commission Brand trả Affiliate | Decimal/Money | Y | Empty | Admin/Ops | > 0; `%` if Percentage, VND if Fixed | Confidential |
| Tenant Revenue Share Rule | rule_id | Khóa revenue share rule | UUID/String | Y | Generated | Platform | Unique | Internal |
| Tenant Revenue Share Rule | tenant_id | Tenant áp dụng | UUID/String | Y | N/A | Admin/Ops | Must reference Tenant | Internal |
| Tenant Revenue Share Rule | brand_id | Brand áp dụng | UUID/String | Y | N/A | Admin/Ops | Must reference assigned Brand | Internal |
| Tenant Revenue Share Rule | category_id | Category override nếu có | UUID/String | N | Empty | Admin/Ops | Category-level override nếu không có Offer rule | Internal |
| Tenant Revenue Share Rule | offer_id | Offer override nếu có | UUID/String | N | Empty | Admin/Ops | Offer-level ưu tiên cao nhất | Internal |
| Tenant Revenue Share Rule | tenant_share_rate | Tỷ lệ Affiliate chia cho Tenant | Decimal percent | Y | Empty | Admin/Ops | > 0 và <= 100; tính trên `gross_commission_amount` | Confidential |

### Data dictionary - Tracking, order, cashback and settlement

| Entity | Field Name | Description | Data Type | Required | Default | Source | Validation / Rule | Sensitivity |
|---|---|---|---|---|---|---|---|---|
| Click Tracking Record | click_id | Khóa tracking outbound | UUID/String | Y | Generated | Platform | Unique | Internal |
| Click Tracking Record | tenant_id | Tenant context | UUID/String | Y | N/A | Platform | Must reference Tenant | Internal |
| Click Tracking Record | user_ref | Member reference từ Tenant nếu có | String | N | Empty | Tenant/Platform | Dùng cho đối soát/tra cứu; MVP1 không dùng để cộng điểm | PII/Pseudonymous |
| Click Tracking Record | brand_id | Brand được click | UUID/String | Y | N/A | Platform | Must pass visibility 2 tầng | Internal |
| Click Tracking Record | offer_id | Offer được click | UUID/String | Conditional | Empty | Platform | Must be active if offer-level click | Internal |
| Click Tracking Record | clicked_at | Thời điểm click | Datetime | Y | Now | Platform | Used for tracking/reporting | Internal |
| Click Tracking Record | destination_url | URL Brand sau khi append tracking | URL/String | Y | N/A | Platform | Valid URL | Confidential |
| Order/Conversion | order_id | Khóa order nội bộ | UUID/String | Y | Generated | Platform | Unique | Internal |
| Order/Conversion | brand_order_id | Mã order từ Brand | String | Y | Empty | Brand | Idempotent with brand_id/click_id | Confidential |
| Order/Conversion | click_id | Click liên quan | UUID/String | Y | Empty | Brand | Must exist and match click context | Internal |
| Order/Conversion | tenant_id | Tenant context | UUID/String | Y | Derived | Platform | Derived from click | Internal |
| Order/Conversion | brand_id | Brand context | UUID/String | Y | Derived | Platform | Derived from click/payload | Internal |
| Order/Conversion | offer_id | Offer context | UUID/String | N | Derived | Platform | Derived if available | Internal |
| Order/Conversion | order_amount | Giá trị giao dịch | Money/Decimal | Y | Empty | Brand | >= 0; currency required | Confidential |
| Order/Conversion | currency | Tiền tệ | Enum/String | Y | VND/TBD | Brand | Must be supported | Internal |
| Order/Conversion | order_success_at | Thời điểm mua thành công | Datetime | Y | Empty | Brand | Used for pending_until | Internal |
| Order/Conversion | pending_until | Thời điểm đủ điều kiện chốt commission/revenue share chính thức | Datetime | Y | Calculated | Platform | order_success_at + brand.pending_days | Internal |
| Order/Conversion | status | Trạng thái order | Enum | Y | Pending | Platform | Pending, Confirmed, Cancelled | Internal |
| Commission Calculation | provisional_gross_commission_amount | Hoa hồng Brand trả Affiliate tạm tính | Money/Decimal | N | Calculated | Platform | Tính từ rule tại thời điểm ghi nhận order nếu đủ dữ liệu | Confidential |
| Commission Calculation | gross_commission_amount | Hoa hồng Brand trả Affiliate chính thức | Money/Decimal | N | Empty | Platform | Chỉ có sau pending_until và không cancel/refund | Confidential |
| Revenue Share Calculation | provisional_tenant_share_amount | Phần Affiliate chia Tenant tạm tính | Money/Decimal | N | Calculated | Platform | Tính từ provisional commission và revenue share rule | Confidential |
| Revenue Share Calculation | tenant_share_amount | Phần Affiliate chia Tenant chính thức | Money/Decimal | N | Empty | Platform | Chỉ có sau commission chính thức | Confidential |
| Revenue Share Calculation | affiliate_keep_amount | Phần Affiliate giữ lại chính thức | Money/Decimal | N | Empty | Platform | gross_commission_amount - tenant_share_amount | Confidential |
| Settlement Record | settlement_id | Khóa settlement | UUID/String | Y | Generated | Platform | Unique | Internal |
| Settlement Record | cycle | Chu kỳ settlement | String/Date range | Y | TBD | Finance/Ops | Monthly/Quarterly/TBD | Confidential |
| Settlement Record | tenant_id | Tenant liên quan | UUID/String | Y | N/A | Platform | Must reference Tenant | Internal |
| Settlement Record | brand_id | Brand liên quan | UUID/String | Y | N/A | Platform | Must reference Brand | Internal |
| Settlement Record | total_gross_commission_amount | Tổng commission Brand trả Affiliate | Money/Decimal | Y | Calculated | Platform | Sum official transactions | Confidential |
| Settlement Record | total_affiliate_keep_amount | Tổng Affiliate giữ lại | Money/Decimal | Y | Calculated | Platform | Sum official transactions | Confidential |
| Settlement Record | total_tenant_share_amount | Tổng Affiliate chia Tenant | Money/Decimal | Y | Calculated | Platform | Sum official transactions | Confidential |
| Settlement Record | status | Trạng thái settlement | Enum | Y | Open | Ops | Open, In Review, Settled, On Hold | Confidential |

## Rule catalog and calculation requirements

| Rule ID | Rule name | Formula / Logic | Applies to | Error behavior |
|---|---|---|---|---|
| RULE-001 | Tenant resolution | Mỗi request marketplace phải resolve đúng 1 Tenant theo hostname/domain active. | Landing page, catalog, click | Nếu fail, hiển thị domain/config error. |
| RULE-002 | Brand/Offer visibility | Brand/Offer chỉ hiển thị/click được nếu Active, còn hiệu lực, `assignment_status = Active` và `tenant_visibility_status = Visible`. | Catalog, direct link, click | Hidden hoặc direct-link blocked. |
| RULE-003 | Default hidden | Brand/Offer mặc định không hiển thị nếu chưa có Tenant Brand/Offer Assignment active; nếu assignment mới active và Tenant chưa thao tác thì mặc định `tenant_visibility_status = Visible`. | Catalog | Không đưa vào response catalog nếu rule AND fail. |
| RULE-004 | Click id uniqueness | Mỗi outbound click tạo click_id duy nhất gắn tenant_id, user_ref, brand_id, offer_id, clicked_at. | Click tracking | Không redirect nếu không tạo được click hợp lệ. |
| RULE-005 | No CPC billing | Click chỉ phục vụ order tracking/reporting, không tạo CPC fee/billing amount. | Click/reporting | Không có CPC config hoặc CPC billing record. |
| RULE-006 | Click_id matching | Order success hợp lệ phải có `click_id` tồn tại và match đúng context click đã ghi nhận. | Order success | Fail thì reject hoặc exception queue. |
| RULE-007 | Commission calculation | Brand trả commission theo Offer nếu order có offer_id và Offer có commission rule active; nếu không có Offer commission active thì fallback sang Category/default category của Brand. | Commission config/order | Không tạo exception chỉ vì thiếu Offer commission; chỉ exception khi không có default category hoặc không có commission rule hợp lệ sau fallback. |
| RULE-008 | Tenant revenue share | Affiliate chia cho Tenant theo `tenant_share_rate%`; resolve rule Offer -> Category -> Brand default nếu có. Tenant share không hỗ trợ Fixed amount/VND. | Revenue share/order | Không active rule nếu rate không hợp lệ hoặc > 100%. |
| RULE-009 | Pending until | pending_until = order_success_at + Brand.pending_days. | Order lifecycle | Nếu missing pending_days bắt buộc thì không auto finalize. |
| RULE-010 | Cancel/refund theo Order Item | Chỉ Order `Pending` được tự động điều chỉnh. Item trong event chuyển `Refunded`; hệ thống tính lại dữ liệu và tổng hợp Order Status. Event cho Order `Confirmed` bị từ chối, giữ nguyên dữ liệu đã chốt và ghi Exception để Admin xử lý đối soát thủ công. | Order lifecycle | Không hỗ trợ hoàn một phần Qty của cùng item trong MVP1. |
| RULE-011 | Deferred point posting | MVP1 không chuyển Order sang Rewarded và không có point posting. | Cashback/Order | Không phát sinh Posting Failed do Tenant Loyalty API. |
| RULE-012 | Landing earn display | Landing card hiển thị earn/cashback display text do Tenant cấu hình, ví dụ `Nhận x điểm với mỗi 20,000đ chi tiêu`, không hiển thị số điểm dự kiến cụ thể. | Landing page | Không render estimated point amount trên card. |
| RULE-013 | Tenant reporting scope | Tenant Admin chỉ xem dữ liệu có tenant_id thuộc Tenant của mình. | Reporting | Unauthorized nếu truy cập Tenant khác. |
| RULE-014 | Idempotent Brand order | Duplicate theo brand_id + brand_order_id hoặc click_id/order key không tạo order trùng. | Order API | Trả response idempotent. |
| RULE-015 | Deferred idempotent point posting | Không áp dụng MVP1. | Tenant Loyalty API | Xử lý ở phase sau. |

## Interface and integration requirements

| Interface | Direction | Data exchanged | Error handling | Owner |
|---|---|---|---|---|
| Tenant domain/DNS/SSL | Tenant/Admin -> Platform/DNS | hostname, DNS/SSL verification status | Domain inactive, marketplace unavailable | Admin/Ops, Tenant |
| Brand order success API | Brand -> Platform | click_id, brand_order_id, amount, currency, order_time, metadata | Reject invalid auth/schema; idempotent duplicate response | Brand, Platform |
| Brand cancel/refund notification | Brand -> Platform | request_id, brand_id/code, brand_order_id, order_id optional, event_type, event_at, items[].item_code, reason optional | Contract theo Order Transaction SRS; chỉ xử lý Order Pending; invalid/unmatched/Confirmed vào Exception | Brand, Platform |
| Tenant loyalty point posting API | Deferred sau MVP1 | Không trao đổi dữ liệu trong MVP1 | N/A | Tenant, Platform |
| Reporting/analytics | Platform internal | click, order, commission, revenue share, settlement metrics | Partial data indicator/log nếu pipeline fail | Platform |

### API payload fields - Brand order success

| Field Name | Description | Data Type | Required | Source | Validation / Rule |
|---|---|---|---|---|---|
| request_id | ID request từ Brand để trace/idempotency | String | Y | Brand | Unique or reusable for idempotent retry |
| brand_id / brand_code | Định danh Brand gửi request | String | Y | Brand/Platform credential | Must match API credential |
| click_id | Click tracking ID từ redirect | String | Y | Brand receives from redirect | Must exist and match click context |
| brand_order_id | Mã đơn hàng phía Brand | String | Y | Brand | Idempotent with brand_id |
| order_success_at | Thời điểm order thành công | Datetime | Y | Brand | Must be parseable; used for pending_until |
| order_amount | Giá trị giao dịch đủ điều kiện | Decimal | Y | Brand | >= 0 |
| currency | Tiền tệ giao dịch | String/Enum | Y | Brand | Must be supported currency |
| customer_ref | Tham chiếu khách hàng nếu Brand gửi | String | N | Brand | Không thay thế Tenant member_ref nếu không được map |
| order_metadata | Metadata đơn hàng | JSON object | N | Brand | Không chứa dữ liệu nhạy cảm ngoài contract |
| signature/auth header | Thông tin xác thực request | Header/String | Y | Brand | Must pass authentication |

### API payload fields - Brand cancel/refund notification

Contract được chốt theo Order Transaction SRS. Event xử lý một hoặc nhiều item nhưng mỗi item chỉ được hoàn/hủy toàn bộ.

| Field Name | Description | Data Type | Required | Source | Validation / Rule |
|---|---|---|---|---|---|
| request_id | ID request cancel/refund | String | Y | Brand | Used for trace/idempotency |
| brand_id / brand_code | Brand gửi event | String | Y | Brand | Must match credential |
| brand_order_id | Mã order phía Brand | String | Y | Brand | Must map to existing order or exception queue |
| order_id | Mã order nội bộ Platform nếu Brand lưu được | String | N | Brand/Platform | Used as secondary lookup |
| event_type | Loại event | Enum: `ORDER_CANCELLED`, `ITEM_CANCELLED`, `ITEM_REFUNDED` | Y | Brand | Chỉ áp dụng cho Order `Pending`; `ORDER_CANCELLED` phải bao phủ toàn bộ item còn hợp lệ. |
| event_at | Thời điểm hoàn/hủy | Datetime | Y | Brand | Must be parseable |
| items | Danh sách item hoàn/hủy toàn bộ | Array | Y | Brand | Không rỗng; mỗi phần tử bắt buộc có `item_code` match đúng Order |
| items[].item_code | Mã item phía Brand | String | Y | Brand | Match duy nhất trong Brand Order; không hỗ trợ partial Qty |
| items[].reason | Lý do riêng của item | String | N | Brand | Optional |
| reason | Lý do hoàn/hủy | String | N | Brand | Optional but useful for Ops |
| signature/auth header | Thông tin xác thực request | Header/String | Y | Brand | Must pass authentication |

### API payload fields - Tenant loyalty point posting request

Deferred sau MVP1 theo CR-01. MVP1 không gửi request Tenant Loyalty API, không tính points và không sinh Point Posting Log.

### API payload fields - Tenant loyalty point posting response

Deferred sau MVP1 theo CR-01.

## Validation and error handling

| Validation | Error behavior |
|---|---|
| Tenant code/domain unique | Không cho lưu |
| Domain DNS/SSL active trước khi public | Hiển thị trạng thái chưa hoàn tất |
| Commission/revenue share rule hợp lệ theo scope Brand/Category/Offer; `tenant_share_rate` > 0 và <= 100 | Không cho active rule |
| B1/cashback rule | Deferred sau MVP1; không hiển thị cấu hình này |
| Brand Active trước khi active Offer | Không cho Active |
| Offer Active và còn hiệu lực trước khi hiển thị/click | Ẩn hoặc chặn click |
| Assignment active trước khi hiển thị/click | Ẩn hoặc direct-link blocked |
| Brand API auth/schema hợp lệ | Reject và log |
| Order success idempotent | Không tạo order trùng |
| Click_id match | Reject/exception nếu fail |
| pending_until reached và không cancel/refund | Mới cho finalize commission/revenue share |
| Tenant Loyalty API success | Deferred sau MVP1; không dùng làm điều kiện trạng thái trong MVP1 |

## Observability and audit

- Lưu audit log cho thay đổi Tenant/Brand/Offer, visibility assignment, commission rule, revenue share rule, earn/cashback display text và Brand integration config.
- Lưu click_id và correlation giữa click, order, commission/revenue share và settlement.
- Lưu request/response metadata cho Brand order success, không lưu secret ở dạng plain text.
- Exception queue phải phân loại lỗi: auth fail, schema fail, duplicate, click_id invalid, visibility fail, `category_mapping_missing`, `default_category_missing`, `commission_rule_missing`, cancel/refund unmatched.

## Acceptance criteria

### AC-001 — Marketplace hiển thị theo Tenant (SR-010, SR-008)

- Given Brand/Offer active nhưng chưa assigned cho Tenant A
- When End user mở marketplace Tenant A
- Then Brand/Offer đó không hiển thị
- And direct link đến offer đó bị chặn

### AC-002 — Landing page hiển thị earn rate mới nhất (SR-010)

- Given Offer active, assigned cho Tenant và có earn rate
- When End user xem landing page
- Then card hiển thị `Nhận x điểm với mỗi 20,000đ chi tiêu`
- And không hiển thị số điểm dự kiến, `Hiệu lực đến`, `Còn ... ngày`, hoặc button `Xem ưu đãi`

### AC-003 — Click tracking không tính CPC (SR-012)

- Given End user chọn Offer/Brand hợp lệ trong MVP1
- When Platform xử lý click
- Then click_id được tạo và lưu
- And End user được redirect sang Brand
- And không phát sinh CPC billing amount

### AC-004 — Order success tạo Pending Order (SR-013)

- Given Brand gửi payload hợp lệ với click_id match được click tracking record
- When Platform nhận order success
- Then Platform tạo Order/Conversion trạng thái `Pending`
- And hệ thống tính commission/revenue share tạm tính nếu đủ dữ liệu rule

### AC-005 — Cancel/refund ngăn chốt commission chính thức (SR-014, SR-016)

- Given Order đang `Pending`
- When Brand báo cancel/refund trước ngày chốt
- Then Order chuyển `Cancelled`
- And Platform không chốt commission/revenue share chính thức
- And Platform không gọi Tenant Loyalty API để cộng điểm

### AC-006 — Deferred cộng điểm End user (SR-016, SR-017)

- Given Order đã đến pending_until và không cancel/refund
- When Platform chốt transaction trong MVP1
- Then hệ thống chỉ chốt commission/revenue share chính thức
- And không tạo cashback B1, không tính điểm và không gọi Tenant Loyalty API

### AC-007 — Commission/revenue share hợp lệ (SR-005)

- Given Brand commission rule hợp lệ và Tenant revenue share rule có `tenant_share_rate%` hợp lệ
- When Admin/Ops active rule
- Then hệ thống cho phép dùng rule để tính transaction

### AC-008 — Deferred cashback B1 (SR-009)

- Given Admin/Ops cấu hình revenue share cho Tenant trong MVP1
- When lưu rule
- Then hệ thống không yêu cầu nhập B1 hoặc point conversion

### AC-009 — Tenant reporting scoped (SR-018)

- Given Tenant Admin thuộc Tenant A
- When Tenant Admin mở reporting
- Then chỉ dữ liệu Tenant A được hiển thị

### AC-010 — Không có posting failure trong MVP1 (SR-017, SR-019)

- Given Order đủ điều kiện chốt commission/revenue share
- When Platform finalization chạy trong MVP1
- Then không có trạng thái `Posting Failed` do Tenant Loyalty API
- And exception point posting không phát sinh trong Admin/Ops queue

## Traceability matrix

| Business requirement | System requirement | Use case | Acceptance criteria |
|---|---|---|---|
| BR-001, BR-004, BR-005 | SR-001, SR-002, SR-008, SR-010 | UC-001, UC-002, UC-008, UC-010 | AC-001 |
| BR-003, BR-017 | SR-007, SR-010, SR-015 | UC-007, UC-010, UC-015 | AC-002, AC-006 |
| BR-006, BR-007 | SR-012 | UC-012 | AC-003 |
| BR-009, BR-010, BR-011 | SR-013 | UC-013 | AC-004 |
| BR-012 | SR-005, SR-020 | UC-005, UC-020 | AC-007 |
| BR-013, BR-014, BR-018 | SR-009, SR-017 | UC-009, UC-017 | AC-006, AC-008 |
| BR-015, BR-016 | SR-014, SR-016 | UC-014, UC-016 | AC-005 |
| BR-019 | SR-018 | UC-018 | AC-009 |
| BR-020, BR-021, BR-022 | SR-019, SR-020 | UC-019, UC-020 | AC-010 |

## Dependencies and constraints

- Tenant domain/DNS/SSL readiness.
- Tenant Loyalty API readiness and authentication deferred sau MVP1.
- Brand order success API readiness and credentials.
- Brand phải triển khai Cancel/Refund API theo Order Transaction SRS; MVP1 chỉ hỗ trợ hoàn/hủy toàn bộ item của Order `Pending`.
- Commercial/legal approval for Tenant-Brand visibility assignment.
- Settlement cycle cấu hình theo từng hợp đồng Brand/Tenant.
- Locale MVP1 gồm `vi-VN`, `en-US`.
- Data privacy, tracking consent and data sharing terms between Tenant, Platform and Brand.

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Brand/Offer hiển thị sai Tenant | Vi phạm commercial/legal, sai click/order tracking | Default hidden; active assignment required |
| Brand gửi cancel/refund sau khi Order đã Confirmed | Không được tự động thay đổi dữ liệu đã chốt | Từ chối event, giữ nguyên Transaction và ghi Exception để Admin xử lý đối soát thủ công |
| Tenant Loyalty API lỗi | Không ảnh hưởng MVP1 vì chưa gọi API cộng điểm | Đưa integration/point posting sang phase sau |
| Revenue share cấu hình sai | Sai phân bổ doanh thu cho Tenant | Validate rule theo scope Brand/Category/Offer và quyền cấu hình |
| Rò rỉ dữ liệu giữa Tenant | Compliance/data trust risk | Tenant-scoped permission và reporting |
| Wireframe cũ khác mockup mới | Sai UI expectation | SRS lấy mockup/latest user request làm source ưu tiên cho landing page |

## Open questions

| Question | Owner | Impact |
|---|---|---|
| Chi tiết nghiệp vụ và chứng từ manual adjustment sau khi Cancel/Refund của Order `Confirmed` bị ghi Exception | Product/Finance/Ops | Không chặn Cancel/Refund API; được đặc tả trong Reporting/Reconciliation |

## Closed decisions

| Nội dung | Quyết định | Tác động |
|---|---|---|
| Ngôn ngữ MVP1 | Hỗ trợ `vi-VN` và `en-US`; default `vi-VN`. | Content, validation và QA theo 2 locale. |
| End user chưa định danh member reference | Vẫn được click/mua; cần warning rằng quyền lợi/cashback/đối chiếu theo hội viên có thể không được đảm bảo. | Click tracking cho phép thiếu `member_ref`. |
| Settlement cycle | Theo từng hợp đồng Brand/Tenant. | Settlement config không hard-code tháng/quý. |

## Repository evidence

- [Functional analysis](../analysis/affiliate-marketplace-platform-analysis.md)
- [BRD](../brd/affiliate-marketplace-platform.md)
- [Use case list](../usecases/affiliate-marketplace-platform-usecase-list.md)
- [PlantUML activity diagram](../modeling/affiliate-marketplace-customer-journey-activity-diagram.md)
- [Landing page mockup](../mockups/affiliate-marketplace-landing-page-desktop.html)

## Readiness

`DRAFTED`
