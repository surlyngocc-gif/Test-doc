# Wireframe Specification: White-label Affiliate Marketplace Landing Page

## Document control

- Status: Draft
- Owner: TBD
- Related discovery: Conversation discovery brief for Affiliate Marketplace Platform
- Related analysis: [docs/analysis/affiliate-marketplace-platform-analysis.md](../analysis/affiliate-marketplace-platform-analysis.md)
- Related modeling: [docs/modeling/affiliate-marketplace-platform-modeling.md](../modeling/affiliate-marketplace-platform-modeling.md)
- Related BRD: [docs/brd/affiliate-marketplace-platform.md](../brd/affiliate-marketplace-platform.md)
- Last updated: 2026-07-26

## Status

`READY_FOR_SRS`

## Summary

Wireframe này mô tả landing page marketplace white-label dành cho End user của Tenant. Trang hiển thị Brand/Offer được Platform assign cho Tenant và đáp ứng điều kiện hiển thị, cho phép End user tìm kiếm/lọc, xem Earn/Cashback Display Text do Tenant cấu hình, click sang website chính thức của Brand và truy cập `My Orders` để tra cứu thông tin đơn hàng cơ bản phát sinh qua Nền tảng ưu đãi liên kết. MVP1 không cấu hình Cashback B1, không tính điểm/cashback và không hiển thị lịch sử hoàn thưởng/point posting.

Wireframe tập trung vào cấu trúc, hành vi, trạng thái và traceability. Không mô tả visual design high-fidelity.

## Actors and user goals

| Actor | Goal | Related screens | Notes |
|---|---|---|---|
| End user | Xem ưu đãi, tìm Brand/Offer, click sang Brand | WF-001 | Có thể định danh qua member reference để đảm bảo quyền lợi; nếu chưa định danh vẫn được click/mua sau warning |
| Affiliate Platform | Resolve Tenant, lọc catalog, tracking click, redirect | WF-001 | Chỉ hiển thị Brand/Offer active và visible theo rule 2 tầng |
| Admin/Ops | Không thao tác trên landing page | N/A | Cấu hình Brand, Offer, assignment và commission trong CMS; Earn/Cashback Display Text do Tenant cấu hình tại Tenant Portal |

## Screen inventory

| Screen ID | Screen name | Purpose | Actor | Related requirement |
|---|---|---|---|---|
| WF-001 | Landing page marketplace white-label | Hiển thị catalog Brand/Offer theo Tenant, cho phép tìm/lọc và click sang Brand | End user | FR-014, FR-015, FR-016, FR-017, FR-018, FR-031, BRULE-012, BRULE-013, BRULE-022, BRULE-023, BRULE-024 |

## Navigation map

```text
Tenant white-label domain
  -> WF-001 Landing page marketplace
     -> Search/filter Brand/Offer
     -> Offer detail preview/section on page
     -> Click "Mua ngay" / "Xem ưu đãi"
        -> Platform creates click_id
        -> Redirect to Brand destination URL
     -> "Đơn hàng của tôi"
        -> My Orders: danh sách thông tin đơn hàng cơ bản
     -> Empty state: no assigned active Brand/Offer
     -> Error state: domain/config/catalog error
```

## Screen specifications

### WF-001 — Landing page marketplace white-label

#### Purpose

Cho phép End user truy cập marketplace của Tenant, xem Brand/Offer được phép hiển thị, đọc Earn/Cashback Display Text do Tenant cấu hình, click sang Brand để mua hàng và tra cứu các đơn hàng cơ bản đã phát sinh qua nền tảng.

#### Related requirements

- FR-014: Hiển thị marketplace theo Tenant
- FR-015: Hiển thị Brand/Offer theo Tenant assignment
- FR-016: Hiển thị Offer và Earn/Cashback Display Text theo Brand/Category/Offer
- FR-017: Ghi nhận click tracking
- FR-018: Redirect sang Brand
- FR-031: Tracking click không tính CPC
- BRULE-012: Offer có Status = `Active` và còn hiệu lực mới được hiển thị
- BRULE-013: Mỗi outbound click có click_id duy nhất
- BRULE-022: Chỉ tracking click, không tính CPC billing
- BRULE-023: MVP1 chỉ hiển thị Earn/Cashback Display Text; không cấu hình hoặc tính Cashback B1/điểm
- BRULE-024: Brand/Offer mặc định ẩn nếu chưa có assignment active

#### Low-fidelity layout - desktop

