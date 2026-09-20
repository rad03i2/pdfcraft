# Security Policy

PDFCraft processes local documents and should be treated as document-handling software, not as an audited cryptographic product.

## Reporting

Please report security concerns privately to the repository owner through an appropriate private GitHub contact channel when available. Do not publish sensitive documents, passwords, exploit payloads containing secrets, or personal data in a public issue.

## Scope

Relevant reports include unintended file overwrite/deletion, unsafe path handling, unexpected network activity, password disclosure introduced by PDFCraft, or malformed-PDF behavior that causes unsafe writes.

Dependency vulnerabilities in `pypdf` should also be checked against the upstream project.
