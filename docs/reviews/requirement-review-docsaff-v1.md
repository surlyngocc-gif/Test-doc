# BÁO CÁO REVIEW YÊU CẦU — AFFILIATE MARKETPLACE PLATFORM

## Thông tin báo cáo

| Thuộc tính | Giá trị |
|---|---|
| Phạm vi review | Toàn bộ tài liệu tại `docs/requirements/docsaff_v1` |
| Đường dẫn người dùng yêu cầu | `docs/requirements/docsaff` — không tồn tại; báo cáo sử dụng thư mục thực tế `docsaff_v1` |
| Ngày review | 31/07/2026 |
| Vai trò review | Senior QA Lead |
| Mục tiêu | Đánh giá toàn bộ luồng hệ thống, độ đầy đủ, tính nhất quán, khả năng kiểm thử và mức sẵn sàng cho QA |
| Ngoài phạm vi | Không tạo Test Plan, Test Scenario hoặc Test Case |

## 1. Requirement Summary

### 1.1 Tổng quan sản phẩm

Affiliate Marketplace Platform là nền tảng affiliate đa Tenant, cung cấp:

- Marketplace white-label theo domain/subdomain và branding của từng Tenant.
- CMS cho Platform Admin/Ops quản lý Tenant, Brand, Category, Offer, commission, revenue share, giao dịch, exception, reporting, reconciliation và audit.
- Tenant Portal cho người dùng phía Tenant quản lý tài khoản, quyền, Brand/Offer visibility, Earn Display, dashboard và giao dịch trong đúng Tenant scope.
- Landing Page cho End User duyệt Brand/Offer, click chuyển sang Brand và tra cứu Basic My Orders.
- API/worker xử lý click attribution, Order Success, Cancel/Refund, tính commission và finalize Order.

MVP1 không tính Cashback B1, không quy đổi/cộng điểm, không gọi Tenant Loyalty API và không tạo trạng thái Rewarded/Point Posting.

### 1.2 Mục tiêu nghiệp vụ

- Onboard nhiều Tenant với trải nghiệm marketplace mang thương hiệu riêng.
- Phân phối Brand/Offer đúng phạm vi commercial/legal của từng Tenant.
- Theo dõi click và quy kết Order từ Brand theo `click_id`.
- Tính commission Brand → Affiliate và Tenant revenue share chính xác.
- Cung cấp số liệu tạm tính/chính thức, exception handling và đối soát có thể audit.
- Bảo đảm tenant isolation, RBAC và bảo vệ dữ liệu nhạy cảm.

### 1.3 Actor và vai trò

| Actor/Vai trò | Trách nhiệm chính |
|---|---|
| Platform Admin/Ops | Quản trị Tenant, Brand, Category, Offer, assignment, commission, revenue share, transaction, exception và audit |
| Platform Finance | Reporting, reconciliation, settlement, adjustment và export |
| Tenant Admin | Quản lý user, assigned Brand/Offer, Earn Display và dữ liệu Tenant theo quyền |
| Tenant Marketing/Ops | Vận hành visibility và Earn Display theo permission matrix |
| Tenant Finance | Xem dashboard, transaction và export theo quyền |
| Tenant Viewer | Chỉ xem các module được cấp quyền |
| End User | Duyệt marketplace, click Brand/Offer và tra cứu Basic My Orders |
| Brand System | Gửi Order Success và Cancel/Refund event |
| Platform Backend/Worker | Validate, match click, tính commission, finalize và ghi exception/audit |
| Tenant Loyalty System | Deferred sau MVP1 |

### 1.4 Artefact đã review

Đã kiểm tra 212 file:

- 19 file Markdown nghiệp vụ/đặc tả.
- 10 SRS cấp module và 1 SRS tổng.
- 41 HTML mockup và 1 CSS.
- 44 SVG/PUML mô tả logic/model.
- 99 PNG mockup/reference.
- 3 XLSX mẫu export.
- 4 file lock tạm `.~lock*.md#`; đây không phải requirement hợp lệ và nên loại khỏi repository.

## 2. Toàn bộ luồng hệ thống

### 2.1 Luồng A — Onboard Tenant và kích hoạt white-label marketplace

