from flask import Blueprint, current_app, render_template, session

from ..models import AnalysisRecord
from ..services.content import get_disease_by_label


history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
def index():
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    records = AnalysisRecord.query.order_by(AnalysisRecord.created_at.desc()).all()
    enriched_records = []
    for record in records:
        disease = get_disease_by_label(record.primary_label, lang)
        enriched_records.append(
            {
                "record": record,
                "disease": disease,
                "advice_text": record.advice_text_kk if lang == "kk" else record.advice_text_ru,
                "confidence_note": record.confidence_note_kk if lang == "kk" else record.confidence_note_ru,
            }
        )
    return render_template("history/index.html", records=enriched_records)


@history_bp.route("/history/<int:record_id>")
def detail(record_id):
    lang = session.get("lang", current_app.config["DEFAULT_LANGUAGE"])
    record = db.get_or_404(AnalysisRecord, record_id)
    disease = get_disease_by_label(record.primary_label, lang)
    advice_text = record.advice_text_kk if lang == "kk" else record.advice_text_ru
    confidence_note = record.confidence_note_kk if lang == "kk" else record.confidence_note_ru
    return render_template(
        "history/detail.html",
        record=record,
        disease=disease,
        advice_text=advice_text,
        confidence_note=confidence_note,
    )
