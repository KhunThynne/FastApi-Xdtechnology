@echo off
cd /d "%~dp0"

set PYTHONPATH=%CD%\src
set PYTHONDONTWRITEBYTECODE=1

call venv\Scripts\activate

echo [0/5] Cleaning up __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo [1/5] Running Ruff Formatter...
ruff format src/

echo [2/5] Running Ruff Linter...
ruff check src/ --fix

echo [3/5] Running Mypy Type Checker...
mypy src/

echo [4/5] Starting FastAPI Server...
python src\main.py

pause
