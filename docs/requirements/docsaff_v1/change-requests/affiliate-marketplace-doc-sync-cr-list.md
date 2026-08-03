# Change Request List — Đồng bộ tài liệu Affiliate Marketplace Platform

## Document control

- Status: Draft
- Owner: TBD
- Ngày lập: 2026-07-22
- Mục đích: Đồng bộ toàn bộ bộ tài liệu `docsaff` sau khi phạm vi MVP1 và mô hình commission bị thay đổi. Bộ tài liệu hiện tách làm 2 thế hệ:
  - **Thế hệ cũ (2026-07-09):** BRD, Analysis, SRS chính, Modeling, Use Case List — mô hình commission `A + B = X`, có cashback B1 + cộng điểm loyalty trong MVP1.
  - **Thế hệ mới (2026-07-22):** Function List + 5 SRS module (Tenant Mgmt, Brand & Offer, Order & Transaction, Tenant Portal, Landing Page) — mô hình revenue share Affiliate→Tenant, **không** cashback/điểm trong MVP1, commission theo Category/Offer, có số tạm tính (provisional).

## Quy ước

- **Severity:** P0 (chặn build/gây sai tiền) · P1 (mâu thuẫn phạm vi/logic lớn) · P2 (không nhất quán, cần chốt) · P3 (housekeeping).
- Mỗi CR gồm: Vấn đề → Tài liệu ảnh hưởng → Thay đổi đề xuất → Quyết định cần chốt (nếu có).
- Viết tắt tài liệu (tên file trong `docsaff/`):
  - **BRD** = `brd/affiliate-marketplace-platform.md`
  - **ANL** = `analysis/affiliate-marketplace-platform-analysis.md`
  - **SRS** = `srs/affiliate-marketplace-platform.md`
  - **MDL** = `modeling/affiliate-marketplace-platform-modeling.md`
  - **UCL** = `usecases/affiliate-marketplace-platform-usecase-list.md`
  - **FNL** = `function-list/affiliate-marketplace-platform-function-list.md`
  - **M-TEN** = `srs/tenant-management-module-04-template.md`
  - **M-BRO** = `srs/brand-offer-management-module-04-template.md`
  - **M-ORD** = `srs/order-transaction-management-module-04-template.md`
  - **M-TP** = `srs/tenant-portal-module-04-template.md`
  - **M-LP** = `srs/landing-page-module-04-template.md`
  - Ký hiệu **"↔"** = đối chiếu/đồng bộ giữa hai tài liệu.

---

## Nhật ký quyết định (Decision Log)

Cập nhật 2026-07-22. Các quyết định đã được chốt bởi chủ dự án:

| CR | Trạng thái | Quyết định chốt |
|---|---|---|
| CR-01 | ✅ Đã chốt | MVP1 **không** làm cashback B1, không tính điểm, không gọi Tenant Loyalty API. |
| CR-02 | ✅ Đã chốt | **Bỏ hoàn toàn** mô hình `A/B/X`; thay bằng `tenant_share_rate` (Affiliate→Tenant). |
| CR-03 | ✅ Đã chốt | `order_status` còn 3: `Pending / Confirmed / Cancelled` (**bỏ `Refunded` + `Rejected`**). Cancel/Refund API chỉ xử lý Order Pending; Order Confirmed bị từ chối, giữ nguyên dữ liệu và ghi Exception để xử lý đối soát thủ công. |
| CR-04 | ✅ Đã chốt | **Bỏ hẳn `commission_status`** — tạm tính/chính thức suy từ `order_status` (Pending→tạm tính, Confirmed→chính thức). Ca không tính được → Exception queue. |
| CR-05 | ✅ Đã chốt (có thể xem lại) | Tenant share **chỉ dạng %**, bỏ share cố định (VND) → loại bỏ rủi ro `affiliate_keep` âm. Việc bỏ Fixed cho commission Brand→Affiliate còn đang cân nhắc. |
| CR-06 | ✅ Đã chốt | Đồng bộ provisional fields vào data model M-TP (theo đề xuất). |
| CR-08 | ✅ Đã chốt & áp | **Tenant Portal** là nơi cấu hình Earn Display; đã gỡ mục CMS trùng khỏi FNL, OQ-TENANT-003 Closed. |
| CR-09 | ✅ Đã chốt & áp | Mô hình 2 tầng visibility, rule AND, schema `assignment_status`+`tenant_visibility_status` thống nhất. |
| CR-10 | ✅ Đã chốt | 3 tab lịch sử End user → **Deferred** (hệ quả của CR-01). |
| CR-11 | ✅ Đã chốt | `pending_days` = thời gian chốt commission; hết hạn thì doanh thu/hoa hồng Affiliate & Tenant chuyển từ **tạm tính → chính thức**. |
| CR-12 | ❌ Không áp dụng | Bộ Đăng ký/OTP không liên quan phạm vi affiliate. |
| CR-13 | ✅ Đã chốt | `commission_value > 0` cho mọi loại (Percentage `>0..<=100`); bỏ Fixed = 0. |
| CR-14 | ✅ Đã chốt & áp | Tài khoản **Tenant Portal** dùng `Active / Inactive / Locked`; `Locked` do Auth Service tự động thiết lập sau 5 lần đăng nhập sai liên tiếp và chỉ Tenant Admin được mở khóa. Không áp dụng quy tắc này cho tài khoản CMS. |
| CR-15 | ✅ Đã chốt | Offer chỉ `Draft / Active / Inactive`; thay "Published/Ready" → "Active". |
| CR-16 | ✅ Đã xử lý | Loại bỏ kiểm tra thời hạn theo click; chỉ match `click_id` hợp lệ. |
| CR-18 | ✅ Đã chốt & áp | `effective_from/to` earn display = **`Datetime`** (M-TP + M-LP). |
| CR-19 | ❌ Không còn áp dụng | File tài liệu OTP đã bị gỡ khỏi bộ `docsaff/` → CR moot. |
| CR-23 | ✅ Đã chốt | Order thiếu category id → dùng **category mặc định của Brand** tính commission, thay vì exception. |
| CR-24 | ✅ Đã chốt | **Offer commission không bắt buộc**; Offer thiếu commission thì hoa hồng tính theo Category như bình thường (không exception). |

### Trạng thái áp dụng vào tài liệu (verify bằng rà soát toàn repo)

