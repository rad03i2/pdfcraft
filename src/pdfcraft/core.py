from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


class PDFCraftError(RuntimeError):
    """A user-facing PDFCraft error."""


def _reader(path: str | Path, password: str | None = None) -> PdfReader:
    source = Path(path)
    if not source.is_file():
        raise PDFCraftError(f"PDF not found: {source}")
    try:
        reader = PdfReader(source)
        if reader.is_encrypted:
            if not password or reader.decrypt(password) == 0:
                raise PDFCraftError(f"Password required or incorrect: {source}")
        return reader
    except PDFCraftError:
        raise
    except (PdfReadError, OSError, ValueError) as exc:
        raise PDFCraftError(f"Cannot read {source}: {exc}") from exc


def _output(path: str | Path, *, force: bool = False) -> Path:
    target = Path(path)
    if target.exists() and not force:
        raise PDFCraftError(f"Output exists; use --force to replace it: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def _write(writer: PdfWriter, path: str | Path, *, force: bool = False) -> Path:
    target = _output(path, force=force)
    temp = target.with_name(f".{target.name}.pdfcraft.tmp")
    try:
        with temp.open("wb") as stream:
            writer.write(stream)
        temp.replace(target)
    finally:
        if temp.exists():
            temp.unlink()
    return target


def parse_pages(spec: str, total: int) -> list[int]:
    """Parse 1-based pages such as '1,3-5,8' into unique zero-based indexes."""
    if total < 1:
        raise PDFCraftError("PDF has no pages")
    pages: list[int] = []
    seen: set[int] = set()
    try:
        for chunk in spec.split(","):
            chunk = chunk.strip()
            if not chunk:
                raise ValueError
            if "-" in chunk:
                start_s, end_s = chunk.split("-", 1)
                start, end = int(start_s), int(end_s)
                if start > end:
                    raise ValueError
                values = range(start, end + 1)
            else:
                values = [int(chunk)]
            for value in values:
                if value < 1 or value > total:
                    raise PDFCraftError(f"Page {value} is outside 1-{total}")
                index = value - 1
                if index not in seen:
                    seen.add(index)
                    pages.append(index)
    except ValueError as exc:
        raise PDFCraftError(f"Invalid page selection: {spec!r}") from exc
    return pages


def info(path: str | Path, password: str | None = None) -> dict[str, object]:
    reader = _reader(path, password)
    meta = reader.metadata or {}
    return {
        "file": str(Path(path)),
        "pages": len(reader.pages),
        "encrypted": bool(reader.is_encrypted),
        "title": meta.get("/Title"),
        "author": meta.get("/Author"),
        "subject": meta.get("/Subject"),
    }


def merge(inputs: Iterable[str | Path], output: str | Path, *, force: bool = False) -> Path:
    sources = list(inputs)
    if len(sources) < 2:
        raise PDFCraftError("Merge requires at least two input PDFs")
    writer = PdfWriter()
    for source in sources:
        reader = _reader(source)
        for page in reader.pages:
            writer.add_page(page)
    return _write(writer, output, force=force)


def extract(input_path: str | Path, pages: str, output: str | Path, *, force: bool = False) -> Path:
    reader = _reader(input_path)
    writer = PdfWriter()
    for index in parse_pages(pages, len(reader.pages)):
        writer.add_page(reader.pages[index])
    return _write(writer, output, force=force)


def split(input_path: str | Path, output_dir: str | Path, *, force: bool = False) -> list[Path]:
    reader = _reader(input_path)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for number, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        outputs.append(_write(writer, folder / f"page-{number:04d}.pdf", force=force))
    return outputs


def rotate(input_path: str | Path, degrees: int, output: str | Path, *, force: bool = False) -> Path:
    if degrees not in {90, 180, 270}:
        raise PDFCraftError("Rotation must be 90, 180, or 270 degrees")
    reader = _reader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    return _write(writer, output, force=force)


def encrypt(input_path: str | Path, password: str, output: str | Path, *, force: bool = False) -> Path:
    if not password:
        raise PDFCraftError("Password cannot be empty")
    reader = _reader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    return _write(writer, output, force=force)


def decrypt(input_path: str | Path, password: str, output: str | Path, *, force: bool = False) -> Path:
    reader = _reader(input_path, password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    return _write(writer, output, force=force)


def watermark(input_path: str | Path, mark_path: str | Path, output: str | Path, *, force: bool = False) -> Path:
    reader = _reader(input_path)
    mark = _reader(mark_path)
    if not mark.pages:
        raise PDFCraftError("Watermark PDF has no pages")
    overlay = mark.pages[0]
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(overlay)
        writer.add_page(page)
    return _write(writer, output, force=force)
