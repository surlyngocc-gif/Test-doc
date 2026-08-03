# Use Case List: Affiliate Marketplace Platform

## Document control

- Status: Draft
- Owner: TBD
- Related analysis: [docs/analysis/affiliate-marketplace-platform-analysis.md](../analysis/affiliate-marketplace-platform-analysis.md)
- Related modeling: [docs/modeling/affiliate-marketplace-platform-modeling.md](../modeling/affiliate-marketplace-platform-modeling.md)
- Related BRD: [docs/brd/affiliate-marketplace-platform.md](../brd/affiliate-marketplace-platform.md)
- Last updated: 2026-07-23

## Scope

Danh sách use case này mô tả các nghiệp vụ chính của MVP1 cho Affiliate Marketplace Platform, bao gồm Admin/Ops, Tenant Admin, End user, Brand System và Platform/System jobs.

## Actor list

| Actor | Mô tả |
|---|---|
| Admin/Ops | Người vận hành platform, cấu hình Tenant, Brand, Offer, visibility, commission, settlement và exception. |
| Tenant Admin | Người dùng phía Tenant, xem reporting và dữ liệu trong phạm vi Tenant của mình. |
| End user | Người dùng cuối thuộc loyalty member base của Tenant, truy cập marketplace, click Offer/Brand và tra cứu Basic My Orders khi app Tenant cung cấp End User context. Cashback/Point History ba tab thuộc Deferred/Phase 2. |
| Brand System | Hệ thống của Brand/Merchant gửi order success và cancel/refund event cho Platform. |
| Affiliate Platform | Hệ thống trung gian xử lý tracking click/order, commission/revenue share và settlement state. |
| Tenant Loyalty System | Hệ thống loyalty của Tenant. MVP1 không gọi API cộng điểm sang hệ thống này theo CR-01. |

## Use case list

