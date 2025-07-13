from pathlib import Path
from typing import Iterable

import PyPDF2


def extract_text_from_pdfs(paths: Iterable[Path], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_files = []
    for path in paths:
        reader = PyPDF2.PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        out_path = output_dir / f"{path.stem}.txt"
        out_path.write_text(text)
        out_files.append(out_path)
    return out_files
