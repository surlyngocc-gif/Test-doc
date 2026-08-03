# BRD: White-label Affiliate Marketplace Platform

## Document control

- Status: Draft
- Owner: TBD
- Business owner: TBD
- Stakeholders: Business, Partnership, Product, Operations, Tenant Success, Finance, Legal/Compliance, Engineering, QA
- Last updated: 2026-07-23

## Executive summary

Doanh nghiệp cần xây dựng một white-label Affiliate Marketplace Platform đóng vai trò trung gian giữa Brand/Merchant và các Tenant có hệ sinh thái loyalty. Platform giúp Brand tiếp cận tập khách hàng trung thành của nhiều Tenant, giúp Tenant mở rộng giá trị hệ sinh thái và tạo doanh thu từ commission, đồng thời cho phép End user xem ưu đãi và click sang Brand để mua hàng.

MVP1 tập trung vào marketplace theo Tenant, cấu hình Brand/Offer hiển thị theo Tenant, tracking click, nhận order success từ Brand qua API real-time, tính commission/revenue share, chờ số ngày theo Brand để chốt commission chính thức sau giai đoạn tạm tính, báo cáo và đối soát. MVP1 **không** làm cashback B1, không tính/cộng điểm cho End user và không gọi Tenant Loyalty API; các nội dung earn/cashback nếu có chỉ là text hiển thị do Tenant cấu hình. Listing fee chỉ trao đổi ở mặt commercial, không đưa vào hệ thống. CPC không tính tiền trong scope hiện tại; hệ thống chỉ tracking click phục vụ order tracking và reporting.

## Business background

### Current situation

Các Tenant có tập khách hàng loyalty lớn nhưng muốn mở rộng giá trị hệ sinh thái mà không phải tự tích hợp từng Brand riêng lẻ. Brand/Merchant có nhu cầu bán hàng online và tiếp cận khách hàng trung thành qua nhiều kênh đối tác. Nếu không có platform trung gian, mỗi quan hệ Tenant-Brand sẽ cần tích hợp, vận hành, tracking, đối soát và chính sách cashback riêng, dẫn đến chi phí vận hành cao và khó mở rộng.

### Business problem or opportunity

Platform tạo một mô hình marketplace affiliate multi-tenant, trong đó:

- Brand trả commission cho Affiliate Platform theo cấu hình Category/Offer.
- Affiliate Platform chia một phần commission cho Tenant theo cấu hình revenue share.
- Tenant có thể tự quyết định chính sách truyền thông/hoàn thưởng với End user ngoài phạm vi tính/cộng điểm tự động của MVP1.
- Platform hỗ trợ cấu hình earn/cashback display text để hiển thị cho End user, nhưng không dùng text này để tính/cộng điểm trong MVP1.

Cơ hội kinh doanh là tạo một lớp trung gian chuẩn hóa onboarding Brand/Tenant, quản lý offer, tracking click/order, commission, revenue share, reporting và đối soát, từ đó tăng khả năng scale mạng lưới đối tác.

### Evidence

- Discovery and analysis đã xác định 4 nhóm actor chính: Brand/Merchant, Tenant, End user, Admin/Ops.
- Functional analysis đã ở trạng thái `READY_FOR_MODELING`.
- Modeling output đã ở trạng thái `READY_FOR_WIREFRAME`.
- Người dùng đã chốt các quyết định chính: MVP1 không làm cashback B1/point posting/Tenant Loyalty API, Tenant integration bằng white-label subdomain/custom domain, Brand order success API real-time, đa ngôn ngữ trong MVP1, CPC chỉ tracking, listing fee ngoài hệ thống, commission/revenue share.

## Business objectives and success metrics

| Objective | Metric | Baseline | Target | Measurement window |
|---|---|---:|---:|---|
| Tăng nguồn doanh thu qua affiliate partnership | Affiliate keep amount sau khi chia revenue share cho Tenant | TBD | TBD | Monthly/Quarterly |
| Mở rộng mạng lưới Tenant sử dụng marketplace | Số Tenant active | 0 | TBD | Monthly |
| Mở rộng nguồn cung ưu đãi cho Tenant | Số Brand/Offer active và assigned theo Tenant | 0 | TBD | Monthly |
| Tăng tương tác End user với marketplace | Click-through rate, số click hợp lệ | 0 | TBD | Weekly/Monthly |
| Tăng giao dịch được ghi nhận | Conversion count, conversion rate, GMV tracked | 0 | TBD | Monthly |
| Đảm bảo tính đúng commission/revenue share | Reconciliation accuracy, duplicate/error rate | TBD | TBD | Settlement cycle |
| Đảm bảo vận hành order tracking | Order ingestion success rate, duplicate/error rate | TBD | TBD | Daily/Monthly |

