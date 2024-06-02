from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
import os
from django.conf import settings
from .functions.image_to_text import image_to_text
from .functions.after_processing import after_processing
from .functions.search_postsql import search_postgresql
# Create your views here.

@permission_classes([AllowAny])
class OCRView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = os.path.join(settings.MEDIA_ROOT, file_obj.name)

        # 업로드된 파일 저장
        with open(file_path, 'wb') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # OCR 수행
        result = image_to_text(file_path, verbose=False)  # 디버깅을 위해 verbose=True로 설정할 수 있습니다.
        after_process = after_processing(result)
        postgresql_result = search_postgresql(after_process)
        return Response({"result": result, "after": after_process, "postgresql": postgresql_result}, status=status.HTTP_200_OK)
