# MedVision

MedVision is a diploma project for chest X-ray analysis that combines a Flask web application with a PyTorch-based classification pipeline. The system lets a user upload an X-ray image, receive the top predicted findings, read short recommendations, browse a disease reference catalog, and review saved analysis history.

The project supports two inference modes:

- `demo` mode for interface testing without a trained checkpoint
- `real` mode for inference with a saved PyTorch model checkpoint

## Features

- Upload chest X-ray images in `PNG`, `JPG`, or `JPEG`
- Show top-3 predicted findings with confidence values
- Store analysis history in SQLite
- Provide disease descriptions and short recommendations
- Support Kazakh and Russian interface languages
- Run either with a demo predictor or a real model checkpoint

## Project Structure

```text
medvision/
  blueprints/        Flask routes for pages and analysis flow
  content/           Disease catalog and localized content
  services/          Prediction logic, recommendations, content loaders
  static/            CSS and JavaScript assets
  templates/         Jinja2 HTML templates
tests/               Basic application tests
sample_xrays/        Example chest X-ray images
run.py               Flask app entry point
main.py              Training / evaluation entry point for the ML pipeline
trainer.py           Model training logic
config.py            Training configuration
requirements.txt     Python dependencies
```

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PyTorch
- OpenCV
- NumPy
- Pandas
- Matplotlib

## Installation

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

## Run The Web App

Start the application with:

```powershell
python run.py
```

After launch, open the local address shown by Flask in your browser, usually:

```text
http://127.0.0.1:5000
```

## How The Web App Works

The web application includes these main sections:

- `/` - main landing page
- `/analyze` - upload and analyze an X-ray image
- `/diseases` - disease catalog and system overview
- `/history` - saved analysis history

Uploaded files are stored in `instance/uploads`, and analysis records are saved in `instance/app.db`.

## Inference Modes

### Demo Mode

If no real checkpoint is found, the application uses demo mode automatically. In this mode, predictions are generated deterministically from the uploaded image so the interface can be tested safely.

### Real Model Mode

If the checkpoint file exists, the application can run real inference with PyTorch.

Default checkpoint path:

```text
models/stage1_1e-05_03.pth
```

You can also set the mode manually before launch:

```powershell
$env:PREDICTOR_MODE="real"
$env:MODEL_CHECKPOINT="C:\path\to\stage1_1e-05_03.pth"
python run.py
```

To force demo mode:

```powershell
$env:PREDICTOR_MODE="demo"
python run.py
```

## Machine Learning Pipeline

The repository also contains the original model training and testing pipeline for multi-label chest X-ray classification.

Main files:

- `main.py`
- `trainer.py`
- `config.py`
- `datasets.py`
- `losses.py`

Run training:

```powershell
python main.py
```

Resume from checkpoint:

```powershell
python main.py --resume --ckpt checkpoint_file.pth --stage 2
```

Run testing:

```powershell
python main.py --test --ckpt checkpoint_file.pth
```

## Dataset

The training pipeline is based on the NIH Chest X-ray dataset:

[NIH Chest X-ray Dataset](https://www.kaggle.com/nih-chest-xrays/data#Data_Entry_2017.csv)

Predicted labels include:

- Atelectasis
- Cardiomegaly
- Consolidation
- Edema
- Effusion
- Emphysema
- Fibrosis
- Hernia
- Infiltration
- Mass
- Nodule
- No Finding
- Pleural Thickening
- Pneumonia
- Pneumothorax

Note: large folders such as `data/`, `models/`, `pickles/`, and virtual environment files are excluded from Git to keep the repository lightweight.

## Testing

Run the application tests with:

```powershell
python -m unittest tests.test_app
```

The current tests cover:

- rendering of core pages
- language switching
- upload flow and history creation
- validation of unsupported file formats

## Sample Images

Example images for quick interface checks are available in `sample_xrays/`.

## Notes

- The app is intended as an educational and diploma project, not as a medical diagnostic device.
- Predictions and recommendations must not replace a doctor's conclusion.
- If ML dependencies or checkpoint assets are missing, use demo mode for presentation and interface testing.

## Author

Diploma project repository for X-ray disease classification and MedVision web interface.
