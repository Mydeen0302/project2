from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
from google.cloud import storage
import requests
from ..models import DatasetEntry
from ..extensions import db
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-creds.json"

upload_bp = Blueprint('upload', __name__)

BUCKET_NAME = "dsstorage_1"

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() == '.csv'

@upload_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    file = request.files.get('file')
    user_id = request.form.get('user_id')
    if not file or file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    file_name_without_type = filename.rsplit('.', 1)[0]

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_file(file, content_type=file.content_type)

        new_dataset_entry = DatasetEntry(dataset_name=file_name_without_type, user_id=user_id)
        db.session.add(new_dataset_entry)
        db.session.commit()
        doc_id = new_dataset_entry.doc_id
        # url = "http://localhost:5000/toairflow"
        # load = {'doc_id': doc_id}
        # response = requests.post(url, json=load)
        return jsonify({'message': 'File uploaded successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
