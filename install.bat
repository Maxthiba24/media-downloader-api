@echo off
echo 📦 Installation de l'API Media Downloader...

python -m venv venv
call venv\Scripts\activate

pip install -r requirements.txt

:: choco install ffmpeg

pip install spotdl

echo ✅ Installation terminee!
echo 🚀 Pour demarrer l'API: python run.py

