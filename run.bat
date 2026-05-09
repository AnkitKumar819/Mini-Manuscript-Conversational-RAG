@echo off
echo ==========================================
echo Starting Manuscript RAG Setup and Run
echo ==========================================

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found. Creating from .env.example...
    copy .env.example .env
    echo [IMPORTANT] Please open .env and add your OPENAI_API_KEY.
    pause
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install requirements
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

REM Run the application
echo Starting Streamlit app...
streamlit run src\streamlit_app.py

pause
