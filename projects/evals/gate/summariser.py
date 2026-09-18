"""Stands in for the AI. Each version is a different wording of the instructions.

live    : today's wording. Misses 8 of the hard invoices (faded, credit notes, some two-pagers).
broken  : reworded; also drops the total on 5 handwritten scans.
better  : reworded; fixes 3 invoices the live wording was getting wrong.
"""
LIVE_FAILS = {"credit-note-77", "credit-note-88", "faded-fax-02", "two-page-14",
              "scan-009", "scan-010", "scan-011", "usd-pkr-09"}
BROKEN_EXTRA = {"scan-000", "scan-001", "scan-002", "scan-003", "scan-004"}
BETTER_FIXES = {"credit-note-77", "faded-fax-02", "two-page-14"}


def summarise(case, version):
    fails = set(LIVE_FAILS)
    if version == "broken":
        fails |= BROKEN_EXTRA
    if version == "better":
        fails -= BETTER_FIXES
    if case["invoice"] in fails:
        return f"Invoice {case['invoice']} from a supplier, due on receipt."      # no total
    return f"Invoice {case['invoice']}, total {case['must_include']}, due on receipt."