| Đợt | CR | Kết quả verify |
|---|---|---|
| 1 | CR-01, 02, 03, 04 | ✅ Đạt — **trừ** `wireframe/affiliate-marketplace-landing-page-wireframe.md` chưa cập nhật (vẫn bản 2026-07-09, còn cashback B1/điểm dự kiến/lịch sử cashback như MVP1). |
| 2 | CR-05, 06, 13, 14, 15 | ✅ Đạt toàn bộ. |
| 2 | CR-23, CR-24 | ✅ Đạt toàn bộ (áp sớm cùng đợt). |
| 3 | CR-08, 09, 18 | ✅ Đạt toàn bộ (verify 2026-07-22): FNL gỡ earn display CMS; BRULE-024 2 tầng + schema thống nhất; earn display Datetime ở M-TP/M-LP. |
| 3 | CR-19 | ❌ Không còn áp dụng — file OTP đã bị gỡ khỏi bộ tài liệu. |

**Còn tồn đọng cần xử lý:**
1. File `wireframe/affiliate-marketplace-landing-page-wireframe.md` — chưa áp CR-01 và CR-15 (mục P0 duy nhất còn lại).
2. `srs/affiliate-marketplace-platform.md:209` — Sort enum còn `điểm cao` (MVP1 chỉ có earn display dạng text, không có giá trị điểm để sort).
3. `srs/affiliate-marketplace-platform.md:242,244` — `Cashback B1%` / `Loyalty endpoint` vẫn nằm trong bảng GUI Admin setup MVP1 (chỉ ghi Deferred ở cột rule); nên tách xuống mục Deferred riêng.

Các CR còn lại (CR-07, CR-17, CR-20, CR-21, CR-22) **chưa chốt**.

---

## Nhóm A — Quyết định gốc (phải chốt trước, các CR khác phụ thuộc)

### CR-01 — Chốt một phạm vi MVP1 duy nhất (P0) — ✅ ĐÃ CHỐT

- **Vấn đề:** FNL (22/07) tuyên bố MVP1 **không** làm cashback B1, tính điểm, gọi Tenant Loyalty API. BRD/ANL/SRS/MDL/UCL (09/07) vẫn liệt kê những phần này là **Must trong MVP1** (BR-013/014/018, BRULE-023, AC-004/006, FR-004/016/026/027, UC-009/017, FEAT-008/009).
- **Tài liệu ảnh hưởng:** BRD, ANL, SRS, MDL, UCL, FNL, tất cả module SRS.
- **✅ Quyết định (2026-07-22):** MVP1 **KHÔNG** làm cashback B1, **KHÔNG** tính điểm cho End user, **KHÔNG** gọi Tenant Loyalty API. Phạm vi FNL 22/07 là chuẩn chính thức.
- **Hành động cập nhật tài liệu:**
  - BRD: gỡ khỏi Must và chuyển sang "Ngoài phạm vi MVP1 / Deferred": BR-013, BR-014, BR-018; đưa BRULE-023 về diện deferred; xóa AC-004, AC-006.
  - ANL: chuyển FR-004 (point conversion), FR-016 (điểm dự kiến), FR-026 (cộng điểm), FR-027 (Rewarded), BRULE-023 sang deferred; cập nhật happy path bỏ bước 16/18–21 liên quan cộng điểm.
  - SRS: gỡ FEAT-008 (phần cashback/point), FEAT-009 (Tenant Loyalty Posting), SR-017; điều chỉnh SR-009/SR-016.
  - MDL: cắt nhánh B1/point posting trong business process, activity, sequence, state (Cashback Transaction) — hoặc đánh dấu "Phase sau".
  - UCL: đánh dấu UC-009, UC-017 = **Deferred** (bỏ khỏi MVP1 = Yes).
  - Tham chiếu bảng P1–P7 của FNL cho phần deferred.

### CR-02 — Đồng bộ mô hình commission trong tài liệu gốc (P0) — ✅ ĐÃ CHỐT

- **Vấn đề:** Tài liệu gốc dùng `A + B = X` (phần trăm, VR-007/BRULE-009). Thế hệ mới dùng: commission Brand→Affiliate theo **% hoặc số tiền cố định (VND)**, theo **Category hoặc Offer**; phần Tenant = `gross_commission × tenant_share_rate` với thứ tự ưu tiên **Offer → Category → Brand**. Hai mô hình mâu thuẫn trực tiếp.
- **Tài liệu ảnh hưởng:** BRD (BR-012, BRULE-008/009, AC-003), ANL (FR-008/009, BRULE-009, VR-007), SRS (SR-005, GUI Platform A%/Tenant B%), MDL (data model Commission Allocation Rule).
- **✅ Quyết định (2026-07-22):** **Bỏ hoàn toàn** khái niệm "A% Platform giữ / B% Tenant / A+B=X". Thay bằng mô hình mới:
  1. **Brand→Affiliate commission** (`gross_commission_amount`): cấu hình theo Offer hoặc Category.
  2. **Tenant Revenue Share**: `tenant_share_amount = gross_commission_amount × tenant_share_rate%`, resolve theo thứ tự **Offer → Category → Brand**.
  3. `affiliate_keep_amount = gross_commission_amount − tenant_share_amount`.
  - Nguồn chân lý công thức: M-ORD §IV.4.f.
- **Hành động cập nhật tài liệu:**
  - BRD: viết lại BR-012; xóa/thay BRULE-008, BRULE-009; sửa AC-003 (bỏ kiểm tra A+B=X, thay bằng tenant_share_rate).
  - ANL: viết lại FR-008/FR-009 theo tenant_share_rate; xóa BRULE-009 & VR-007 (A+B=X); cập nhật data object "Commission Allocation Rule" → "Tenant Revenue Share Rule".
  - SRS: gỡ field GUI "Platform A%" và "Tenant B%", thay bằng "Brand→Affiliate commission" + "Tenant share rate %"; sửa SR-005.
  - MDL: đổi entity/relationship "Commission Allocation Rule (A/B)" → "Tenant Revenue Share Rule (tenant_share_rate)".
- **Liên hệ CR-05:** tenant share **chỉ dạng %** (không Fixed).

---

## Nhóm B — Mâu thuẫn enum & data model (P0/P1, chặn build)

### CR-03 — Thống nhất enum `order_status` giữa 2 file M-ORD ↔ M-TP (P0) — ✅ ĐÃ CHỐT

