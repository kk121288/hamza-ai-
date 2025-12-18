@echo off
cd /d "D:\New folder\AI-Plagiarism-Checker"
call venv\Scripts\activate.bat
python -m uvicorn main:app --host 0.0.0.0 --port 8000 >> "logs\uvicorn-out.log" 2>> "logs\uvicorn-err.log"
