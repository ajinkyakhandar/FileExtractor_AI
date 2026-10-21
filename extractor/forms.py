from pathlib import Path

from django import forms
from django.conf import settings

from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ("file", "extraction_instructions")
        widgets = {
            "file": forms.ClearableFileInput(attrs={"accept": ".pdf,application/pdf"}),
            "extraction_instructions": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Optional: describe the document format and fields to extract, e.g. invoice number, date, vendor, total.",
            }),
        }

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        if Path(uploaded.name).suffix.lower() != ".pdf":
            raise forms.ValidationError("Please choose a PDF file.")
        if uploaded.size > settings.MAX_UPLOAD_BYTES:
            raise forms.ValidationError("The PDF must be 20 MB or smaller.")
        header = uploaded.read(5)
        uploaded.seek(0)
        if header != b"%PDF-":
            raise forms.ValidationError("This file does not appear to be a valid PDF.")
        return uploaded