> **Giải thích ký hiệu:** M-ORD = file `srs/order-transaction-management-module-04-template.md`; M-TP = file `srs/tenant-portal-module-04-template.md`. Hai file này mô tả cùng một trạng thái đơn hàng nhưng ghi tên trạng thái khác nhau → cần dùng chung một bộ enum.

- **Vấn đề:** M-ORD = `Pending / Confirmed / Cancelled / Refunded / Rejected`; M-TP = `Pending / Success / Cancelled / Refunded` (dùng "Success" thay "Confirmed", thiếu "Rejected").
- **Tài liệu ảnh hưởng:** M-ORD (IV.3.d, V.2), M-TP (TXN list, Data Req V.5).
- **✅ Quyết định (2026-07-22):** Chuẩn hóa enum `order_status` còn **3 trạng thái**: **`Pending / Confirmed / Cancelled`** (đã **bỏ cả `Refunded` và `Rejected`**). Sửa cả M-ORD và M-TP dùng đúng bộ này.

  | Trạng thái | Ý nghĩa |
  |---|---|
  | `Pending` | Order success hợp lệ, đang trong `pending_days` (hoa hồng tạm tính). |
  | `Confirmed` | Hết `pending_days`, không cancel/refund → đơn chính thức (hoa hồng chốt). |
  | `Cancelled` | Brand báo hủy **hoặc** hoàn trong `pending_days` → loại khỏi commission. |

- **Lý do bỏ `Refunded`:** Đã có `pending_days` làm cửa sổ chờ; mọi cancel/refund trong cửa sổ này gộp về **`Cancelled`**.
- **Lý do bỏ `Rejected`:** Không cần trạng thái đơn "bị từ chối". Order-success **không hợp lệ** (auth fail, sai schema, trùng, click_id invalid, sai visibility) sẽ **không tạo thành order** mà đẩy thẳng vào **Exception queue** (module Exception Management đã có sẵn các loại lỗi này). Đơn nào tồn tại trong bảng orders = đơn đã hợp lệ.
- **Ca hoàn sau Confirmed:** Cancel/Refund API bị từ chối, giữ nguyên Order/Item/Commission/Tenant Share đã chốt và ghi Exception. Admin/Finance xử lý adjustment thủ công trong đối soát/settlement nếu cần; không tự động thay đổi Order Status trong MVP1.
- **Hành động cập nhật tài liệu:**
  - M-ORD: đổi enum `order_status` → `Pending / Confirmed / Cancelled` (IV.3.d, V.2); bỏ `Refunded` và `Rejected`; order-success không hợp lệ → chỉ ghi Exception, không tạo order; refund-trong-pending → `Cancelled`; refund-sau-Confirmed = điều chỉnh settlement thủ công.
  - M-TP: đổi "Success" → "Confirmed", bỏ "Refunded".
  - Cập nhật cancel/refund integration (FNL mục 12/33): event refund hợp lệ trong pending → set `Cancelled`.
  - Đảm bảo các loại lỗi `auth_fail/schema_fail/duplicate/click_id_invalid/visibility_fail` được cover đủ trong Exception Management (thay cho vai trò của `Rejected`).

### CR-04 — Bỏ hẳn `commission_status` (P0) — ✅ ĐÃ CHỐT

- **Vấn đề:** M-ORD = `Not calculated / Pending / Calculated / Exception / Rejected`. M-TP lúc thì `Pending/Calculated/Exception/Rejected/Settled`, lúc thì `Pending/Confirmed/Rejected/Settled` (mâu thuẫn ngay trong cùng file); "Settled" xuất hiện dù settlement ngoài phạm vi module Order.
- **Tài liệu ảnh hưởng:** M-ORD, M-TP, và mọi màn/filter tham chiếu commission status (M-ORD TXN, M-TP transaction list/detail, Admin/Tenant reporting).
- **✅ Quyết định (2026-07-22):** **Bỏ hoàn toàn trường `commission_status`.** Việc phân biệt hoa hồng **tạm tính vs chính thức** chỉ cần dựa vào `order_status` (đã rút còn 3 trạng thái ở CR-03) — ánh xạ 1-1:

  | `order_status` | Ý nghĩa hoa hồng |
  |---|---|
  | `Pending` | Hoa hồng **tạm tính** (provisional) — order còn trong `pending_days`. |
  | `Confirmed` | Hoa hồng **chính thức** (official) — hết `pending_days`, không cancel/refund. |
  | `Cancelled` | **Không** phát sinh hoa hồng. |

- **Lý do bỏ được:** Sau CR-03 (order_status còn 3 trạng thái) và CR-23 (fallback category mặc định), vòng đời hoa hồng trùng khít vòng đời đơn hàng → không còn trục trạng thái riêng để duy trì.
- **Ca "không tính được hoa hồng" xử lý ở đâu:** Khi thiếu commission rule hợp lệ **và** Brand chưa có category mặc định (hiếm, xem CR-23) → đẩy vào **Exception queue** (giống pattern CR-03), và nhận biết trên dòng order bằng **`gross_commission_amount IS NULL`**. Không cần trạng thái `Failed`.
- **Hành động cập nhật tài liệu:**
  - M-ORD: **gỡ trường `commission_status`** khỏi data model, logic COM, màn transaction list/detail và bộ lọc; thay filter "commission status" bằng filter theo `order_status`. Ghi rõ: order `Pending` → dùng các field `provisional_*`; order `Confirmed` → dùng field chính thức.
  - M-TP: gỡ cột/filter commission status khỏi transaction list và dashboard; hiển thị tạm tính/chính thức theo `order_status`.
  - Admin/Tenant reporting: phân biệt số tạm tính vs chính thức theo `order_status` thay vì commission status.
  - Bổ sung rule: khi không tính được hoa hồng → tạo Exception record; `gross_commission_amount` để trống.
- **Lưu ý về `official_calculation_at`:** vẫn giữ để biết thời điểm chốt số chính thức (CR-11); không thay bằng status.

### CR-05 — Tenant share chỉ dạng % (P0 — sai tiền) — ✅ ĐÃ CHỐT (có thể xem lại)

