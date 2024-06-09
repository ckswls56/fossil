import time
import easyocr

# 시작 시간 기록
start_time = time.time()

# EasyOCR 리더 생성
reader = easyocr.Reader(['ko', 'en'])  # 한국어와 영어 지원

# 이미지 파일 경로
image_path = '/home/skxkswls/fossil/fossil/ocr/uploads/rotate_5.png'

# 텍스트 추출
result = reader.readtext(image_path)

# 인식한 텍스트 리스트
text_list = [text for (_, text, _) in result]

# 종료 시간 기록
end_time = time.time()

# 총 실행 시간 계산
total_time = end_time - start_time

# 텍스트 리스트와 총 실행 시간 출력
print(text_list)
print(f"총 실행 시간: {total_time:.2f}초")