1. Platform Admin/Ops tạo Tenant với mã, tên, contact và trạng thái.
2. Hệ thống kiểm tra mã Tenant duy nhất và ghi Audit Log.
3. Admin cấu hình domain/subdomain, DNS/SSL, branding và locale.
4. Khi Tenant được kích hoạt, hệ thống tạo bốn System Role Tenant Portal theo permission matrix.
5. Admin tạo Tenant Portal Admin đầu tiên và gán role hợp lệ cùng Tenant.
6. Tenant chỉ sẵn sàng public khi Tenant, domain và cấu hình bắt buộc đều hợp lệ.
7. Request Landing Page resolve đúng một Tenant từ host/domain; domain không hợp lệ hoặc inactive phải trả trạng thái lỗi cấu hình, không render catalog.

**Điểm chưa đủ:** Chưa có contract đầy đủ cho domain verification, certificate lifecycle, custom-domain conflict, cache invalidation và hành vi khi DNS/SSL đang pending.

### 2.2 Luồng B — Quản lý Category, Brand và Offer

1. Admin tạo Category dùng chung, nội dung `vi-VN`/`en-US`, icon và trạng thái.
2. Admin tạo Brand ở Draft/Inactive, cấu hình content đa ngôn ngữ, destination/integration metadata và `pending_days`.
3. Admin map category phía Brand với Category platform, cấu hình commission và chọn đúng một default category active.
4. Brand chỉ đủ điều kiện Active/assign/nhận Order khi có đúng một default category active.
5. Admin tạo Offer thuộc Brand; Offer commission là tùy chọn.
6. Offer có thể Active khi Brand Active, destination URL hợp lệ, content locale mặc định đầy đủ và thời gian hiệu lực hợp lệ.
7. Nếu Order Item có `brand_offer_code` hợp lệ, hệ thống dùng Offer commission; nếu không, fallback Category rồi default category của Brand.
8. Thay đổi Brand/Offer/Category/commission phải dùng optimistic locking và ghi Audit Log.

**Điểm chưa đủ:** Policy sửa Category code/Brand code sau khi có dependency, bulk import và vòng đời asset/icon vẫn còn mở.

### 2.3 Luồng C — Assign Brand/Offer và visibility hai tầng

1. Platform Admin/Ops assign Brand/Offer vào pool được phép của Tenant.
2. Assignment tầng Platform dùng `assignment_status`.
3. Tenant User có quyền chỉ thấy và thao tác trong pool đã assign.
4. Tenant bật/tắt `tenant_visibility_status`.
5. Khi Tenant chưa thao tác, assignment Active mặc định Visible.
6. End User chỉ thấy Brand/Offer khi đồng thời:
   - Tenant Active.
   - Brand Active.
   - Offer Active và còn hiệu lực, nếu là Offer.
   - `assignment_status = Active`.
   - `tenant_visibility_status = Visible`.
7. API click trực tiếp phải kiểm tra lại cùng rule; không chỉ dựa vào việc UI đã ẩn CTA.

**Điểm chưa đủ:** Chưa chốt chính sách historical eligibility khi visibility thay đổi giữa thời điểm click và Order Success.

### 2.4 Luồng D — Tenant Portal authentication, RBAC và account

1. Tenant User đăng nhập bằng username/password.
2. Backend xác định Tenant, trạng thái User, trạng thái Role và permission.
3. Đăng nhập sai liên tiếp lần thứ 5 chuyển tài khoản sang `Locked`, thu hồi session/token và ghi log.
4. Chỉ Tenant Admin có permission phù hợp được unlock.
5. Forgot Password gửi OTP, kiểm tra hạn dùng/số lần thử, cho đặt mật khẩu mới và vô hiệu hóa session cũ.
6. Tenant Admin quản lý user cùng `tenant_id`, gán đúng một Role Active.
7. System Role không được xóa, inactive hoặc sửa permission.
8. Custom Role và thay đổi Permission có dấu hiệu được mô tả chi tiết trong SRS/HTML nhưng Function List lại đặt Custom Role ở Deferred/Phase 2.
9. Mọi API lấy `tenant_id` từ session/token; tham số client không được mở rộng Tenant scope.

**Điểm chưa đủ:** Password policy, OTP resend/rate limit, session TTL, refresh-token policy, unlock notification và behavior khi IdP/mail service lỗi chưa được chốt đầy đủ.

### 2.5 Luồng E — Cấu hình Earn Display

