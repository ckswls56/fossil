import time
from typing import Union
import cv2
import numpy as np
import imutils
import easyocr
from fuzzywuzzy import fuzz
from imutils.contours import sort_contours
from .marge_images import marge_images
from .show_image import show_image

# OCR 하는 함수 (path : 경로, vervose : 이미지 출력 여부)
def image_to_text(path: str, verbose: bool = False):
    # 시간 측정 시작
    start = time.time()

    # 1. Image Loading 
    org = cv2.imread(path)

    if verbose:
        show_image("Original", org, figsize=(32, 20))

    # 2. Prescription Edge Detection (처방전 틀 검출)
    preprocessed = org
    H, W, _ = preprocessed.shape

    if verbose:
        show_image("Preprocessed", preprocessed)
        
    
    # 3. Histogram Equalization (히스토그램 평탄화 부분)
    #--① 컬러 스케일을 BGR에서 YUV로 변경
    img_yuv = cv2.cvtColor(org, cv2.COLOR_BGR2YUV) 

    #--② 밝기 채널에 대해서 이퀄라이즈 적용
    img_eq = img_yuv.copy()
    img_eq[:,:,0] = cv2.equalizeHist(img_eq[:,:,0])
    img_eq = cv2.cvtColor(img_eq, cv2.COLOR_YUV2BGR)
    
    #--③ 밝기 채널에 대해서 CLAHE 적용
    img_clahe = img_yuv.copy()
    clahe = cv2.createCLAHE(clipLimit=1.3, tileGridSize=(8,8)) #CLAHE 생성
    img_clahe[:,:,0] = clahe.apply(img_clahe[:,:,0])           #CLAHE 적용
    img_clahe = cv2.cvtColor(img_clahe, cv2.COLOR_YUV2BGR)
    
    #--④ 결과 출력
    if verbose:
        show_image('Before', org)
        show_image('CLAHE', img_clahe)
        show_image('equalizeHist', img_eq)
    

    
    # 4. 회전 변환 시작
    
    # Canny 엣지 검출
    img_gray = cv2.cvtColor(img_clahe, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, threshold1=50, threshold2=150)

    # Hough 변환을 이용한 선분 검출 (사진에서 선분들 검출)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # 선분 필터링을 위한 기울기 범위 설정 (범위 내 선분들만 선택하기 위한 설정)
    min_angle = -30  # 일정 기울기 범위 최소값 (예: -30도)
    max_angle = 30   # 일정 기울기 범위 최대값 (예: 30도)
    angle_interval = 5  # 기울기 간격 설정 (5도 간격으로 필터링) (추출한 선분들을 지정 간격으로 그룹화해서 묶음)
    
    filtered_lines = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi  #기울기 측정
    
        if min_angle <= angle <= max_angle: #위에서 지정한 선분들만 선택
            # 기울기 간격에 따라 필터링된 선분 저장
            angle_rounded = round(angle / angle_interval) * angle_interval #위에서 지정한 기울기 간격에 맞춰 기울기 반올림
            filtered_lines.append((x1, y1, x2, y2, angle_rounded)) #필터링한 선분들만 반올림한 기울기 정보 추가해서 같이 저장
    
    
    # 기울기별로 선분 저장할 딕셔너리 생성
    angle_lines_dict = {angle: [] for angle in range(min_angle, max_angle + 1, angle_interval)}

    for line in filtered_lines:
        _, _, _, _, angle_rounded = line
        angle_lines_dict[angle_rounded].append(line) #기울기 간격별로 선분들 그룹화(여기서는 5도 간격)

    # 가장 많은 선분을 포함한 각도 찾기
    most_common_angle = max(angle_lines_dict, key=lambda k: len(angle_lines_dict[k]))

    # 가장 많은 선분을 포함한 각도로 회전 보정
    angle = most_common_angle
    
    # 이미지 중심점 찾기
    height, width = img_gray.shape
    center = (width // 2, height // 2)

    # 회전 변환 매트릭스 생성
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)

    # 이미지 회전
    rotated_image = cv2.warpAffine(img_gray, rotation_matrix, (width, height))
    

    # 결과 출력
    if verbose:
        show_image('Original Image', img_gray)
        show_image('Rotated Image', rotated_image)
    
    
    # Histogram 생성 (히스토그램 정규화 하는 과정 그래프로 보여주는거 굳이 할 필요 없음)
    if verbose:
        hist = cv2.calcHist([rotated_image],[0],None,[256], [0, 256])
        plt.plot(hist)
    
    if verbose:
        print("hist.shape:", hist.shape)
        print("hist.sum():", hist.sum(), "img.shape:",rotated_image.shape)
        plt.show()
        
        
    # #5 Histogram Normalize (히스토그램 정규화) (사용X)
    
    # img_norm2 = cv2.normalize(rotated_image, None, 0, 255, cv2.NORM_MINMAX) #이거 하나로 바로 정규화
    
    # # 위에서 히스토그램 과정 그래프 생성하는거 이것도 굳이 할 필요 없음    
    # if verbose:
    #     hist = cv2.calcHist([rotated_image], [0], None, [256], [0, 255])
    #     hist_norm2 = cv2.calcHist([rotated_image], [0], None, [256], [0, 255])
    
    # # 이미지 출력
    # if verbose:
    #     show_image('Before', rotated_image)
    #     show_image('cv2.normalize()', img_norm2)
    #     # hists = {'Before' : hist, 'cv2.normalize()':hist_norm2}
    #     # for i, (k, v) in enumerate(hists.items()):
    #     #     plt.subplot(1,3,i+1)
    #     #     plt.title(k)
    #     #     plt.plot(v)
    #     # plt.show()

        
    reader = easyocr.Reader(['ko','en'], gpu=True)
    readtext_results = reader.readtext(rotated_image)
    text_list = [text for (_, text, _) in readtext_results]
    
    
    return text_list