# Corpus sources (downloaded 2026-09-23 from FBR, public documents)

| file | source |
|---|---|
| ordinance_2025 | https://download1.fbr.gov.pk/Docs/2025881983148210Income-Tax-Ordinance,-2001-Amended-upto-31.07.2025.pdf |
| ratecard_2025 | https://download1.fbr.gov.pk/Docs/20258181281745641WHT-RateCard.pdf |
| circular_01_2025-26 | https://download1.fbr.gov.pk/Docs/2025841183918948CircularNo01of2025-26IncomeTax.pdf |
| ratecard_2023 | https://download1.fbr.gov.pk/Docs/20238215830342WithholdingRatesCards.pdf |

The PDFs are not committed (17 MB); the `.txt` files are `pdftotext -layout` output and are what the lab reads.
To rebuild: download each PDF into `raw/` under its file name, then `pdftotext -layout raw/<name>.pdf`.
