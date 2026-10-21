from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("documents/<int:pk>/", views.document_detail, name="document_detail"),
    path("documents/<int:pk>/retry/", views.retry_document, name="retry_document"),
]
