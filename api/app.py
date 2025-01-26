from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
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
    file.save(file_path)

    try:
        result = subprocess.run(['python', '../analyze.py'], input=file_path, text=True, capture_output=True)
        if result.returncode != 0:
            return jsonify(error='Error occurred during analysis.', code=result.returncode, details=result.stderr), 500

        analysis_result = json.loads(result.stdout)
        return jsonify(analysis_result), 200
    except Exception as e:
        return jsonify(error='Internal server error.'), 500

if __name__ == '__main__':
    app.run(debug=True)