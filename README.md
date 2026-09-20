# PDFCraft

**A private, offline-first command-line toolkit for everyday PDF work.**

PDFCraft performs common PDF operations locally on your computer: inspect, merge, extract, split, rotate, encrypt, decrypt, and watermark documents. It is intentionally small, scriptable, cross-platform, and designed to avoid uploading sensitive documents to a web service.

> PDFCraft modifies PDF structure; it does not perform OCR, content-aware compression, digital signing, or PDF editing.

## Features

- **Inspect** page count, encryption state, and common metadata.
- **Merge** multiple PDFs in an explicit order.
- **Extract** page selections such as `1,3-5,8`.
- **Split** a document into deterministic `page-0001.pdf` files.
- **Rotate** every page by 90°, 180°, or 270° clockwise.
- **Encrypt / decrypt** PDFs with password protection.
- **Watermark** every page using the first page of another PDF as an overlay.
- **Safe output behavior:** existing files are never replaced unless `--force` is supplied.
- **Atomic writes:** output is written to a temporary file before replacement.
- Friendly non-zero CLI errors for missing, invalid, encrypted, or conflicting files.

## Requirements & installation

- Python 3.10+
- Windows, macOS, or Linux

```bash
git clone https://github.com/rad03i2/pdfcraft.git
cd pdfcraft
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

Check installation:

```bash
pdfcraft --version
pdfcraft --help
```

## Usage

```bash
# Inspect
pdfcraft info report.pdf

# Merge in this exact order
pdfcraft merge cover.pdf report.pdf appendix.pdf -o complete.pdf

# Extract pages 1, 3, 4, 5 and 8
pdfcraft extract complete.pdf --pages "1,3-5,8" -o selection.pdf

# Split to one PDF per page
pdfcraft split complete.pdf -d pages

# Rotate all pages
pdfcraft rotate scan.pdf --degrees 90 -o upright.pdf

# Password protection
pdfcraft encrypt private.pdf --password "your-password" -o locked.pdf
pdfcraft decrypt locked.pdf --password "your-password" -o unlocked.pdf

# Overlay watermark.pdf page 1 on every page
pdfcraft watermark report.pdf --mark watermark.pdf -o marked.pdf
```

Use `--force` on commands that create files if replacement is intentional. Passwords supplied on a command line may be visible in shell history/process listings; avoid shared machines and clear sensitive history when appropriate.

## Project structure

```text
src/pdfcraft/core.py       PDF operations and safety rules
src/pdfcraft/cli.py        argparse command-line interface
src/pdfcraft/__init__.py   public package API/version
tests/test_pdfcraft.py     functional tests
.github/workflows/ci.yml   cross-platform lint/test matrix
pyproject.toml             packaging and dependencies
```

## Testing & development

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
```

CI is configured for Python 3.10, 3.12 and 3.13 on Ubuntu, Windows and macOS. A workflow being configured is not itself a claim that a particular run has passed; check the repository Actions page for the current status.

## Security & privacy

PDFCraft does not intentionally make network requests. Documents stay on the machine where the command runs. Treat decrypted outputs as sensitive data. Encryption quality and interoperability are provided by the underlying `pypdf` library; PDFCraft is not a substitute for an audited secrets-management or archival-security system.

## Limitations

- Encrypted inputs are accepted by `info` (with `--password`) and `decrypt`; other transformations currently expect unencrypted inputs.
- Watermark placement uses PDF page coordinates as-is; PDFs with different page boxes/sizes may require a purpose-built overlay.
- Split is one-file-per-page; arbitrary chunk splitting can be achieved with repeated `extract` commands.
- No OCR, image optimization, redaction, signatures, or PDF/A conversion.

## Contributing

Bug fixes and focused improvements are welcome. Keep behavior deterministic, preserve the no-overwrite default, add tests for behavioral changes, and run `ruff check .` plus `pytest` before submitting changes.

## License

MIT © 2026 Radwan Abdulhadi Ahmed.

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية

**PDFCraft أداة سطر أوامر عملية للتعامل مع ملفات PDF محليًا وبدون رفع المستندات إلى خدمة ويب.**

