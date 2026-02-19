"""Find all PDFs that do not have a corresponding text file and run OCR on
them. Run as:
```sh
python3 ocr_all.py
```
"""

import logging
import os
import subprocess
from logging import getLogger
from pathlib import Path

logging.basicConfig(level="INFO")
logger = getLogger(__name__)


def ocr_pdf(pdf: Path):
    """Returns if the subprocess succeeded."""
    logger.info("Running `marker_single %s --output_dir ./`", pdf)
    output = subprocess.run(
        ["marker_single", str(pdf), "--output_dir", "./"],
    )
    return output.returncode == 0


def main():
    assert os.system("uv tool install marker-pdf") == 0
    with open("done_ocr.txt", "r") as f:
        done_ocr = set(f.read().strip().splitlines())
    successes: list[str] = []
    failures: list[str] = []
    for pdf_name in os.listdir():
        pdf_path = Path(pdf_name)
        if pdf_path.suffix == ".pdf" and pdf_name not in done_ocr:
            if ocr_pdf(pdf_path):
                successes.append(pdf_name)
            else:
                failures.append(pdf_name)
    if len(successes) > 0:
        logger.warning(
            "Successfully processed %d PDFs: %s, writing to `done_ocr.txt`",
            len(successes),
            successes,
        )
        new_done_ocr = list(done_ocr) + successes
        new_done_ocr.sort()
        done_ocr_content = "\n".join(new_done_ocr)
        with open("done_ocr.txt", "w") as f:
            assert f.write(done_ocr_content) == len(done_ocr_content)
    if len(failures) == 0:
        return 0
    else:
        logger.error("Failed to process %d PDFs: %s", len(failures), failures)
        return 1


exit(main()) if __name__ == "__main__" else None
