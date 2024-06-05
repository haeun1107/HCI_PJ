import cv2
import numpy as np

# 이미지 경로 설정
main_image_path = '/Users/she/hci/puzzle/main.png'
current_image_path = '/Users/she/hci/puzzle/current.png'
template_image_path = '/Users/she/hci/puzzle/target.png'

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

#template_image = cv2.resize(template_image, (0, 0), fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
template_image = cv2.resize(template_image, (0, 0), fx=1, fy=1, interpolation=cv2.INTER_AREA)

# 템플릿 이미지를 메인 이미지 크기로 리사이즈
current_resized = cv2.resize(current_image, (main_image.shape[1], main_image.shape[0]))

# 템플릿 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(current_resized, cv2.COLOR_BGR2GRAY)

# Gaussian 블러를 사용하여 노이즈 제거
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection을 사용하여 엣지 검출
edges = cv2.Canny(blurred, 50, 150)

# Contours를 검출
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 메인 이미지에 Contours 그리기 (초록색)
contours_image = main_image.copy()
cv2.drawContours(contours_image, contours, -1, (0, 255, 0), 2)

# 템플릿 이미지를 그레이스케일로 변환 및 리사이즈
template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.resize(template_gray, (0,0), fx=1, fy=1, interpolation=cv2.INTER_AREA)

# 템플릿 크기 조정 (여러 크기로 시도)
scales = [1.0, 0.9, 0.8, 0.7, 0.6]  # 템플릿 이미지의 크기 비율 목록

best_match = None
best_val = -np.inf
best_location = None
best_scale = None

for scale in scales:
    width = int(template_gray.shape[1] * scale)
    height = int(template_gray.shape[0] * scale)
    dim = (width, height)
    
    resized_template = cv2.resize(template_gray, dim, interpolation=cv2.INTER_AREA)
    
    # 템플릿 매칭 수행
    result = cv2.matchTemplate(cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY), resized_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > best_val:
        best_match = resized_template
        best_val = max_val
        best_location = max_loc
        best_scale = scale

# 매칭된 부분에 사각형 그리기 (빨간색)
top_left = best_location
bottom_right = (top_left[0] + best_match.shape[1], top_left[1] + best_match.shape[0])
cv2.rectangle(contours_image, top_left, bottom_right, (0, 0, 255), 2)

# 타겟 이미지 영역 추출
roi = main_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

# ROI에서 라인 검출
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
edges_roi = cv2.Canny(blurred_roi, 50, 150)
contours_roi, _ = cv2.findContours(edges_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 메인 이미지에 타겟 영역 라인 그리기 (빨간색)
#cv2.drawContours(contours_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]], contours_roi, -1, (0, 0, 255), 2)

# 결과 이미지 파일로 저장
result_image_path = 'result_image_with_lines.png'
cv2.imwrite(result_image_path, contours_image)

# 결과 이미지 표시
cv2.imshow('Result', contours_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"결과 이미지가 저장되었습니다: {result_image_path}")
