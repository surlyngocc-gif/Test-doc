# Functional Analysis: White-label Affiliate Marketplace Platform

## Status

`READY_FOR_MODELING`

## 1. Functional overview

Hệ thống Affiliate Marketplace Platform đóng vai trò trung gian giữa Brand/Merchant và các Tenant có hệ sinh thái loyalty. Mỗi Tenant có thể vận hành marketplace white-label trên subdomain/custom domain riêng, cho phép End user xem Brand/Offer và click sang Brand mua hàng; Platform tracking click/order, tính commission/revenue share, báo cáo và đối soát.

MVP1 bao gồm: onboarding Tenant/Brand, quản lý offer/content đa ngôn ngữ, tracking click, nhận order success từ Brand qua API real-time, tính commission/revenue share, chờ số ngày cấu hình theo Brand để chốt commission chính thức sau giai đoạn tạm tính, báo cáo và đối soát. Theo CR-01, MVP1 **không** làm cashback B1, không tính/cộng điểm cho End user và không gọi Tenant Loyalty API. Listing fee chỉ là nội dung trao đổi commercial, không đưa vào hệ thống. CPC không có tính năng tính tiền trong MVP; hệ thống chỉ tracking click để phục vụ nối order theo `click_id` và báo cáo.

## 2. Actors and user roles

| Actor | Role | Goal | Permissions | Related modules |
|---|---|---|---|---|
| Admin/Ops | Quản trị nền tảng trung gian | Vận hành Tenant, Brand, offer, rule, giao dịch, báo cáo, đối soát | Toàn quyền cấu hình và override theo quy trình vận hành | FM-001, FM-002, FM-003, FM-004, FM-005, FM-006, FM-007, FM-008, FM-009 |
| Tenant Admin | Quản trị phía Tenant | Theo dõi hiệu quả marketplace và doanh thu chia sẻ | Xem dashboard/report của Tenant; quản lý thông tin vận hành được phân quyền | FM-001, FM-007, FM-008 |
| Tenant Loyalty System | Hệ thống loyalty của Tenant | Không nhận API cộng điểm trong MVP1 | Tích hợp point posting là deferred sau MVP1 | Deferred |
| Brand/Merchant System | Hệ thống Brand | Bán hàng và gửi sự kiện order success/cancel/refund | Gửi postback/API theo contract được cấp | FM-004, FM-005 |
| End user | Khách hàng loyalty của Tenant | Xem ưu đãi và click sang Brand mua hàng | Truy cập marketplace của Tenant, click offer | FM-003, FM-004, FM-005 |

## 3. Functional modules

| Module ID | Module name | Description | Actor | Priority |
|---|---|---|---|---|
| FM-001 | Tenant management and white-label setup | Quản lý Tenant, domain, branding và ngôn ngữ | Admin/Ops, Tenant Admin | Must |
| FM-002 | Brand management | Quản lý Brand, trạng thái hợp tác, commission, thời gian chờ chốt commission và API credentials | Admin/Ops | Must |
| FM-003 | Offer and content management | Quản lý offer/category/content đa ngôn ngữ và commission rule | Admin/Ops | Must |
| FM-004 | Tenant brand visibility management | Admin cấu hình Brand/Offer vào pool được phép hiển thị; Tenant Portal bật/tắt trong pool đó | Admin/Ops, Tenant Admin | Must |
| FM-005 | Marketplace browsing and outbound click | End user xem marketplace white-label, offer, earn/cashback display text nếu Tenant cấu hình và click sang Brand | End user | Must |
| FM-006 | Tracking and order ingestion | Ghi nhận click, nhận order success từ Brand, match `click_id` và tạo transaction | Brand System, Platform | Must |
| FM-007 | Commission and revenue share calculation | Tính commission Brand→Affiliate và doanh thu chia sẻ Affiliate→Tenant; không tính/cộng điểm End user trong MVP1 | Platform | Must |
| FM-008 | Transaction management and reconciliation | Quản lý lifecycle giao dịch, hoàn/hủy, đối soát, settlement | Admin/Ops, Tenant Admin | Must |
| FM-009 | Reporting and dashboard | Báo cáo click, conversion, doanh thu, commission/revenue share và trạng thái order | Admin/Ops, Tenant Admin | Must |
| FM-010 | Localization management | Quản lý nội dung đa ngôn ngữ cho marketplace/content ngay từ MVP1 | Admin/Ops | Must |
| FM-011 | Click tracking | Ghi nhận click phục vụ order tracking/reporting; không tính phí CPC | Platform | Must |

## 4. Functional flow

### Happy path

1. Admin tạo Tenant, cấu hình white-label subdomain/custom domain, branding và ngôn ngữ.
2. Admin tạo Brand, cấu hình trạng thái hợp tác, commission, số ngày chờ chốt commission sau order success và API credentials.
3. Admin tạo offer, category, content đa ngôn ngữ và rule revenue share cho Tenant.
4. Admin cấu hình Brand/Offer được phép nằm trong pool hiển thị theo từng Tenant; mặc định Brand/Offer không hiển thị nếu chưa được assign cho Tenant.
4a. Tenant Portal cho phép Tenant bật/tắt Brand/Offer trong pool đã được Admin assign; nếu Tenant chưa thao tác thì Brand/Offer assigned active mặc định visible.
5. End user truy cập marketplace white-label của Tenant.
6. Hệ thống xác định Tenant, ngôn ngữ hiển thị và End user/member reference.
7. Hệ thống chỉ hiển thị các Brand/Offer active, còn hiệu lực và thỏa visibility 2 tầng: `assignment_status = Active` AND `tenant_visibility_status = Visible`.
8. End user xem offer và earn/cashback display text nếu Tenant cấu hình; đây chỉ là text hiển thị, không phải số điểm hệ thống tự tính.
9. End user click CTA sang Brand.
10. Hệ thống tạo Click Tracking Record, gắn tenant_id, user/member reference, brand_id, offer_id, click_id và timestamp.
11. Hệ thống redirect End user sang Brand cùng tracking parameter.
12. End user mua hàng thành công tại Brand.
13. Brand gọi API order success real-time về Affiliate Platform.
14. Platform validate API credential, payload, duplicate, click_id, offer/brand status và Tenant visibility 2 tầng.
15. Platform tạo Order/Conversion ở trạng thái pending/tạm tính.
16. Hệ thống chờ `n` ngày theo cấu hình Brand.
17. Nếu Brand báo hoàn/hủy trong thời gian chờ, order chuyển trạng thái hủy/hoàn và không chốt commission/revenue share chính thức.
18. Nếu không có hoàn/hủy, hệ thống chốt commission/revenue share chính thức từ số tạm tính.
19. Admin/Ops và Tenant Admin xem báo cáo click, conversion, commission/revenue share và settlement.

