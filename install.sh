#!/bin/bash

echo "📦 Installation de l'API Media Downloader..."

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ffmpeg
fi

pip install spotdl

echo "✅ Installation terminée!"
echo "🚀 Pour démarrer l'API: python run.py"