## Stakeholders

| Stakeholder | Role | Interest / concern | Approval required |
|---|---|---|---|
| Business Owner | Chủ sở hữu mục tiêu kinh doanh | Revenue model, go-to-market, KPI | Yes |
| Partnership / Commercial | Quản lý quan hệ Brand/Tenant | Hợp đồng Brand commission, Tenant revenue share, Brand visibility theo Tenant | Yes |
| Product | Quản lý phạm vi sản phẩm | Scope MVP1, roadmap, trải nghiệm Tenant/EU/Admin | Yes |
| Admin/Ops | Vận hành platform | Onboarding, cấu hình, exception, đối soát | Yes |
| Tenant Success | Hỗ trợ Tenant | Tenant setup, reporting, cấu hình hiển thị marketplace | Yes |
| Finance | Đối soát và settlement | Commission, payout, settlement cycle | Yes |
| Legal/Compliance | Pháp lý, dữ liệu, tracking consent | Commercial approval, privacy, data sharing | Yes |
| Engineering | Xây dựng hệ thống | Feasibility, architecture, integration constraints | No |
| QA | Kiểm thử nghiệp vụ | Testability, acceptance criteria, edge cases | No |

## Current business process

Hiện tại chưa có platform trung gian được mô tả trong repository. Quy trình giả định nếu không có platform:

1. Tenant và Brand đàm phán riêng từng hợp đồng.
2. Mỗi Tenant/Brand cần thỏa thuận cách hiển thị offer, tracking, commission, revenue share, hoàn/hủy và đối soát.
3. Mỗi quan hệ tích hợp cần luồng tracking và báo cáo riêng.
4. Việc hoàn thưởng/cộng điểm cho End user phụ thuộc vào chính sách riêng của từng Tenant và nằm ngoài phạm vi tự động hóa MVP1.
5. Operations phải xử lý thủ công hoặc bán thủ công các vấn đề về click/order matching, duplicate, refund/cancel và settlement.

## Proposed business process

1. Admin/Ops tạo Tenant và cấu hình white-label domain, branding, locale.
2. Admin/Ops tạo Brand và cấu hình commission, số ngày chờ chốt commission sau order success, API credentials.
3. Admin/Ops tạo Offer/content đa ngôn ngữ và commission rule.
4. Admin/Ops cấu hình Brand/Offer được phép nằm trong pool hiển thị theo từng Tenant. Mặc định Brand/Offer ẩn nếu chưa được assign active.
5. Tenant bật/tắt hiển thị Brand/Offer trong pool đã được Admin assign; nếu Tenant chưa thao tác thì Brand/Offer assigned active mặc định hiển thị.
6. End user truy cập marketplace white-label của Tenant và chỉ thấy các Brand/Offer active, còn hiệu lực, thỏa đồng thời `assignment_status = Active` và `tenant_visibility_status = Visible`.
6. End user click offer; platform tracking click và redirect sang Brand.
7. End user mua hàng tại Brand; Brand gửi order success qua API real-time.
8. Platform validate auth, payload, duplicate, click_id, visibility assignment và tạo order ở trạng thái `Chờ xử lý`.
9. Platform chờ `n` ngày theo cấu hình Brand để hạn chế hoàn/hủy.
10. Cancel/Refund API chỉ điều chỉnh Order còn `Pending` và xử lý theo từng Order Item. Nếu Order đã `Confirmed`, hệ thống từ chối event, giữ nguyên dữ liệu đã chốt và ghi Exception để Admin xử lý đối soát thủ công.
11. Nếu đủ điều kiện, Platform chốt commission/revenue share chính thức từ số tạm tính.
12. Admin/Ops và Tenant Admin theo dõi báo cáo, exception, reconciliation và settlement.

