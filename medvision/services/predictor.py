import hashlib
import pickle
import random
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import torch

from .recommendations import resolve_advice_key


MODEL_LABELS = [
    "Atelectasis",
    "Cardiomegaly",
    "Consolidation",
    "Edema",
    "Effusion",
    "Emphysema",
    "Fibrosis",
    "Hernia",
    "Infiltration",
    "Mass",
    "Nodule",
    "No Finding",
    "Pleural Thickening",
    "Pneumonia",
    "Pneumothorax",
]


@dataclass
class PredictionResult:
    top_predictions: list
    is_healthy: bool
    primary_label: str
    advice_key: str
    confidence_note: dict
    model_mode: str


class BasePredictor:
    def predict(self, image_path: str, lang: str) -> PredictionResult:
        raise NotImplementedError


def _read_image(image_path: str):
    file_bytes = np.fromfile(image_path, dtype=np.uint8)
    if file_bytes.size == 0:
        return None
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)


class DemoPredictor(BasePredictor):
    def predict(self, image_path: str, lang: str) -> PredictionResult:
        image_bytes = Path(image_path).read_bytes()
        digest = hashlib.sha256(image_bytes).hexdigest()
        rng = random.Random(int(digest[:16], 16))
        stem = Path(image_path).stem.lower()

        probabilities = {}
        for label in MODEL_LABELS:
            probabilities[label] = round(0.18 + (rng.random() * 0.72), 2)

        if any(token in stem for token in ("healthy", "normal", "no-finding", "no_finding")):
            probabilities["No Finding"] = 0.92
        if "pneumonia" in stem:
            probabilities["Pneumonia"] = 0.88
        if "edema" in stem:
            probabilities["Edema"] = 0.86
        if "mass" in stem:
            probabilities["Mass"] = 0.84

        top_predictions = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)[:3]
        primary_label, primary_probability = top_predictions[0]
        is_healthy = primary_label == "No Finding" and primary_probability >= 0.55
        advice_key = resolve_advice_key(primary_label, primary_probability, is_healthy)

        if primary_probability >= 0.8:
            confidence_note = {
                "kk": "Demo бағалауында негізгі нәтиже айқын бөлініп тұр.",
                "ru": "В demo-оценке основной результат выделяется достаточно уверенно.",
            }
        elif primary_probability >= 0.6:
            confidence_note = {
                "kk": "Нәтиже орташа сенімділікпен көрсетілді, дәрігерлік тексеру маңызды.",
                "ru": "Результат показан с умеренной уверенностью, поэтому очная оценка врача важна.",
            }
        else:
            confidence_note = {
                "kk": "Нәтиже аралас болуы мүмкін, сондықтан клиникалық тексеру қажет.",
                "ru": "Результат может быть смешанным, поэтому клиническая проверка обязательна.",
            }

        return PredictionResult(
            top_predictions=[
                {"label": label, "probability": probability, "percent": int(probability * 100)}
                for label, probability in top_predictions
            ],
            is_healthy=is_healthy,
            primary_label=primary_label,
            advice_key=advice_key,
            confidence_note=confidence_note,
            model_mode="demo",
        )


class TorchPredictor(BasePredictor):
    def __init__(self, checkpoint_path):
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path else None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.class_labels = None
        self._load_assets()

    def _load_assets(self):
        if not self.checkpoint_path or not self.checkpoint_path.exists():
            raise RuntimeError("Model checkpoint was not found. Please place stage1_1e-05_03.pth in the models folder.")

        try:
            checkpoint = torch.load(self.checkpoint_path, map_location=self.device, weights_only=False)
        except ModuleNotFoundError as exc:
            missing_module = exc.name or "required module"
            raise RuntimeError(
                f"Real model could not be loaded because the current Python environment is missing '{missing_module}'. "
                "Start the web app from the project .venv or install the missing ML dependencies into the current interpreter."
            ) from exc
        self.model = checkpoint["model"]
        self.model.to(self.device)
        self.model.eval()

        labels_path = Path("pickles") / "disease_classes.pickle"
        if not labels_path.exists():
            raise RuntimeError("pickles/disease_classes.pickle is missing. Run the training pipeline at least once before real inference.")

        with labels_path.open("rb") as handle:
            self.class_labels = pickle.load(handle)

    def predict(self, image_path: str, lang: str) -> PredictionResult:
        import config as training_config

        image = _read_image(image_path)
        if image is None:
            raise RuntimeError("The uploaded image could not be read for model inference.")

        tensor = training_config.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.sigmoid(logits)[0].detach().cpu().tolist()

        paired = list(zip(self.class_labels, probabilities))
        top_predictions = sorted(paired, key=lambda item: item[1], reverse=True)[:3]
        primary_label, primary_probability = top_predictions[0]
        is_healthy = primary_label == "No Finding" and primary_probability >= 0.5
        advice_key = resolve_advice_key(primary_label, primary_probability, is_healthy)

        if primary_probability >= 0.8:
            confidence_note = {
                "kk": "Модель негізгі нәтижені жоғары сенімділікпен көрсетті.",
                "ru": "Модель показала основной результат с высокой уверенностью.",
            }
        elif primary_probability >= 0.6:
            confidence_note = {
                "kk": "Нәтиже орташа сенімділікпен көрсетілді, сондықтан дәрігер бағасы маңызды.",
                "ru": "Результат показан с умеренной уверенностью, поэтому оценка врача остается важной.",
            }
        else:
            confidence_note = {
                "kk": "Нәтиже аралас болуы мүмкін, оны клиникалық тексерумен нақтылау керек.",
                "ru": "Результат может быть смешанным, и его стоит уточнять клинической оценкой.",
            }

        return PredictionResult(
            top_predictions=[
                {"label": label, "probability": round(probability, 4), "percent": round(probability * 100)}
                for label, probability in top_predictions
            ],
            is_healthy=is_healthy,
            primary_label=primary_label,
            advice_key=advice_key,
            confidence_note=confidence_note,
            model_mode="real",
        )


def get_predictor(app):
    mode = app.config.get("PREDICTOR_MODE", "demo")
    predictor = app.extensions.get("medvision_predictor")
    if predictor and predictor["mode"] == mode:
        return predictor["instance"]

    if mode == "real":
        instance = TorchPredictor(app.config.get("MODEL_CHECKPOINT"))
    else:
        instance = DemoPredictor()

    app.extensions["medvision_predictor"] = {"mode": mode, "instance": instance}
    return instance
