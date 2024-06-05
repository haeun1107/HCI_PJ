from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'main_image' not in request.files or 'current_image' not in request.files or 'template_image' not in request.files:
        return redirect(request.url)
    
    main_image_file = request.files['main_image']
    current_image_file = request.files['current_image']
    template_image_file = request.files['template_image']

    if main_image_file.filename == '' or current_image_file.filename == '' or template_image_file.filename == '':
        return redirect(request.url)
    
    main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'main_image.jpg')
    current_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'current_image.jpg')
    template_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'template_image.jpg')
    
    main_image_file.save(main_image_path)
    current_image_file.save(current_image_path)
    template_image_file.save(template_image_path)

    # 고유한 파일 이름 생성
    unique_filename = str(uuid.uuid4()) + '.png'
    result_image_path = os.path.join(app.config['RESULT_FOLDER'], unique_filename)

    pieces = int(request.form['pieces'])
    difficulty = request.form['difficulty']

    process_images(main_image_path, current_image_path, template_image_path, result_image_path, pieces, difficulty)
    
    return redirect(url_for('uploaded_file', filename=unique_filename))

@app.route('/results/<filename>')
def uploaded_file(filename):
    return render_template('result.html', filename=filename)

@app.route('/display/<filename>')
def display_image(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

def process_images(main_image_path, current_image_path, template_image_path, result_image_path, pieces, difficulty):
    current_image = cv2.imread(current_image_path)
    main_image = cv2.imread(main_image_path)
    template_image = cv2.imread(template_image_path)

    if pieces == 50:
        template_image = cv2.resize(template_image, (0, 0), fx=1, fy=1, interpolation=cv2.INTER_AREA)
    elif pieces == 100:
        template_image = cv2.resize(template_image, (0, 0), fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
    else: # 1000개 이하
        template_image = cv2.resize(template_image, (0, 0), fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

    current_resized = cv2.resize(current_image, (main_image.shape[1], main_image.shape[0]))

    gray = cv2.cvtColor(current_resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_image = main_image.copy()
    cv2.drawContours(contours_image, contours, -1, (0, 255, 0), 2)

    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    scales = [1.0, 0.9, 0.8, 0.7, 0.6]

    best_match = None
    best_val = -np.inf
    best_location = None

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

    top_left = best_location
    bottom_right = (top_left[0] + best_match.shape[1], top_left[1] + best_match.shape[0])

    if difficulty == 'high':
        rect_top_left = (top_left[0] - best_match.shape[1] * 2, top_left[1] - best_match.shape[0] * 2)
        rect_bottom_right = (bottom_right[0] + best_match.shape[1] * 2, bottom_right[1] + best_match.shape[0] * 2)
    elif difficulty == 'medium':
        rect_top_left = (top_left[0] - best_match.shape[1], top_left[1] - best_match.shape[0])
        rect_bottom_right = (bottom_right[0] + best_match.shape[1], bottom_right[1] + best_match.shape[0])
    else:
        rect_top_left = top_left
        rect_bottom_right = bottom_right

    cv2.rectangle(contours_image, rect_top_left, rect_bottom_right, (0, 0, 255), 2)

    cv2.imwrite(result_image_path, contours_image)

if __name__ == "__main__":
    app.run(debug=True)
