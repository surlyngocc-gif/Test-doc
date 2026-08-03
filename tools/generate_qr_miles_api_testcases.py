from __future__ import annotations

import html
import re
import zipfile
from collections import Counter
from pathlib import Path


OUT = Path("output/qr_miles_payment_api_testcases.xlsx")

COLUMNS = [
    "TC ID",
    "API Name",
    "Method",
    "Endpoint",
    "Category",
    "Test Scenario",
    "Preconditions",
    "Headers",
    "Request Body / Params",
    "Test Data",
    "Steps",
    "Expected Status Code",
    "Expected Result",
    "Priority",
    "Status",
]

CATEGORY_ORDER = {
    "Authentication": 1,
    "Authorization": 2,
    "Functional": 3,
    "Validation": 4,
    "Business Rule": 5,
    "Response Schema": 6,
    "Error Handling": 7,
    "Integration": 8,
    "Database": 9,
    "Security": 10,
    "Performance": 11,
    "Regression": 12,
}

PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}


def clean_sheet_name(name: str) -> str:
    value = re.sub(r"[\[\]\:\*\?\/\\]", "_", name)
    return value[:31]


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def cell_ref(row: int, col: int) -> str:
    s = ""
    while col:
        col, rem = divmod(col - 1, 26)
        s = chr(65 + rem) + s
    return f"{s}{row}"


def sheet_xml(rows: list[list[str]], freeze: bool = True) -> str:
    col_widths = [14, 26, 12, 42, 18, 46, 44, 38, 48, 38, 50, 20, 56, 12, 14]
    cols = "".join(
        f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>'
        for i, width in enumerate(col_widths[: max(len(r) for r in rows)], start=1)
    )
    panes = ""
    if freeze and len(rows) > 1:
        panes = (
            '<sheetViews><sheetView workbookViewId="0">'
            '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            "</sheetView></sheetViews>"
        )
    body = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            style = ' s="1"' if r_idx == 1 else ' s="2"'
            cells.append(
                f'<c r="{cell_ref(r_idx, c_idx)}" t="inlineStr"{style}>'
                f"<is><t>{esc(value)}</t></is></c>"
            )
        body.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    dimension = f"A1:{cell_ref(len(rows), max(len(r) for r in rows))}"
    auto_filter = f'<autoFilter ref="{dimension}"/>' if len(rows) > 1 else ""
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{dimension}"/>{panes}<cols>{cols}</cols><sheetData>{"".join(body)}</sheetData>'
        f"{auto_filter}</worksheet>"
    )


def make_xlsx(path: Path, sheets: list[tuple[str, list[list[str]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook_sheets = []
    workbook_rels = []
    content_overrides = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx, (name, _) in enumerate(sheets, start=1):
        workbook_sheets.append(
            f'<sheet name="{esc(clean_sheet_name(name))}" sheetId="{idx}" r:id="rId{idx}"/>'
        )
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        )
        content_overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheets)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{''.join(workbook_sheets)}</sheets></workbook>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f"{''.join(workbook_rels)}</Relationships>"
    )
    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FFE2F0D9"/><bgColor indexed="64"/></patternFill></fill></fills>'
        '<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left style="thin"/><right style="thin"/><top style="thin"/><bottom style="thin"/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyFont="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        f"{''.join(content_overrides)}</Types>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        zf.writestr("xl/styles.xml", styles)
        for idx, (_, rows) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(rows))


