"""Find all PDFs that do not have a corresponding text file and run OCR on
them.
"""

import logging
import os
import subprocess
from logging import getLogger
from pathlib import Path

logging.basicConfig(level="INFO")
logger = getLogger(__name__)


def ocr_pdf(pdf: Path):
    # Run `nougat {pdf} --no-skipping`
    output = subprocess.run(
        ["nougat", str(pdf), "--no-skipping"],
        stdout=subprocess.PIPE,
        text=True,
    )
    if output.returncode != 0:
        return None
    return output.stdout


def process_pdf(pdf_path: Path):
    md_path = pdf_path.with_suffix(".md")
    if md_path.exists():
        logger.info("Skipping `%s` → `%s`", pdf_path, md_path)
        return 0
    else:
        logger.warning("Starting OCR `%s` → `%s`", pdf_path, md_path)
        markdown = ocr_pdf(pdf_path)
        if markdown is None:
            logger.error("Did not write to `%s`", md_path)
            return 1
        else:
            md_path.write_text(markdown)
            logger.info("Wrote output to `%s`", md_path)
            return 0


def main():
    failures = 0
    for pdf_name in os.listdir():
        pdf_path = Path(pdf_name)
        if pdf_path.suffix == ".pdf":
            failures += process_pdf(pdf_path)
    return failures


exit(main()) if __name__ == "__main__" else None
