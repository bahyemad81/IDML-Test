"""
Flask Backend for IDML Arabic Translation Tool
Handles file uploads, translation, and downloads for both IDML and Word formats
"""

import os
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
from dotenv import load_dotenv
from translator_core import IDMLTranslator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50MB default
app.config['UPLOAD_FOLDER'] = 'uploads'

# Enable CORS
CORS(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'idml'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def translate():
    """Handle IDML file upload and translation"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only .idml files are allowed'}), 400
        
        # Get API key from form or environment (optional now - using free translation)
        api_key = request.form.get('api_key') or os.getenv('GOOGLE_API_KEY')
        # API key is optional now since we're using free Google Translate
        
        # Get target language (default to Arabic)
        target_lang = request.form.get('target_lang', 'ar')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(upload_path)
        
        # Initialize translator with target language
        translator = IDMLTranslator(api_key, target_lang=target_lang)
        
        # Track progress (simple implementation)
        progress_data = {'status': 'Starting...', 'progress': 0}
        
        def progress_callback(status, progress):
            progress_data['status'] = status
            progress_data['progress'] = progress
            print(f"Progress: {progress}% - {status}")
        
        # Perform translation
        output_paths = translator.translate_idml(str(upload_path), progress_callback)
        
        # Clean up uploaded file
        os.remove(upload_path)
        
        # Return JSON with both file names
        return jsonify({
            'success': True,
            'idml_file': Path(output_paths['idml']).name,
            'word_file': Path(output_paths['word']).name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<file_type>/<filename>', methods=['GET'])
def download_file(file_type, filename):
    """Download translated file (IDML or Word)"""
    try:
        file_path = Path(app.config['UPLOAD_FOLDER']) / filename
        
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        # Determine mimetype based on file type
        if file_type == 'word':
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:  # idml
            mimetype = 'application/octet-stream'
        
        response = send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
        # Clean up file after download
        @response.call_on_close
        def cleanup():
            try:
                if file_path.exists():
                    os.remove(file_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'IDML Arabic Translator'})


if __name__ == '__main__':
    print("=" * 60)
    print("IDML Arabic Translation Tool - Web Server")
    print("Using FREE Google Translate (No API Key Required)")
    print("=" * 60)
    print("\nServer starting at: http://localhost:5000")
    print("\nFeatures:")
    print("  - Translate IDML files to Arabic")
    print("  - Download as IDML or Word (.docx)")
    print("  - No API key required!")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