## Phạm vi

### Trong phạm vi

- Marketplace white-label responsive, hỗ trợ multi-tenant.
- Subdomain/custom domain theo từng Tenant.
- Branding theo Tenant và hỗ trợ locale cơ bản cho yêu cầu đa ngôn ngữ ở MVP1.
- Onboarding Brand/Merchant.
- Quản lý Offer/content có hỗ trợ localization.
- Admin cấu hình Brand/Offer hiển thị theo từng Tenant.
- Brand/Offer mặc định bị ẩn cho đến khi assignment được active.
- Tracking click phục vụ order tracking/reporting.
- Nhận Brand order success qua API real-time.
- Xử lý sự kiện Brand cancel/refund theo từng Order Item là năng lực MVP1; contract được đặc tả tại Order Transaction SRS.
- Mô hình commission/revenue share:
  - Brand trả commission cho Affiliate theo Category hoặc Offer.
  - Affiliate chia revenue share cho Tenant theo rule cấu hình.
  - Trước ngày chốt, hệ thống ghi nhận số tạm tính; sau `pending_days`, nếu không hoàn/hủy thì chốt số chính thức.
- Báo cáo cho Tenant.
- Báo cáo Admin/Ops, xử lý exception, reconciliation và settlement tracking.

### Ngoài phạm vi

- Billing/reporting listing fee trong hệ thống.
- CPC billing hoặc tính phí CPC.
- Brand portal trong MVP1.
- Full accounting ledger.
- Checkout hoặc xử lý thanh toán của Brand bên trong Platform.
- Native mobile app như một sản phẩm riêng.
- Batch loyalty posting trong MVP1.
- Cashback B1, point conversion, tự động tính/cộng điểm cho End user và Tenant Loyalty API posting trong MVP1.
- Lịch sử order/cashback End user với 3 tab `Chờ xử lý`, `Đã hoàn điểm`, `Đã hủy` trong MVP1.

## Yêu cầu nghiệp vụ