1. Tenant User có quyền mở danh sách Brand đã được assign.
2. Tenant cấu hình text hiển thị quyền lợi theo Brand, override theo Category hoặc Offer.
3. Nội dung hỗ trợ `vi-VN` và `en-US`, tối đa 160 ký tự theo SRS Tenant Portal.
4. Thứ tự resolve hiển thị: Offer → Category → Brand.
5. Offer/Category/Brand inactive hoặc ngoài scope không được cấu hình qua UI hoặc API.
6. Landing Page chỉ render text; không diễn giải text thành công thức, không tính cashback/point.
7. Thay đổi ghi Audit Log và phản ánh lên Landing Page theo consistency/cache policy.

**Điểm chưa đủ:** Chưa có SLA propagation/cache invalidation rõ ràng; chưa định nghĩa đầy đủ xử lý khoảng thời gian hiệu lực chồng lấn và timezone.

### 2.6 Luồng F — Landing Page và Basic My Orders

1. End User truy cập domain Tenant.
2. Hệ thống resolve Tenant, branding, locale và catalog hợp lệ.
3. User tìm kiếm/lọc Category/Top Brand và sort theo `Phổ biến` hoặc `Tên A-Z`.
4. User xem Brand Detail/Offer content và Earn Display.
5. Khi click CTA, hệ thống cảnh báo nếu thiếu `member_ref` nhưng vẫn có thể tiếp tục theo Function List.
6. Platform tạo `click_id`, lưu context và redirect sang destination URL kèm tracking parameter.
7. Basic My Orders hiển thị Order/Item thuộc đúng Tenant và End User; không hiển thị cashback/point history.

**Điểm chưa đủ:** Cơ chế tin cậy để nhận `member_ref/user_ref`, session handoff từ app Tenant, chống giả mạo reference và retention của click chưa được định nghĩa. UC-015 Basic My Orders thuộc MVP1 nhưng trace về FR-023 đang mang mô tả Deferred, gây traceability không sạch.

### 2.7 Luồng G — Order Success, click match và tạo Transaction

1. Brand gọi Order Success API với authentication, `request_id`, Brand Order ID, `click_id`, currency, amount và danh sách item.
2. Hệ thống validate credential trước payload.
3. Hệ thống validate schema, item uniqueness và idempotency.
4. Hệ thống match `click_id` với Tenant/Brand/context.
5. Hệ thống kiểm tra eligibility/visibility theo policy.
6. Mỗi item resolve commission:
   - Offer commission theo `brand_offer_code` thực tế của item.
   - Category commission theo category mapping.
   - Default category commission.
   - Không resolve được thì ghi Exception.
7. Tính:
   - `gross_commission_amount`.
   - `tenant_share_amount = gross_commission_amount × tenant_share_rate`.
   - `affiliate_keep_amount = gross_commission_amount - tenant_share_amount`.
8. Lưu Order, Items, rule snapshot và số provisional trong một transaction nguyên tử.
9. Order hợp lệ được tạo ở `Pending`; request lỗi không tạo Order mà vào Exception.

**Điểm chưa đủ:** Chưa có API contract triển khai đầy đủ về path/version, headers, canonical signature, HTTP status, error schema, precision/rounding, timezone, payload limit, timeout và retry/backoff.

### 2.8 Luồng H — Cancel/Refund và finalize

1. Brand gửi event Cancel/Refund theo toàn bộ Order Item; MVP1 không hỗ trợ partial quantity trong cùng item.
2. API chỉ cập nhật Order `Pending`.
3. Item match chuyển sang trạng thái refunded/cancelled nội bộ theo SRS; Order tổng hợp còn `Pending` hoặc chuyển `Cancelled`.
4. Hệ thống tính lại final amount và số commission/share provisional.
5. Với Order `Confirmed`, API từ chối, giữ nguyên dữ liệu và ghi Exception.
6. Worker chạy khi `pending_until` đến hạn.
7. Order Pending còn hợp lệ chuyển `Confirmed`; số provisional trở thành official và ghi `official_calculation_at`.
8. Order Cancelled không phát sinh commission.

**Điểm chưa đủ:** Cơ chế API riêng hay event type dùng chung vẫn xuất hiện là open question; lịch job, timezone, retry, race giữa finalize và refund, late event, job recovery và reconciliation behavior chưa đủ testable.

### 2.9 Luồng I — Exception management

