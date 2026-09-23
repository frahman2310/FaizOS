# questions.jsonl: retrieval test set (150 questions)

## How it was built
- Written by hand after reading `corpus/raw/ratecard_2025.txt` in full, `circular_01_2025-26.txt` in full, and targeted sections of `ordinance_2025.txt` (s.2 definitions, 12(2A), 21(q)/(s), 24, 82, 113, 114C, 231AB, 231B, 236C, Second Schedule clauses 145A/151/3A, First Schedule salary table, Fifteenth Schedule).
- Every answer comes from a 2025 document. `ratecard_2023.txt` was used only to set `changed`.
- `changed=true` means the 2023 card gives a different rate or rule for the same item. Examples: salary slabs, bank profit 15%→20%, 153 services 4%→6% and 9/11%→15%, sportspersons 10%→15%, cash withdrawal 0.6%→0.8%, 231B(1) fixed amounts→% of value, 236C 3%→4.5–5.5%, 236K 3%→1.5–2.5%, 236G/236H non-ATL. Items that are new in 2025 (e.g. toll manufacturing, e-commerce 153(2A), 151A, pension) are `false`.
- `client` questions use everyday words and contain no anchor string (the verifier checks this). `law` questions use the document's own terms.
- Split: items sorted by (topic, changed, wording) and every third one sent to holdout, so both splits cover every topic.

## Counts
| field | values |
|---|---|
| wording | client 90, law 60 |
| changed | true 36, false 114 |
| doc | ratecard_2025 105, circular_01_2025-26 24, ordinance_2025 21 |
| split | dev 100, holdout 50 (holdout: 33 client / 17 law, 13 changed, 35 ratecard / 10 circular / 5 ordinance) |

Topics (23): vehicles 19, contracts/services/supplies 17, non-residents 11, profit on debt 10, property 10, dividends 8, imports 7, salary 7, commissions 7, e-commerce 6, rent 6, electricity/telephone 5, other advance taxes 5, exemptions 5, pension 4, exports 4, cash withdrawal 4, deductions 4, late filers 3, definitions 3, prizes 2, procedure 2, minimum tax 1.

## Verification
`python3 verify_questions.py` normalises each doc (lowercase, whitespace collapsed) and checks that:
- each question has 2 or 3 anchors of 1 to 5 words;
- every anchor is found in its `doc`;
- all anchors fall inside one span of 120 words or fewer;
- no anchor appears in a client question;
- no question uses ratecard_2023 as its doc.

Result: **150/150 pass, 0 failing.**

## Caveats
- The circular is OCR text. Anchors copy its typos exactly (`flat rcle of 15%`, `lt enabled services`); OCR-broken phrases such as `min imum`, `lnvestor` were avoided as anchors. A retriever that fixes spelling will still find the passage, but exact-match scoring will be strict.
- The circular's salary table gives Rs 345,000 / 615,000. The rate card and the Ordinance give Rs 346,000 / 616,000. The salary answers use 346,000 / 616,000.
- Two sources disagree on 152(1D) (SCRA debt gains). The 2025 rate card gives 10% for both holding periods. The circular gives 20% if sold within 6 months and 10% after. Question q040 uses the circular's version.
- There are 36 `changed=true` questions (the target was about 30). Each was checked by hand against the OCR'd 2023 card, which is messy.
- `-layout` tables interleave columns. Anchors were kept to single printed lines where possible. The 120-word window check confirms they still sit together.
