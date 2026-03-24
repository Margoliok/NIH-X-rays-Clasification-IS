from pathlib import Path

from flask import Flask, request, session

from .blueprints.analysis import analysis_bp
from .blueprints.diseases import diseases_bp
from .blueprints.history import history_bp
from .blueprints.main import main_bp
from .config import Config
from .extensions import db
from .services.content import get_supported_languages, get_ui_strings


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{Path(app.instance_path) / 'app.db'}"
    app.config["UPLOAD_FOLDER"] = str(Path(app.instance_path) / "uploads")
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    if test_config:
        app.config.update(test_config)
        if "UPLOAD_FOLDER" in app.config:
            Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(diseases_bp)
    app.register_blueprint(history_bp)

    supported_languages = get_supported_languages()

    @app.before_request
    def ensure_language():
        lang = session.get("lang", app.config["DEFAULT_LANGUAGE"])
        if lang not in supported_languages:
            session["lang"] = app.config["DEFAULT_LANGUAGE"]

    @app.context_processor
    def inject_ui():
        current_lang = session.get("lang", app.config["DEFAULT_LANGUAGE"])
        ui = get_ui_strings(current_lang)
        return {
            "ui": ui,
            "current_lang": current_lang,
            "supported_languages": supported_languages,
            "current_path": request.full_path if request.query_string else request.path,
        }

    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()

    return app