- **Vấn đề:** Chỉ có công thức tenant share dạng %. Với share **cố định (VND)**, không có công thức; nếu share cố định > `gross_commission` nhỏ → `affiliate_keep_amount` **âm**, vi phạm BR-COM-001-04. Chưa có rule clamp/reject.
- **Tài liệu ảnh hưởng:** M-ORD (IV.4.f, BR-COM-001-04), M-TEN (RS-002, OQ-TENANT-004), FNL (mục 25, 37).
- **✅ Quyết định (2026-07-22):** **Tenant share chỉ dạng %** (`tenant_share_rate`), **bỏ tùy chọn share cố định (VND) cho Tenant**. Vì `tenant_share = gross_commission × rate%` luôn ≤ gross_commission → **loại bỏ hoàn toàn rủi ro `affiliate_keep` âm**; không cần rule clamp/reject cho tenant share nữa. OQ-TENANT-004 (Fixed theo đơn/commission event) trở nên **không áp dụng** cho tenant share.
- **Hành động cập nhật tài liệu:**
  - M-TEN (RS-002) & FNL (mục 25): bỏ `commission_type` cho tenant revenue share, chỉ còn `tenant_share_rate` (%). Gỡ đơn vị "VND" khỏi màn Revenue share.
  - M-ORD: giữ 1 công thức tenant share duy nhất (%); giữ BR-COM-001-04 như một invariant hiển nhiên (không cần rule chặn Fixed).
  - Đóng OQ-TENANT-004 với ghi chú "N/A do tenant share chỉ %".

### CR-06 — Đồng bộ provisional fields vào data model Tenant Portal (P1) — ✅ ĐÃ CHỐT

- **Vấn đề:** M-TP hiển thị cột "Tạm tính/Provisional" + ngày tính trên UI, nhưng data model M-TP (V.5) chỉ có `gross_commission_amount` + `tenant_share_amount`, thiếu các field provisional/expected-calc-date mà M-ORD v1.1.0 đã định nghĩa.
- **Tài liệu ảnh hưởng:** M-TP (Data Req V.5), M-ORD (v1.1.0 fields).
- **✅ Quyết định (2026-07-22):** Đồng ý theo đề xuất. Bổ sung vào data model M-TP: `provisional_revenue_amount`, `provisional_gross_commission_amount`, `provisional_tenant_share_amount`, `expected_calculation_at`, `official_calculation_at` — đặt tên field trùng khớp M-ORD. **Không** thêm `commission_status` (đã bỏ hẳn theo CR-04); phân biệt tạm tính/chính thức dựa vào `order_status`.
- **Liên hệ CR-11:** khái niệm tạm tính → chính thức được chốt tại thời điểm `pending_days` hết hạn (xem CR-11).

### CR-07 — Bổ sung `provisional_affiliate_keep_amount` vào field tạo transaction (P2)

- **Vấn đề:** `provisional_affiliate_keep_amount` có trong logic COM (IV.4.f), màn detail (TXN item 3) và data model (V.2), nhưng thiếu trong danh sách "Transaction Creation Fields" (IV.3.d chỉ liệt kê provisional_revenue/gross_commission/tenant_share).
- **Tài liệu ảnh hưởng:** M-ORD (IV.3.d).
- **Thay đổi đề xuất:** Thêm `provisional_affiliate_keep_amount` vào field set khi tạo transaction cho nhất quán.

### CR-23 — Category mặc định của Brand làm fallback tính commission (P1) — ✅ ĐÃ CHỐT

- **Bối cảnh:** Trước đây, order không có `offer_id` mà cũng không có/không map được `brand_category_id` → đẩy exception `category mapping missing`, không tính được commission.
- **✅ Quyết định (2026-07-22):** Bổ sung **category mặc định của Brand**. Khi Brand **không gửi** category id (hoặc category id không map được) → dùng **category mặc định của Brand** để tính commission, **thay vì** báo exception.
- **Thứ tự resolve commission (đã cập nhật theo quyết định item-level):**
  1. Order Item có `brand_offer_code` do Brand gửi và mapping/rule Offer hợp lệ → dùng **Offer-level commission**. Offer được ghi nhận tại click/URL chỉ phục vụ attribution, không quyết định commission.
  2. Item không áp dụng Offer nhưng có `brand_category_id/code` map được → dùng **Category-level commission**.
  3. Không có/không map được category id → dùng **Category mặc định của Brand**.
  4. **Chỉ** đẩy exception khi Brand **chưa cấu hình** category mặc định hoặc không có commission rule hợp lệ nào.
- **Tài liệu ảnh hưởng:** M-BRO (Brand Category Mapping & Commission — thêm cờ "default category"; mockup màn thêm category cho Brand), M-ORD (logic tính commission, exception `category mapping missing`), FNL (mục 23/24 mapping, mục 36 commission calc).
- **Hành động cập nhật tài liệu:**
  - M-BRO: thêm thuộc tính **`is_default_category`** (hoặc `default_category_id` ở cấp Brand) trong Brand Category Mapping; mockup "Thêm category cho Brand" cho phép đánh dấu 1 category là mặc định; validate mỗi Brand có tối đa 1 default active.
  - M-ORD: cập nhật bước resolve commission theo thứ tự trên; thu hẹp exception `category mapping missing` chỉ còn khi thiếu default + thiếu rule.
  - FNL: cập nhật mục 23/24 (thêm cột default) và mục 36 (fallback default).
- **Liên hệ:** giảm đáng kể ca không tính được hoa hồng (CR-04 — nay đẩy Exception queue thay vì status) và exception `category mapping missing` (CR-17).
- **Quyết định cần chốt kèm theo:** Brand **bắt buộc** phải có category mặc định trước khi go-live không? (Đề xuất: có, để tránh mọi order thiếu category rơi vào exception.)

### CR-24 — Offer commission là tùy chọn; thiếu thì fallback về Category (P1) — ✅ ĐÃ CHỐT

- **Bối cảnh:** Offer commission là tùy chọn. Việc End User click Offer chỉ tạo attribution context; commission của giao dịch phải được resolve theo dữ liệu thực tế Brand gửi trên từng Order Item.
- **Vấn đề:** Offer không nhất thiết là chương trình có hoa hồng riêng. Offer có thể chỉ là **chương trình giới thiệu / điều hướng khách hàng đến đích** (landing, campaign link). Bắt buộc nhập commission làm không tạo được loại Offer này.
- **✅ Quyết định (2026-07-22):**
  1. **Offer commission KHÔNG bắt buộc.** Offer vẫn được Active/publish khi không có commission (chỉ cần Brand active, Destination URL hợp lệ, title default locale).
  2. **Nếu Order Item có `brand_offer_code` thực tế và mapping/rule Offer Active** → item tính theo **Offer commission**.
  3. Offer đã click/URL không được dùng thay cho `brand_offer_code` của item; item không áp dụng Offer được xử lý theo Category/Category Default theo Order Transaction SRS.