| ID | Yêu cầu | Lý do | Độ ưu tiên | Nguồn |
|---|---|---|---|---|
| BR-001 | Platform phải hỗ trợ nhiều Tenant, mỗi Tenant có marketplace white-label theo subdomain/custom domain. | Cho phép onboarding Tenant ở quy mô lớn và giữ trải nghiệm theo thương hiệu Tenant. | Must | Discovery/Analysis |
| BR-002 | Platform phải cho phép Admin/Ops onboarding và quản lý Brand/Merchant. | Brand là nhóm đối tác cung cấp offer và giao dịch. | Must | Discovery/Analysis |
| BR-003 | Platform phải cho phép Admin/Ops tạo và quản lý Offer/content có hỗ trợ đa ngôn ngữ. | MVP1 yêu cầu marketplace content đa ngôn ngữ. | Must | User update/Analysis |
| BR-004 | Platform phải cho phép Admin/Ops cấu hình Brand/Offer được phép hiển thị theo từng Tenant; Tenant Portal cho phép Tenant bật/tắt trong pool đó. | Catalog của mỗi Tenant phụ thuộc vào phê duyệt commercial/legal và lựa chọn vận hành của Tenant. | Must | User update/Analysis/CR-09 |
| BR-005 | Brand/Offer phải mặc định ẩn khỏi Tenant nếu chưa được assign active. | Tránh hiển thị sai hoặc hiển thị khi chưa được phê duyệt. | Must | User update/BRULE-024 |
| BR-006 | Platform phải tracking outbound click để phục vụ order tracking và reporting. | Click tracking vẫn cần thiết dù CPC billing ngoài phạm vi. | Must | User update/Analysis |
| BR-007 | Platform không được tính CPC billing hoặc CPC fee. | Người dùng đã loại bỏ monetization theo CPC khỏi phạm vi. | Must | User update |
| BR-008 | Platform không quản lý billing/reporting listing fee. | Listing fee chỉ là trao đổi commercial ngoài hệ thống. | Must | User update |
| BR-009 | Platform phải nhận Brand order success qua API real-time. | Order success là trigger cho commission/revenue share flow. | Must | Discovery/Analysis |
| BR-011 | Platform phải validate visibility 2 tầng khi xử lý click/conversion: Admin assignment active và Tenant visibility visible. | Tránh ghi nhận commission cho quan hệ Tenant-Brand chưa được phép hiển thị hoặc đã bị Tenant tắt. | Must | Analysis/Modeling/CR-09 |
| BR-012 | Platform phải hỗ trợ commission Brand trả Affiliate theo Category hoặc Offer và revenue share Affiliate chia Tenant. | Đây là revenue model cốt lõi của MVP1. | Must | User update/CR-01 |
| BR-013 | Cashback B1 và chính sách Tenant chia điểm/tiền cho End user không thuộc phạm vi tính toán tự động MVP1. | CR-01 chốt MVP1 không làm cashback B1/point posting. | Deferred | CR-01 |
| BR-014 | Point conversion theo Tenant không thuộc phạm vi MVP1. | MVP1 không tính/cộng điểm cho End user. | Deferred | CR-01 |
| BR-015 | Platform phải chờ n ngày sau Brand order success trước khi chốt commission/revenue share chính thức, theo cấu hình Brand. | Giảm rủi ro chốt doanh thu cho order bị hủy/hoàn. | Must | User update/CR-01 |
| BR-016 | Platform phải ngăn chốt commission/revenue share chính thức khi Brand báo cancel/refund trước ngày chốt. | Tránh ghi nhận doanh thu sai. | Must | User update/CR-01 |
| BR-017 | Lịch sử order/cashback End user với 3 tab `Chờ xử lý`, `Đã hoàn điểm`, `Đã hủy` không thuộc MVP1. | Phụ thuộc point posting/cashback B1 đã deferred. | Deferred | CR-01 |
| BR-018 | Tenant Loyalty API posting để cộng điểm không thuộc phạm vi MVP1. | CR-01 chốt không gọi Tenant Loyalty API. | Deferred | CR-01 |
| BR-019 | Tenant Admin chỉ được xem reporting trong phạm vi Tenant của mình. | Đảm bảo data isolation và phân quyền theo Tenant. | Must | Analysis |
| BR-020 | Admin/Ops phải xem được reporting và reconciliation data trên toàn hệ thống theo Tenant/Brand/Offer. | Cần cho vận hành platform và đối soát. | Must | Analysis |
| BR-021 | Platform phải hỗ trợ xử lý exception cho order success không hợp lệ, duplicate order, lỗi click_id và lỗi visibility. | Cần kiểm soát vận hành và xử lý sai lệch. | Must | Analysis/Modeling |
| BR-022 | Platform phải giữ traceability giữa click, order, commission, revenue share và settlement records. | Hỗ trợ audit, reporting và reconciliation. | Must | Modeling |

## Quy tắc nghiệp vụ