### Alternate and exception flows

| Flow | Condition | Expected behavior | Related module |
|---|---|---|---|
| A1 | Tenant domain chưa active hoặc không map được Tenant | Không hiển thị marketplace; trả lỗi domain/config | FM-001 |
| A2 | End user chưa định danh được member reference | Vẫn cho click/mua nhưng hiển thị warning rằng quyền lợi/cashback/đối chiếu theo hội viên có thể không được đảm bảo nếu chưa định danh | FM-004 |
| A3 | Brand/Offer chưa được assign cho Tenant, assignment inactive hoặc Tenant đã tắt visibility | Không hiển thị Brand/Offer; không cho click nếu truy cập trực tiếp link cũ | FM-004, FM-005 |
| A4 | Offer hết hạn/tạm dừng | Không cho click hoặc không hiển thị offer | FM-003, FM-005 |
| A5 | Brand gửi order success thiếu/sai click_id | Reject hoặc đưa vào exception queue để Ops xử lý | FM-006 |
| A6 | Brand gửi duplicate order success | Không tạo giao dịch trùng; trả response idempotent | FM-006 |
| A8 | Brand báo hoàn/hủy một hoặc nhiều item trong thời gian chờ | Item được hoàn/hủy chuyển `Refunded`; Platform tính lại Final Amount/Gross Commission/Tenant Share và tổng hợp Order Status. Chỉ khi tất cả item Refunded thì Order mới `Cancelled` | FM-008 |
| A9 | Tenant loyalty API lỗi khi cộng điểm | Không áp dụng trong MVP1 theo CR-01; point posting là deferred | Deferred |
| A10 | Nội dung thiếu bản dịch | Fallback theo ngôn ngữ mặc định hoặc không cho Active content tùy rule | FM-010 |

## 5. Functional requirements