1. Lỗi auth, schema, click, eligibility, commission, tenant share, cancel/refund hoặc persistence tạo Exception.
2. Exception có group/type/severity/status/retry count, correlation và context đã mask.
3. Admin/Ops có permission xem danh sách/chi tiết và retry/resolve.
4. Retry không được tạo double transaction hoặc ghi đè dữ liệu đã chốt.
5. Thao tác xử lý phải ghi Audit Log.
6. XLSX export cung cấp thông tin exception theo filter.

**Điểm chưa đủ:** State machine Exception, điều kiện chuyển trạng thái, retry limit/backoff, ownership/SLA, dead-letter behavior và rule tự động đóng Exception chưa đầy đủ.

### 2.10 Luồng J — Reporting, reconciliation, settlement và adjustment

1. Tenant dashboard/report chỉ đọc dữ liệu đúng Tenant và không expose gross commission/source nội bộ.
2. Admin report xem toàn hệ thống theo Tenant/Brand/Offer.
3. Reporting phân biệt provisional và official theo `order_status`.
4. Finance tạo kỳ settlement, review lines và cập nhật trạng thái.
5. Cancel/Refund sau Confirmed/Settled không sửa Order gốc; Admin/Finance tạo manual adjustment.
6. Export phải tôn trọng filter, quyền, tenant scope và mask dữ liệu.

**Điểm chưa đủ:** Settlement cycle, cut-off, currency, rounding, tax, attachment/evidence, approval workflow và công thức adjustment tác động gross/tenant share/affiliate keep chưa chốt. Đây là gap tài chính mức High.

### 2.11 Luồng K — Audit

1. Các thay đổi cấu hình, quyền, user, transaction exception, export và settlement tạo Audit Event.
2. Event chứa actor, action, entity, Tenant, timestamp server, correlation và before/after đã mask.
3. Audit append-only/immutable.
4. MVP1 Admin CMS được tra cứu log Tenant Portal; Tenant Audit UI là Phase 2.
5. Audit write bắt buộc không được silently fail; phải rollback hoặc dùng durable outbox.

**Điểm chưa đủ:** Retention, failed-action/security-event scope, archive/legal hold, export Tenant và mockup Admin Audit chưa chốt.

## 3. Requirement Review

| Category | Status | Finding | Recommendation |
|---|---|---|---|
| Phạm vi MVP1 | OK | Đã thống nhất không Cashback B1, point posting và Loyalty API | Duy trì một scope matrix có version/approval |
| Luồng nghiệp vụ end-to-end | OK | Onboard → catalog → click → order → commission → settlement đã có trace chính | Bổ sung sequence cho race/error trọng yếu |
| Document control | High Risk | Nhiều file còn Draft, Owner TBD, approval Pending | Gán owner, version, approver và baseline chính thức |
| API Order Success | High Risk | Có field/logic nhưng thiếu OpenAPI-level contract | Cung cấp OpenAPI và integration security contract |
| API Cancel/Refund | High Risk | Cơ chế endpoint/event vẫn chưa chốt thống nhất | Chốt transport, idempotency key và response contract |
| Commission calculation | Ambiguous | Công thức chính rõ nhưng precision/rounding/tax/currency chưa đủ | Chốt decimal precision, rounding level và currency policy |
| Settlement/Adjustment | High Risk | Công thức tác động sau adjustment chưa chốt | Finance phê duyệt rule và approval workflow |
| Visibility | Ambiguous | Rule AND rõ nhưng historical eligibility chưa chốt | Chốt dùng snapshot tại click hay trạng thái tại order |
| Tenant isolation | OK | SRS nhấn mạnh backend enforce tenant scope | Bổ sung error policy 403/404 thống nhất |
| RBAC | Ambiguous | Permission catalog chi tiết nhưng Custom Role vừa mô tả vừa Deferred | Tách rõ System Role MVP1 và Custom Role Phase 2 |
| Authentication | Ambiguous | Lock sau 5 lần rõ; password/OTP/session policy chưa hoàn chỉnh | Ban hành security policy có tham số cụ thể |
| Landing Page | OK | UI, locale, search/filter và click flow tương đối rõ | Chốt empty/error/loading/responsive acceptance |
| Basic My Orders | Ambiguous | MVP1 nhưng trace FR-023 vẫn gắn nội dung deferred | Tạo FR riêng cho Basic My Orders |
| Earn Display | OK | Ownership Tenant Portal và fallback rõ | Bổ sung overlap/timezone/cache propagation |
| State transition | Ambiguous | Order enum đã chuẩn hóa nhưng item status và late event cần rõ hơn | Cung cấp state matrix Order/Item/Exception/Settlement |
| Idempotency | Ambiguous | Có yêu cầu nhưng key precedence/retention/response chưa đủ | Định nghĩa idempotency contract theo endpoint |
| Concurrency | Ambiguous | Optimistic locking được nêu nhưng không xuyên suốt mọi entity | Chốt ETag/version và 409 response |
| Exception handling | Ambiguous | Nhóm lỗi tốt nhưng lifecycle/SLA/retry chưa đủ | Định nghĩa state machine và retry ownership |
| Audit | Ambiguous | Capture/masking/immutability tốt; retention còn mở | Chốt retention, failure handling và access matrix |
| NFR Performance | Missing | Nhiều target là TBD/baseline đề xuất | Product/Ops phê duyệt SLA/SLO và tải chuẩn |
| Availability/DR | Missing | Chưa có RTO/RPO, backup/restore target cụ thể | Bổ sung NFR vận hành có số đo |
| Privacy/Retention | Missing | Có nguyên tắc mask nhưng thiếu retention theo object | Ban hành data classification/retention schedule |
| Accessibility | Ambiguous | Có định hướng nhưng chưa có chuẩn/level phê duyệt | Chốt WCAG level và browser/device matrix |
| Export XLSX | High Risk | Tenant export có nhãn lỗi và cột/dữ liệu không đồng nhất | Sửa template và chốt export schema/version |
| Traceability | Ambiguous | Một số CR đã áp nhưng CR list vẫn ghi tồn đọng cũ | Re-run trace matrix và đóng CR bằng evidence |
| Repository hygiene | Missing | Có 4 lock file tạm trong SRS | Xóa lock file và thêm ignore rule |

