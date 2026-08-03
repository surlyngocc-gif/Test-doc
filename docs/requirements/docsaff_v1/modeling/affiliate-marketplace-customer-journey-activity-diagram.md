# Activity Diagram: Hành trình khách hàng từ landing page đến ghi nhận commission cho Tenant

## Document control

- Status: Draft
- Owner: TBD
- Related modeling: [docs/modeling/affiliate-marketplace-platform-modeling.md](./affiliate-marketplace-platform-modeling.md)
- Related use cases: [docs/usecases/affiliate-marketplace-platform-usecase-list.md](../usecases/affiliate-marketplace-platform-usecase-list.md)
- Related mockup: [docs/mockups/affiliate-marketplace-landing-page-desktop.html](../mockups/affiliate-marketplace-landing-page-desktop.html)
- Last updated: 2026-07-23

## Scope

Activity diagram này mô tả hành trình End user từ lúc vào landing page white-label của Tenant, chọn Brand/Offer, được redirect sang Brand để mua hàng, Brand báo order success, Platform chờ số ngày theo cấu hình Brand, sau đó chốt commission Brand trả Affiliate và revenue share Affiliate chia Tenant.

Theo CR-01, MVP1 không làm cashback B1, không tính/cộng điểm cho End user và không gọi Tenant Loyalty API. Các nội dung earn/cashback nếu hiển thị trên landing page chỉ là display text do Tenant cấu hình.

## Activity diagram with swimlanes - PlantUML

```plantuml
@startuml
title Hành trình khách hàng từ landing page đến ghi nhận commission cho Tenant

skinparam shadowing false
skinparam activity {
  BackgroundColor #FFFFFF
  BorderColor #334155
  FontColor #17212F
  DiamondBackgroundColor #F8FAFC
  DiamondBorderColor #334155
}
skinparam swimlaneBorderColor #CBD5E1
skinparam swimlaneTitleBackgroundColor #E6F4F5
skinparam swimlaneTitleFontColor #095F78

|End user|
start
:Mở landing page marketplace của Tenant;

|White-label Marketplace|
:Resolve domain Tenant,\nngôn ngữ và branding;

|Affiliate Platform|
if (Tenant/domain active?) then (Có)
  |White-label Marketplace|
  :Load catalog theo Tenant;

  |Affiliate Platform|
  if (Brand/Offer active\nvà assigned cho Tenant?) then (Có)
    |White-label Marketplace|
    :Hiển thị Brand/Offer active\nđược assign cho Tenant;
    :Hiển thị earn/cashback display text\nnếu Tenant cấu hình;

    |End user|
    :Xem Top brands,\ncategory và offer;
    :Chọn Brand/Offer muốn mua;

    |White-label Marketplace|
    :Gửi yêu cầu tracking click;

    |Affiliate Platform|
    if (Có member reference hợp lệ?) then (Có)
      :Tạo Click Tracking Record\nvà click_id;
    else (Không)
      |White-label Marketplace|
      :Hiển thị warning:\nquyền lợi/cashback/đối chiếu\ncó thể không đảm bảo;

      |Affiliate Platform|
      :Tạo Click Tracking Record\nkhông có member_ref\nvà click_id;
    endif

    |White-label Marketplace|
    :Redirect sang Brand\nkèm tracking parameter;

    |Brand System|
    :Nhận user từ redirect;

    |End user|
    :Mua hàng trên website/app của Brand;

      |Brand System|
      :Ghi nhận mua hàng thành công;
      :Gửi API order success\nvề Platform;

      |Affiliate Platform|
      if (Order success hợp lệ?) then (Có)
        :Tạo Order/Conversion\ntrạng thái Pending;
        :Tính commission và revenue share\ntạm tính nếu đủ rule;
        :Set pending_until theo\nsố ngày chờ của Brand;

        if (Có cancel/refund item\ntrước khi chốt?) then (Có)
          :Chuyển item hợp lệ sang Refunded;
          :Tính lại Final Amount,\nGross Commission và Tenant Share;
          if (Tất cả item Refunded?) then (Có)
            :Chuyển Order sang\nCancelled;
            |End user|
            stop
          else (Không)
            :Giữ Order Pending nếu còn item Pending;\nConfirmed nếu item còn lại đều Confirmed;
          endif
        endif

        |Scheduler/System Job|
        :Chờ đến ngày xác nhận\ntheo pending_until;
        :Trigger job kiểm tra\norder đến hạn;

        |Affiliate Platform|
        if (Đến pending_until?) then (Có)
          :Chốt commission của\ncác item còn hợp lệ;
          :Chốt revenue share\nAffiliate chia Tenant;
          :Tổng hợp Order Status;
          :Đưa giao dịch vào\nreporting/reconciliation;
          stop
        else (Chưa)
          |Scheduler/System Job|
          :Tiếp tục chờ đến pending_until;
          stop
        endif
      else (Không)
        :Từ chối order hoặc\nđưa vào exception queue;

        |End user|
        stop
      endif
  else (Không)
    |White-label Marketplace|
    :Hiển thị empty state\nhoặc ẩn offer không hợp lệ;

    |End user|
    stop
  endif
else (Không)
  |White-label Marketplace|
  :Hiển thị lỗi domain/cấu hình;

  |End user|
  stop
endif

@enduml
```