| UC ID | Tên use case | Actor chính | Mục tiêu | Trigger | Điều kiện trước | Kết quả sau | MVP1 | Ưu tiên | Trace |
|---|---|---|---|---|---|---|---|---|---|
| UC-001 | Onboard Tenant | Admin/Ops | Tạo Tenant và cấu hình thông tin cơ bản cho marketplace white-label. | Tenant partnership được duyệt. | Admin/Ops có quyền cấu hình. | Tenant được tạo và sẵn sàng cấu hình domain/branding/integration. | Yes | Must | FR-001..FR-005 |
| UC-002 | Cấu hình domain và branding Tenant | Admin/Ops | Cấu hình subdomain/custom domain, logo, theme, locale và thông tin hiển thị theo Tenant. | Tenant cần public marketplace. | Tenant đã tồn tại. | Marketplace render đúng Tenant khi End user truy cập domain hợp lệ. | Yes | Must | FR-002, FR-003, FR-014 |
| UC-003 | Cấu hình loyalty integration Tenant | Admin/Ops | Deferred sau MVP1; MVP1 không cấu hình hoặc gọi API cộng điểm sang Tenant Loyalty System. | Phase sau khi bật point posting. | Không áp dụng MVP1. | Không áp dụng MVP1. | No | Deferred | FR-005, FR-026 |
| UC-004 | Onboard Brand/Merchant | Admin/Ops | Tạo Brand profile và cấu hình thông tin tích hợp Brand. | Brand partnership được duyệt. | Có thông tin Brand và điều khoản commercial. | Brand active hoặc draft trên Platform. | Yes | Must | FR-006, FR-011 |
| UC-005 | Cấu hình commission Brand và revenue share Tenant | Admin/Ops | Cấu hình commission Brand trả Affiliate theo Category/Offer và phần Affiliate chia Tenant theo Brand default hoặc override Category/Offer. | Có điều khoản commission với Brand/Tenant. | Brand/Tenant tồn tại. | Rule hợp lệ khi value/type/scope được validate. | Yes | Must | FR-008, FR-009 |
| UC-006 | Cấu hình pending_days theo Brand | Admin/Ops | Cấu hình số ngày chờ trước khi chốt commission/revenue share chính thức. | Brand cần rule chốt commission. | Brand tồn tại. | Pending rule active. | Yes | Must | FR-007 |
| UC-007 | Tạo và active Offer/content đa ngôn ngữ | Admin/Ops | Tạo Offer, nội dung hiển thị, Category, Top Brand content và bản dịch. Banner Management thuộc Deferred/Phase 2. | Campaign/offer sẵn sàng. | Brand Active. | Offer được Active hoặc lưu Draft. | Yes | Must | FR-012, FR-014, BRULE-021 |
| UC-008 | Cấu hình Brand/Offer hiển thị theo Tenant | Admin/Ops, Tenant Admin | Admin/Ops assign/unassign Brand/Offer vào pool; Tenant bật/tắt visibility trong pool. Mặc định ẩn nếu chưa assign active; mặc định visible nếu đã assign active và Tenant chưa thao tác. | Có phê duyệt commercial/legal giữa Tenant và Brand. | Tenant và Brand/Offer tồn tại. | Assignment active/inactive, Tenant visibility visible/hidden, catalog Tenant được cập nhật theo rule AND. | Yes | Must | FR-013, FR-015, BRULE-024 |
| UC-009 | Cấu hình cashback tầng 2 cho Tenant | Admin/Ops | Deferred sau MVP1; MVP1 không cấu hình B1, point conversion hoặc disbursement cho End user. | Phase sau khi bật automatic cashback. | Không áp dụng MVP1. | Không áp dụng MVP1. | No | Deferred | FR-004, FR-016, FR-022, FR-026 |
| UC-010 | Xem marketplace white-label | End user | Truy cập landing page marketplace theo Tenant và xem catalog Brand/Offer được phép hiển thị. | End user mở domain Tenant. | Domain/Tenant active. | Catalog theo Tenant được hiển thị. | Yes | Must | FR-014, FR-015, FR-016 |
| UC-011 | Tìm kiếm/lọc Brand/Offer | End user | Tìm Brand/Offer theo keyword, Category hoặc nhóm Top Brands. Banner không thuộc phạm vi MVP1. | End user nhập search hoặc chọn filter/category/top brand. | Catalog đã load. | Danh sách Brand/Offer được lọc đúng trong phạm vi Tenant. | Yes | Must | FR-015, FR-016 |
| UC-012 | Click Offer/Brand và redirect sang Brand | End user | Click vào Offer/Brand để sang website Brand mua hàng. Click Banner thuộc Deferred/Phase 2. | End user chọn Offer hoặc Brand hợp lệ. | Tenant active, Offer/Brand active, visibility 2 tầng pass, member context hợp lệ theo rule. | Platform tạo click_id, tracking click và redirect sang Brand. | Yes | Must | FR-017, FR-018, FR-031 |
| UC-013 | Brand báo order success | Brand System | Gửi order success sau khi End user mua hàng tại Brand. | Purchase completed tại Brand. | API credential hợp lệ; có click_id/order data. | Platform accept/reject order, tạo order pending nếu hợp lệ. | Yes | Must | FR-019..FR-022 |
| UC-014 | Brand báo cancel/refund theo Order Item | Brand System | Hoàn/hủy toàn bộ các item được chỉ định trong Order `Pending` và tính lại dữ liệu tài chính. | Brand phát sinh hoàn/hủy item. | Order tồn tại, đang `Pending`; các `item_code` match đúng Order. | Item hợp lệ chuyển `Refunded`; Order Status được tổng hợp lại. Order `Confirmed` bị từ chối và ghi Exception. | Yes | Must | FR-024 |
| UC-015 | Tra cứu Basic My Orders | End user | Xem danh sách Order cơ bản, sao chép Brand Order ID và xem chi tiết item; không hiển thị Cashback/Point. | End user chọn `Đơn hàng của tôi`. | Tenant Active và có `member_ref/user_ref` hoặc session context hợp lệ từ app Tenant. | Danh sách/chi tiết Order thuộc đúng Tenant và End User được hiển thị. | Yes | Must | FR-023, BRULE-017 |
| UC-016 | Finalize order đủ điều kiện | Affiliate Platform | Sau n ngày pending, xác nhận đơn không hoàn/hủy để chốt commission/revenue share chính thức. | pending_until reached. | Pending order tồn tại. | Commission/revenue share chuyển từ tạm tính sang chính thức hoặc order bị hủy/hoàn. | Yes | Must | FR-025 |
| UC-017 | Cộng điểm qua Tenant loyalty API | Affiliate Platform, Tenant Loyalty System | Deferred sau MVP1; MVP1 không tính điểm, không tạo Point Posting Log và không gọi Tenant Loyalty API. | Phase sau khi bật point posting. | Không áp dụng MVP1. | Không áp dụng MVP1. | No | Deferred | FR-026, FR-027 |
| UC-018 | Xem Tenant reporting | Tenant Admin | Theo dõi performance, click, conversion và doanh thu chia sẻ trong phạm vi Tenant. | Tenant Admin mở portal/reporting. | Tenant Admin authorized. | Dashboard/report scoped theo Tenant. | Yes | Must | FR-028 |
| UC-019 | Xem Admin reporting và exception | Admin/Ops | Theo dõi toàn hệ thống theo Tenant/Brand/Offer; xử lý lỗi click_id, visibility, order API, commission/revenue share. | Admin/Ops mở dashboard/report hoặc exception queue. | Admin/Ops authorized. | Dữ liệu vận hành hiển thị; exception có trạng thái xử lý. | Yes | Must | FR-029 |
| UC-020 | Reconciliation và settlement tracking | Admin/Ops, Finance | Đối soát commission/revenue share và theo dõi settlement với Brand/Tenant. | Đến settlement cycle. | Có transaction đủ điều kiện. | Settlement record/report được cập nhật. | Yes | Must | FR-030 |

## Out of scope / deferred use cases

| UC ID | Use case | Lý do defer |
|---|---|---|
| UC-D01 | Tính phí CPC billing | Scope hiện tại chỉ tracking click, không tính tiền CPC. |
| UC-D02 | Quản lý listing fee trong hệ thống | Listing fee chỉ trao đổi commercial, không đưa vào hệ thống. |
| UC-D03 | Brand portal tự cấu hình commission/cashback | MVP1 chốt Admin only. |
| UC-D04 | Batch point posting/fallback chính thức | CR-01 defer toàn bộ point posting ra sau MVP1. |
| UC-D05 | Cấu hình loyalty integration Tenant | CR-01 chốt MVP1 không gọi Tenant Loyalty API. |
| UC-D06 | Cấu hình cashback B1/point conversion | CR-01 chốt MVP1 không làm cashback B1 và không tính điểm. |
| UC-D07 | Lịch sử order/cashback End user 3 tab | CR-01 chốt deferred vì phụ thuộc cashback/point posting. |

## Notes

- Các use case UC-010 đến UC-012 cần đồng bộ với mockup landing page desktop hiện tại.
- UC-008 là use case quan trọng để đảm bảo Brand/Offer chỉ hiển thị theo từng Tenant.
- UC-003, UC-009 và UC-017 là deferred theo CR-01. UC-015 Basic My Orders thuộc MVP1; chỉ Cashback/Point History ba tab được Deferred.
- Cancel/refund event contract đã được chốt tại Order Transaction SRS; MVP1 không hỗ trợ hoàn một phần Qty của cùng item.

## Readiness

`READY_FOR_SRS`
