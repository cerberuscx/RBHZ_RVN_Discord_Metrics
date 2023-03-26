@echo off
setlocal

cd /d "%~dp0"
cd ..\RBHZ_RVN_Discord_Metrics

python -m venv venv
call "venv\Scripts\activate.bat"
python -m pip install -U pip
pip install -r requirements.txt

echo Setup complete. To run the script, use: LAUNCH.bat
pause
