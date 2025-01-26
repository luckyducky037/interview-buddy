from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'Welcome to the Interview Helper Backend!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file uploaded.'), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No file uploaded.'), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        file.save(file_path)
    except Exception as e:
        app.logger.error(f"Error saving file: {e}")
        return jsonify(error='Failed to save file.'), 500

    try:
        result = subprocess.run(['python', '../analyze.py'], input=file_path, text=True, capture_output=True)
        if result.returncode != 0:
            app.logger.error(f"Error in Python process: {result.stderr}")
            return jsonify(error='Error occurred during analysis.', code=result.returncode, details=result.stderr), 500

        analysis_result = json.loads(result.stdout)
        return jsonify(analysis_result), 200
    except Exception as e:
        app.logger.error(f"Error during analysis: {e}")
        return jsonify(error='Internal server error.'), 500

if __name__ == '__main__':
    app.run(debug=True)