| FR ID | Function name | Description | Priority | Actor | Trigger | Input | Processing | Output | Precondition | Postcondition | Related rule |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-001 | Tạo Tenant | Admin tạo Tenant trên platform. | Must | Admin/Ops | Onboard Tenant | Tenant name, code, contact, status | Validate uniqueness, tạo Tenant record | Tenant created | Admin có quyền | Tenant sẵn sàng cấu hình | BRULE-001 |
| FR-002 | Cấu hình white-label domain | Admin cấu hình subdomain/custom domain cho Tenant. | Must | Admin/Ops | Setup Tenant | domain, tenant_id, SSL/DNS status | Validate domain mapping và trạng thái kích hoạt | Domain active/inactive | Tenant tồn tại | Marketplace có thể resolve theo Tenant | BRULE-002 |
| FR-003 | Cấu hình branding Tenant | Admin cấu hình logo, màu sắc, theme và ngôn ngữ cho Tenant. | Must | Admin/Ops | Setup branding | branding assets, theme, locale config | Lưu cấu hình và áp dụng khi render marketplace | Tenant branding config | Tenant tồn tại | Marketplace hiển thị theo brand Tenant | BRULE-003, BRULE-021 |
| FR-004 | Cấu hình quy đổi điểm theo Tenant | Deferred sau MVP1 theo CR-01; MVP1 không tính điểm cho End user. | Deferred | Admin/Ops | Phase sau | TBD | TBD | Point conversion rule | Tenant tồn tại | Không áp dụng MVP1 | BRULE-004 |
| FR-005 | Cấu hình Tenant loyalty API | Deferred sau MVP1 theo CR-01; MVP1 không gọi Tenant Loyalty API. | Deferred | Admin/Ops | Phase sau | endpoint, auth config, retry policy | TBD | Loyalty integration config | Tenant tồn tại | Không áp dụng MVP1 | BRULE-005 |
| FR-006 | Tạo Brand | Admin tạo Brand/Merchant trên platform. | Must | Admin/Ops | Onboard Brand | Brand profile, category, status | Validate và lưu Brand | Brand created | Admin có quyền | Brand sẵn sàng cấu hình offer | BRULE-006 |
| FR-007 | Cấu hình pending_days theo Brand | Admin cấu hình số ngày chờ sau order success trước khi chốt commission/revenue share chính thức. | Must | Admin/Ops | Setup Brand rule | brand_id, pending_days | Validate số ngày hợp lệ | Brand pending rule | Brand tồn tại | Order success sẽ chờ n ngày trước khi chốt chính thức | BRULE-007 |
| FR-008 | Cấu hình commission Brand -> Affiliate | Admin cấu hình commission Brand trả Affiliate theo Category của từng Brand hoặc tùy chọn theo Offer. Commission có thể là Percentage hoặc Fixed amount theo Brand/Offer commercial terms. Offer commission là tùy chọn và không có effective period riêng; nếu Offer không có commission, order fallback sang Category/default category. Category mapping của Brand phải có đúng 1 category mặc định để fallback khi Brand không truyền hoặc không map được category ID/code. | Must | Admin/Ops | Setup commission | brand_id, affiliate_category_id/brand_category_id, is_default hoặc offer_id, commission_type, commission_value | Validate type/value, scope, exactly one active default category per Brand | Brand/Offer commission rule | Brand/Offer/Category tồn tại | Rule sẵn sàng tính `gross_commission_amount` hoặc fallback Category/default category | BRULE-008 |
| FR-009 | Cấu hình revenue share Affiliate -> Tenant | Admin cấu hình `tenant_share_rate%` Affiliate chia cho Tenant theo Brand default, hoặc override theo Category/Offer nếu cần. | Must | Admin/Ops | Setup revenue share | tenant_id, brand_id, category_id/offer_id optional, tenant_share_rate, effective period | Validate rate > 0 và <= 100; validate scope/effective period | Tenant Revenue Share Rule | Tenant và Brand/Offer tồn tại | Rule sẵn sàng tính phần chia cho Tenant | BRULE-009 |
| FR-011 | Loại trừ listing fee khỏi hệ thống | Hệ thống không quản lý/tính billing listing fee; listing fee chỉ trao đổi ở mặt commercial ngoài hệ thống. | Must | Admin/Ops | Define commercial scope | N/A | Không tạo module/bảng tính listing fee | Scope exclusion | N/A | Listing fee không xuất hiện trong report/billing hệ thống | BRULE-011 |
| FR-012 | Tạo offer/content đa ngôn ngữ | Admin tạo offer và nội dung theo các locale hỗ trợ. | Must | Admin/Ops | Activate offer | title, description, images, terms, locale content | Validate required locales và trạng thái Active | Offer Active/Draft | Brand tồn tại | Offer có thể hiển thị khi Active | BRULE-012, BRULE-021 |
| FR-013 | Cấu hình Brand/Offer visibility theo Tenant | Admin assign/unassign Brand/Offer vào pool được phép hiển thị; Tenant Portal bật/tắt hiển thị trong pool đó. | Must | Admin/Ops, Tenant Admin | Setup tenant marketplace catalog | tenant_id, brand_id, offer_id optional, assignment_status, tenant_visibility_status | Validate Tenant/Brand/Offer, lưu assignment và tenant visibility | Tenant Brand/Offer Assignment, Tenant Visibility | Tenant và Brand/Offer tồn tại | Brand/Offer có trạng thái visibility cuối cùng rõ ràng theo rule AND | BRULE-024 |
| FR-014 | Hiển thị marketplace theo Tenant | Hệ thống render marketplace white-label theo domain Tenant. | Must | Platform | End user truy cập domain | host/domain, locale | Resolve Tenant, load branding/content | Marketplace page | Domain active | End user thấy marketplace đúng Tenant | BRULE-001, BRULE-002, BRULE-003 |
| FR-015 | Hiển thị Brand/Offer theo visibility 2 tầng | Hệ thống chỉ hiển thị Brand/Offer active, còn hiệu lực, `assignment_status = Active` và `tenant_visibility_status = Visible`. | Must | Platform | Load marketplace/catalog | tenant_id, locale, assignment_status, tenant_visibility_status | Filter Brand/Offer theo rule AND và trạng thái | Tenant-specific catalog | Tenant active | EU chỉ thấy Brand/Offer được phép và đang visible | BRULE-012, BRULE-024 |
| FR-016 | Hiển thị earn/cashback display text | End user xem nội dung quyền lợi do Tenant cấu hình tại Tenant Portal, ví dụ `Nhận 20 điểm với mỗi 20.000đ chi tiêu`; đây chỉ là text hiển thị, không tự tính điểm. | Must | End user | Browse marketplace | tenant_id, offer_id, locale | Resolve display text theo Brand/Category/Offer | Offer listing/detail | Offer active và thỏa visibility 2 tầng | End user thấy display text nếu có cấu hình | BRULE-023, BRULE-024 |
| FR-017 | Ghi nhận click tracking | Hệ thống tạo click record khi End user click offer. | Must | End user/Platform | Click CTA | tenant_id, user_ref, brand_id, offer_id | Sinh click_id, lưu tracking context | Click Tracking Record | Offer active, Tenant active, visibility 2 tầng pass | Click được ghi nhận | BRULE-013, BRULE-024 |
| FR-018 | Redirect sang Brand | Hệ thống redirect End user sang URL Brand kèm tracking parameter. | Must | Platform | Click recorded | click_id, destination_url | Append tracking params và redirect | Redirect response | Click record created | End user sang Brand site | BRULE-013 |
| FR-019 | Nhận API order success từ Brand | Platform nhận sự kiện order success real-time từ Brand. | Must | Brand System | Purchase success | API payload, auth, click_id/order_id | Validate auth/schema và xử lý idempotency | Order success accepted/rejected | Brand active | Conversion được tạo hoặc reject | BRULE-014, BRULE-015 |
| FR-020 | Match click_id | Hệ thống kiểm tra order success có `click_id` tồn tại và match đúng Tenant/Brand/Offer context đã ghi nhận ở click tracking. | Must | Platform | Order success received | click_id, order_time | Tìm click record, đối chiếu Tenant/Brand/Offer và trạng thái click | Click match pass/fail | Click record tồn tại | Conversion đủ/không đủ điều kiện theo click_id | BRULE-013 |
| FR-021 | Validate Tenant visibility for conversion | Hệ thống kiểm tra Brand/Offer của click thỏa visibility 2 tầng theo rule vận hành. | Must | Platform | Order success received | tenant_id, brand_id, offer_id, click_time, order_time | Kiểm tra Admin assignment active và Tenant visibility visible hoặc historical eligibility theo policy | Visibility pass/fail | Click record tồn tại | Conversion đủ/không đủ điều kiện theo Tenant visibility | BRULE-024 |
| FR-022 | Tạo Order/Conversion pending | Hệ thống tạo order/conversion ở trạng thái pending/tạm tính sau khi order success hợp lệ. | Must | Platform | Order success valid | order data, commission data | Tính commission/revenue share tạm tính; set pending_until | Pending order/transaction | Click_id và visibility pass | Transaction chờ ngày chốt chính thức | BRULE-007, BRULE-016, BRULE-023 |
| FR-023 | Hiển thị đơn hàng/cashback của End user | Deferred sau MVP1 theo CR-01; 3 tab End user phụ thuộc cashback/point posting. | Deferred | End user | Phase sau | user/member reference, tenant_id | TBD | TBD | User được định danh | Không áp dụng MVP1 | BRULE-017 |
| FR-024 | Xử lý hoàn/hủy theo Order Item từ Brand | Hệ thống nhận event hoàn/hủy toàn bộ một hoặc nhiều item của Order Pending; MVP1 không hoàn một phần Qty trong cùng item. | Must | Brand System/Admin | Refund/cancel event | brand_id, brand_order_id, event_at, items[].item_code, reason | Validate Order/item; chuyển item hợp lệ sang Refunded; tính lại Final Amount, Gross Commission, Tenant Share; tổng hợp Order Status | Order tiếp tục Pending, chuyển Confirmed hoặc Cancelled theo trạng thái toàn bộ item | Order đang Pending và item match | Order Confirmed bị từ chối, giữ nguyên dữ liệu và ghi Exception | BRULE-018 |
| FR-025 | Job xác nhận đủ điều kiện sau thời gian chờ | Đến pending_until, hệ thống xác nhận order không hoàn/hủy để finalize commission/revenue share. | Must | Platform | Scheduled check | pending orders | Kiểm tra status và eligibility | Confirmed transaction | Order pending đến hạn | Transaction sẵn sàng settlement/reconciliation | BRULE-007, BRULE-018, BRULE-023 |
| FR-026 | Cộng điểm qua Tenant loyalty real-time API | Deferred sau MVP1 theo CR-01; MVP1 không gọi Tenant Loyalty API. | Deferred | Platform/Tenant Loyalty System | Phase sau | TBD | TBD | TBD | Không áp dụng MVP1 | Không áp dụng MVP1 | BRULE-005, BRULE-019, BRULE-023 |
| FR-027 | Chuyển đơn sang Đã hoàn điểm | Deferred sau MVP1 theo CR-01; không có trạng thái Rewarded/Đã hoàn điểm trong MVP1. | Deferred | Platform | Phase sau | TBD | TBD | TBD | Không áp dụng MVP1 | Không áp dụng MVP1 | BRULE-017 |
| FR-028 | Báo cáo Tenant | Tenant Admin xem báo cáo click, order và doanh thu chia sẻ trong phạm vi Tenant. | Must | Tenant Admin | Open portal report | tenant_id, date range | Aggregate tenant scoped metrics | Tenant dashboard/report | Tenant Admin authorized | Tenant theo dõi hiệu quả | BRULE-020 |
| FR-029 | Báo cáo Admin/Ops | Admin xem báo cáo toàn hệ thống theo Tenant/Brand/Offer, gồm commission và revenue share. | Must | Admin/Ops | Open admin report | filters | Aggregate metrics and statuses | Admin dashboard/report | Admin authorized | Ops theo dõi vận hành/đối soát | BRULE-020 |
| FR-030 | Đối soát và settlement | Admin/Ops theo dõi trạng thái giao dịch, commission, payout/settlement. | Must | Admin/Ops | Settlement cycle | transaction data | Summarize payable/receivable, mark status | Settlement report/status | Transactions exist | Sẵn sàng đối soát Brand/Tenant | BRULE-020 |
| FR-031 | Tracking click không tính CPC | Hệ thống ghi nhận click để nối order theo `click_id` và phục vụ reporting, không tính tiền CPC và không có cấu hình CPC billing. | Must | Platform | End user click offer | click event | Store click tracking record | Click metric | Offer active | Click sẵn sàng cho order tracking/report | BRULE-022 |

