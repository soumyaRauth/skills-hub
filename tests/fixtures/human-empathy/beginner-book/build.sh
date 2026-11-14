#!/usr/bin/env bash
# Builds dist/from-zero-to-api.pdf from the chapters.
set -euo pipefail
mkdir -p dist
pandoc chapters/*.md --standalone --css theme/pdf.css \
  --metadata title="From Zero to API" -o dist/book.html
weasyprint dist/book.html dist/from-zero-to-api.pdf
