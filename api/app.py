from flask import Flask, request, jsonify
<<<<<<< HEAD
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
=======
import os
from flask_cors import CORS
import analyze

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
>>>>>>> b69ae5f5715a1696b3d122c46882e2cc49ec42a8

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
<<<<<<< HEAD
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
=======
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        file.save(file_path)

        # Placeholder: Generate feedback (replace this with actual audio processing)
        feedback = generate_feedback(file_path)

        return jsonify({
            'message': 'File uploaded and feedback generated successfully!',
            'filename': file.filename,
            'feedback': feedback
        })
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

def prepare_questions(job_desc):
    questions = analyze.generate_questions(job_desc)
    questions = questions.split("\n")
    questions = [q[2:] for q in questions if q.startswith("- ")]
    with open("questions.txt", "w") as f:
        f.write("\n".join(questions))
    return {
        "questions": questions
    }

def generate_feedback_questions(file_path):
    # Placeholder logic for feedback generation
    # Replace this with actual audio processing/transcription logic
    out = analyze.main_questions(file_path)
    return {
        "transcription": "Questions: \n" + out["questions"] + "\n---\nResponses:\n" + out["transcript"],
        "tips": [
            i["feedback"] for i in out["short_form"]
        ]
    }

def generate_feedback(file_path):
    # Placeholder logic for feedback generation
    # Replace this with actual audio processing/transcription logic
    out = analyze.main(file_path)
    return {
        "transcription": out["transcript"],
        "tips": [
            i["feedback"] for i in out["short_form"]
        ]
    }

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the File Upload and Feedback API'}), 200

if __name__ == '__main__':
    app.run(port=4000, debug=True)
>>>>>>> b69ae5f5715a1696b3d122c46882e2cc49ec42a8