## 6. Business rules

| Rule ID | Rule | Applies to FR | Exception | Source |
|---|---|---|---|---|
| BRULE-001 | Mỗi marketplace request phải resolve được đúng một Tenant theo domain/subdomain. | FR-001, FR-014 | Domain chưa active thì không hiển thị marketplace | Discovery |
| BRULE-002 | Tenant white-label domain chỉ hoạt động khi cấu hình domain/DNS/SSL hợp lệ. | FR-002, FR-014 | Có thể dùng domain tạm trong môi trường test | Discovery |
| BRULE-003 | Marketplace phải hiển thị theo branding của Tenant. | FR-003, FR-014 | Fallback theme mặc định nếu thiếu optional assets | Discovery |
| BRULE-004 | Point conversion theo Tenant là deferred sau MVP1. | FR-004, FR-026 | Không áp dụng MVP1 | CR-01 |
| BRULE-005 | MVP1 không gọi Tenant loyalty API để cộng điểm. | FR-005, FR-026 | Batch/API posting đều là phase sau | CR-01 |
| BRULE-006 | Brand phải ở trạng thái Active mới được active Offer và nhận order success. | FR-006, FR-012, FR-019 | Admin có thể giữ Brand Draft/Inactive | CR-15 |
| BRULE-007 | Mỗi Brand cấu hình được số ngày chờ sau order success trước khi chốt commission/revenue share chính thức. | FR-007, FR-022, FR-025 | Nếu chưa cấu hình thì không chốt chính thức tự động | CR-01 |
| BRULE-008 | Brand trả commission cho Affiliate theo Offer nếu Offer có commission rule active; nếu Offer không có commission hoặc order không có Offer thì fallback sang Category, sau đó Default Category của Brand. Chỉ exception khi không có default category hoặc không có commission rule hợp lệ. | FR-008, FR-022, FR-030 | Brand portal không thuộc MVP | CR-24 |
| BRULE-008A | Một Brand chỉ đủ điều kiện Active/assign/ready for order commission khi có đúng 1 category active được đánh dấu mặc định. | FR-008, FR-013, FR-022 | Brand có thể được tạo ở Draft trước khi cấu hình category | User update |
| BRULE-009 | Tenant revenue share chỉ dùng `tenant_share_rate%`, tính trên `gross_commission_amount`, resolve theo thứ tự Offer -> Category -> Brand. | FR-009, FR-022, FR-030 | Không active rule nếu rate không hợp lệ | CR-02 |
| BRULE-011 | Listing fee chỉ trao đổi ở mặt commercial, không quản lý, không tính tiền và không báo cáo như một chức năng trong hệ thống. | FR-011 | Không | User update |
| BRULE-012 | Offer chỉ hiển thị khi ở trạng thái Active và trong thời gian hiệu lực. | FR-012, FR-015, FR-016, FR-017 | Không | CR-15 |
| BRULE-013 | Mỗi outbound click phải có click_id duy nhất để nối order success với click tracking trước đó. | FR-017, FR-018, FR-020 | Không | Discovery |
| BRULE-014 | Brand order success API phải được xác thực bằng credential được cấp. | FR-019 | Reject nếu auth fail | Discovery |
| BRULE-015 | Order success phải xử lý idempotent theo Brand/order_id/click_id để tránh trùng giao dịch. | FR-019 | Duplicate trả kết quả đã nhận trước đó | Analysis |
| BRULE-016 | Order success hợp lệ tạo transaction/order ở trạng thái pending/tạm tính. | FR-022 | Không | CR-01 |
| BRULE-017 | Lịch sử order/cashback End user 3 tab là deferred sau MVP1. | FR-023, FR-027 | Không áp dụng MVP1 | CR-01 |
| BRULE-018 | Cancel/Refund chỉ tự động áp dụng cho Order `Pending` theo từng item. Order `Confirmed` bị từ chối, giữ nguyên dữ liệu đã chốt và ghi Exception để Admin xử lý đối soát thủ công. | FR-024, FR-025 | Contract tại Order Transaction SRS | CR-03 |
| BRULE-019 | Không có trạng thái `Rewarded`/point posting trong MVP1. | FR-026, FR-027 | Không áp dụng MVP1 | CR-01 |
| BRULE-020 | Báo cáo phải phân quyền theo Tenant; Tenant chỉ thấy dữ liệu của chính Tenant. | FR-028, FR-029, FR-030 | Admin thấy toàn hệ thống | Analysis |
| BRULE-021 | MVP1 hỗ trợ đa ngôn ngữ ngay từ đầu, gồm `vi-VN` và `en-US`; default locale là `vi-VN`. | FR-003, FR-012, FR-014 | Thiếu bản dịch locale hiện tại thì fallback `vi-VN` | User update |
| BRULE-022 | Hệ thống chỉ tracking click; không có tính năng tính tiền CPC trong MVP hoặc scope hiện tại. | FR-017, FR-031 | Không | User update |
| BRULE-023 | Cashback B1, B1 <= B và disbursement điểm là deferred sau MVP1. MVP1 chỉ hỗ trợ earn/cashback display text do Tenant cấu hình, không tự tính/cộng điểm. | FR-004, FR-016, FR-022, FR-026 | Không áp dụng tính/cộng điểm trong MVP1 | CR-01 |
| BRULE-024 | Visibility áp dụng mô hình 2 tầng: Admin assignment pool và Tenant visibility. EU thấy Brand/Offer khi `assignment_status = Active` AND `tenant_visibility_status = Visible`; khi Tenant chưa thao tác, assigned active mặc định visible. | FR-013, FR-015, FR-016, FR-017, FR-021 | Admin có thể unassign/inactive; Tenant có thể hide trong pool | CR-09 |

