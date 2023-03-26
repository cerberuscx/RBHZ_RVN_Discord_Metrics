@echo off
setlocal

cd /d "%~dp0"
cd ..\RBHZ_RVN_Discord_Metrics

python -m venv venv
call "venv\Scripts\activate.bat"
python -m pip install -U pip
pip install -r requirements.txt
python Ravencoin.py

echo Initialization complete. Launching Ravencoin.py
pause
