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
        return False
    else:
        logger.warning("Starting OCR `%s` → `%s`", pdf_path, md_path)
        markdown = ocr_pdf(pdf_path)
        if markdown is None:
            logger.error("Did not write to `%s`", md_path)
            return True
        else:
            md_path.write_text(markdown)
            logger.info("Wrote output to `%s`", md_path)
            return False


def main():
    failures: list[Path] = []
    for pdf_name in os.listdir():
        pdf_path = Path(pdf_name)
        if pdf_path.suffix == ".pdf":
            if process_pdf(pdf_path):
                failures.append(pdf_name)
    if len(failures) == 0:
        return 0
    else:
        logger.error("Failed to process %d PDFs: %s", len(failures), failures)
        return 1


exit(main()) if __name__ == "__main__" else None