## 7. Validation rules

| Rule ID | Type | Validation | Applies to | Error behavior |
|---|---|---|---|---|
| VR-001 | Input | Tenant code/domain không được trùng | Tenant setup | Không cho lưu |
| VR-002 | Business | Domain chỉ active khi DNS/SSL hợp lệ | White-label setup | Hiển thị trạng thái cấu hình chưa hoàn tất |
| VR-003 | Deferred | Point conversion rate validation không áp dụng MVP1 | Tenant point rule | Xử lý ở phase sau |
| VR-004 | Deferred | Tenant loyalty API endpoint/auth validation không áp dụng MVP1 | Loyalty integration | Xử lý ở phase sau |
| VR-005 | Input | Brand code/order identifier namespace không được trùng trong phạm vi tích hợp | Brand setup | Không cho lưu |
| VR-006 | Input | Pending days theo Brand phải là số nguyên không âm hoặc theo ngưỡng vận hành được cấu hình | Brand reward delay | Không cho lưu |
| VR-007 | Business | Tenant revenue share rule phải có `tenant_share_rate` > 0 và <= 100 theo scope Brand/Category/Offer | Rule setup | Không cho active rule |
| VR-017 | Deferred | Cashback B1 validation không áp dụng MVP1 | Cashback setup | Xử lý ở phase sau |
| VR-008 | Business | Offer Active phải có Brand Active và thời gian hiệu lực hợp lệ | Offer active | Không cho Active |
| VR-018 | Business | Brand/Offer chỉ được hiển thị trên Tenant marketplace khi có `assignment_status = Active` và `tenant_visibility_status = Visible` | Marketplace catalog | Ẩn Brand/Offer hoặc chặn click trực tiếp |
| VR-009 | Data | Nội dung đa ngôn ngữ phải đủ các field bắt buộc theo locale active | Offer/content | Không cho Active hoặc fallback theo rule |
| VR-010 | Permission | Tenant Admin chỉ truy cập dữ liệu của Tenant mình | Tenant portal/report | Trả lỗi unauthorized |
| VR-011 | Integration | Brand order success API phải pass authentication và schema validation | Order API | Reject request và log lỗi |
| VR-012 | Data | click_id trong order success phải tồn tại và chưa bị dùng sai rule idempotency | Order API | Reject hoặc đưa exception queue |
| VR-014 | Data | Duplicate Brand order_id/click_id không được tạo nhiều order | Order API | Trả response idempotent |
| VR-015 | Timing | Chỉ chốt commission/revenue share sau pending_until và order chưa bị hủy/hoàn | Commission finalization | Không chốt chính thức nếu chưa đủ điều kiện |
| VR-016 | Deferred | Tenant loyalty API response validation không áp dụng MVP1 | Point posting | Xử lý ở phase sau |

