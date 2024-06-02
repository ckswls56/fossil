import easyocr

# EasyOCR 리더 생성
reader = easyocr.Reader(['ko', 'en'])  # 한국어와 영어 지원

# 이미지 파일 경로
image_path = 'C:/Users/woobi/Documents/fossil/fossil/ocr/uploads/menu1.png'

# 텍스트 추출
result = reader.readtext(image_path)

# 인식한 텍스트 리스트
text_list = [text for (_, text, _) in result]

# 텍스트 리스트 출력
print(text_list)
