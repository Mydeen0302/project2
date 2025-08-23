from flask import Blueprint, jsonify
from ..models import DatasetEntry

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todo', methods=['GET'])
def return_todo():
    dataset = DatasetEntry.query \
        .filter(DatasetEntry.status_code == 0) \
        .order_by(DatasetEntry.created_time) \
        .first()
    if dataset:
        return jsonify({"doc_id": dataset.doc_id, "dataset_name": dataset.dataset_name})
    else:
        return jsonify({'message': 'No data found'}), 404
