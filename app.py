from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # 업로드된 파일을 저장할 폴더
RESULT_FOLDER = 'results'  # 결과 이미지를 저장할 폴더
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# 업로드 폴더가 존재하지 않으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 결과 폴더가 존재하지 않으면 생성
if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

@app.route('/')
def upload_form():
    # 메인 페이지 렌더링
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    # 이미지 파일이 폼 데이터에 포함되어 있는지 확인
    if 'main_image' not in request.files or 'current_image' not in request.files or 'template_image' not in request.files:
        return redirect(request.url)
    
    # 파일을 가져옴
    main_image_file = request.files['main_image']
    current_image_file = request.files['current_image']
    template_image_file = request.files['template_image']

    # 파일 이름이 비어있는지 확인
    if main_image_file.filename == '' or current_image_file.filename == '' or template_image_file.filename == '':
        return redirect(request.url)
    
    # 파일 경로 설정
    main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'main_image.jpg')
    current_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'current_image.jpg')
    template_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'template_image.jpg')
    
    # 파일 저장
    main_image_file.save(main_image_path)
    current_image_file.save(current_image_path)
    template_image_file.save(template_image_path)

    # 고유한 파일 이름 생성
    unique_filename = str(uuid.uuid4()) + '.png'
    result_image_path = os.path.join(app.config['RESULT_FOLDER'], unique_filename)

    # 폼에서 입력된 퍼즐 조각 수와 난이도를 가져옴
    pieces = int(request.form['pieces'])
    difficulty = request.form['difficulty']

    # 이미지를 처리하는 함수 호출
    process_images(main_image_path, current_image_path, template_image_path, result_image_path, pieces, difficulty)
    
    # 결과 페이지로 리다이렉트
    return redirect(url_for('uploaded_file', filename=unique_filename))

@app.route('/results/<filename>')
def uploaded_file(filename):
    # 결과 페이지 렌더링
    return render_template('result.html', filename=filename)

@app.route('/display/<filename>')
def display_image(filename):
    # 결과 이미지를 클라이언트에 전송
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

def process_images(main_image_path, current_image_path, template_image_path, result_image_path, pieces, difficulty):
    # 이미지 파일 읽기
    current_image = cv2.imread(current_image_path)
    main_image = cv2.imread(main_image_path)
    template_image = cv2.imread(template_image_path)

    # 퍼즐 조각 수에 따른 템플릿 이미지 크기 조정
    if pieces == 50:
        template_image = cv2.resize(template_image, (0, 0), fx=1, fy=1, interpolation=cv2.INTER_AREA)
    elif pieces == 100:
        template_image = cv2.resize(template_image, (0, 0), fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
    else:  # 1000개 이하
        template_image = cv2.resize(template_image, (0, 0), fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

    # 현재 맞춘 퍼즐 이미지를 메인 이미지 크기로 리사이즈
    current_resized = cv2.resize(current_image, (main_image.shape[1], main_image.shape[0]))

    # 이미지 전처리 (그레이스케일 변환, 가우시안 블러, 하이부스트 필터링)
    gray = cv2.cvtColor(current_resized, cv2.COLOR_BGR2GRAY)  # 그레이스케일 변환
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # 가우시안 블러 적용
    highboost = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)  # 하이부스트 필터링 적용
    edges = cv2.Canny(highboost, 50, 150)  # Canny 엣지 검출 적용
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 컨투어 검출

    # 메인 이미지에 컨투어 그리기 (초록색)
    contours_image = main_image.copy()
    cv2.drawContours(contours_image, contours, -1, (0, 255, 0), 2)

    if pieces == 50:
        # 템플릿 이미지를 그레이스케일로 변환 및 히스토그램 계산
        template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
        template_hist = cv2.calcHist([template_gray], [0], None, [256], [0, 256])
        cv2.normalize(template_hist, template_hist, 0, 1, cv2.NORM_MINMAX)  # 히스토그램 정규화

        best_match = None
        best_val = np.inf
        best_location = None

        scales = [1.0, 0.9, 0.8, 0.7, 0.6]  # 템플릿 이미지의 크기 비율 목록

        for scale in scales:
            width = int(template_gray.shape[1] * scale)
            height = int(template_gray.shape[0] * scale)
            resized_template = cv2.resize(template_gray, (width, height), interpolation=cv2.INTER_AREA)

            for i in range(main_image.shape[0] - height + 1):
                for j in range(main_image.shape[1] - width + 1):
                    roi = main_image[i:i + height, j:j + width]
                    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    roi_hist = cv2.calcHist([roi_gray], [0], None, [256], [0, 256])
                    cv2.normalize(roi_hist, roi_hist, 0, 1, cv2.NORM_MINMAX)

                    hist_diff = cv2.compareHist(template_hist, roi_hist, cv2.HISTCMP_BHATTACHARYYA)

                    if hist_diff < best_val:
                        best_val = hist_diff
                        best_location = (j, i)
                        best_match = roi
        
        # 매칭된 부분의 좌표
        top_left = best_location
        bottom_right = (top_left[0] + int(template_gray.shape[1] * scale), top_left[1] + int(template_gray.shape[0] * scale))

    else:
        # 템플릿 매칭 코드 (기존 코드 유지)
        template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
        best_match = None
        best_val = -np.inf
        best_location = None

        scales = [1.0, 0.9, 0.8, 0.7, 0.6]  # 템플릿 이미지의 크기 비율 목록

        for scale in scales:
            width = int(template_gray.shape[1] * scale)
            height = int(template_gray.shape[0] * scale)
            resized_template = cv2.resize(template_gray, (width, height), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY), resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > best_val:
                best_match = resized_template
                best_val = max_val
                best_location = max_loc

        # 매칭된 부분의 좌표
        top_left = best_location
        bottom_right = (top_left[0] + best_match.shape[1], top_left[1] + best_match.shape[0])

    # 난이도에 따라 사각형 크기 조정
    if difficulty == 'high':
        rect_top_left = (top_left[0] - best_match.shape[1] * 2, top_left[1] - best_match.shape[0] * 2)
        rect_bottom_right = (bottom_right[0] + best_match.shape[1] * 2, bottom_right[1] + best_match.shape[0] * 2)
    elif difficulty == 'medium':
        rect_top_left = (top_left[0] - best_match.shape[1], top_left[1] - best_match.shape[0])
        rect_bottom_right = (bottom_right[0] + best_match.shape[1], bottom_right[1] + best_match.shape[0])
    else:
        rect_top_left = top_left
        rect_bottom_right = bottom_right

    # 매칭된 부분에 사각형 그리기 (빨간색)
    cv2.rectangle(contours_image, rect_top_left, rect_bottom_right, (0, 0, 255), 2)

    # 결과 이미지 파일로 저장
    cv2.imwrite(result_image_path, contours_image)

if __name__ == "__main__":
    app.run(debug=True)
