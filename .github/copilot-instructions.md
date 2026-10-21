# Project guidance

- This is a minimal Django PDF extraction app; keep changes aligned with Django conventions.
- Uploaded PDFs are validated in `extractor/forms.py`, extraction logic belongs in `extractor/services.py`, and persisted records use `extractor/models.py`.
- Keep API credentials in environment variables; never hard-code secrets.
- Run migrations and `python manage.py test` after model or workflow changes.
- Extraction fields remain flexible JSON until sample PDFs and required field names are provided.
