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
.
+-- medvision/
|   +-- blueprints/       Flask routes
|   +-- content/          disease descriptions and localized UI data
|   +-- services/         prediction, recommendations, content loading
|   +-- static/           CSS and JavaScript
|   +-- templates/        Jinja2 templates
|   +-- __init__.py       app factory
|   +-- config.py         Flask config
|   +-- extensions.py     SQLAlchemy init
|   \-- models.py         database models
+-- tests/                automated tests for the web app
+-- sample_xrays/         example X-ray images for demo and screenshots
+-- data/                 dataset files for training and evaluation
+-- models/               saved checkpoints and training plots
+-- pickles/              generated metadata files for classes and splits
+-- instance/             SQLite DB and uploaded files at runtime
+-- ОТЧЕТ/                diploma report materials
+-- run.py                starts the Flask web application
+-- main.py               starts model training / resume / testing
+-- trainer.py            training loop and checkpoint saving
+-- datasets.py           dataset preparation classes
+-- config.py             transform and ML pipeline settings
+-- losses.py             loss functions
+-- requirements.txt      Python dependencies
\-- README.md             project documentation
```

Main working folders:

```text
medvision/
  blueprints/        pages and analysis flow
  content/           disease catalog and localized content
  services/          prediction logic and recommendations
  static/            CSS and JavaScript assets
  templates/         HTML templates
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

## Dataset Preparation

The training code expects the NIH dataset inside the local `data/` folder.

Expected layout:

```text
data/
\-- NIH Chest X-rays/
    +-- Data_Entry_2017.csv
    +-- train_val_list.txt
    +-- test_list.txt
    +-- images_001/
    |   \-- images/
    +-- images_002/
    |   \-- images/
    +-- images_003/
    |   \-- images/
    \-- ...
```

Important details:

- `Data_Entry_2017.csv` is required for labels and metadata
- `train_val_list.txt` and `test_list.txt` are required for the split logic in `datasets.py`
- image files are discovered by the pattern `images*/*/*.png`
- by default `main.py` uses `--data_path "NIH Chest X-rays"`, which means the full path becomes `data/NIH Chest X-rays/`

### How To Download The Dataset

1. Open the NIH Chest X-ray dataset page on Kaggle:

[NIH Chest X-ray Dataset](https://www.kaggle.com/nih-chest-xrays/data#Data_Entry_2017.csv)

2. Download:

- the image archive folders
- `Data_Entry_2017.csv`
- `train_val_list.txt`
- `test_list.txt`

3. Unpack everything into:

```text
data/NIH Chest X-rays/
```

4. After extraction, make sure the following file exists:

```text
data/NIH Chest X-rays/Data_Entry_2017.csv
```

5. Then run training:

```powershell
python main.py
```

If you want to use another folder name, you can pass it manually:

```powershell
python main.py --data_path "My Dataset Folder"
```

In that case the code will look for:

```text
data/My Dataset Folder/
```

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

Generated ML artifacts:

- `pickles/train_val_df.pickle` - cached train/validation split dataframe
- `pickles/test_df.pickle` - cached test dataframe
- `pickles/disease_classes.pickle` - saved class labels
- `models/*.pth` - trained checkpoints
- `models/losses_*.png` - training loss plots

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
