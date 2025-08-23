from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class DatasetEntry(db.Model):
    __tablename__ = 'datasetentries'
    doc_id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_code = db.Column(db.Integer, default=0)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    metrics = db.relationship('MetricsEntry', backref='dataset', uselist=False)

class MetricsEntry(db.Model):
    __tablename__ = 'metrics'
    metrics_id = db.Column(db.Integer, primary_key=True)
    metrics = db.Column(db.JSON, nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('datasetentries.doc_id'))
