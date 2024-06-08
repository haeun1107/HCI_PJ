import cv2
import numpy as np

# 이미지 경로 설정
main_image_path = '/Users/she/Desktop/인컴/pi.jpg'
current_image_path = '/Users/she/Desktop/인컴/pi1.jpg'
template_image_path = '/Users/she/Desktop/인컴/f.jpg'

# 이미지를 불러오기
current_image = cv2.imread(current_image_path)
main_image = cv2.imread(main_image_path)
template_image = cv2.imread(template_image_path)

# 이미지가 제대로 불러와졌는지 확인
if current_image is None:
    raise FileNotFoundError(f"템플릿 이미지를 찾을 수 없습니다: {current_image_path}")
if main_image is None:
    raise FileNotFoundError(f"메인 이미지를 찾을 수 없습니다: {main_image_path}")
if template_image is None:
    raise FileNotFoundError(f"타겟 이미지를 찾을 수 없습니다: {template_image_path}")

# 템플릿 이미지를 메인 이미지 크기로 리사이즈
template_image = cv2.resize(template_image, (0, 0), fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

# 현재 맞춘 퍼즐 이미지를 메인 이미지 크기로 리사이즈
current_resized = cv2.resize(current_image, (main_image.shape[1], main_image.shape[0]))

# 이미지 전처리 (그레이스케일 변환, 가우시안 블러, 하이부스트 필터링)
gray = cv2.cvtColor(current_resized, cv2.COLOR_BGR2GRAY)  # 그레이스케일 변환
blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # 가우시안 블러 적용
highboost = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)  # 하이부스트 필터링 적용
#_, otsu_thresh = cv2.threshold(highboost, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # OTSU 임계처리 적용
edges = cv2.Canny(highboost, 50, 150)  # Canny 엣지 검출 적용
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 컨투어 검출

# 메인 이미지에 컨투어 그리기 (초록색)
contours_image = main_image.copy()
#cv2.drawContours(contours_image, contours, -1, (0, 255, 0), 2)

# 템플릿 이미지를 그레이스케일로 변환 및 히스토그램 계산
template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
template_hist = cv2.calcHist([template_gray], [0], None, [256], [0, 256])
cv2.normalize(template_hist, template_hist, 0, 1, cv2.NORM_MINMAX) # 히스토그램 정규화

best_match = None
best_val = -np.inf
best_location = None

scales = [1.0, 0.9, 0.8, 0.7, 0.6] # 템플릿 이미지의 크기 비율 목록

# 여러 크기의 템플릿 이미지로 매칭 수행
for scale in scales:
    width = int(template_gray.shape[1] * scale)
    height = int(template_gray.shape[0] * scale)
    resized_template = cv2.resize(template_gray, (width, height), interpolation=cv2.INTER_AREA)  # 템플릿 이미지 리사이즈
    result = cv2.matchTemplate(cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY), resized_template, cv2.TM_CCORR_NORMED)  # 템플릿 매칭 수행
    _, max_val, _, max_loc = cv2.minMaxLoc(result)  # 매칭 결과에서 최댓값 및 위치 찾기

    if max_val > best_val:
        best_match = resized_template
        best_val = max_val
        best_location = max_loc

# 매칭된 부분의 좌표
top_left = best_location
bottom_right = (top_left[0] + best_match.shape[1], top_left[1] + best_match.shape[0])

rect_top_left = top_left
rect_bottom_right = bottom_right

# 매칭된 부분에 사각형 그리기 (빨간색)
cv2.rectangle(contours_image, rect_top_left, rect_bottom_right, (0, 0, 255), 2)

# 결과 이미지 표시
cv2.imshow('TM_CCORR_NORMED', contours_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

