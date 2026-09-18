"""The 100 test cases: 18 real complaints from the firm, 82 invented at the desk (decision 2)."""

REAL_COMPLAINTS = [
    # 12 handwritten scans, 6 other awkward invoices. Each is an invoice that really failed.
    {"id": f"scan-{i:03d}", "kind": "handwritten", "total": f"PKR {80 + i},000"} for i in range(12)
] + [
    {"id": "credit-note-77", "kind": "credit_note", "total": "-$310"},
    {"id": "two-page-14", "kind": "two_page", "total": "$4,120"},
    {"id": "two-page-31", "kind": "two_page", "total": "$980"},
    {"id": "usd-pkr-09", "kind": "mixed_currency", "total": "$1,450"},
    {"id": "credit-note-88", "kind": "credit_note", "total": "-$95"},
    {"id": "faded-fax-02", "kind": "faded", "total": "$212"},
]

INVENTED = [{"id": f"typed-{i:03d}", "kind": "typed", "total": f"${100 + i * 7}"} for i in range(82)]

CASES = [{"invoice": c["id"], "kind": c["kind"], "must_include": c["total"]}
         for c in REAL_COMPLAINTS + INVENTED]
