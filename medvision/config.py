import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DEFAULT_CHECKPOINT_PATH = BASE_DIR / "models" / "stage1_1e-05_03.pth"
    SECRET_KEY = os.environ.get("SECRET_KEY", "medvision-dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    PREDICTOR_MODE = os.environ.get("PREDICTOR_MODE", "real" if DEFAULT_CHECKPOINT_PATH.exists() else "demo")
    MODEL_CHECKPOINT = os.environ.get(
        "MODEL_CHECKPOINT",
        str(DEFAULT_CHECKPOINT_PATH) if DEFAULT_CHECKPOINT_PATH.exists() else "",
    )
    DEFAULT_LANGUAGE = "kk"
    LANGUAGES = ("kk", "ru")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
