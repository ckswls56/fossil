from django.urls import path
from ocr.views import *

urlpatterns = [
    path('', OCRView.as_view()),
]