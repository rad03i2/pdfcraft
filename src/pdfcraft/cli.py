from __future__ import annotations

import argparse
import json
import sys

from .core import PDFCraftError, decrypt, encrypt, extract, info, merge, rotate, split, watermark


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pdfcraft", description="Private, offline PDF toolkit")
    p.add_argument("--version", action="version", version="PDFCraft 1.0.0 — Radwan Abdulhadi Ahmed (@rad03i2)")
    sub = p.add_subparsers(dest="command", required=True)

    i = sub.add_parser("info", help="Inspect a PDF")
    i.add_argument("input")
    i.add_argument("--password")

    m = sub.add_parser("merge", help="Merge PDFs in the given order")
    m.add_argument("inputs", nargs="+")
    m.add_argument("-o", "--output", required=True)
    m.add_argument("--force", action="store_true")

    e = sub.add_parser("extract", help="Extract selected pages (example: 1,3-5)")
    e.add_argument("input")
    e.add_argument("--pages", required=True)
    e.add_argument("-o", "--output", required=True)
    e.add_argument("--force", action="store_true")

    s = sub.add_parser("split", help="Split a PDF into one file per page")
    s.add_argument("input")
    s.add_argument("-d", "--output-dir", required=True)
    s.add_argument("--force", action="store_true")

    r = sub.add_parser("rotate", help="Rotate every page clockwise")
    r.add_argument("input")
    r.add_argument("--degrees", type=int, required=True, choices=[90, 180, 270])
    r.add_argument("-o", "--output", required=True)
    r.add_argument("--force", action="store_true")

    for name in ("encrypt", "decrypt"):
        c = sub.add_parser(name, help=f"{name.title()} a PDF")
        c.add_argument("input")
        c.add_argument("--password", required=True)
        c.add_argument("-o", "--output", required=True)
        c.add_argument("--force", action="store_true")

    w = sub.add_parser("watermark", help="Overlay the first page of another PDF on every page")
    w.add_argument("input")
    w.add_argument("--mark", required=True)
    w.add_argument("-o", "--output", required=True)
    w.add_argument("--force", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "info":
            print(json.dumps(info(args.input, args.password), indent=2, ensure_ascii=False))
        elif args.command == "merge":
            print(merge(args.inputs, args.output, force=args.force))
        elif args.command == "extract":
            print(extract(args.input, args.pages, args.output, force=args.force))
        elif args.command == "split":
            for path in split(args.input, args.output_dir, force=args.force):
                print(path)
        elif args.command == "rotate":
            print(rotate(args.input, args.degrees, args.output, force=args.force))
        elif args.command == "encrypt":
            print(encrypt(args.input, args.password, args.output, force=args.force))
        elif args.command == "decrypt":
            print(decrypt(args.input, args.password, args.output, force=args.force))
        elif args.command == "watermark":
            print(watermark(args.input, args.mark, args.output, force=args.force))
        return 0
    except PDFCraftError as exc:
        print(f"pdfcraft: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