- **Thứ tự resolve commission (cập nhật, thay thế thứ tự ở CR-23):**
  1. Order Item có `brand_offer_code` thực tế và mapping/rule Offer **active + còn hiệu lực** → **Offer commission**.
  2. Không lấy `offer_id` trong Click Tracking Record để quyết định commission source của item.
  3. Nhánh Category: có `brand_category_id/code` map được → **Category commission**.
  4. Không có/không map được category id → **Category mặc định của Brand** (CR-23).
  5. Không resolve được rule nào → exception (`commission_rule_missing` / `default_category_missing`).
- **Traceability:** ghi rõ `commission_source` = `Offer` / `Category` / `DefaultCategory` để phân biệt ca fallback khi đối soát.
- **Tài liệu & vị trí cần sửa:**
  - **M-BRO** (`brand-offer-management-module-04-template.md`):
    - dòng 693 (điều kiện Active), 729 (rule nút Save), 785 & 824 (rule sửa Offer), 881–882 (validate khi đổi Active + thông báo lỗi), 890 & 899 (Active validation) → **bỏ điều kiện "Offer commission hợp lệ"**.
    - `BR-OFFER-002-04` → Offer commission được resolve theo `brand_offer_code` thực tế của từng Order Item; Offer đã click/URL chỉ dùng attribution.
    - dòng 750 `BR-OFFER-002-05` ("Offer commission bắt buộc khi Active") → **xóa hoặc đảo thành optional**.
    - dòng 759 `AC-OFFER-002-04` → bỏ vế commission; bổ sung AC mới: Offer không có commission vẫn Active được.
  - **M-ORD** (`order-transaction-management-module-04-template.md`):
    - dòng 429 (bảng resolve commission) và dòng 444 `BR-COM-001-02` → viết lại theo thứ tự 5 bước ở trên.
    - dòng 260 `BR-ORD-001-06` → bổ sung ca "có `offer_id` nhưng Offer thiếu commission active".
    - Bổ sung AC mới: order có `offer_id`, Offer không có commission → tính theo Category/Default category, **không** tạo exception.
    - Bổ sung giá trị `commission_source` cho ca fallback.
  - **FNL** (`function-list/...`): mục 14 (dòng 39) bỏ "commission bắt buộc khi Active Offer"; mục 16 (dòng 41) bỏ "Nếu thiếu Offer commission thì chỉ cho lưu Draft"; mục 36 cập nhật logic fallback.
  - **ANL**: `BRULE-008` (dòng 123) và `FR-008` → bổ sung ca Offer không có commission.
  - **Mockup** (`mockups/cms-offer-create.html`): dòng 586/593/601 bỏ dấu `*` bắt buộc ở Commission type / value / Effective from; dòng 505 & 582 sửa lại ghi chú ("Nếu Offer không cấu hình commission, hoa hồng tính theo Category của Brand"); bỏ câu "Nếu thiếu commission, Offer chỉ được lưu Draft".
- **Lưu ý validate:** khi Admin **có** nhập commission thì vẫn áp rule cũ (`commission_value > 0`, Percentage `<= 100` — CR-13). Chỉ bỏ tính **bắt buộc**, không nới lỏng validate giá trị.
- **Tinh chỉnh bổ sung khi triển khai (2026-07-22):** Offer commission **không có `effective_from`/`effective_to` riêng** (M-BRO `BR-OFFER-002-06`); hiệu lực của Offer commission lấy theo **Start date/End date và status của chính Offer**. Field commission ở cấp Offer rút còn `commission_type` + `commission_value`.
- **✅ Đã áp dụng & verify (2026-07-22):** M-BRO (`BR-OFFER-002-05/-06`, `BR-011`, `AC-OFFER-002-03/-04`, `AC-OFFER-003-02`, `AC-OFFER-004-03`, màn Active dòng 881), M-ORD (`BR-ORD-001-06`, bảng resolve dòng 430 đúng 4 bước, `BR-COM-001-02`, `AC-ORD-001-06`, `AC-COM-001-02A`), FNL (mục 14 & 16), SRS chính (`RULE-007`), mockup `cms-offer-create.html` (bỏ dấu `*`, ghi chú "Không bắt buộc").

---

## Nhóm C — Mâu thuẫn phạm vi & quyền sở hữu chức năng (P1)

### CR-08 — Chốt module sở hữu & chủ thể cấu hình "Earn Display" (P1) — ✅ ĐÃ CHỐT

- **Vấn đề:** M-TEN để "Customer earn display" **Out of Scope** (OQ-TENANT-003: module riêng, rule còn pending). Nhưng M-TP (TP-EARN-001/002), M-LP (LP-008), M-BRO (BR-010) đặc tả/tiêu thụ nó như **MVP1 Must**. FNL còn cấu hình earn display ở **cả** CMS (mục 26) lẫn Tenant Portal (mục 47–48).
- **Tài liệu ảnh hưởng:** M-TEN, M-TP, M-LP, M-BRO, FNL.
- **✅ Quyết định (2026-07-22):** **Tenant Portal** là nơi (duy nhất) cấu hình Earn Display. Tenant tự nhập text hiển thị theo Brand + override Category/Offer, đa ngôn ngữ, chỉ để hiển thị (không auto tính/cộng).
- **Hành động cập nhật tài liệu:**
  - FNL: **bỏ** mục 26 "Tenant Offer Earn Display" ở nhóm CMS (tránh trùng); giữ mục 47–48 ở Tenant Portal.
  - M-TEN: gỡ trạng thái "out of scope/pending", chỉ ghi rõ earn display do Tenant Portal sở hữu; đóng OQ-TENANT-003.
  - M-TP (TP-EARN-001/002): xác nhận là nguồn chân lý; M-LP (LP-008) tiêu thụ theo thứ tự Offer → Category → Brand.
  - M-BRO (BR-010): sửa mô tả "earn display configured per Tenant" → "cấu hình tại Tenant Portal".

### CR-09 — Chốt chủ thể & thứ tự ưu tiên visibility, hợp nhất schema (P1) — ✅ ĐÃ CHỐT