apis = [
    {
        "code": "API01",
        "name": "Tạo phiên thanh toán",
        "method": "POST",
        "endpoint": "/v1/partner/payment/payment-sessions",
        "actor": "Merchant Backend",
        "auth": "X-Merchant-Code, X-Loyalty-Signature",
        "purpose": "Merchant tạo order payment session và nhận QR payload.",
        "rules": "Merchant ACTIVE; merchantCode trong body khớp header; rate và milesAmount khớp cấu hình burn rate; không tạo trùng phiên pending.",
        "headers": "Content-Type: application/json; X-Merchant-Code; X-Loyalty-Signature",
        "body": "merchantCode, merchantOrderId, vendingMachineId, items[], milesAmount, totalPrice, rate",
        "success": "201/200 Cần xác nhận",
    },
    {
        "code": "API02",
        "name": "Lấy trạng thái phiên thanh toán",
        "method": "GET",
        "endpoint": "/v1/partner/payment/payment-sessions/{paymentSessionId}",
        "actor": "Merchant Backend",
        "auth": "X-Merchant-Code, X-Loyalty-Signature",
        "purpose": "Merchant đọc trạng thái/detail của payment session.",
        "rules": "Read phải scoped theo merchant; session hết hạn trả 410 Gone.",
        "headers": "X-Merchant-Code; X-Loyalty-Signature",
        "body": "paymentSessionId path param",
        "success": "200",
    },
    {
        "code": "API03",
        "name": "Tạo yêu cầu hoàn Miles",
        "method": "POST",
        "endpoint": "/v1/partner/payment/refunds",
        "actor": "Merchant Backend",
        "auth": "X-Merchant-Code, X-Loyalty-Signature",
        "purpose": "Merchant tạo full hoặc partial refund.",
        "rules": "paymentTransactionId và merchantRefundId bắt buộc; refund Miles do payment-service tính; không vượt paid/refundable Miles; merchantRefundId idempotent.",
        "headers": "Content-Type: application/json; X-Merchant-Code; X-Loyalty-Signature",
        "body": "paymentTransactionId, merchantRefundId, refundReason, items[] optional",
        "success": "201/200 Cần xác nhận",
    },
    {
        "code": "API04",
        "name": "Lấy trạng thái hoàn Miles",
        "method": "GET",
        "endpoint": "/v1/partner/payment/refunds/{refundTransactionId}",
        "actor": "Merchant Backend",
        "auth": "X-Merchant-Code, X-Loyalty-Signature",
        "purpose": "Merchant đọc trạng thái/detail refund.",
        "rules": "Read phải scoped theo merchant.",
        "headers": "X-Merchant-Code; X-Loyalty-Signature",
        "body": "refundTransactionId path param",
        "success": "200",
    },
    {
        "code": "API05",
        "name": "Validate QR",
        "method": "POST",
        "endpoint": "/v1/customer/payment/qr-payments/validate",
        "actor": "Member",
        "auth": "Kong validate member token và forward X-User-Id",
        "purpose": "Parse QR, validate session và trả confirmation details.",
        "rules": "QR payload là hashed paymentSessionId; session tồn tại, chưa hết hạn, chưa paid; không trả canPay/local balance.",
        "headers": "Content-Type: application/json; X-User-Id",
        "body": "qrPayload",
        "success": "200",
    },
    {
        "code": "API06",
        "name": "Yêu cầu OTP",
        "method": "POST",
        "endpoint": "/v1/customer/payment/qr-payments/{sessionCode}/otp",
        "actor": "Member",
        "auth": "Kong validate member token và forward X-User-Id",
        "purpose": "Gửi SMS OTP trước khi confirm payment.",
        "rules": "Session valid/unpaid/unexpired; request thuộc active attempt; FPT burn init được gọi trước khi gửi OTP.",
        "headers": "X-User-Id",
        "body": "sessionCode path param",
        "success": "200",
    },
    {
        "code": "API07",
        "name": "Gửi lại OTP",
        "method": "POST",
        "endpoint": "/v1/customer/payment/qr-payments/{sessionCode}/otp/resend",
        "actor": "Member",
        "auth": "Kong validate member token và forward X-User-Id",
        "purpose": "Gửi OTP mới cho active pending attempt.",
        "rules": "Chỉ hoạt động cho authenticated customer's active pending attempt; FPT quản lý vòng đời và invalidation OTP.",
        "headers": "X-User-Id",
        "body": "sessionCode path param",
        "success": "200",
    },
    {
        "code": "API08",
        "name": "Xác nhận thanh toán",
        "method": "POST",
        "endpoint": "/v1/customer/payment/qr-payments/{sessionCode}/confirm",
        "actor": "Member",
        "auth": "Kong validate member token và forward X-User-Id",
        "purpose": "Submit OTP, trừ Miles và đánh dấu payment success/failure.",
        "rules": "OTP tồn tại, chưa hết hạn, đúng; tối đa wrong attempts trước khi cần resend; claim session atomic; idempotent theo merchantTransactionId.",
        "headers": "Content-Type: application/json; X-User-Id",
        "body": "otp",
        "success": "200",
    },
    {
        "code": "API09",
        "name": "Chi tiết thanh toán",
        "method": "GET",
        "endpoint": "/v1/customer/payment/qr-payments/{transactionCode}",
        "actor": "Member",
        "auth": "Kong validate member token và forward X-User-Id",
        "purpose": "Trả kết quả/detail thanh toán cho màn hình success/failure.",
        "rules": "Customer-scoped read; không cho user khác đọc transaction.",
        "headers": "X-User-Id",
        "body": "transactionCode path param",
        "success": "200",
    },
    {
        "code": "API10",
        "name": "Lịch sử thanh toán và hoàn Miles",
        "method": "GET",
        "endpoint": "/v1/customer/payment/qr-payment-transactions",
        "actor": "Member",
        "auth": "Kong validate member token và forward X-User-Id",
        "purpose": "Trả Purchased hoặc Refunded history với filter thời gian và cursor paging.",
        "rules": "PURCHASED trả Miles âm; REFUNDED trả Miles dương; empty result trả list rỗng; sort field phải whitelist.",
        "headers": "X-User-Id",
        "body": "type, fromDate, toDate, cursor/next, limit, sort, preset",
        "success": "200",
    },
    {
        "code": "API11",
        "name": "Tạo merchant thanh toán",
        "method": "POST",
        "endpoint": "/v1/portal/payment/merchants",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Tạo merchant profile, conversion settings và API Secret.",
        "rules": "code unique; status ACTIVE/INACTIVE; holdTimeMinutes > 0; rate > 0; secret chỉ hiển thị khi create/rotate.",
        "headers": "Authorization: Bearer token; Content-Type: application/json",
        "body": "name, code, description, contactEmail, status, holdTimeMinutes, earnRate, burnRate, maxEarnMilesPerDay, maxBurnMilesPerDay, roundingRuleMiles",
        "success": "201/200 Cần xác nhận",
    },
    {
        "code": "API12",
        "name": "Tìm kiếm merchant thanh toán",
        "method": "GET",
        "endpoint": "/v1/portal/payment/merchants",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Search/list Payment Merchants.",
        "rules": "Response dạng PageResponse; không trả plaintext apiSecret.",
        "headers": "Authorization: Bearer token",
        "body": "keyword, status, page, size",
        "success": "200",
    },
    {
        "code": "API13",
        "name": "Chi tiết merchant thanh toán",
        "method": "GET",
        "endpoint": "/v1/portal/payment/merchants/{merchantCode hoặc merchantId}",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Xem merchant profile và conversion settings.",
        "rules": "Path param trong tài liệu chưa thống nhất giữa merchantCode và merchantId; không trả plaintext apiSecret.",
        "headers": "Authorization: Bearer token",
        "body": "merchantCode hoặc merchantId path param - Cần xác nhận",
        "success": "200",
    },
    {
        "code": "API14",
        "name": "Cập nhật merchant thanh toán",
        "method": "PUT",
        "endpoint": "/v1/portal/payment/merchants/{merchantCode hoặc merchantId}",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Cập nhật profile, hold time, status và conversion settings.",
        "rules": "code nên immutable trừ khi được approve; update phải ghi config/auth cache.",
        "headers": "Authorization: Bearer token; Content-Type: application/json",
        "body": "Các field merchant được phép update - Cần xác nhận",
        "success": "200",
    },
    {
        "code": "API15",
        "name": "Cập nhật trạng thái merchant",
        "method": "PATCH",
        "endpoint": "/v1/portal/payment/merchants/{merchantId}/status?status=INACTIVE",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Đổi trạng thái ACTIVE/INACTIVE của merchant.",
        "rules": "Status chỉ nhận ACTIVE hoặc INACTIVE; update cache cấu hình và auth.",
        "headers": "Authorization: Bearer token",
        "body": "status query param",
        "success": "200",
    },
    {
        "code": "API16",
        "name": "Rotate API Secret",
        "method": "POST",
        "endpoint": "/v1/portal/payment/merchants/{merchantId}/secret/rotate",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Sinh API Secret mới và invalidate secret cũ.",
        "rules": "Plain secret chỉ hiển thị một lần; secret lưu hashed/encrypted; path khác với spec candidate `/api-secret/rotate` cần xác nhận.",
        "headers": "Authorization: Bearer token",
        "body": "merchantId path param",
        "success": "200",
    },
    {
        "code": "API17",
        "name": "Tìm kiếm payment transactions",
        "method": "GET",
        "endpoint": "/v1/portal/payment/transactions",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Search payment records.",
        "rules": "Search theo field riêng lẻ; response CursorListResponse; sensitive customer fields phải mask/omit.",
        "headers": "Authorization: Bearer token",
        "body": "transactionCode, merchantTransactionId, status, userId, merchantId, pre, next, limit",
        "success": "200",
    },
    {
        "code": "API18",
        "name": "Tìm kiếm payment refunds",
        "method": "GET",
        "endpoint": "/v1/portal/payment/refunds",
        "actor": "Management user",
        "auth": "Authorization: Bearer PORTAL_JWT; role/permission manager",
        "purpose": "Search refund records.",
        "rules": "Search theo field riêng lẻ; response CursorListResponse; sensitive customer fields phải mask/omit.",
        "headers": "Authorization: Bearer token",
        "body": "refundCode, merchantRefundId, status, userId, merchantId, paymentTransactionId, pre, next, limit",
        "success": "200",
    },
    {
        "code": "API19",
        "name": "Process due refunds",
        "method": "POST",
        "endpoint": "/v1/internal/payment/refunds/due/process",
        "actor": "Internal schedule service",
        "auth": "Trusted service network/gateway rule - Cần xác nhận",
        "purpose": "Process Pending refunds sau hold time.",
        "rules": "Publish eligible refunds một lần; chỉ internal service gọi được.",
        "headers": "Internal service auth - Cần xác nhận",
        "body": "Không có body theo ví dụ",
        "success": "200/202 Cần xác nhận",
    },
    {
        "code": "API20",
        "name": "Credit refund Miles",
        "method": "POST",
        "endpoint": "/v1/internal/payment/refunds/{refundId}/credit",
        "actor": "Internal consumer service",
        "auth": "Trusted service network/gateway rule - Cần xác nhận",
        "purpose": "Credit Miles cho một refund.",
        "rules": "Idempotent theo refund_code; retry/DLQ flow; duplicate merchant transaction response xem như success.",
        "headers": "Internal service auth - Cần xác nhận",
        "body": "refundId path param",
        "success": "200/202 Cần xác nhận",
    },
    {
        "code": "API21",
        "name": "Gửi merchant webhook result",
        "method": "POST",
        "endpoint": "/v1/internal/payment/merchant-webhooks/results/{resultId}/send",
        "actor": "Internal consumer service",
        "auth": "Trusted service network/gateway rule - Cần xác nhận",
        "purpose": "Consumer gọi internal send API để gửi callback trạng thái payment tới Merchant.",
        "rules": "Payload phải ký bằng merchant webhook secret; retry và DLT khi delivery thất bại.",
        "headers": "Internal service auth - Cần xác nhận",
        "body": "resultId path param",
        "success": "200/202 Cần xác nhận",
    },
]


