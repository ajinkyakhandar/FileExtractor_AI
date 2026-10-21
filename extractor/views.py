from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentUploadForm
from .models import Document
from .services import process_document


def index(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.original_filename = request.FILES["file"].name[:255]
            document.status = Document.Status.PROCESSING
            document.save()
            try:
                document.extracted_data = process_document(document)
                document.status = Document.Status.COMPLETED
            except Exception as exc:
                document.status = Document.Status.FAILED
                document.error_message = str(exc)
            document.save()
            return redirect("document_detail", pk=document.pk)
    else:
        form = DocumentUploadForm()

    return render(request, "extractor/index.html", {
        "form": form,
        "documents": Document.objects.all()[:20],
    })


def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, "extractor/detail.html", {"document": document})


def retry_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        document.status = Document.Status.PROCESSING
        document.error_message = ""
        document.save(update_fields=["status", "error_message", "updated_at"])
        try:
            document.extracted_data = process_document(document)
            document.status = Document.Status.COMPLETED
        except Exception as exc:
            document.status = Document.Status.FAILED
            document.error_message = str(exc)
        document.save()
        messages.info(request, "Processing finished.")
    return redirect("document_detail", pk=document.pk)
