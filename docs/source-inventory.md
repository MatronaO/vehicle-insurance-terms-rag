# Vehicle insurance RAG — source inventory

This is a **source inventory**, not the ingested document corpus. A listed URL does not mean the source file was downloaded, committed, processed or indexed.

## Verified starting sources

| ID | Insurer | Document type | Version / date | Source | Status |
| --- | --- | --- | --- | --- | --- |
| if-purchase-2026-05 | If | pre-purchase information | May 2026 (document date) | https://www.if.se/globalassets/se/dokument/privat/bilforsakring-forkopsinformation.pdf | identified only |
| if-motor-terms-current | If | motor insurance terms | Verify from PDF | https://www.if.se/globalassets/se/dokument/privat/motorforsakring-villkor.pdf | identified only |
| if-motor-terms-older | If | historical motor insurance terms | Older version; verify applicability | https://www.if.se/globalassets/se/dokument/privat/motorforsakring-villkor-old.pdf | identified only |
| svedea-purchase-2026-06-01 | Svedea | pre-purchase information, private car | 2026-06-01 (website label) | https://www.svedea.se/dokument/91215c0f-a89f-41be-ab56-797542d79227 | identified only |
| svedea-purchase-2024-04-01 | Svedea | pre-purchase information, private car | 2024-04-01 (website label) | https://www.svedea.se/dokument/92462bd5-b13a-4fda-923d-525f70f36401 | identified only |
| svedea-terms-2026-06-01 | Svedea | conditions, private car | 2026-06-01 (website label) | https://www.svedea.se/dokument/43989252-3996-440f-baae-16c439406c09 | identified only |
| svedea-terms-2024-04-01 | Svedea | conditions, private car | 2024-04-01 (website label) | https://www.svedea.se/dokument/0ac880f3-6632-4c84-85e2-acbb76c2f231 | identified only |

Svedea links lead to document landing pages; the underlying PDF download endpoint is not yet verified. Do not label these items PDFs until their actual files are retrieved and validated.

## Metadata to capture upon ingestion

- `source_url`: exact source document URL
- `source_file`: local repository file path
- `insurer`
- `document_type`: conditions, pre-purchase information, IPID, etc.
- `product`: private car insurance (or exact scope)
- `version_label`: date or version printed in the document
- `effective_from`: **only** when explicitly supported by the document; otherwise null
- `language`
- `format`: detected actual format, not assumed from a page label
- `sha256`: calculated from downloaded bytes
- `retrieved_at`: date of successful download
- `status`: identified / downloaded / validated / ingested

Preserve older versions as separate sources so retrieval can select the applicable version. A publication date, retrieval date and effective date are not interchangeable.

## Next collection steps

1. Download each item, verifying response content type and whether the link is a landing page or document.
2. Verify document title, document type, scope, version and effective date from the actual file.
3. Save source files under `data/raw/<insurer>/`, and record their SHA-256 checksums in a machine-readable manifest.
4. Add further insurers and document types; ensure the final corpus meets the assignment's document, format, category and source requirements.
5. Run extraction and preprocessing only after source files are validated.

Sources were checked on 2026-11-13. Links and documents can change; keep downloaded source snapshots separate from metadata.