```text
+----------------------------------------------------------------------------------+
| Tenant logo                                      [Ngôn ngữ v] [Đơn hàng của tôi] |
+----------------------------------------------------------------------------------+
| Hero / intro                                                                      |
| "Ưu đãi dành riêng cho hội viên <Tenant>"                                         |
| [Search: Tìm thương hiệu hoặc ưu đãi...]                                          |
+----------------------------------------------------------------------------------+
| Danh mục / Bộ lọc                                                                 |
| [Tất cả] [Du lịch] [Ăn uống] [Mua sắm] [Dịch vụ]                                |
+----------------------------------------------------------------------------------+
| Featured offers                                                                   |
| +----------------------+ +----------------------+ +----------------------+       |
| | Brand logo           | | Brand logo           | | Brand logo           |       |
| | Tên Brand            | | Tên Brand            | | Tên Brand            |       |
| | Tên ưu đãi           | | Tên ưu đãi           | | Tên ưu đãi           |       |
| | Nhận 20 điểm/20.000đ | | Xem quyền lợi        | | Hoàn đến 50.000đ     |       |
| | Điều kiện ngắn       | | Điều kiện ngắn       | | Điều kiện ngắn       |       |
| | [Xem ưu đãi]         | | [Xem ưu đãi]         | | [Xem ưu đãi]         |       |
| +----------------------+ +----------------------+ +----------------------+       |
+----------------------------------------------------------------------------------+
| Tất cả thương hiệu / ưu đãi                                                       |
| Sort: [Phổ biến v]       View: [Grid/List]                                        |
| +----------------------+ +----------------------+ +----------------------+       |
| | Brand/Offer card     | | Brand/Offer card     | | Brand/Offer card     |       |
| +----------------------+ +----------------------+ +----------------------+       |
| +----------------------+ +----------------------+ +----------------------+       |
| | Brand/Offer card     | | Brand/Offer card     | | Brand/Offer card     |       |
| +----------------------+ +----------------------+ +----------------------+       |
+----------------------------------------------------------------------------------+
| Footer: Điều khoản | Chính sách dữ liệu | Hỗ trợ                               |
+----------------------------------------------------------------------------------+
```

#### Low-fidelity layout - mobile

```text
+----------------------------------+
| Tenant logo        [Menu]        |
+----------------------------------+
| "Ưu đãi dành riêng cho hội viên" |
| [Tìm Brand/Offer...]             |
+----------------------------------+
| [Tất cả] [Mua sắm] [Ăn uống] ... |
+----------------------------------+
| Featured                         |
| +------------------------------+ |
| | Brand logo                   | |
| | Tên Brand                    | |
| | Tên ưu đãi                   | |
| | Nhận 20 điểm/20.000đ         | |
| | [Xem ưu đãi]                 | |
| +------------------------------+ |
| +------------------------------+ |
| | Brand/Offer card             | |
| +------------------------------+ |
+----------------------------------+
| [Đơn hàng của tôi] [Hỗ trợ]      |
+----------------------------------+
```

#### Brand/Offer card layout

```text
+--------------------------------------+
| Brand logo        Badge: "Mới"        |
| Tên Brand                            |
| Tiêu đề ưu đãi                       |
| Mô tả ngắn / điều kiện chính         |
| Earn/Cashback Display Text           |
| Hiệu lực đến: <date>                 |
| [Xem ưu đãi]                         |
+--------------------------------------+
```

Nếu Tenant chưa cấu hình Earn/Cashback Display Text phù hợp:

```text
+--------------------------------------+
| Brand logo                            |
| Tên Brand                             |
| Tiêu đề ưu đãi                        |
| Mô tả ngắn / điều kiện chính          |
| [Xem ưu đãi]                          |
+--------------------------------------+
```

#### Fields

| Field | Type | Required | Default | Validation | Source |
|---|---|---:|---|---|---|
| Tenant logo/branding | Display | Yes | Tenant branding config | Fallback nếu thiếu optional assets | FR-003, FR-014 |
| Ngôn ngữ | Select | Yes | Tenant default locale | Chỉ hiển thị locale được hỗ trợ | BRULE-021 |
| Search keyword | Text input | No | Empty | Trim whitespace; no submit required | WF behavior |
| Category filter | Segmented/list filter | No | `Tất cả` | Chỉ hiển thị category có offer active/assigned | FR-015 |
| Sort | Select | No | `Phổ biến` | Giá trị hợp lệ theo danh sách sort | WF behavior |
| Brand logo | Display | Yes | Brand asset | Ẩn card nếu Brand inactive | BRULE-006, BRULE-024 |
| Offer title | Display | Yes | Localized content | Fallback theo locale policy nếu thiếu bản dịch | BRULE-021 |
| Earn/Cashback Display Text | Display | Conditional | `Xem quyền lợi hiện có` | Hiển thị nội dung do Tenant cấu hình theo đúng Brand/Category/Offer context và locale; không dùng để tính điểm/cashback | FR-016, BRULE-023 |
| Offer validity | Display | No | N/A | Offer hết hạn không hiển thị/click | BRULE-012 |