## 4. Missing Requirements

1. OpenAPI/spec chính thức cho Order Success, Cancel/Refund, click tracking, My Orders và các API Portal/CMS quan trọng.
2. Quy ước API versioning, correlation ID, pagination, filter, sort và error envelope thống nhất.
3. Authentication contract với Brand: header, HMAC canonical string/token, nonce, clock skew, key rotation và revoke.
4. Data retention cho click, Order, Exception, Audit, export file, OTP và session.
5. SLA/SLO định lượng cho API, worker finalize, dashboard, export và propagation Earn Display.
6. RTO/RPO, backup frequency, restore verification và failover.
7. Quy tắc timezone chuẩn cho `clicked_at`, `order_time`, offer/effective period, `pending_until` và settlement cut-off.
8. Currency scope MVP1 và behavior nếu Brand gửi currency không hỗ trợ.
9. Giới hạn payload, số item tối đa, kích thước text/metadata và export row limit.
10. Malware/content validation cho asset upload hoặc attachment settlement nếu được dùng.
11. Cơ chế notification cho account lock/unlock, password reset, failed export, settlement và exception assignment.
12. Chính sách observability: metric, alert threshold, log retention, PII masking và dashboard vận hành.
13. Quy tắc accessibility cụ thể và device/browser support được phê duyệt.
14. Error/loading/empty/offline states nhất quán cho toàn bộ CMS/Tenant Portal/Landing Page.
15. Ownership và source of truth cho từng entity/reporting view.

## 5. Missing Business Rules

1. Historical visibility: eligibility lấy tại click time, order time hay snapshot nào.
2. Click validity/retention sau khi đã bỏ expiry-based matching.
3. Một click có thể gắn bao nhiêu Order và giới hạn chống reuse/fraud.
4. Duplicate precedence giữa `request_id`, `brand_id + brand_order_id` và `click_id`.
5. Late Order Success, out-of-order event và event có `order_time` trước `clicked_at`.
6. Race giữa finalize job và Cancel/Refund cùng thời điểm.
7. Partial Order qua nhiều Cancel/Refund event và duplicate item event.
8. Rounding per item hay per Order; số chữ số decimal và xử lý chênh lệch tổng.
9. Thuế/phí/discount/shipping có thuộc `amount/final_amount` làm base commission không.
10. Multi-currency và FX rate nếu không giới hạn VND.
11. Settlement cut-off, cycle, reopen, approval và rollback.
12. Adjustment dương/âm tác động các trường tài chính và kỳ settlement nào.
13. Exception retry tối đa, auto/manual retry và điều kiện Resolved/Closed.
14. Custom Role có thực sự thuộc MVP1 hay Phase 2.
15. Tenant/Admin cuối cùng khi role bị inactive, user locked hoặc Tenant deactivated.
16. Domain reassignment giữa Tenant và behavior với URL cũ.
17. Offer/category/Brand code migration khi đã có historical transaction.
18. Fallback locale khi cả locale hiện tại và `vi-VN` đều thiếu.
19. Rule ranking “Phổ biến” trên Landing Page.
20. Data freshness và timezone của dashboard/report/export.