- **Vấn đề:** Hai tầng visibility với schema khác nhau, không định nghĩa ai thắng: Admin CMS (`visibility_scope = Hidden/All active offers/Custom offers` + status Active/Inactive) vs Tenant Portal (`visibility_status = Visible/Hidden` + `offer_visibility_mode`). Tài liệu gốc lại nói visibility là Admin-only (BRULE-024). Rủi ro tracking: 1 click "hiển thị" theo tầng này nhưng "ẩn" theo tầng kia.
- **Tài liệu ảnh hưởng:** BRD/ANL (BRULE-024, FR-013), M-TEN (CMS-TENANT-VIS), M-TP (TP-BRAND-002/TP-OFFER-001), M-LP.
- **✅ Quyết định (2026-07-22):** Áp dụng **mô hình 2 tầng**:
  1. **Tầng 1 (Admin/Ops):** assign = tập Brand/Offer **được phép** hiển thị cho Tenant (pool).
  2. **Tầng 2 (Tenant Portal):** Tenant bật/tắt hiển thị **trong pool** đã được assign.
  3. **Quy tắc hiệu lực cuối (AND):** `EU thấy = (Admin-assigned Active) AND (Tenant-visible)`.
  4. **Mặc định:** khi Tenant chưa thao tác → theo Admin (Brand/Offer đã assign Active thì hiển thị).
- **Hành động cập nhật tài liệu:**
  - BRD/ANL: sửa BRULE-024/FR-013 bỏ "Admin-only", mô tả 2 tầng + quy tắc AND.
  - Hợp nhất schema: dùng chung tên field/enum giữa M-TEN và M-TP cho 2 tầng (ví dụ tầng Admin = `assignment_status`, tầng Tenant = `tenant_visibility_status`); định nghĩa rõ để tránh trùng tên khác nghĩa.
  - M-LP: catalog lọc theo công thức AND.

### CR-10 — "3 tab lịch sử đơn End user": Must hay Deferred (P1) — ✅ ĐÃ CHỐT

- **Vấn đề:** BR-017/BRULE-017/FR-023/UC-015 coi 3 tab (`Chờ xử lý/Đã hoàn điểm/Đã hủy`) là Must; FNL đưa vào **P6 (Deferred)**.
- **Tài liệu ảnh hưởng:** BRD, ANL, SRS, UCL, FNL.
- **✅ Quyết định (2026-07-22, làm rõ 2026-07-29):** Chỉ 3 tab Cashback/Point History của End user → **Deferred sau MVP1** vì phụ thuộc cashback/point posting. `Basic My Orders` gồm danh sách Order, Order Status và chi tiết item vẫn thuộc MVP1.
- **Hành động cập nhật tài liệu:**
  - BRD: gỡ BR-017 khỏi Must (→ deferred); đưa BRULE-017 về diện deferred.
  - ANL/SRS: chỉ defer Cashback/Point History ba tab; giữ Basic My Orders trong screen behavior MVP1.
  - UCL: UC-015 được dùng cho Basic My Orders (MVP1 = Yes); Cashback/Point History được ghi riêng trong danh sách Deferred.

### CR-11 — Định nghĩa lại vai trò `pending_days` trong MVP1 mới (P2) — ✅ ĐÃ CHỐT

- **Vấn đề:** Gốc: pending_days để trì hoãn cộng điểm. MVP1 mới bỏ cộng điểm nhưng vẫn giữ pending_days với ghi chú lấp lửng "nếu còn dùng cho đối soát".
- **Tài liệu ảnh hưởng:** BRD (BR-015), ANL (FR-007/025), FNL (mục 6, 35), M-BRO, M-ORD (provisional → official).
- **✅ Quyết định (2026-07-22):** `pending_days` = **thời gian chốt commission**. Khi order còn trong pending_days: doanh thu/hoa hồng của Affiliate và Tenant là **tạm tính (provisional)**. Khi `pending_days` hết hạn (và order không bị cancel/refund): hệ thống **chốt chính thức** — `provisional_* → official` (`gross_commission_amount`, `tenant_share_amount`, `affiliate_keep_amount` trở thành số chính thức, set `official_calculation_at`).
- **Hành động cập nhật tài liệu:**
  - BRD (BR-015): đổi mô tả từ "chờ n ngày trước khi cộng điểm" → "chờ n ngày trước khi chốt commission chính thức".
  - ANL (FR-007/025): pending_until = mốc chuyển provisional → official (bỏ liên hệ cộng điểm).
  - FNL (mục 6): bỏ ghi chú lấp lửng "nếu còn dùng cho đối soát"; nêu rõ pending_days = mốc chốt commission.
  - M-ORD: gắn rõ transition `order_status: Pending → Confirmed` xảy ra tại `pending_until`, đồng thời set `official_calculation_at` và chuyển số tạm tính thành số chính thức (không dùng `commission_status` — xem CR-04).
- **Liên hệ CR-06:** đây là định nghĩa vòng đời cho các provisional field đã bổ sung.

### CR-12 — Làm rõ quan hệ bộ "Đăng ký/OTP" với Affiliate Platform (P2) — ❌ KHÔNG ÁP DỤNG

- **Vấn đề:** Tài liệu affiliate giả định EU đã là loyalty member của Tenant (map qua member_ref). Bộ Đăng ký/OTP mô tả luồng tự đăng ký Customer bằng SĐT trên mobile app.
- **❌ Quyết định (2026-07-22):** Bộ Đăng ký/OTP **không liên quan** phạm vi Affiliate Marketplace — là tài liệu/feature độc lập. Không cần đồng bộ chéo. CR này **đóng, không xử lý**.

---

## Nhóm D — Không nhất quán chi tiết (P2)

### CR-13 — Chuẩn hóa validate `commission_value` (Fixed >=0 vs >0) (P2) — ✅ ĐÃ CHỐT

- **Vấn đề:** Màn hình cho Fixed `>= 0`; phần Data/Logic yêu cầu `> 0` → Fixed = 0 vừa được phép vừa bị cấm (Category, Offer, Revenue share).
- **Tài liệu ảnh hưởng:** M-BRO (§5, §7, V.2, V.3), M-TEN (RS-002, V.4).
- **✅ Quyết định (2026-07-22):** Chốt theo đề xuất — `commission_value > 0` cho mọi loại (không cho phép 0). Percentage: `> 0 và <= 100`.
- **Hành động cập nhật tài liệu:** Sửa các bảng màn hình đang ghi `>= 0` thành `> 0` (M-BRO §5/§7, M-TEN RS-002); đồng bộ với phần Data Req.

