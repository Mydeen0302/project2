from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models import DatasetEntry
from ..extensions import db

history_bp = Blueprint('history', __name__)
    
@history_bp.route('/history', methods=['GET'])
@jwt_required()
def return_history():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'user_id is required'}), 400
        datasets = DatasetEntry.query.filter_by(user_id=user_id).all()
        dataset_list = []
        for d in datasets:
            if d.metrics:
                metrics_data = d.metrics.metrics
            else:
                metrics_data = {"message": "not computed yet"}
            dataset_list.append({
                "dataset_name": d.dataset_name,
                "status_code": 'not started' if d.status_code == 0 else 'finish',
                "metrics": metrics_data
            })

        return jsonify({'message': 'entries sent', 'datasets': dataset_list})

    except Exception as e:
        print('Error in /history:', e)
        return jsonify({'message': str(e)}), 500