#### Actions

| Action | Trigger | Result | Validation before action | Related requirement |
|---|---|---|---|---|
| Search | User nhập keyword | Danh sách Brand/Offer được lọc theo keyword | Catalog đã load | FR-015 |
| Select category | User chọn category | Danh sách lọc theo category | Category hợp lệ | FR-015 |
| Change language | User chọn ngôn ngữ | Reload content theo locale | Locale thuộc `vi-VN`, `en-US` | BRULE-021 |
| View offer / Xem ưu đãi | User click CTA trên card | Platform warning nếu chưa có member_ref, tạo click_id và redirect sang Brand | Tenant active, Offer active, visibility 2 tầng pass | FR-017, FR-018, BRULE-013, BRULE-024 |
| Open My Orders | User click `Đơn hàng của tôi` | Điều hướng sang màn My Orders và hiển thị các đơn hàng cơ bản phát sinh qua nền tảng | Scope đúng `tenant_id`; nếu có End User context thì scope thêm theo `member_ref/user_ref` | FR-023 |
| Retry load | User click retry trên error state | Load lại catalog | N/A | UI state |

#### States

| State | When it happens | UI behavior | User action |
|---|---|---|---|
| Loading | Đang resolve Tenant/catalog | Hiển thị skeleton header, filter, card placeholders | Chờ hoặc refresh |
| Empty | Không có Brand/Offer active assigned cho Tenant | Hiển thị thông báo: `Hiện chưa có ưu đãi phù hợp.`; ẩn section Featured | Thử đổi filter/search hoặc quay lại sau |
| No search result | Có catalog nhưng không match keyword/filter | Hiển thị `Không tìm thấy ưu đãi phù hợp.` | Xóa search/filter |
| Error - Tenant domain | Domain không resolve được Tenant hoặc inactive | Hiển thị lỗi cấu hình marketplace | Liên hệ hỗ trợ |
| Error - Catalog | Load catalog lỗi | Hiển thị thông báo lỗi và nút `Thử lại` | Retry |
| Error - Direct link blocked | User truy cập trực tiếp offer không assigned | Hiển thị `Ưu đãi không khả dụng trên marketplace này.` | Quay lại landing page |
| Success - Click accepted | Click hợp lệ | Không cần success screen; redirect sang Brand | N/A |
| Warning - Missing member reference | Member reference thiếu khi user click đi mua | Hiển thị warning rằng quyền lợi và việc đối chiếu giao dịch theo hội viên có thể không được đảm bảo; cho phép tiếp tục | Định danh hoặc tiếp tục mua |

#### Business and validation rules

| Rule ID | Rule | UI impact |
|---|---|---|
| BRULE-001 | Marketplace request phải resolve đúng một Tenant | Nếu fail, hiển thị error domain/config |
| BRULE-002 | Domain chỉ hoạt động khi DNS/SSL/config active | Nếu inactive, không hiển thị catalog |
| BRULE-003 | Marketplace render branding của Tenant | Header/theme dùng Tenant branding |
| BRULE-012 | Offer chỉ hiển thị khi Status = `Active` và còn hiệu lực | Ẩn Offer hết hạn, Draft hoặc Inactive |
| BRULE-013 | Mỗi outbound click có click_id duy nhất | CTA gọi tracking trước redirect |
| BRULE-021 | MVP1 hỗ trợ đa ngôn ngữ | Có control chọn ngôn ngữ nếu nhiều locale active |
| BRULE-022 | Chỉ tracking click, không tính CPC billing | Không hiển thị nội dung phí CPC |
| BRULE-023 | MVP1 không cấu hình Cashback B1, không tính điểm/cashback và không gọi Tenant Loyalty API | Chỉ render Earn/Cashback Display Text do Tenant cấu hình; không hiển thị giá trị điểm/cashback do Platform tính |
| BRULE-024 | Brand/Offer mặc định ẩn nếu chưa assigned active | Catalog chỉ gồm Brand/Offer assigned active |
| WF-BR-001 | `My Orders` thuộc MVP1 nhưng không phải Cashback/Point History | Hiển thị Brand Order ID, Brand, Order Date, Amount, Order Status, thao tác Copy/View và chi tiết item. Không hiển thị commission, Tenant Share, cashback, điểm hoặc point posting. Item `Refunded` có Final amount bằng `0` và không được cộng vào Amount trên Order header. |

#### Accessibility notes

- Search input có label rõ ràng.
- CTA `Xem ưu đãi` có accessible name gồm tên Brand/Offer.
- Card không chỉ dựa vào màu để thể hiện trạng thái.
- Keyboard focus đi theo thứ tự: header -> search -> filter -> cards -> footer.
- Trạng thái loading/error/empty có text rõ ràng.

