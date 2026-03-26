# 🎙️ Audify - txt2mp3 

> Turn any text into natural-sounding audio — paste, upload, or convert from the command line.  
> Free. No API key. Powered by Microsoft Edge neural voices.

**Live demo:** https://audify-txt2mp3.streamlit.appp

---

## 📂 Project Structure

```
readout/
├── app.py            ← Streamlit web app
├── tts.py            ← CLI tool
├── requirements.txt
├── .gitignore
├── example.txt       ← sample input
└── README.md
```

---

## 📦 Installation

```bash
git https://github.com/s3achan/Audify---txt2mp3
cd readout
pip install -r requirements.txt
```

---

## 🌐 Web App (Streamlit)

### Run locally

```bash
streamlit run app.py
```

### Deploy for free

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. **New app** → select repo → main file: `app.py` → Deploy

You'll get a public shareable URL. No secrets or environment variables needed.

**Features:**
- Paste text or upload a `.txt` file
- Live word count + estimated audio duration
- 9 neural voices (US + British English)
- Speaking rate slider (−30% to +30%)
- In-browser audio preview + MP3 download

---

## 💻 CLI Tool

### Basic

```bash
python tts.py notes.txt
# → notes.mp3
```

### Custom voice and rate

```bash
python tts.py prep.txt --voice en-US-AriaNeural --rate -10%
```

### Batch conversion

```bash
python tts.py file1.txt file2.txt file3.txt
```

### Custom output path

```bash
python tts.py notes.txt --output audio/notes.mp3
```

### List all available voices

```bash
python tts.py --list-voices
python tts.py --list-voices --filter en-US
python tts.py --list-voices --filter en-GB
```

### All options

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--voice` | `-v` | Voice name | `en-US-EmmaNeural` |
| `--rate` | `-r` | Speaking rate (`+20%`, `-10%`, etc.) | `+0%` |
| `--output` | `-o` | Output path (single file only) | `<input>.mp3` |
| `--list-voices` | `-l` | Print all voices and exit | — |
| `--filter` | `-f` | Filter voice list by locale or name | — |

---

## 🎤 Voices

| Voice | Gender | Style |
|-------|--------|-------|
| `en-US-EmmaNeural` | Female | Natural, clear |
| `en-US-AriaNeural` | Female | Expressive |
| `en-US-JennyNeural` | Female | Friendly |
| `en-US-MichelleNeural` | Female | Warm |
| `en-US-GuyNeural` | Male | Professional |
| `en-US-AndrewNeural` | Male | Warm |
| `en-US-BrianNeural` | Male | Deep |
| `en-GB-RyanNeural` | Male | British |
| `en-GB-SoniaNeural` | Female | British |

> To see all voices across all languages: `python tts.py --list-voices`

---

## 💡 Tips

- **Study / interview prep:** `--rate -10%` for a relaxed, easy-to-follow pace
- **Quick review:** `--rate +20%` when skimming familiar material
- **Personal `.txt` files are gitignored** — your notes stay local; only `example.txt` is committed

---

## 🔗 Credits

Built on [edge-tts](https://github.com/rany2/edge-tts) by rany2.

---

## 📄 License

MIT
