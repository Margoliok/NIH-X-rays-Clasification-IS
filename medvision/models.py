import json
from datetime import datetime, timezone

from .extensions import db


class AnalysisRecord(db.Model):
    __tablename__ = "analysis_records"

    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255), nullable=False)
    stored_path = db.Column(db.String(512), nullable=False)
    primary_label = db.Column(db.String(120), nullable=False)
    is_healthy = db.Column(db.Boolean, nullable=False, default=False)
    top_predictions_json = db.Column(db.Text, nullable=False)
    advice_text_kk = db.Column(db.Text, nullable=False)
    advice_text_ru = db.Column(db.Text, nullable=False)
    confidence_note_kk = db.Column(db.String(255), nullable=False)
    confidence_note_ru = db.Column(db.String(255), nullable=False)
    model_mode = db.Column(db.String(20), nullable=False, default="demo")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    @property
    def top_predictions(self):
        return json.loads(self.top_predictions_json)