def tc(api, category, scenario, pre, req, data, steps, status, result, priority, kind):
    return {
        "API Name": api["name"],
        "Method": api["method"],
        "Endpoint": api["endpoint"],
        "Category": category,
        "Test Scenario": scenario,
        "Preconditions": pre,
        "Headers": api["headers"],
        "Request Body / Params": req,
        "Test Data": data,
        "Steps": steps,
        "Expected Status Code": status,
        "Expected Result": result,
        "Priority": priority,
        "Status": "Not Run",
        "_kind": kind,
    }


def build_cases(api):
    a = api["auth"].lower()
    cases = []
    if "x-merchant-code" in a:
        cases += [
            tc(api, "Authentication", "Thiếu header X-Merchant-Code", "Merchant đã onboard.", api["body"], "Bỏ X-Merchant-Code", "Gửi request với signature hợp lệ nhưng thiếu merchant code.", "401", "Response lỗi merchant authentication; không ghi dữ liệu nhạy cảm vào log.", "High", "Negative"),
            tc(api, "Authentication", "Sai X-Loyalty-Signature", "Merchant ACTIVE.", api["body"], "X-Loyalty-Signature không khớp secret", "Gửi request với merchant code đúng và signature sai.", "401", "Trả lỗi PAYMENT_MERCHANT_INVALID_SECRET hoặc merchant authentication tương đương.", "High", "Negative"),
            tc(api, "Authorization", "Merchant không được truy cập dữ liệu của merchant khác", "Tồn tại dữ liệu thuộc merchant khác.", api["body"], "Header LOTUS_MALL truy cập resource của VEND_A", "Gửi request bằng credential của merchant A tới resource của merchant B.", "403/404 Cần xác nhận", "Không lộ dữ liệu ngoài phạm vi merchant.", "High", "Negative"),
        ]
    elif "x-user-id" in a:
        cases += [
            tc(api, "Authentication", "Thiếu X-User-Id do Kong không forward", "Endpoint customer đi qua Kong.", api["body"], "Không có X-User-Id", "Gửi request thiếu X-User-Id.", "401", "Request bị từ chối; không xử lý payment/refund/history.", "High", "Negative"),
            tc(api, "Authorization", "User không đọc/sửa dữ liệu của user khác", "Có transaction/session thuộc user khác.", api["body"], "X-User-Id khác owner", "Gửi request với X-User-Id không phải owner.", "403/404 Cần xác nhận", "Không trả dữ liệu customer khác, tránh IDOR.", "High", "Negative"),
        ]
    elif "bearer" in a:
        cases += [
            tc(api, "Authentication", "Thiếu bearer token portal", "Không có token CMS.", api["body"], "Không gửi Authorization", "Gửi request thiếu Authorization header.", "401", "Request bị từ chối.", "High", "Negative"),
            tc(api, "Authorization", "User portal thiếu quyền manager", "Token hợp lệ nhưng thiếu role/permission.", api["body"], "Token role thường", "Gửi request bằng token không đủ quyền.", "403", "Không cho thao tác/xem dữ liệu management.", "High", "Negative"),
        ]
    elif "internal" in a or "trusted" in a:
        cases += [
            tc(api, "Authentication", "Nguồn gọi không thuộc trusted service", "Gateway/network rule đã cấu hình.", api["body"], "Request từ nguồn không tin cậy", "Gửi request từ client ngoài internal network.", "401/403 Cần xác nhận", "Endpoint internal không thể truy cập công khai.", "High", "Negative"),
            tc(api, "Authorization", "Service không đúng phạm vi gọi internal API", "Có nhiều internal service.", api["body"], "Service identity không được cấp quyền", "Gửi request bằng service credential không được phép.", "403 Cần xác nhận", "Không thực thi job/credit/webhook ngoài phạm vi.", "High", "Negative"),
        ]

    cases.append(tc(api, "Functional", "Request hợp lệ xử lý thành công", "Dữ liệu nền hợp lệ; " + api["rules"], api["body"], "Dữ liệu theo sample trong tài liệu", "Gửi request hợp lệ và kiểm tra status code, response body.", api["success"], "API thực hiện đúng purpose; response dùng envelope/shape đã mô tả.", "High" if api["method"] != "GET" else "Medium", "Positive"))

    if api["method"] in ("POST", "PUT", "PATCH"):
        cases.append(tc(api, "Validation", "Thiếu field bắt buộc hoặc param bắt buộc", "API có field/param bắt buộc theo tài liệu.", api["body"], "Bỏ một required field/param", "Gửi request thiếu từng required field/param.", "400", "Trả PaymentErrorResponse hoặc lỗi validation tương đương, không tạo/cập nhật dữ liệu.", "Medium", "Negative"))
        cases.append(tc(api, "Validation", "Giá trị sai kiểu hoặc sai enum", "API có field number/enum/date.", api["body"], "rate='abc', status='UNKNOWN', quantity='x'", "Gửi request với data type/enum không hợp lệ theo field liên quan.", "400", "Trả lỗi validation rõ ràng; không commit transaction.", "Medium", "Negative"))
    else:
        cases.append(tc(api, "Validation", "Query/path param không hợp lệ", "API có path/query param.", api["body"], "Id không tồn tại/sai format; limit âm; sort không whitelist", "Gửi request với param sai format hoặc ngoài whitelist.", "400/404 Cần xác nhận", "Trả lỗi phù hợp, không trả dữ liệu sai scope.", "Medium", "Negative"))

    cases.append(tc(api, "Response Schema", "Kiểm tra schema response thành công", "Request thành công.", api["body"], "Dữ liệu hợp lệ", "Gửi request thành công và đối chiếu field, kiểu dữ liệu, nullability.", "Theo success status", "Response đúng schema: data/metadata hoặc field business theo tài liệu; không có field nhạy cảm ngoài scope.", "Medium", "Positive"))
    cases.append(tc(api, "Error Handling", "Resource không tồn tại hoặc trạng thái không còn hợp lệ", "Resource id/session/transaction không tồn tại hoặc expired/used.", api["body"], "paymentSessionId/refundId/transactionCode không tồn tại hoặc expired", "Gửi request tới resource không tồn tại/hết hạn/đã xử lý.", "404/410/409 Cần xác nhận", "Trả errorCode/message ổn định như tài liệu; không throw 500 ngoài ý muốn.", "Medium", "Negative"))

    rule_text = api["rules"].lower()
    if "rate" in rule_text or "miles" in rule_text or "refund" in rule_text or "otp" in rule_text or "secret" in rule_text or "status" in rule_text or "cursor" in rule_text or "atomic" in rule_text:
        cases.append(tc(api, "Business Rule", "Kiểm tra business rule chính của API", api["rules"], api["body"], "Data vi phạm rule chính", "Gửi request vi phạm rule business được mô tả trong tài liệu.", "400/409 Cần xác nhận", "API reject đúng rule; dữ liệu hiện có không bị sai lệch.", "High", "Negative"))

    if api["method"] in ("POST", "PUT", "PATCH"):
        cases.append(tc(api, "Database", "Kiểm tra dữ liệu persist/audit sau request thành công", "Request thành công và có quyền kiểm tra DB/log audit.", api["body"], "Dữ liệu hợp lệ", "Gửi request thành công, kiểm tra bản ghi, status, created_at/updated_at, idempotency key nếu có.", "Theo success status", "DB cập nhật đúng bảng/model liên quan, không lưu secret/signature/OTP plaintext.", "Medium", "Positive"))

    cases.append(tc(api, "Security", "Input chứa SQL Injection/XSS hoặc dữ liệu nhạy cảm", "Endpoint nhận input text/query/body.", api["body"], "' OR 1=1 --, <script>alert(1)</script>", "Gửi payload/query chứa chuỗi injection/XSS ở các field text.", "400 hoặc xử lý an toàn", "Không execute injection; response/log không lộ token, signature, OTP, API secret hoặc dữ liệu customer nhạy cảm.", "High", "Negative"))

    if api["method"] == "GET":
        cases.append(tc(api, "Performance", "Truy vấn với limit/page boundary", "Có dữ liệu nhiều hơn một trang.", api["body"], "limit=1, limit=20, limit rất lớn", "Gửi request với limit/page/cursor boundary.", "200/400 Cần xác nhận", "Response trong ngưỡng Cần xác nhận; metadata paging đúng, limit lớn được chặn hoặc giới hạn.", "Low", "Boundary"))
    else:
        cases.append(tc(api, "Integration", "Dependency bên ngoài/cache/message broker lỗi hoặc timeout", "Có thể giả lập lỗi FPT/cache/Kafka/webhook hoặc DB fallback theo API.", api["body"], "Dependency timeout/error", "Gửi request khi dependency liên quan lỗi/timeout.", "500/202/Retry Cần xác nhận", "API map lỗi đúng envelope, giữ idempotency/retry/reconciliation theo tài liệu.", "Medium", "Negative"))

    cases.append(tc(api, "Regression", "Retest flow liên quan sau thay đổi API", "Các API upstream/downstream có dữ liệu liên quan.", api["body"], "Flow end-to-end tương ứng", "Chạy lại smoke flow liên quan tới API này.", "Theo từng API", "Không regress auth, cache, DB consistency, response envelope và các flow release checklist.", "Medium", "Positive"))
    return cases


