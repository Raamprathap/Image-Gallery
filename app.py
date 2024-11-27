from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with the path to your local image folder
IMAGE_FOLDER = r'C:\Users\raamp\OneDrive\Desktop\Hello World\Photography Website\image'

@app.route('/get-images', methods=['GET'])
def get_images():
    try:
        # List all files in the image folder
        image_filenames = []
        for filename in os.listdir(IMAGE_FOLDER):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Add more image formats if needed
                image_filenames.append({"id": filename, "name": filename})
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
    app.run(debug=True)
