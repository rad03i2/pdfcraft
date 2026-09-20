"""PDFCraft — offline PDF utilities."""

from .core import PDFCraftError, decrypt, encrypt, extract, info, merge, parse_pages, rotate, split, watermark

__all__ = ["PDFCraftError", "decrypt", "encrypt", "extract", "info", "merge", "parse_pages", "rotate", "split", "watermark"]
__version__ = "1.0.0"
