import json
from pathlib import Path
from uuid import uuid4

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import AnalysisRecord
from ..services.content import get_disease_by_label
from ..services.predictor import get_predictor
from ..services.recommendations import get_recommendation


analysis_bp = Blueprint("analysis", __name__)


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


def _save_upload(upload: FileStorage):
    extension = upload.filename.rsplit(".", 1)[1].lower()
    safe_stem = secure_filename(Path(upload.filename).stem) or "xray"
    generated_name = f"{safe_stem}-{uuid4().hex[:12]}.{extension}"
    save_path = Path(current_app.config["UPLOAD_FOLDER"]) / generated_name
    upload.save(save_path)
    return generated_name, save_path


@analysis_bp.route("/analyze", methods=["GET", "POST"])
def analyze():
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    model_mode = current_app.config["PREDICTOR_MODE"]
    mode_notice = {
        "demo": {
            "kk": "Қазіргі нұсқа demo режимінде жұмыс істейді. Интерфейс нақты модельге дайын, бірақ бұл нұсқада нәтиже демонстрациялық мақсатта құрылады.",
            "ru": "Текущая версия работает в demo-режиме. Интерфейс готов для реальной модели, но в этой поставке результат формируется демонстрационно.",
        },
        "real": {
            "kk": "Қазіргі нұсқа stage1_1e-05_03.pth чекпоинтымен нақты инференс орындайды. Нәтижелер әлі де дәрігер қорытындысын алмастырмайды.",
            "ru": "Текущая версия выполняет реальный инференс через checkpoint stage1_1e-05_03.pth. Результаты все равно не заменяют заключение врача.",
        },
    }
    mode_badges = {
        "demo": "Demo mode",
        "real": "AI model",
    }

    if request.method == "POST":
        upload = request.files.get("xray_image")
        if not upload or upload.filename == "":
            flash("Please choose an X-ray image before submitting.", "error")
            return redirect(url_for("analysis.analyze"))

        if not _allowed_file(upload.filename):
            flash("Unsupported format. Upload PNG, JPG, or JPEG.", "error")
            return redirect(url_for("analysis.analyze"))

        image_filename, save_path = _save_upload(upload)
        predictor = get_predictor(current_app)

        try:
            result = predictor.predict(str(save_path), lang)
        except RuntimeError as exc:
            save_path.unlink(missing_ok=True)
            flash(str(exc), "error")
            return redirect(url_for("analysis.analyze"))

        advice = get_recommendation(result.advice_key)
        record = AnalysisRecord(
            image_filename=image_filename,
            stored_path=str(save_path),
            primary_label=result.primary_label,
            is_healthy=result.is_healthy,
            top_predictions_json=json.dumps(result.top_predictions, ensure_ascii=False),
            advice_text_kk=advice["kk"],
            advice_text_ru=advice["ru"],
            confidence_note_kk=result.confidence_note["kk"],
            confidence_note_ru=result.confidence_note["ru"],
            model_mode=result.model_mode,
        )
        db.session.add(record)
        db.session.commit()
        return redirect(url_for("analysis.result", record_id=record.id))

    return render_template(
        "analysis/analyze.html",
        model_mode=model_mode,
        mode_notice=mode_notice.get(model_mode, mode_notice["demo"])[lang],
        mode_badge=mode_badges.get(model_mode, model_mode),
    )


@analysis_bp.route("/analysis/result/<int:record_id>")
def result(record_id):
    record = db.get_or_404(AnalysisRecord, record_id)
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    disease = get_disease_by_label(record.primary_label, lang)
    advice_text = record.advice_text_kk if lang == "kk" else record.advice_text_ru
    confidence_note = record.confidence_note_kk if lang == "kk" else record.confidence_note_ru
    return render_template(
        "analysis/result.html",
        record=record,
        disease=disease,
        advice_text=advice_text,
        confidence_note=confidence_note,
    )


@analysis_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    safe_path = upload_dir / filename
    if not safe_path.exists():
        abort(404)
    return send_from_directory(upload_dir, filename)