### CR-14 — Đồng bộ enum trạng thái user Tenant (P2) — ✅ ĐÃ CHỐT

- **Vấn đề:** Quyết định cũ bỏ `Locked` không còn phù hợp với nghiệp vụ Tenant Portal tự động khóa tài khoản sau 5 lần đăng nhập sai liên tiếp.
- **Tài liệu ảnh hưởng:** M-TEN (tài khoản Tenant Portal do CMS quản lý), M-TP (Login, Account Management, Data Requirements và Security Rules).
- **✅ Quyết định cập nhật (2026-07-30):** Tài khoản đăng nhập **Tenant Portal** thống nhất có ba trạng thái **`Active / Inactive / Locked`**.
- **Hành động cập nhật tài liệu:**
  - `Active`: tài khoản được phép đăng nhập khi Tenant và Role cũng Active và user có permission phù hợp.
  - `Inactive`: trạng thái quản trị; tài khoản bị chặn đăng nhập và session/token hiện hành bị thu hồi.
  - `Locked`: trạng thái bảo mật do Auth Service tự động thiết lập tại lần đăng nhập sai Password liên tiếp thứ 5; tài khoản bị chặn đăng nhập và session/token hiện hành bị thu hồi.
  - Chỉ Tenant Admin có quyền quản lý Account mới được mở khóa bằng cách chuyển `Locked → Active`; thao tác mở khóa reset failed-login counter.
  - Forgot Password không tự động mở khóa tài khoản `Locked`.
  - CMS Tenant Management phải hiển thị đúng trạng thái `Locked` của tài khoản Tenant Portal được đồng bộ từ Tenant User/Auth Service.
  - Quyết định này chỉ áp dụng cho tài khoản Tenant Portal; không định nghĩa hoặc thay đổi enum trạng thái của tài khoản đăng nhập Admin CMS.

### CR-15 — Định nghĩa hoặc bỏ trạng thái Offer "Published/Ready" (P2) — ✅ ĐÃ CHỐT

- **Vấn đề:** Quy ước M-BRO nhắc Offer "Ready/Published", Landing gate `Active/Published` (BR-LP-001-03), nhưng enum chính thức chỉ `Draft/Active/Inactive`.
- **Tài liệu ảnh hưởng:** M-BRO, M-LP.
- **✅ Quyết định (2026-07-22):** Chốt theo đề xuất — enum Offer duy nhất = **`Draft / Active / Inactive`**. Thay mọi tham chiếu "Published/Ready" bằng "Active".
- **Hành động cập nhật tài liệu:** M-BRO — gỡ "Ready/Published" khỏi quy ước; M-LP — sửa gate BR-LP-001-03 từ `Active/Published` → `Active`.

### CR-16 — Loại bỏ kiểm tra thời hạn theo click (P1) — ✅ ĐÃ XỬ LÝ

- **Quyết định:** Loại bỏ toàn bộ cấu hình và kiểm tra thời hạn tính commission theo thời điểm click khỏi MVP1.
- **Rule mới:** Order success chỉ cần match `click_id` hợp lệ với click record và context Tenant/Brand/Offer; không kiểm tra thời lượng kể từ thời điểm click.
- **Exception:** Dùng `click_id_invalid` khi thiếu click_id, click_id không tồn tại, đã bị dùng sai rule idempotency hoặc không match context.
- **Tài liệu ảnh hưởng:** Đã cập nhật ANL, FNL, M-ORD, BRD, usecase list, landing page SRS và diagram liên quan.
- **✅ Đã verify (2026-07-22):** Quét toàn bộ `docsaff/` (trừ thư mục change-requests) — **0 tham chiếu** còn lại tới `attribution`, `attribution_fail`, `BRULE-010`. Các kết quả chứa từ "window" còn lại đều không liên quan (Measurement window ở bảng metric BRD; session/action window cho chống double-click; "Key attributes" ở tiêu đề bảng).
- **Hệ quả:** Attribution do phía Brand tự xử lý; Platform tin theo `click_id` Brand gửi kèm. Không còn giới hạn thời gian giữa `clicked_at` và `order_success_at`.

### CR-17 — Sửa đánh số business rule bị nhảy trong M-ORD (P2)