## Main success path

| Step | Lane | Mô tả | Trace |
|---|---|---|---|
| 1 | End user | Mở landing page marketplace của Tenant. | UC-010, FR-014 |
| 2 | Marketplace/Platform | Resolve Tenant, load catalog và chỉ hiển thị Brand/Offer được assigned active. | UC-010, UC-011, FR-015, BRULE-024 |
| 3 | Marketplace | Hiển thị earn/cashback display text nếu Tenant cấu hình, ví dụ `Nhận x điểm với mỗi 20,000đ chi tiêu`. | UC-010, FR-016 |
| 4 | End user/Marketplace/Platform | End user chọn Brand/Offer; Platform tạo click_id và redirect sang Brand. Banner và click Banner thuộc Deferred/Phase 2. | UC-012, FR-017, FR-018 |
| 5 | Brand System | Brand ghi nhận mua hàng thành công và gửi API order success. | UC-013, FR-019 |
| 6 | Platform | Validate order, click_id, visibility; tạo order `Pending` và tính commission/revenue share tạm tính. | UC-013, FR-020..FR-022 |
| 7 | Scheduler/Platform | Chờ đến `pending_until` theo số ngày cấu hình của Brand. | UC-016, FR-007, FR-025 |
| 8 | Platform | Nếu không có cancel/refund, chốt commission Brand trả Affiliate. | UC-016, FR-024, FR-025 |
| 9 | Platform | Chốt revenue share Affiliate chia Tenant và đưa vào reporting/reconciliation. | UC-016, UC-020, FR-030 |

## Alternate paths

| Case | Điều kiện | Kết quả |
|---|---|---|
| Tenant/domain không active | Không resolve được marketplace hoặc domain config lỗi. | Hiển thị lỗi domain/cấu hình, không load catalog. |
| Không có Brand/Offer phù hợp | Brand/Offer không active, hết hiệu lực hoặc chưa assign cho Tenant. | Ẩn offer hoặc hiển thị empty state. |
| Thiếu member reference | End User chưa định danh trước khi click. | Hiển thị warning quyền lợi/cashback/đối chiếu hội viên; vẫn tạo click tracking và redirect. |
| Order success invalid | Auth/schema/idempotency/click_id/visibility không hợp lệ. | Reject hoặc đưa vào exception queue, không tạo order pending. |
| Brand báo hoàn/hủy | Cancel/refund toàn bộ một hoặc nhiều item đến khi Order còn `Pending`. | Item chuyển `Refunded`; Platform tính lại số liệu và tổng hợp Order Status. Chỉ khi tất cả item Refunded thì Order chuyển `Cancelled`; Order đã Confirmed bị từ chối và ghi Exception. |
| Tenant Loyalty API lỗi | Deferred sau MVP1. | Không áp dụng trong MVP1. |

## Notes

- Diagram này phản ánh CR-01: không có B1, point conversion, Tenant Loyalty API hoặc trạng thái `Rewarded/Đã hoàn điểm` trong MVP1.
- Landing page mockup hiện tại không hiển thị số điểm dự kiến cụ thể; chỉ hiển thị earn/cashback display text.
- Cancel/refund contract được đặc tả tại Order Transaction SRS: xử lý theo item cho Order `Pending`; Order `Confirmed` bị từ chối và ghi Exception.

## Readiness

`READY_FOR_SRS`
