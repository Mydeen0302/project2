from .auth import auth_bp
from .upload import upload_bp
from .metrics import metrics_bp
from .history import history_bp
from .todo import todo_bp
from .protected import protected_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(protected_bp)