all_cases = []
sheets = []
overview_rows = [["API", "Method", "Endpoint", "Actor", "Mục đích", "Auth", "Business rule chính"]]
for api in apis:
    cases = build_cases(api)
    cases.sort(key=lambda c: (CATEGORY_ORDER[c["Category"]], PRIORITY_ORDER[c["Priority"]]))
    for idx, case in enumerate(cases, start=1):
        case["TC ID"] = f'{api["code"]}-TC-{idx:03d}'
        all_cases.append(case)
    rows = [COLUMNS]
    rows += [[case.get(col, "") for col in COLUMNS] for case in cases]
    sheet_name = f'{api["code"]}_{api["name"].replace(" ", "_")}'
    sheets.append((sheet_name, rows))
    overview_rows.append([api["name"], api["method"], api["endpoint"], api["actor"], api["purpose"], api["auth"], api["rules"]])

counter_cat = Counter(c["Category"] for c in all_cases)
counter_pri = Counter(c["Priority"] for c in all_cases)
counter_kind = Counter(c["_kind"] for c in all_cases)
risks = [
    "Final path của một số API còn cần design approval; tài liệu có khác biệt giữa merchantCode và merchantId, `/api-secret/rotate` và `/secret/rotate`.",
    "Một số success status code chưa được định nghĩa rõ là 200, 201 hay 202.",
    "Quy tắc auth cho internal API mới ghi trusted network/gateway rule, chưa có header/service identity cụ thể.",
    "Threshold response time, rate limit, retry backoff và chính sách lock timeout cần xác nhận.",
    "Error code/message cuối cùng cần đồng bộ với style hiện hữu của target service.",
]
summary_rows = [
    ["Metric", "Value"],
    ["Total APIs", len(apis)],
    ["Total Test Cases", len(all_cases)],
    ["Total Positive Cases", counter_kind["Positive"]],
    ["Total Negative Cases", counter_kind["Negative"]],
    ["Total Boundary Cases", counter_kind["Boundary"]],
    ["Total Authentication Cases", counter_cat["Authentication"]],
    ["Total Authorization Cases", counter_cat["Authorization"]],
    ["Total Validation Cases", counter_cat["Validation"]],
    ["Total Security Cases", counter_cat["Security"]],
    ["Total Regression Cases", counter_cat["Regression"]],
    ["Total High Priority Cases", counter_pri["High"]],
    ["Risks & Recommendations", "\n".join(f"- {r}" for r in risks)],
    [],
    ["API Overview", "", "", "", "", "", ""],
] + overview_rows

make_xlsx(OUT, [("Summary", summary_rows)] + sheets)
print(OUT)
print(f"APIs: {len(apis)}")
print(f"Test cases: {len(all_cases)}")