| ID | Quy tắc | Áp dụng cho | Ngoại lệ |
|---|---|---|---|
| BRULE-001 | Marketplace request phải resolve đúng một Tenant theo domain/subdomain. | Tenant marketplace | Domain inactive trả lỗi cấu hình |
| BRULE-002 | White-label domain chỉ hoạt động khi DNS/SSL/domain config active. | Tenant setup | Có thể dùng test domain ở môi trường non-production |
| BRULE-003 | Marketplace phải render branding của Tenant. | Tenant marketplace | Chỉ fallback mặc định cho optional assets |
| BRULE-004 | Point conversion theo Tenant không được triển khai trong MVP1. | Deferred cashback/point | Xem lại ở phase sau |
| BRULE-005 | MVP1 không gọi Tenant loyalty API để cộng điểm. | Deferred point posting | Batch/API posting đều là phase sau |
| BRULE-006 | Brand phải Active mới được active Offer và nhận order success. | Brand/Offer | Brand Draft/Inactive không được go live |
| BRULE-007 | Mỗi Brand có thể cấu hình số ngày chờ trước khi chốt commission/revenue share chính thức. | Order/commission | Không chốt chính thức nếu thiếu cấu hình bắt buộc |
| BRULE-008 | Brand trả commission cho Affiliate theo cấu hình Category hoặc Offer. | Commission | Brand portal ngoài phạm vi MVP |
| BRULE-009 | Affiliate chia revenue share cho Tenant theo `tenant_share_rate%`; resolve rule theo thứ tự Offer -> Category -> Brand; không dùng mô hình phân bổ cũ trong MVP1. | Revenue share | Rule sai/thiếu thì đưa vào exception |
| BRULE-011 | Listing fee chỉ là commercial-only và không quản lý trong hệ thống. | Scope | Không |
| BRULE-012 | Offer chỉ hiển thị khi Active và còn hiệu lực. | Marketplace catalog | Không |
| BRULE-013 | Mỗi outbound click phải có click_id duy nhất. | Click tracking | Không |
| BRULE-014 | Brand order success API phải được authentication. | Brand integration | Reject khi auth fail |
| BRULE-015 | Order success phải idempotent theo Brand/order_id/click_id. | Order ingestion | Duplicate trả lại kết quả trước đó |
| BRULE-016 | Order success hợp lệ tạo transaction/order ở trạng thái pending/tạm tính. | Order lifecycle | Không |
| BRULE-017 | Lịch sử order/cashback End user 3 tab là deferred sau MVP1. | End-user visibility | Không áp dụng MVP1 |
| BRULE-018 | Cancel/Refund hợp lệ chỉ áp dụng cho Order `Pending`: item trong event chuyển `Refunded`, các giá trị tài chính được tính lại và Order Status được tổng hợp từ toàn bộ item. Order `Confirmed` bị từ chối, giữ nguyên dữ liệu và ghi Exception để xử lý đối soát thủ công. | Order/commission | Contract tại Order Transaction SRS |
| BRULE-019 | Không có trạng thái `Rewarded`/point posting trong MVP1. | Deferred point posting | Không áp dụng MVP1 |
| BRULE-020 | Tenant reporting chỉ scoped theo Tenant; Admin/Ops xem được toàn bộ. | Reporting | Không |
| BRULE-021 | MVP1 hỗ trợ đa ngôn ngữ gồm tiếng Việt và tiếng Anh: `vi-VN`, `en-US`. | Marketplace/content | Default locale `vi-VN`; thiếu bản dịch thì fallback `vi-VN` |
| BRULE-022 | Platform tracking click nhưng không tính CPC billing. | Click tracking | Không |
| BRULE-023 | Cashback B1, B1 <= B và disbursement điểm là deferred sau MVP1. | Deferred cashback policy | MVP1 chỉ hỗ trợ earn/cashback display text nếu Tenant cấu hình |
| BRULE-024 | Visibility áp dụng mô hình 2 tầng: Admin/Ops assign Brand/Offer vào pool, Tenant bật/tắt trong pool; hiển thị cuối cùng khi `assignment_status = Active` AND `tenant_visibility_status = Visible`. Nếu Tenant chưa thao tác thì Brand/Offer assigned active mặc định visible. | Tenant marketplace catalog | Admin có thể assign/unassign; Tenant có thể hide trong pool |

## Nhu cầu reporting và analytics

| Báo cáo / metric | Người xem | Mục đích | Chiều dữ liệu chính |
|---|---|---|---|
| Hiệu quả Tenant marketplace | Tenant Admin, Admin/Ops | Theo dõi hiệu quả từng Tenant | Tenant, Brand, Offer, ngày, locale |
| Click report | Tenant Admin, Admin/Ops | Theo dõi engagement outbound và dữ liệu click tracking | Tenant, Brand, Offer, click_id, ngày |
| Conversion report | Tenant Admin, Admin/Ops | Theo dõi order thành công và conversion rate | Tenant, Brand, Offer, order status, ngày |
| Commission/revenue share report | Admin/Ops, Finance | Theo dõi commission Brand→Affiliate và doanh thu chia sẻ Tenant | Tenant, Brand, Offer, transaction, settlement cycle |
| Exception report | Admin/Ops | Xử lý invalid API, duplicate, click_id invalid, visibility fail, commission/revenue share calculation fail | Error type, Brand, Tenant, timestamp |
| Settlement report | Admin/Ops, Finance | Hỗ trợ reconciliation và theo dõi payable/receivable | Settlement cycle, Tenant, Brand, commission/revenue share |

## Tác động vận hành

### Con người

