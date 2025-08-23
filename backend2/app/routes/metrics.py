from flask import Blueprint, request, jsonify
from ..models import MetricsEntry, DatasetEntry
from ..extensions import db

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/metrics', methods=['POST'])
def store_metrics():
    try:
        data = request.get_json()
        metrics = data.get('metrics')
        status = data.get('status')
        doc_id = data.get('doc_id')

        if not metrics:
            return jsonify({'error': 'metrics not computed'}), 400
        if not doc_id:
            return jsonify({'error': 'doc_id is required'}), 400

        new_metric = MetricsEntry(metrics=metrics, doc_id=doc_id)
        db.session.add(new_metric)

        dataset = DatasetEntry.query.get(doc_id)
        if dataset:
            dataset.status_code = status
        db.session.commit()

        return jsonify({'message': 'Metrics stored successfully', 'metrics': metrics}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
