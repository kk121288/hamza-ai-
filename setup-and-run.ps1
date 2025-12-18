if (-not (Test-Path -Path ".\venv")) {
    python -m venv venv
}

.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 --log-level debug