- Admin/Ops cần quản lý Tenant setup, Brand setup, Offer activation, Tenant-specific Brand/Offer visibility, commission rules và exception queues.
- Tenant Success cần điều phối Tenant onboarding, domain readiness, cấu hình hiển thị marketplace và quyền truy cập reporting.
- Partnership/Commercial cần cung cấp phê duyệt Tenant-Brand visibility và commission terms.
- Finance cần vận hành settlement cycles và reconcile commission/revenue share.

### Quy trình

- Cần bước phê duyệt commercial/legal cho quan hệ Tenant-Brand trước khi Brand/Offer assignment active cho Tenant.
- Brand order success integration phải được test trước khi Brand/Offer go live.
- Cancel/refund theo item được tự động hóa trong MVP1 cho Order `Pending`; event của Order `Confirmed` được ghi Exception để xử lý đối soát thủ công.

### Chính sách

- Brand/Offer visibility mặc định là hidden nếu chưa được assign active.
- Không hỗ trợ CPC billing.
- Listing fee không được ghi nhận trong hệ thống.
- Cashback B1/point posting không thuộc MVP1; nếu Tenant muốn hoàn thưởng cho End user thì xử lý ngoài Platform hoặc phase sau.

### Hỗ trợ / đào tạo

- Admin/Ops cần được đào tạo về Tenant/Brand setup, visibility assignment, commission configuration, exception handling và settlement review.
- Tenant Admin cần được đào tạo cách đọc dashboard/report.
- Đội tích hợp Brand phải hướng dẫn onboarding Order Success và Cancel/Refund API theo contract trong Order Transaction SRS.

## Acceptance criteria

### AC-001 — Hiển thị marketplace theo Tenant (BR-004, BR-005)

- Cho biết Brand/Offer đang active nhưng chưa được assign cho Tenant A
- Khi End user mở marketplace của Tenant A
- Thì Brand/Offer không được hiển thị và direct click access bị chặn

### AC-002 — Click tracking không có CPC billing (BR-006, BR-007)

- Cho biết End user click một Offer active đã được assign
- Khi Platform tạo click tracking record
- Thì click_id được lưu để phục vụ order tracking/reporting
- Và không phát sinh CPC billing amount

### AC-003 — Commission/revenue share MVP1 (BR-012)

- Cho biết Brand commission rule và Tenant revenue share rule đã được cấu hình
- Khi một conversion hợp lệ được accepted
- Thì Platform tính commission Brand trả Affiliate
- Và tính phần Affiliate chia Tenant theo rule Brand default hoặc override Category/Offer nếu có

### AC-004 — Deferred cashback/point posting (BR-013, BR-014, BR-018)

- Cho biết đang ở phạm vi MVP1
- Khi một order đủ điều kiện được chốt commission/revenue share
- Thì hệ thống không tạo cashback B1, không tính điểm và không gọi Tenant Loyalty API

### AC-005 — Pending days và cancel/refund (BR-015, BR-016)

- Cho biết Brand order success đã được accepted
- Khi order vẫn còn trong pending days đã cấu hình
- Thì order giữ trạng thái `Chờ xử lý`
- Và nếu Brand báo cancel/refund trước ngày chốt, order chuyển trạng thái hủy/hoàn và không chốt commission/revenue share chính thức

### AC-006 — Tenant Loyalty API không được gọi trong MVP1 (BR-018)

- Cho biết order đủ điều kiện và đã hết pending days
- Khi hệ thống chốt commission/revenue share chính thức
- Thì không phát sinh request cộng điểm sang Tenant Loyalty API
- Và không sinh trạng thái `Đã hoàn điểm` trong MVP1

### AC-007 — Reporting scoped theo Tenant (BR-019)

- Cho biết Tenant Admin mở reporting
- Khi report được tải
- Thì Tenant Admin chỉ thấy dữ liệu thuộc Tenant của mình

## Dependencies và constraints

- Tenant white-label domain, DNS và SSL setup.
- Brand order success API contract và authentication.
- Cơ chế Brand cancel/refund đã chốt theo từng Order Item; không hỗ trợ hoàn một phần Qty của cùng item trong MVP1.
- Phê duyệt commercial/legal giữa Tenant-Brand cho visibility assignment.
- Commission và revenue share terms.
- Quy trình content đa ngôn ngữ và translation cho MVP1.
- Data privacy, tracking consent và data sharing terms giữa Tenant, Platform và Brand.
- Quy trình vận hành cho exception queue, retry, reconciliation và settlement.

