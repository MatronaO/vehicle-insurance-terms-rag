"""Download verified public source PDFs for local RAG experiments.

Run from repository root:
    python scripts/download_sources.py

The original PDFs are stored in data/raw/ (gitignored).
The script does not commit third-party documents to a public repository.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "if"
MAX_BYTES = 25 * 1024 * 1024
SOURCES = [
    {
        "file": "if-bilforsakring-forkopsinformation-2026-05.pdf",
        "url": "https://www.if.se/globalassets/se/dokument/privat/bilforsakring-forkopsinformation.pdf",
        "insurer": "If",
        "document_type": "pre_purchase_information",
        "version_label": "May 2026",
    },
    {
        "file": "if-fordonsforsakring-villkor-2026-05.pdf",
        "url": "https://www.if.se/globalassets/se/dokument/privat/motorforsakring-villkor.pdf",
        "insurer": "If",
        "document_type": "insurance_terms",
        "version_label": "May 2026",
    },
    {
        "file": "if-fordonsforsakring-villkor-2025-05.pdf",
        "url": "https://www.if.se/globalassets/se/dokument/privat/motorforsakring-villkor-old.pdf",
        "insurer": "If",
        "document_type": "insurance_terms",
        "version_label": "May 2025",
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    failures = 0
    for source in SOURCES:
        target = OUT / source["file"]
        try:
            request = urllib.request.Request(
                source["url"], headers={"User-Agent": "VehicleTermsRAG/0.1 (educational corpus)"}
            )
            with urllib.request.urlopen(request, timeout=45) as response:
                final_url = response.geturl()
                if not final_url.startswith("https://www.if.se/"):
                    raise ValueError(f"Unexpected redirect: {final_url}")
                pdf = response.read(MAX_BYTES + 1)
            if not pdf.startswith(b"%PDF-"):
                raise ValueError("Response is not a PDF")
            if len(pdf) > MAX_BYTES:
                raise ValueError("PDF exceeds size limit")
            if len(pdf) < 1024:
                raise ValueError("Suspiciously small PDF")
            tmp = target.with_suffix(".pdf.tmp")
            try:
                tmp.write_bytes(pdf)
                tmp.replace(target)
            finally:
                tmp.unlink(missing_ok=True)
            manifest.append({
                **source,
                "source_url": source["url"],
                "source_file": str(target.relative_to(ROOT)).replace("\\", "/"),
                "format": "pdf",
                "effective_from": None,
                "sha256": hashlib.sha256(pdf).hexdigest(),
                "byte_size": len(pdf),
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "status": "downloaded_unreviewed",
            })
            print(f"OK: {target.relative_to(ROOT)} ({len(pdf)} bytes)")
        except Exception as exc:
            failures += 1
            print(f"FAILED: {source['file']}: {exc}")
    manifest_path = ROOT / "data" / "raw" / "source-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest: {manifest_path.relative_to(ROOT)}")
    if failures:
        raise SystemExit(f"{failures} of {len(SOURCES)} downloads failed")


if __name__ == "__main__":
    main()