#### Analytics / events

| Event | Trigger | Properties |
|---|---|---|
| marketplace_viewed | Landing page load thành công | tenant_id, locale, user_ref_available |
| catalog_loaded | Catalog load xong | tenant_id, offer_count, brand_count, locale |
| search_used | User nhập search | tenant_id, keyword_length, result_count |
| category_selected | User chọn category | tenant_id, category_id, result_count |
| offer_clicked | User click CTA | tenant_id, brand_id, offer_id, click_id, member_ref_available |
| my_orders_opened | User mở `Đơn hàng của tôi` | tenant_id, member_ref_available |
| direct_link_blocked | Offer direct link bị chặn | tenant_id, brand_id, offer_id, reason |

## Cross-screen behavior

### Permissions

- End user chỉ thấy Brand/Offer thuộc Tenant marketplace hiện tại.
- Tenant Admin/Admin/Ops không thao tác cấu hình trên landing page.
- Nếu thiếu member reference, CTA hiển thị warning về quyền lợi/đối chiếu hội viên nhưng không chặn redirect trong MVP1.
- My Orders phải luôn scope theo Tenant hiện tại; nếu runtime có `member_ref/user_ref` thì chỉ trả đơn hàng của End User tương ứng.

### Notifications

- Không dùng toast cho click success vì user được redirect ngay.
- Lỗi catalog/domain hiển thị inline trên page.
- Lỗi direct link hiển thị page-level message.

### Confirmations

- Không cần confirmation trước khi click `Xem ưu đãi` vì đây không phải hành động phá hủy hoặc tài chính trực tiếp trong Platform.

### Duplicate actions

- Nếu user double-click CTA, Platform chỉ nên tạo một click tracking hợp lệ hoặc xử lý idempotent theo session/action window.
- CTA có thể chuyển sang trạng thái disabled ngắn trong lúc tracking/redirect.

### Unsaved changes

- Không áp dụng. Landing page không có form lưu dữ liệu.

## Assumptions

- Landing page là trang End user của Tenant marketplace, không phải Admin landing page.
- Tenant branding config đã tồn tại trước khi page được public.
- Brand/Offer assignment đã được Admin/Ops cấu hình ở màn riêng.
- MVP1 không tính điểm dự kiến; chỉ hiển thị earn/cashback display text do Tenant cấu hình.
- Danh sách category là dữ liệu cấu hình/content, không hard-code trong wireframe.

## Open questions

| Question | Impact |
|---|---|
| Có cần trang offer detail riêng hay chỉ dùng card + redirect trực tiếp? | Ảnh hưởng navigation và screen inventory |
| Có cần hiển thị toàn bộ điều kiện của Offer trên Brand Detail hay chỉ hiển thị tóm tắt và `See more`? | Ảnh hưởng nội dung card và compliance copy |

## Closed decisions

| Decision | Answer |
|---|---|
| Ngôn ngữ MVP1 | `vi-VN`, `en-US`; default `vi-VN`. |
| End user chưa định danh member reference | Vẫn được click/mua; UI warning về quyền lợi và khả năng đối chiếu giao dịch theo hội viên. |
| Phạm vi My Orders | Thuộc MVP1; chỉ hiển thị thông tin đơn hàng cơ bản. Cashback/Point History và trạng thái hoàn thưởng được Deferred sau MVP1. |

## Traceability matrix

| Screen | UI element / action | Requirement | Acceptance criteria |
|---|---|---|---|
| WF-001 | Tenant header/branding | FR-014, BRULE-003 | N/A |
| WF-001 | Brand/Offer catalog | FR-015, BRULE-012, BRULE-024 | AC-001 |
| WF-001 | Earn/Cashback Display Text | FR-016, BRULE-023 | AC-004 |
| WF-001 | CTA `Xem ưu đãi` | FR-017, FR-018, BRULE-013 | AC-002 |
| WF-001 | No CPC billing behavior | FR-031, BRULE-022 | AC-002 |
| WF-001 | My Orders link | FR-023, WF-BR-001 | AC-005, AC-006 |
| WF-001 | Empty/error states | BRULE-001, BRULE-002, BRULE-024 | AC-001 |

## Readiness check

- Landing page actor and goal are identified.
- Primary browsing/click flow is represented.
- Brand/Offer visibility by Tenant is represented.
- Empty, loading, error, direct-link-blocked, and identity-needed states are covered.
- Click tracking and redirect behavior are specified.
- Earn/Cashback Display Text được tách khỏi logic tính điểm/cashback.
- My Orders cơ bản thuộc MVP1; Cashback/Point History được Deferred.
- Open questions are separated from assumptions.

`READY_FOR_SRS`