## 6. Missing Validation Rules

1. Min/max length và character set cho hầu hết code, ID, name, contact và metadata.
2. Chuẩn normalize/case sensitivity cho Tenant code, Brand code, Category code, username và email.
3. URL allowlist/scheme, open redirect, punycode và SSRF protection cho destination URL/custom domain.
4. File type/size/dimension/virus scan cho logo, icon và image.
5. Decimal precision/scale cho amount, commission và revenue share.
6. Max `pending_days` và behavior khi thay đổi trong lúc có Order Pending.
7. Date/time range, timezone, DST và boundary `effective_to`.
8. Payload/items maximum và duplicate `item_code` qua retry/update.
9. Phone/email normalization và uniqueness scope.
10. Password length/complexity/history/expiry/common-password policy.
11. OTP length, TTL, retry, resend cooldown và attempt reset.
12. Search/filter max range và export date-range limit.
13. HTML/script/special-character sanitization cho localized content và Earn Display.
14. Blank/whitespace-only text và Unicode normalization.
15. Error code/message catalog song ngữ cho UI và API.

## 7. Missing Permission Rules

1. Ma trận permission CMS đầy đủ theo action cho Tenant, Brand, Offer, Category, Transaction, Exception, Reporting, Settlement và Audit.
2. Quyền Finance so với Admin/Ops đối với adjustment, settlement status và export.
3. Quyền xem dữ liệu nhạy cảm trong Exception Detail/raw integration metadata.
4. Quyền rotate/revoke Brand API credential.
5. Quyền quản lý domain/branding và phê duyệt publish.
6. Quyền xem/download export job do user khác tạo.
7. Quyền retry exception có thể làm phát sinh/cập nhật transaction tài chính.
8. Rule maker-checker cho commission, revenue share và manual adjustment.
9. Behavior khi permission/role thay đổi trong session đang hoạt động.
10. Quyền Custom Role trong MVP1 cần đóng hoặc loại khỏi UI/API/mockup.

## 8. Missing Edge Cases

1. Tenant/domain/Brand/Offer bị inactive giữa click và Order Success.
2. Offer hết hạn đúng thời điểm click hoặc order.
3. Click hợp lệ nhưng Brand gửi sai Tenant/Offer context.
4. Một Brand Order ID được gửi với payload khác ở lần retry.
5. Order Success commit thành công nhưng response timeout khiến Brand retry.
6. Cancel/Refund đến trước Order Success.
7. Cancel/Refund trùng, đảo thứ tự hoặc chứa item đã cancel.
8. Finalize job chạy hai lần hoặc crash giữa tính và commit.
9. Revenue share/commission rule thay đổi khi Order đang Pending.
10. Default category bị inactive sau click nhưng trước Order.
11. Concurrent edit cùng entity từ hai Admin/Tenant User.
12. Tenant Admin cuối cùng tự khóa/đổi role/bị lock bởi Auth.
13. Forgot Password OTP được dùng đồng thời trên nhiều thiết bị.
14. Export lớn, timeout, file expired hoặc user mất quyền trước khi download.
15. Dashboard có dữ liệu partial/late-arriving và timezone khác nhau.
16. Audit service outage trong action bắt buộc audit.
17. Database commit thành công nhưng Audit/outbox publish thất bại.
18. Locale content chứa HTML/script hoặc thiếu toàn bộ fallback.
19. End User thiếu/giả mạo `member_ref`.
20. Custom domain trùng, certificate hết hạn hoặc DNS thay đổi.

## 9. Rủi ro

### 9.1 High Risk

