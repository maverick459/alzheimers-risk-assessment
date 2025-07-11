
@echo off
echo Installing dependencies...
pip install psycopg2-binary flask openai python-dotenv reportlab numpy matplotlib

echo.
echo Starting Flask application...
python main.py

pause
