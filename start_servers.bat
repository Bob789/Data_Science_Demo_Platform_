@echo off
REM =====================================================
REM ML Platform - Start Both Servers
REM =====================================================

echo.
echo ====================================================
echo   ML PLATFORM - Starting Servers
echo ====================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then install requirements: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo [INFO] Starting FastAPI server...
echo.
start "FastAPI Server" cmd /k ".venv\Scripts\python.exe -m uvicorn app_fastapi.app_fastapi:app --reload --port 8000"

REM Wait a bit for FastAPI to start
timeout /t 3 /nobreak >nul

echo [INFO] Starting Streamlit frontend...
echo.
start "Streamlit Frontend" cmd /k ".venv\Scripts\python.exe -m streamlit run app_streamlit/app_streamlit.py"

echo.
echo ====================================================
echo   SERVERS STARTED SUCCESSFULLY!
echo ====================================================
echo.
echo FastAPI Server:  http://localhost:8000
echo Streamlit App:   http://localhost:8501
echo.
echo Two new terminal windows have been opened:
echo   - FastAPI Server (Backend API)
echo   - Streamlit Frontend (Web Interface)
echo.
echo To stop the servers, close both terminal windows.
echo ====================================================
echo.

echo Press any key to close this window...
pause >nul