| ID | Mô tả | Tác động | Khuyến nghị |
|---|---|---|---|
| H-01 | API contract chưa đủ cấp triển khai | Brand tích hợp khác nhau, khó test contract, mất/nhân đôi Order | Phát hành OpenAPI + security/idempotency contract |
| H-02 | Settlement/adjustment chưa chốt công thức | Sai số tiền phải thu/trả và tranh chấp đối soát | Finance phê duyệt rule trước build/UAT |
| H-03 | Rounding/precision/tax/currency chưa rõ | Sai commission/share giữa item, order, report và export | Chốt financial calculation standard |
| H-04 | Historical visibility chưa rõ | Order hợp lệ có thể bị reject hoặc ghi nhận sai | Chốt snapshot/eligibility policy |
| H-05 | Race finalize và Cancel/Refund chưa rõ | Order có thể chốt sai hoặc cập nhật sau Confirmed | Thiết kế state transition nguyên tử và concurrency rule |
| H-06 | Requirement vẫn Draft/TBD/Pending approval | QA không có baseline ổn định | Baseline tài liệu và ký duyệt |
| H-07 | Custom Role mâu thuẫn phạm vi | Dev xây khác nhau giữa UI, API và RBAC | Chốt MVP1/Phase 2, gỡ artefact trái phạm vi |
| H-08 | Tenant export XLSX lỗi contract | Người dùng hiểu sai dữ liệu tài chính | Sửa nhãn/schema và thêm data contract validation |
| H-09 | End User identity context chưa an toàn | Lộ My Orders hoặc attribution sai user | Định nghĩa signed session/token handoff |

### 9.2 Medium Risk

| ID | Mô tả | Tác động | Khuyến nghị |
|---|---|---|---|
| M-01 | Password/OTP/session policy thiếu tham số | Lỗ hổng brute force/session | Ban hành security policy |
| M-02 | Exception lifecycle/retry chưa đủ | Exception tồn đọng hoặc retry gây side effect | Chốt state machine, SLA và retry policy |
| M-03 | Data retention/DR chưa định lượng | Rủi ro compliance và mất dữ liệu | Chốt retention, RTO/RPO |
| M-04 | NFR chỉ là baseline đề xuất/TBD | Không có tiêu chí performance release | Product/Ops phê duyệt SLO |
| M-05 | Basic My Orders trace về FR deferred | Thiếu coverage hoặc hiểu sai scope | Tạo FR riêng và cập nhật trace |
| M-06 | Code mutation policy còn mở | Mất liên kết historical data | Chốt immutable/migration policy |
| M-07 | Cache propagation Earn Display chưa rõ | Landing hiển thị nội dung cũ | Chốt SLA và invalidation |
| M-08 | Audit retention/failed event còn mở | Thiếu bằng chứng điều tra | Chốt audit/security logging policy |

### 9.3 Low Risk

| ID | Mô tả | Tác động | Khuyến nghị |
|---|---|---|---|
| L-01 | Có 4 file lock tạm | Nhiễu tài liệu/review | Xóa và ignore |
| L-02 | CR list còn mô tả tồn đọng đã được cập nhật ở wireframe | Gây nhầm trạng thái | Cập nhật CR evidence |
| L-03 | Open question bị lặp trong Analysis | Tăng nhiễu | Gộp một dòng |
| L-04 | Một số mockup dùng ngôn ngữ/nhãn chưa thống nhất | UX không nhất quán | Chuẩn hóa content glossary |
| L-05 | XLSX Tenant có typo `Commission Commission At` | Sai nhãn export | Đổi thành `Commission Finalized At` |

## 10. Đối chiếu artefact UI và export

### 10.1 Mockup/UI

- Các HTML mockup bao phủ phần lớn màn CMS và Tenant Portal.
- Mockup Tenant Role Create/Edit/Permissions vẫn hiện diện dù Custom Role được Function List ghi Deferred/Phase 2.
- Các màn form có nhiều placeholder/hint nhưng không phải tất cả validation đã được đưa vào SRS dưới dạng rule có thể test.
- Cần coi SRS là nguồn chân lý; mockup không được tự tạo business rule.

### 10.2 XLSX export

| File | Finding |
|---|---|
| `cms-exception-export.xlsx` | Có các cột chính nhưng một số sample row thiếu Order/Brand Order/Tenant; cần quy định nullability và mapping theo exception group |
| `cms-transaction-export.xlsx` | Phân biệt Estimated/Actual tốt; cần chốt schema, data type, currency và timezone |
| `tenant-portal-transaction-export.xlsx` | Nhãn `Commission Commission At` sai; dữ liệu sample có dấu hiệu lệch/thiếu cột; cần bảo đảm không expose Gross Commission/source nội bộ |

## 11. Questions for BA / PO