- **Vấn đề:** COM rules nhảy BR-COM-001-01 → -03, -04, -06... (thiếu -02, -05). Nghi rule xử lý `tenant_share_rule_missing` bị rơi.
- **Tài liệu ảnh hưởng:** M-ORD (COM business rules, exception types, OQ #4).
- **Thay đổi đề xuất:** Bổ sung rule còn thiếu, đặc biệt định nghĩa hành vi khi thiếu tenant-share rule (block → exception `tenant_share_rule_missing`, hay default rate = 0). Đánh số lại liên tục.
- **Quyết định cần chốt:** Thiếu tenant-share rule thì block hay default 0.
- **Liên hệ CR-23:** với **commission** cấp Brand→Affiliate đã có fallback category mặc định (không còn `category mapping missing` khi thiếu category id). CR-17 tập trung phần **tenant-share** còn lại. Cân nhắc áp dụng logic default tương tự cho tenant-share rule.

### CR-18 — Thống nhất kiểu ngày earn display (Date vs Datetime) (P3) — ✅ ĐÃ CHỐT

- **Vấn đề:** M-TP dùng `Date` cho `effective_from/to`; M-LP dùng `Datetime` cho cùng entity.
- **Tài liệu ảnh hưởng:** M-TP (V.4), M-LP (V.6).
- **✅ Quyết định (2026-07-22):** Dùng **`Datetime`** cho `effective_from/effective_to` (nhất quán với các effective period khác).
- **Hành động cập nhật tài liệu:** M-TP (V.4) đổi `Date` → `Datetime`; M-LP giữ nguyên `Datetime`.

### CR-19 — Sửa off-by-one giới hạn sai OTP (P3) — ❌ KHÔNG CÒN ÁP DỤNG

- **Vấn đề (ban đầu):** BRULE-005 "sai OTP tối đa 5 lần" nhưng decision/FR-009 dùng `failed_attempt_count > 5` → chưa rõ block ở lần thứ 5 hay 6.
- **❌ Cập nhật (2026-07-22):** Hai file tài liệu OTP (`srs/account-registration-otp.md`, `analysis/account-registration-otp-analysis.md`) **đã bị gỡ khỏi bộ `docsaff/`** (nhất quán với CR-12 — OTP không thuộc phạm vi affiliate). CR này **moot, đóng không xử lý**. Nếu tài liệu OTP được đưa vào lại ở nơi khác thì áp quyết định `failed_attempt_count >= 5` (chặn ở lần sai thứ 5).
- **✅ Đã verify (2026-07-22):** `find docsaff/ -iname "*otp*"` chỉ còn 2 file PNG asset; không còn file `.md` OTP.

---

## Nhóm E — Housekeeping (P3)

### CR-20 — Xây permission catalog thống nhất + chốt quyền Viewer xem tài chính (P3)

- **Vấn đề:** CMS dùng action dấu chấm (`tenant.visibility.update`...), Tenant Portal dùng kiểu khác (`brand_visibility.manage`...); chưa có catalog quyền hợp nhất. "Viewer thấy tài chính không" để treo (OQ M-TP #2).
- **Tài liệu ảnh hưởng:** M-TEN, M-ORD, M-TP.
- **Thay đổi đề xuất:** Lập 1 bảng permission catalog (CMS + Tenant Portal). Chốt Viewer có/không thấy commission/tenant_share.

### CR-21 — Giải quyết các Open Question còn treo (P2)

- **Vấn đề:** 5 câu hỏi mở lặp ở nhiều tài liệu vẫn chưa chốt dù SRS đã "READY": (a) cơ chế API cancel/refund; (b) danh sách locale MVP1; (c) retry policy loyalty API (nếu còn liên quan sau CR-01); (d) EU chưa định danh có được click/mua; (e) settlement cycle. Cộng thêm OQ trong từng module (partial refund, post-settlement adjustment, password reset, export limit...).
- **Tài liệu ảnh hưởng:** Toàn bộ.
- **Thay đổi đề xuất:** Lập bảng theo dõi open question với owner + hạn chốt; giải quyết trước khi khóa SRS/API contract. Loại (c) khỏi MVP1 nếu CR-01 defer loyalty.

### CR-22 — Cập nhật metadata & phê duyệt tài liệu (P3)

- **Vấn đề:** Tất cả file `Status: Draft`, Owner/Business owner **TBD**, bảng phê duyệt toàn Pending; metric BRD phần lớn baseline/target = TBD.
- **Tài liệu ảnh hưởng:** Toàn bộ.
- **Thay đổi đề xuất:** Gán Owner thực, điền baseline/target đo được, chạy vòng phê duyệt sau khi CR-01/CR-02 được chốt. Cập nhật "Last updated" + revision history khi áp dụng các CR.

---

## Bảng tổng hợp ưu tiên

| CR | Tiêu đề | Severity | Phụ thuộc | Trạng thái |
|---|---|---|---|---|
| CR-01 | Chốt phạm vi MVP1 (cashback/điểm in/out) | P0 | — | ✅ Đã chốt |
| CR-02 | Đồng bộ mô hình commission tài liệu gốc | P0 | CR-01 | ✅ Đã chốt |
| CR-03 | Enum order_status | P0 | — | ✅ Đã chốt |
| CR-04 | Bỏ hẳn commission_status (suy từ order_status) | P0 | CR-03 | ✅ Đã chốt |
| CR-05 | Tenant share chỉ dạng % | P0 | — | ✅ Đã chốt (có thể xem lại) |
| CR-06 | Provisional fields vào data model M-TP | P1 | CR-04 | ✅ Đã chốt |
| CR-07 | provisional_affiliate_keep_amount ở creation fields | P2 | — | ⏳ Chưa chốt |
| CR-08 | Chủ thể/module sở hữu Earn Display | P1 | CR-01 | ✅ Đã chốt & áp |
| CR-09 | Chủ thể + ưu tiên visibility, hợp nhất schema | P1 | — | ✅ Đã chốt & áp |
| CR-10 | 3 tab lịch sử End user: Must/Deferred | P1 | CR-01 | ✅ Đã chốt |
| CR-11 | Vai trò pending_days MVP1 mới | P2 | CR-01 | ✅ Đã chốt |
| CR-12 | Quan hệ Đăng ký/OTP với Platform | P2 | — | ❌ Không áp dụng |
| CR-13 | Validate commission_value | P2 | — | ✅ Đã chốt |
| CR-14 | Enum Tenant Portal User (`Active / Inactive / Locked`) | P2 | — | ✅ Đã chốt & áp |
| CR-15 | Offer "Published/Ready" | P2 | — | ✅ Đã chốt |
| CR-16 | Loại bỏ kiểm tra thời hạn theo click | P1 | — | ✅ Đã xử lý |
| CR-17 | BR numbering M-ORD + tenant_share_rule_missing | P2 | — | ⏳ Chưa chốt |
| CR-18 | Kiểu ngày earn display | P3 | CR-08 | ✅ Đã chốt & áp |
| CR-19 | Off-by-one OTP | P3 | — | ❌ Không còn áp dụng (file OTP đã gỡ) |
| CR-20 | Permission catalog + Viewer financial | P3 | — | ⏳ Chưa chốt |
| CR-21 | Open questions còn treo | P2 | CR-01 | ⏳ Chưa chốt |
| CR-22 | Metadata & phê duyệt | P3 | CR-01, CR-02 | ⏳ Chưa chốt |
| CR-23 | Category mặc định của Brand làm fallback commission | P1 | CR-02 | ✅ Đã chốt |
| CR-24 | Offer commission tùy chọn; thiếu thì fallback Category | P1 | CR-23 | ✅ Đã chốt |

> **Ghi chú:** CR-03, CR-04, CR-06, CR-11, CR-23 đã chốt và nhất quán với nhau — chỉ còn **một** trục trạng thái là `order_status` = `Pending / Confirmed / Cancelled`; chuyển `Pending → Confirmed` tại `pending_until` (đồng thời số tạm tính → chính thức). Không còn `commission_status`. Mọi ca lỗi (đơn không hợp lệ, không tính được hoa hồng) đều đi vào **Exception queue**.

## Trình tự triển khai đề xuất

1. **Sprint chốt quyết định:** CR-01, CR-02, CR-05, CR-08, CR-09, CR-16 (các quyết định gốc).
2. **Sprint đồng bộ enum/data model:** CR-03, CR-04, CR-06, CR-07, CR-14, CR-15, CR-17, CR-18.
3. **Sprint dọn phạm vi & mô tả:** CR-10, CR-11, CR-12, CR-13, CR-19, CR-21.
4. **Sprint housekeeping & phê duyệt:** CR-20, CR-22.
