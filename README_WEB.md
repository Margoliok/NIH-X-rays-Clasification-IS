# MedVision Flask Web App

## Run
1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python run.py
```

## Notes
- The first version uses `demo` prediction mode.
- Uploaded files are stored in `instance/uploads`.
- Analysis history is stored in `instance/app.db`.
- To switch languages, use the header language toggle inside the app.

## Future Real Model Integration
Set environment variables before launch:

```bash
set PREDICTOR_MODE=real
set MODEL_CHECKPOINT=path\to\checkpoint.pth
python run.py
```

If no checkpoint is available, the app will stay in demo mode for now.