1. Trạng thái requirement baseline chính thức là phiên bản nào, ai là Owner và ai phê duyệt cuối?
2. Custom Role/Create-Edit-Delete Permission thuộc MVP1 hay Phase 2? Nếu Phase 2, có gỡ toàn bộ menu, API và mockup khỏi acceptance MVP1 không?
3. Visibility/eligibility của Order được đánh giá theo snapshot lúc click hay trạng thái hiện tại lúc Order Success?
4. Một `click_id` được phép tạo nhiều Order không? Nếu có, giới hạn và anti-fraud rule là gì?
5. Brand Cancel/Refund dùng endpoint riêng hay event type chung? Contract idempotency chính thức là gì?
6. Khi Cancel/Refund và finalize job xảy ra đồng thời, thao tác nào thắng và backend khóa/version thế nào?
7. Precision/rounding áp dụng ở item hay Order; số chữ số decimal và quy tắc phân bổ chênh lệch là gì?
8. Base amount tính commission có bao gồm thuế, shipping, discount, voucher và fee không?
9. MVP1 chỉ VND hay multi-currency? Request currency khác VND được reject hay quy đổi?
10. Settlement cycle/cut-off/status/approval chính thức là gì?
11. Manual adjustment tác động gross commission, tenant share và affiliate keep theo công thức nào; có cần maker-checker không?
12. End User context (`member_ref/user_ref`) được ký/xác thực và truyền từ app Tenant sang Landing Page/My Orders bằng cơ chế nào?
13. Click không có `member_ref` vẫn được tạo Order/commission hay chỉ phục vụ analytics?
14. Password policy, OTP TTL/resend/attempt limit, session TTL và refresh-token policy chính thức là gì?
15. Retention cho Click, Order, Exception, Audit, OTP, session và export file là bao lâu?
16. RTO/RPO và availability target được phê duyệt là bao nhiêu?
17. Exception có các trạng thái và transition chính thức nào; retry tối đa/auto retry/SLA ra sao?
18. `pending_days` thay đổi có áp dụng hồi tố cho Order Pending hiện tại không?
19. Rule xếp hạng `Phổ biến` trên Landing Page dựa trên dữ liệu nào?
20. Basic My Orders có cần FR riêng thay cho trace vào FR-023 Deferred không?
21. Khi cả locale hiện tại và `vi-VN` đều thiếu content, hệ thống ẩn entity hay hiển thị fallback kỹ thuật?
22. Audit failed/security action có lưu chung Audit Log hay Security Log; retention và quyền xem là gì?
23. Category/Brand code đã có dependency có hoàn toàn immutable hay hỗ trợ migration?
24. Giới hạn số dòng/export, thời gian lưu file và quyền download lại là gì?
25. Có chấp nhận sửa template Tenant export thành `Commission Finalized At` và chốt lại thứ tự/cột dữ liệu không?

## 12. Overall Assessment

| Tiêu chí | Điểm |
|---|---:|
| Requirement Completeness Score | 72/100 |
| Testability Score | 68/100 |
| Consistency Score | 74/100 |
| Traceability Score | 70/100 |
| Readiness Status | PARTIAL PASS |

### Kết luận

Bộ tài liệu đã mô tả tương đối đầy đủ kiến trúc nghiệp vụ và các luồng chính của Affiliate Marketplace Platform. Các quyết định quan trọng về phạm vi MVP1, commission, Tenant share, visibility hai tầng và Order status đã được đồng bộ phần lớn.

Tuy nhiên, requirement **chưa sẵn sàng PASS để bắt đầu Test Planning toàn hệ thống** do còn các gap High Risk liên quan API contract, financial rounding/settlement/adjustment, historical eligibility, concurrency finalize-refund, End User identity và trạng thái phê duyệt tài liệu.

### Khuyến nghị tổng thể

1. Chặn baseline QA đối với Order/Commission/Settlement cho đến khi đóng H-01 đến H-06.
2. Phát hành OpenAPI và state-transition matrix cho Order, Item, Exception và Settlement.
3. Finance phê duyệt calculation/rounding/adjustment/cut-off bằng ví dụ số chuẩn.
4. Chốt scope Custom Role và làm sạch trace Basic My Orders.
5. Sửa ba template export, đặc biệt Tenant transaction export.
6. Gán Owner/Approver, đóng Open Questions và phát hành requirement baseline mới.
7. Sau khi cập nhật, thực hiện một vòng requirement re-review trước Test Planning/Test Design.