## Rủi ro và phương án giảm thiểu

| Rủi ro | Tác động | Khả năng xảy ra | Giảm thiểu |
|---|---|---:|---|
| Brand/Offer hiển thị sai Tenant | Vi phạm commercial/legal và sai click/order tracking | Medium | Mặc định hidden; yêu cầu active Tenant Brand/Offer Assignment |
| Brand gửi order event không hợp lệ hoặc duplicate | Sai commission/revenue share | High | Auth, schema validation, idempotency theo Brand/order_id/click_id |
| Brand gửi cancel/refund trễ sau khi Order đã Confirmed | Dữ liệu đã chốt không được tự động điều chỉnh | Medium | Từ chối API, giữ nguyên Transaction và ghi Exception để Admin xử lý đối soát thủ công |
| Cấu hình revenue share sai | Sai phân bổ doanh thu Affiliate/Tenant | Medium | Validate rule trước khi active |
| Thiếu locale content | Trải nghiệm marketplace không đầy đủ | Medium | Locale validation/fallback policy |
| End user chưa định danh | Không thể gắn giao dịch với member_ref để Tenant đối chiếu quyền lợi hội viên | Medium | Cho phép click/mua nhưng hiển thị warning về quyền lợi nếu chưa định danh |
| Rò rỉ dữ liệu giữa các Tenant | Ảnh hưởng nghiêm trọng tới niềm tin/compliance | Low/Medium | Phân quyền và reporting scoped theo Tenant |

## Giả định

- End user có thể là loyalty member của Tenant và có thể map với Tenant member reference nếu đã định danh. Nếu chưa định danh, End user vẫn được click/mua nhưng cần được warning rằng quyền lợi/cashback/đối chiếu theo hội viên có thể không được đảm bảo.
- Brand checkout diễn ra ngoài Platform.
- Admin/Ops cấu hình Brand commission và Tenant revenue share.
- Brand portal không thuộc MVP1.
- Tenant portal thuộc MVP1 cho reporting/visibility.
- Cashback B1, point conversion, point posting và order/cashback history End user là phase sau MVP1.

## Câu hỏi mở

| Câu hỏi | Owner | Tác động |
|---|---|---|
| Brand báo hoàn/hủy bằng API riêng, cùng postback event, hay webhook event type? | Product/Engineering/Brand Partnership | Chặn SRS/API contract chi tiết |

## Quyết định đã chốt

| Nội dung | Quyết định | Tác động |
|---|---|---|
| Ngôn ngữ MVP1 | Hỗ trợ tiếng Việt và tiếng Anh: `vi-VN`, `en-US`; default `vi-VN`. | Content, QA và fallback locale phải kiểm tra theo 2 locale này. |
| End user chưa định danh member reference | Vẫn được click/mua; landing page cần warning rằng quyền lợi/cashback/đối chiếu theo hội viên có thể không được đảm bảo nếu chưa định danh. | Click tracking cho phép thiếu `member_ref`; order/reporting có thể thiếu user/member mapping. |
| Settlement cycle Brand/Tenant | Theo từng hợp đồng. | Settlement/reconciliation cần lưu cấu hình cycle theo contract thay vì hard-code tháng/quý. |

## Phê duyệt

| Tên | Vai trò | Trạng thái | Ngày |
|---|---|---|---|
| TBD | Business Owner | Pending | TBD |
| TBD | Product Owner | Pending | TBD |
| TBD | Partnership Lead | Pending | TBD |
| TBD | Operations Lead | Pending | TBD |
| TBD | Finance Lead | Pending | TBD |
| TBD | Legal/Compliance | Pending | TBD |

## Bằng chứng repository

- [Functional Analysis: Affiliate Marketplace Platform](../analysis/affiliate-marketplace-platform-analysis.md)
- [Modeling Specification: Affiliate Marketplace Platform](../modeling/affiliate-marketplace-platform-modeling.md)
- [.BASkill requirements-authoring skill](../../.BASkill/skills/requirements-authoring/SKILL.md)
- [.BASkill BRD template](../../.BASkill/skills/requirements-authoring/references/brd-template.md)
