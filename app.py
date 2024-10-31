import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
EDITED_FOLDER = 'static/edited/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EDITED_FOLDER'] = EDITED_FOLDER

# Ensure upload and edited directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EDITED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))
    
    # Save the uploaded file temporarily
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Resize the uploaded image to 200x200 pixels
    image = cv2.imread(filepath)
    resized_image = cv2.resize(image, (200, 200))
    cv2.imwrite(filepath, resized_image)  # Overwrite with the resized image
    
    return redirect(url_for('edit_image', filename=file.filename))

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(filepath)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'grayscale':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif action == 'rotate':
            angle = int(request.form.get('angle') or 0)
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            image = cv2.warpAffine(image, M, (w, h))
        elif action == 'resize':
            # Set default size if width/height is not provided
            width = int(request.form.get('width') or 200)
            height = int(request.form.get('height') or 200)
            image = cv2.resize(image, (width, height))
        elif action == 'crop':
            x = int(request.form.get('x') or 0)
            y = int(request.form.get('y') or 0)
            w = int(request.form.get('width') or image.shape[1])
            h = int(request.form.get('height') or image.shape[0])
            image = image[y:y+h, x:x+w]
        elif action == 'blur':
            ksize = int(request.form.get('ksize') or 3)  # Default kernel size for blur
            image = cv2.GaussianBlur(image, (ksize, ksize), 0)
        elif action == 'edge':
            image = cv2.Canny(image, 100, 200)
        
        edited_image_path = os.path.join(app.config['EDITED_FOLDER'], 'edited_' + filename)
        cv2.imwrite(edited_image_path, image)
        return redirect(url_for('edit_image', filename=filename))
    
    return render_template('edit.html', filename=filename, edited_filename='edited_' + filename)


@app.route('/download/<filename>')
def download_image(filename):
    file_path = os.path.join(app.config['EDITED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
