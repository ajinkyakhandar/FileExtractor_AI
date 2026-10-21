from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Document


class UploadFlowTests(TestCase):
    def test_index_loads(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_rejects_non_pdf(self):
        upload = SimpleUploadedFile("notes.txt", b"hello", content_type="text/plain")
        response = self.client.post(reverse("index"), {"file": upload})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Document.objects.exists())
        self.assertContains(response, "Please choose a PDF file.")

    @patch("extractor.views.process_document", return_value={"document_type": "example", "fields": {}})
    def test_upload_stores_extraction(self, mock_process):
        upload = SimpleUploadedFile("sample.pdf", b"%PDF-1.4 sample", content_type="application/pdf")
        response = self.client.post(reverse("index"), {"file": upload, "extraction_instructions": "Extract ID"})
        document = Document.objects.get()
        self.assertRedirects(response, reverse("document_detail", args=[document.pk]))
        self.assertEqual(document.status, Document.Status.COMPLETED)
        self.assertEqual(document.extracted_data["document_type"], "example")
        mock_process.assert_called_once_with(document)
