## **개요**

이 프로그램은 Django와 easyocr을 활용하여 이미지에서 텍스트를 추출하는데 사용됩니다. 사용자는 이미지를 업로드하고 해당 이미지에서 텍스트를 추출할 수 있습니다.

## **사용 방법**

### **1. Docker 설치**

이 프로그램은 Docker를 사용하여 로컬 환경에서 실행됩니다. Docker가 설치되어 있지 않은 경우에는 https://docs.docker.com/get-docker/ 에서 Docker를 설치하세요.

### **2. Docker Compose로 프로그램 실행**

아래의 명령어를 사용하여 Docker Compose를 실행하세요.

```bash
docker-compose up -d
```

### **3. 프로그램 접속**

프로그램이 성공적으로 실행되면 브라우저에서 다음 URL에 접속하세요:

```
http://localhost
```

### **4. 이미지 업로드 및 텍스트 추출**

프로그램에 접속한 후, 이미지 업로드 페이지에서 이미지를 선택하여 업로드하세요. 프로그램은 이미지에서 텍스트를 추출하고 그 결과를 표시합니다.

## **API 엔드포인트**

이미지를 업로드하고 텍스트를 추출하기 위한 API 엔드포인트는 다음과 같습니다:

```
POST http://localhost/ocr
```

Body는 form-data 형식으로 file 필드에 이미지를 첨부하여 요청하세요.

## **인프라 구성**

이 프로그램은 다음과 같은 Docker Compose 구성 파일을 사용하여 구축됩니다:

## **참고**

- easyocr: https://github.com/JaidedAI/EasyOCR
- Django: https://www.djangoproject.com/