## 8. Exception flows

| Error / exception | Cause | Expected result | Recovery | Related FR |
|---|---|---|---|---|
| Không resolve được Tenant | Domain sai/chưa active | Không hiển thị marketplace | Admin kiểm tra domain/DNS/SSL | FR-002, FR-014 |
| Offer không còn hiệu lực | Offer expired/paused | Không hiển thị hoặc không cho click | Admin cập nhật offer | FR-012, FR-015 |
| Brand/Offer chưa visible với Tenant | Chưa có assignment active, assignment bị inactive hoặc Tenant visibility = Hidden | Không hiển thị trên marketplace; chặn click link trực tiếp | Admin cấu hình assignment pool hoặc Tenant bật/tắt visibility | FR-013, FR-015, FR-017 |
| Không định danh End user | Thiếu member reference từ Tenant | Vẫn cho click/mua, tạo click tracking không có member_ref nếu cần; UI warning về quyền lợi hội viên/cashback/đối chiếu có thể không được đảm bảo | Tenant cung cấp member context để gắn quyền lợi chính xác nếu user định danh | FR-016, FR-017 |
| Brand API auth fail | Credential sai/hết hạn | Reject order success | Brand/Admin cập nhật credential | FR-019 |
| Payload order success sai schema | Thiếu field bắt buộc | Reject và log lỗi | Brand gửi lại payload đúng | FR-019 |
| Duplicate order success | Brand retry hoặc gửi trùng | Không tạo order trùng | Trả response idempotent | FR-019 |
| Conversion không hợp lệ theo Tenant visibility | Click/order không thuộc assignment hợp lệ | Không ghi nhận commission/revenue share hoặc đưa exception queue | Ops kiểm tra lịch sử assignment | FR-021 |
| Brand báo hoàn/hủy | Một hoặc nhiều item của Order Pending bị hoàn/hủy toàn bộ | Chuyển item tương ứng sang `Refunded`, tính lại số tiền/commission/share và tổng hợp Order Status; chỉ tất cả item Refunded mới làm Order `Cancelled` | Ops/Tenant xem trạng thái và số liệu đã tính lại trong transaction/report | FR-024 |
| Loyalty API timeout/lỗi | Tenant API unavailable | Không áp dụng MVP1 | Xử lý ở phase sau | FR-026 |
| Thiếu bản dịch | Content chưa đủ locale | Fallback hoặc không cho Active | Admin bổ sung bản dịch | FR-012 |

## 9. Decision points

| Decision | Condition | Yes path | No path | Related rule |
|---|---|---|---|---|
| Tenant domain active? | Domain/DNS/SSL hợp lệ | Render marketplace | Trả lỗi cấu hình | BRULE-002 |
| Offer active và trong hiệu lực? | Offer status/time pass | Cho hiển thị/click | Ẩn hoặc chặn click | BRULE-012 |
| Brand/Offer visible cuối cùng với Tenant? | Có `assignment_status = Active` và `tenant_visibility_status = Visible` | Hiển thị Brand/Offer và cho click | Ẩn Brand/Offer hoặc chặn direct link | BRULE-024 |
| End user có member reference? | Có user/member context | Ghi nhận click/order kèm user_id/member_ref nếu có | Vẫn cho click/mua, hiển thị warning quyền lợi nếu chưa định danh và ghi nhận click thiếu member_ref | BRULE-013 |
| Order success authenticated? | API credential hợp lệ | Validate payload | Reject request | BRULE-014 |
| Order success duplicate? | Trùng Brand order_id/click_id | Trả response idempotent | Tạo order mới nếu hợp lệ | BRULE-015 |
| Đã đến ngày xác nhận sau thời gian chờ? | current date >= pending_until | Kiểm tra hoàn/hủy | Giữ Chờ xử lý | BRULE-007 |
| Cancel/refund item hợp lệ? | Event đến khi Order Pending và match toàn bộ item yêu cầu | Chuyển item sang `Refunded`, tính lại dữ liệu và tổng hợp Order Status | Giữ nguyên dữ liệu, ghi Exception nếu event không hợp lệ; Order Confirmed không tự động điều chỉnh | BRULE-018 |
| Tất cả item đã Refunded? | Mọi item của Order đều `Refunded` | Order chuyển `Cancelled` | Nếu còn item Pending thì Order `Pending`; nếu các item còn lại đều Confirmed thì Order `Confirmed` | BRULE-018 |
| Tenant có cấu hình earn/cashback display text? | Có text theo Brand/Category/Offer | Hiển thị text trên landing page | Không hiển thị text quyền lợi | BRULE-023 |
| Tenant loyalty API cộng điểm thành công? | Deferred sau MVP1 | Không áp dụng | Không áp dụng | BRULE-019 |

