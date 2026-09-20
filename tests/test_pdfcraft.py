from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdfcraft.core import PDFCraftError, decrypt, encrypt, extract, info, merge, parse_pages, rotate, split


def make_pdf(path: Path, pages: int = 2) -> Path:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=200, height=300)
    with path.open("wb") as stream:
        writer.write(stream)
    return path


def test_parse_pages_unique_and_ordered():
    assert parse_pages("3,1-2,2", 4) == [2, 0, 1]
    with pytest.raises(PDFCraftError):
        parse_pages("1,9", 4)


def test_info_merge_extract_split_and_rotate(tmp_path):
    first = make_pdf(tmp_path / "a.pdf", 2)
    second = make_pdf(tmp_path / "b.pdf", 1)
    merged = merge([first, second], tmp_path / "merged.pdf")
    assert info(merged)["pages"] == 3

    selected = extract(merged, "1,3", tmp_path / "selected.pdf")
    assert len(PdfReader(selected).pages) == 2

    parts = split(selected, tmp_path / "parts")
    assert len(parts) == 2
    assert all(path.exists() for path in parts)

    rotated = rotate(selected, 90, tmp_path / "rotated.pdf")
    assert all(page.rotation == 90 for page in PdfReader(rotated).pages)


def test_encrypt_decrypt_and_overwrite_protection(tmp_path):
    source = make_pdf(tmp_path / "source.pdf", 1)
    locked = encrypt(source, "correct-horse", tmp_path / "locked.pdf")
    assert PdfReader(locked).is_encrypted

    with pytest.raises(PDFCraftError):
        decrypt(locked, "wrong", tmp_path / "bad.pdf")

    unlocked = decrypt(locked, "correct-horse", tmp_path / "unlocked.pdf")
    assert len(PdfReader(unlocked).pages) == 1

    with pytest.raises(PDFCraftError):
        extract(source, "1", unlocked)