يوفر المشروع العمليات اليومية الأساسية على PDF مع سلوك آمن وواضح: فحص المستند، الدمج، استخراج صفحات محددة، التقسيم، التدوير، التشفير وفك التشفير، وإضافة علامة مائية.

> الأداة تعالج بنية PDF، وليست محرر PDF ولا أداة OCR أو توقيع رقمي أو ضغط ذكي.

## لماذا PDFCraft؟

عند التعامل مع تقارير أو وثائق خاصة، قد لا يكون رفع الملف إلى موقع خارجي مناسبًا. PDFCraft يعمل على جهازك، ويمكن استخدامه يدويًا أو داخل سكربتات الأتمتة.

## المزايا

- عرض عدد الصفحات وحالة التشفير وبعض بيانات المستند.
- دمج عدة ملفات بالترتيب الذي تحدده.
- استخراج صفحات بصيغة سهلة مثل `1,3-5,8`.
- تقسيم الملف إلى ملف مستقل لكل صفحة.
- تدوير الصفحات 90 أو 180 أو 270 درجة.
- تشفير الملف بكلمة مرور وفك تشفيره.
- وضع الصفحة الأولى من ملف PDF آخر كعلامة مائية فوق جميع الصفحات.
- عدم استبدال أي ملف موجود افتراضيًا؛ يلزم `--force` للاستبدال المقصود.
- كتابة آمنة عبر ملف مؤقت قبل اعتماد الناتج النهائي.

## التثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/pdfcraft.git
cd pdfcraft
python -m venv .venv
python -m pip install -e .
```

في ويندوز فعّل البيئة بواسطة `.venv\Scripts\activate`، وفي Linux/macOS استخدم `source .venv/bin/activate`.

## أمثلة الاستخدام

```bash
pdfcraft info report.pdf
pdfcraft merge first.pdf second.pdf -o merged.pdf
pdfcraft extract merged.pdf --pages "1,3-5" -o selected.pdf
pdfcraft split merged.pdf -d pages
pdfcraft rotate scan.pdf --degrees 90 -o fixed.pdf
pdfcraft encrypt document.pdf --password "your-password" -o protected.pdf
pdfcraft decrypt protected.pdf --password "your-password" -o restored.pdf
pdfcraft watermark report.pdf --mark watermark.pdf -o marked.pdf
```

## الاختبارات والتطوير

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
```

تم إعداد GitHub Actions لفحص المشروع على Windows وLinux وmacOS، لكن وجود إعداد CI لا يعني الادعاء بأن تشغيلًا معينًا نجح؛ حالة التشغيل الحالية تظهر في صفحة Actions بالمستودع.

## الخصوصية والأمان

لا ينفذ PDFCraft اتصالات شبكة بشكل مقصود، لذلك تبقى ملفاتك على الجهاز الذي يشغل الأمر. تعامل مع الملفات الناتجة بعد فك التشفير باعتبارها حساسة. كذلك، كتابة كلمة المرور مباشرة في الأمر قد تجعلها ظاهرة في سجل الطرفية أو قائمة العمليات في بعض الأنظمة.

## القيود الحالية

- أغلب عمليات التحويل تتوقع ملف إدخال غير مشفر؛ استخدم `decrypt` أولًا للملفات المحمية.
- العلامة المائية تعتمد إحداثيات صفحات PDF الأصلية؛ اختلاف أحجام الصفحات قد يتطلب إعداد علامة مائية مخصصة.
- التقسيم الحالي ينتج ملفًا لكل صفحة.
- لا توجد ميزات OCR أو التنقيح الآمن أو التوقيع الرقمي أو PDF/A أو تحسين الصور.

## المساهمة

عند إضافة ميزة أو إصلاح خطأ، حافظ على مبدأ عدم الاستبدال الافتراضي، وأضف اختبارات للسلوك الجديد، وشغّل `ruff check .` و`pytest` قبل إرسال التغييرات.

## الترخيص

المشروع متاح بترخيص MIT © 2026 Radwan Abdulhadi Ahmed.

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