## 10. Data objects

| Object | Description | Created | Read | Updated | Deleted | Related FR |
|---|---|---:|---:|---:|---:|---|
| Tenant | Đối tác sở hữu marketplace white-label | Yes | Yes | Yes | TBD | FR-001, FR-014 |
| Tenant Domain | Domain/subdomain white-label của Tenant | Yes | Yes | Yes | TBD | FR-002, FR-014 |
| Tenant Branding Config | Logo, theme, locale config | Yes | Yes | Yes | TBD | FR-003, FR-014 |
| Tenant Loyalty Integration | Deferred sau MVP1, không cấu hình/call API trong MVP1 | No | No | No | No | FR-005, FR-026 |
| Point Conversion Rule | Deferred sau MVP1, không quy đổi điểm trong MVP1 | No | No | No | No | FR-004, FR-016, FR-026 |
| Brand | Thông tin Brand/Merchant | Yes | Yes | Yes | TBD | FR-006, FR-019 |
| Brand Commission Rule | Commission Brand trả Affiliate theo Category/Offer và thời gian hiệu lực; Category rule có cờ `is_default` để fallback khi Brand không truyền category ID/code | Yes | Yes | Yes | TBD | FR-008, FR-022 |
| Tenant Revenue Share Rule | Rule Affiliate chia cho Tenant theo Brand/Category/Offer | Yes | Yes | Yes | TBD | FR-009, FR-022, FR-030 |
| Offer | Ưu đãi/campaign hiển thị trên marketplace | Yes | Yes | Yes | TBD | FR-012, FR-015, FR-016 |
| Tenant Brand/Offer Assignment + Tenant Visibility | Cấu hình pool Brand/Offer được phép hiển thị và trạng thái Tenant bật/tắt trong pool | Yes | Yes | Yes | TBD | FR-013, FR-015, FR-017, FR-021 |
| Localized Content | Nội dung offer/category theo ngôn ngữ | Yes | Yes | Yes | TBD | FR-012, FR-014 |
| Earn/Cashback Display Text | Text Tenant cấu hình để hiển thị quyền lợi trên landing page; không dùng để tính/cộng điểm MVP1 | Yes | Yes | Yes | TBD | FR-016 |
| Click Tracking Record | Bản ghi click outbound sang Brand | Yes | Yes | No | TBD | FR-017, FR-018, FR-020 |
| Order/Conversion | Đơn hàng/conversion được Brand gửi về | Yes | Yes | Yes | TBD | FR-019, FR-022, FR-024, FR-027 |
| Cashback Transaction | Deferred sau MVP1 | No | No | No | No | FR-022, FR-026, FR-027 |
| Point Posting Log | Deferred sau MVP1 | No | No | No | No | FR-026 |
| Settlement Record | Bản ghi đối soát/payout/receivable/payable | Yes | Yes | Yes | TBD | FR-030 |

## 11. State and status changes

| Entity | Current state | Event | Next state | Rule | Related FR |
|---|---|---|---|---|---|
| Tenant | Draft | Domain/branding/integration configured | Active | BRULE-001, BRULE-002 | FR-001, FR-002 |
| Tenant Domain | Pending Verification | DNS/SSL verified | Active | BRULE-002 | FR-002 |
| Brand | Draft | Admin activates Brand | Active | BRULE-006 | FR-006 |
| Offer | Draft | Admin activates offer | Active | BRULE-012, BRULE-021 | FR-012 |
| Offer | Active | Offer expired/paused | Inactive | BRULE-012 | FR-012 |
| Tenant Brand/Offer Assignment | Unassigned | Admin assigns Brand/Offer to Tenant | Active | BRULE-024 | FR-013 |
| Tenant Brand/Offer Assignment | Active | Admin hides/unassigns Brand/Offer from Tenant | Inactive | BRULE-024 | FR-013 |
| Click Tracking Record | Created | Redirect completed | Redirected | BRULE-013, BRULE-024 | FR-017, FR-018 |
| Order/Conversion | None | Brand sends valid order success | Pending | BRULE-016 | FR-019, FR-022 |
| Order Item | Pending | Brand reports valid full-item cancel/refund | Refunded | BRULE-018 | FR-024 |
| Order/Conversion | Pending | Cancel/refund applied, at least one item remains Pending | Pending | BRULE-018 | FR-024 |
| Order/Conversion | Pending | Cancel/refund applied, all remaining non-refunded items are Confirmed | Confirmed | BRULE-018 | FR-024 |
| Order/Conversion | Pending | Cancel/refund applied, all items are Refunded | Cancelled | BRULE-018 | FR-024 |
| Order/Conversion | Pending | pending_until reached and no cancel/refund | Confirmed | BRULE-007, BRULE-018 | FR-025 |
| Commission Calculation | Provisional | Order eligible | Official | BRULE-007, BRULE-018 | FR-025 |
| Revenue Share Calculation | Provisional | Commission official | Official | BRULE-009 | FR-025, FR-030 |
| Settlement Record | Open | Ops closes cycle | Settled | BRULE-020 | FR-030 |

## 12. Integration points

