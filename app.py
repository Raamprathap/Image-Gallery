from flask import Flask, jsonify, send_from_directory, render_template  # Added render_template import
from flask_cors import CORS
import os
from urllib.parse import quote

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with the path to your local image folder
IMAGE_FOLDER = r'image'

@app.route('/')
def index():
    return render_template('gallery.html')  # Serve the gallery.html file

@app.route('/get-images', methods=['GET'])
def get_images():
    try:
        # List all files in the image folder
        image_filenames = []
        for filename in os.listdir(IMAGE_FOLDER):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):  # Add more image formats if needed
                image_url = f'/images/{quote(filename)}'  # Use /images/ and URL encode the filename
                image_filenames.append({"id": filename, "name": filename, "url": image_url})
        return jsonify(image_filenames)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    # Serve the image from the local image folder
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/get-images', methods=['OPTIONS'])
def options_get_images():
    return '', 200  # Respond with a 200 OK for OPTIONS requests

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Allow specific methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow specific headers
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
