# PDF Extractor

A small Django app for uploading PDFs, extracting their text, sending that text plus your field instructions to an AI extraction step, and saving the original file and structured JSON in SQLite. The upload page works with both of your PDF formats: describe the format and requested fields in the instructions box. The app deliberately keeps the extracted schema flexible because the sample documents and exact fields were not included yet.

## Requirements

- Python 3.10+
- An OpenAI API key for AI extraction

## Setup

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set `OPENAI_API_KEY` in your shell. Optionally set `OPENAI_MODEL`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` as shown in `.env.example`.
4. Run `python manage.py migrate`.
5. Run `python manage.py runserver` and open the local Django address in a browser.

Upload a PDF and optionally describe its format and the fields you want, for example: “Format B: extract account holder, statement date, and ending balance.” Each successful or failed attempt is saved and appears in the recent documents list. Failed jobs can be retried from their detail page.

## Notes

- PDFs must be at most 20 MB and contain selectable text. Image-only scans need OCR, which is not included in this starter app.
- Extracted content is stored in `Document.extracted_data` as JSON; the raw text and original PDF are also retained.
- Processing is synchronous in the web request to keep the project simple. For larger files or production use, move processing to a background worker and add authentication, malware scanning, retention rules, and production storage settings.
- Do not commit API keys. `.env.example` is a reference; export secrets in your local shell instead.

## Tests

Run `python manage.py test`.