| Integration | Type | Data exchanged | Direction | Failure behavior | Related FR |
|---|---|---|---|---|---|
| Tenant domain/DNS/SSL | External system | Domain mapping, verification status | Tenant/Admin -> Platform/DNS | Domain inactive; marketplace unavailable | FR-002, FR-014 |
| Brand order success API | API | click_id, brand_order_id, order amount, currency, order time, customer/order metadata | Brand -> Platform | Reject invalid request; log error; idempotent duplicate handling | FR-019, FR-020, FR-021, FR-022 |
| Brand cancel/refund notification | API theo Order Transaction SRS | request_id, brand_id/code, brand_order_id, order_id optional, event_type, event_at, items[].item_code, reason optional | Brand -> Platform | Chỉ hoàn/hủy toàn bộ item của Order Pending; event atomically và idempotent | FR-024 |
| Tenant loyalty point posting API | Deferred | Không trao đổi dữ liệu trong MVP1 | N/A | N/A | FR-026 |
| Reporting/analytics | Analytics/database | Click, conversion, commission, tenant revenue share, settlement metrics | Platform internal | Report delay or partial data if pipeline fails | FR-028, FR-029, FR-030 |

## 13. Dependencies

- Business/commercial terms with Brands: commission Brand trả Affiliate theo Category/Offer, pending days, refund/cancel responsibility. Listing fee nằm ngoài hệ thống.
- Tenant commercial terms: revenue share Affiliate trả Tenant theo Brand/Category/Offer và settlement cycle.
- Tenant-Brand commercial/legal approval determining which Brand/Offer may appear on each Tenant marketplace.
- Tenant identity/member mapping for End user.
- Brand order success API contract and authentication.
- Brand cancel/refund đã chốt theo từng Order Item cho Order `Pending`; không hỗ trợ partial Qty.
- DNS/SSL/custom domain operation for white-label tenants.
- Localization process and translation ownership for MVP1.
- Admin/Ops process for exception queue, dispute, reconciliation and settlement.
- Privacy/data sharing consent for tracking End user, click and order data across Tenant, Platform and Brand.
- Fraud/duplicate detection policy for clicks/orders/conversions.

## 14. Assumptions

- End user có thể định danh thành loyalty member của Tenant để map với tenant member reference; nếu chưa định danh vẫn được click/mua nhưng cần warning về quyền lợi.
- Brand checkout happens outside Affiliate Platform.
- Admin/Ops configures Brand commission by Category/Offer and Tenant revenue share by `tenant_share_rate%`. Brand portal is not included in MVP1.
- Tenant có thể truyền thông quyền lợi cho End user bằng earn/cashback display text; Platform không dùng text này để tính/cộng điểm trong MVP1.
- Tenant portal is included in MVP1 for reporting/visibility.
- End user không có màn lịch sử order/cashback trong MVP1; nếu có display text thì chỉ thấy trên landing/brand/offer public.
- Commission/revenue share chỉ được chốt chính thức sau pending days và không có cancel/refund.
- Tenant Loyalty API, point conversion và cashback B1 là later phase.
- CPC billing is out of scope; click tracking remains in scope for order tracking and reporting.
- MVP1 hỗ trợ 2 locale: `vi-VN` và `en-US`; default locale là `vi-VN`.

## 15. Open questions

| Question | Blocks modeling | Blocks wireframe | Blocks SRS |
|---|---:|---:|---:|
| Brand báo hoàn/hủy bằng API riêng, cùng postback event, hay webhook event type? | No | No | Yes |
| Brand báo hoàn/hủy bằng API riêng, cùng postback event, hay webhook event type? | No | No | Yes |

## 15.1 Closed decisions

| Decision | Answer | Impact |
|---|---|---|
| Danh sách ngôn ngữ MVP1 | `vi-VN`, `en-US`; default `vi-VN`. | Content inventory, validation và QA localization theo 2 locale. |
| End user chưa định danh member reference | Được click/mua; UI warning về quyền lợi nếu chưa định danh. | Click tracking cho phép thiếu `member_ref`; order/reporting có thể thiếu mapping hội viên. |
| Settlement cycle với Brand/Tenant | Tùy hợp đồng. | Settlement config cần lưu cycle theo contract. |

## 16. Completeness score

| Dimension | Score | Reason |
|---|---:|---|
| Coverage | 8/10 | Core modules, actors, flow, transaction/commission lifecycle, reports và integrations đã rõ; còn chi tiết refund API và locale list. |
| Logic | 9/10 | Flow order success → Pending → cancel/refund theo item hoặc chốt Confirmed đã rõ; Order Confirmed nhận cancel/refund bị ghi Exception. |
| Risk | 7/10 | Các rủi ro lớn nằm ở cross-system click/order matching, idempotency, refund/cancel, revenue share và data isolation. |
| Missing information | 7/10 | Thiếu API contract hoàn/hủy, exact locale list, member identity edge behavior và settlement cycle. |

## 17. Modeling readiness

`READY_FOR_MODELING`

Đã đủ thông tin để tạo:

- Business process model cho vận hành Brand/Tenant/End user/Admin.
- Use case model cho Admin, Tenant Admin, End user, Brand System và Affiliate Platform.
- Activity model cho click tracking, order success, pending commission, cancel/refund và chốt revenue share.
- Sequence model giữa End user, Marketplace, Brand và Affiliate Platform.
- State model cho Tenant, Brand, Offer, Tenant Brand/Offer Assignment, Order/Conversion, Commission/Revenue Share và Settlement.
- Data model cho Tenant, Brand, Offer, Tenant Brand/Offer Assignment, Click, Order, Commission/Revenue Share và Settlement.
- Integration context model cho Brand API, domain/DNS và reporting.
