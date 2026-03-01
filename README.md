# Media Downloader API

API REST pour télécharger des médias depuis YouTube, Spotify, Instagram, TikTok et Pinterest.

## 🚀 Installation

### Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

### Windows
```batch
install.bat
```

## 🏃 Utilisation

```bash
python run.py
```

L'API sera disponible sur `http://localhost:8000`

## 📚 Documentation API

Une fois l'API lancée :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## 🎯 Endpoints

### `GET /api/health`
Vérifie que l'API fonctionne.

### `GET /api/info?url={URL}`
Récupère les métadonnées d'un lien.

### `POST /api/download`
Télécharge un média.

Body JSON :
```json
{
  "url": "https://youtube.com/watch?v=...",
  "format_id": "mp4_hd"
}
```

## 🔧 Formats disponibles

- `mp4_hd` : Vidéo HD 1080p
- `mp4_sd` : Vidéo SD 480p  
- `mp3` : Audio MP3 320kbps
- `wav` : Audio WAV lossless

## 🌐 Plateformes supportées

- ✅ YouTube (vidéos, playlists)
- ✅ Spotify (titres, playlists)
- ✅ Instagram (posts, reels, stories)
- ✅ TikTok (vidéos sans watermark)
- ✅ Pinterest (pins, vidéos)

## ⚙️ Configuration

Modifiez `app/config.py` pour personnaliser :
- Dossier de téléchargement
- Taille max des fichiers
- Rate limiting
- Formats disponibles

