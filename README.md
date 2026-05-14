<div align="center">

# 📚 StudyBuddy

### AI-Powered Multimodal Study Platform

**Transform any PDF into a complete study kit in under 60 seconds — completely free.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036?style=flat-square)](https://console.groq.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22C55E?style=flat-square)]()

[Features](#-features) · [Quick Start](#-quick-start) · [Tech Stack](#-tech-stack) · [Architecture](#-architecture) · [API Reference](#-api-reference) · [Deployment](#-deployment)

</div>

---

## 🧠 What is StudyBuddy?

StudyBuddy is a full-stack web application that solves one of the biggest pain points in student life — the hours it takes to manually convert raw study material into useful formats.

Upload **any PDF** and get back:

| Artefact | What you get | Powered by |
|---|---|---|
| 📝 **Summary** | Structured prose with Key Concepts, Glossary, and Takeaways | Groq · Llama 3.3 70B |
| 🃏 **Flashcards** | 10–20 flip cards, auto-saved for spaced repetition | Groq · Llama 3.3 70B |
| 🧠 **Quiz** | 10 MCQs with 4 options, correct answer, and explanation | Groq · Llama 3.3 70B |
| 🎧 **Audio Notes** | MP3 audiobook of your content — study on the go | Groq script + gTTS |

Plus a **document-aware AI chatbot**, **SM-2 spaced repetition review**, **quiz performance analytics**, **Weak Area Detector**, **Pomodoro timer**, and a **12-badge achievement system** — all in one app, with **zero database required**.

---

## ✨ Features

### 🏠 Dashboard
- **Drag-and-drop PDF upload** — drop your file or click to browse
- **One-click generation** — Summary, Flashcards, Quiz, and Audio Notes individually
- **Generate Everything** — fires all four concurrently with `Promise.all()`
- **3D flip flashcards** — CSS perspective transform, click to reveal answer
- **Live quiz** — progress bar, per-question explanations, score tracking
- **Built-in audio player** — HTML5 `<audio>` element with generated MP3
- **Floating AI chatbot** — document-aware, multi-turn, context-injected

### 👤 Profile — 5 Tabs

| Tab | What's inside |
|---|---|
| 📊 **Overview** | 24-week GitHub-style activity heatmap · Quiz performance bar chart with ↑/↓ trend · Weak Area Detector (topics under 75%) · Pomodoro timer (25/5/15 min) · Recent activity feed |
| 🃏 **Review Cards** | SM-2 spaced repetition — Due Now / Learning / Mastered · Full flip-card review session · Got It / Didn't Know scheduling |
| 🏅 **Achievements** | 12 badges — First Upload, Quiz Master, Perfect Score, On Fire, Week Warrior, Night Owl, Early Bird, Power User, and more |
| 📂 **Files** | Full upload library — filename, pages, word count, date, delete |
| 📈 **Progress** | Animated progress bars · Full quiz score history with colour-coded circles |

### 🛡️ Reliability
- **3-model fallback chain** — auto-retries on rate limit with no user interruption
- **JSON fence stripping** — handles markdown-wrapped AI responses gracefully
- **Error toasts** — clear user-facing messages for every failure mode

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | [python.org](https://python.org) |
| pip | 22.0+ | Bundled with Python |
| Groq API Key | Free | [console.groq.com/keys](https://console.groq.com/keys) — takes 60 seconds |
| Web Browser | Chrome/Edge/Firefox 100+ | Must support ES2020 + localStorage |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/studybuddy.git
cd studybuddy

# 2. (Recommended) Create a virtual environment
python -m venv venv

# Activate on macOS / Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Set your API key

```bash
# macOS / Linux
export GROQ_API_KEY=gsk_your_key_here

# Windows — Command Prompt
set GROQ_API_KEY=gsk_your_key_here

# Windows — PowerShell
$env:GROQ_API_KEY = "gsk_your_key_here"
```

> ⚠️ **Never** hardcode your API key in source code. Never commit it to Git. Always use environment variables.

### Run

```bash
python app.py
```

Open **http://localhost:5000** in your browser 🎉

---

## 📁 Project Structure

```
studybuddy/
│
├── app.py                    # Flask backend — all routes and AI logic
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── templates/
│   ├── login.html            # Authentication page (sign in / sign up / guest)
│   ├── dashboard.html        # Main workspace — upload, generate, chat
│   └── profile.html          # Analytics, spaced repetition, achievements
│
└── [audio_files/]            # Auto-created at runtime by tempfile.mkdtemp()
    └── audio_<uuid>.mp3      # Generated audio notes (cleared on server restart)
```

> The `audio_files/` directory is created automatically when the app starts. Do not create it manually.

---

## 🔧 Tech Stack

### Backend
| Package | Version | Purpose |
|---|---|---|
| `flask` | 3.0.3 | Web framework — HTTP routing, template rendering |
| `flask-cors` | 4.0.1 | Cross-Origin Resource Sharing headers |
| `PyPDF2` | 3.0.1 | PDF text extraction — page-by-page text layer reading |
| `gTTS` | 2.5.1 | Google Text-to-Speech — MP3 audio synthesis |
| `groq` | 0.9.0+ | Official Groq SDK — Llama 3.3 70B inference |

### Frontend
| Technology | Purpose |
|---|---|
| HTML5 | Page structure — semantic markup, `<audio>`, drag-and-drop events |
| CSS3 | Styling — CSS custom properties, 3D transforms (flip cards), grid/flex |
| Vanilla JavaScript (ES2020) | All interactivity — fetch API, localStorage, SM-2 algorithm, heatmap |
| Google Fonts | Syne (headings) + DM Sans (body) |

### AI & External Services
| Service | Usage | Cost |
|---|---|---|
| [Groq Cloud](https://console.groq.com) | LLM inference — all content generation | Free (14,400 req/day) |
| [Llama 3.3 70B](https://huggingface.co/meta-llama) | Language model — summary, cards, quiz, chat | Via Groq |
| [Google TTS via gTTS](https://gtts.readthedocs.io) | Audio synthesis | Free |

### Data Storage
No server-side database. All user data persists in **browser localStorage**:

| Key | Contents |
|---|---|
| `sb_user` | Active user profile + stats object |
| `sb_users` | All registered accounts (email → profile map) |
| `sb_sr_cards` | Flashcard array with SM-2 scheduling fields |

---

## 🏗️ Architecture

StudyBuddy follows a **three-tier architecture** running entirely on a single local machine:

```
┌─────────────────────────────────────────────────────────┐
│  TIER 1 — Presentation Layer (Browser)                  │
│  login.html · dashboard.html · profile.html             │
│  Vanilla JS · CSS3 · localStorage                       │
└──────────────────┬──────────────────────────────────────┘
                   │  fetch() · HTTP/JSON
┌──────────────────▼──────────────────────────────────────┐
│  TIER 2 — Application Layer (Flask · localhost:5000)    │
│                                                         │
│  /api/extract   /api/summary   /api/flashcards          │
│  /api/quiz      /api/audio     /api/chat                │
│  /audio/<file>                                          │
└──────────────────┬──────────────────────────────────────┘
                   │  HTTPS / TLS
┌──────────────────▼──────────────────────────────────────┐
│  TIER 3 — Data Layer                                    │
│  Browser localStorage · Local filesystem (MP3 files)   │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  EXTERNAL SERVICES                                      │
│  Groq Cloud API (Llama 3.3 70B)  ·  Google TTS          │
└─────────────────────────────────────────────────────────┘
```

### AI Model Fallback Chain

```python
GROQ_MODEL_FALLBACK = [
    "llama-3.3-70b-versatile",   # Primary — best quality, ~300 tok/sec
    "llama3-70b-8192",            # Fallback 1 — if primary hits rate limit
    "llama3-8b-8192",             # Fallback 2 — smallest, always available
]
```

If any model raises an exception, the system silently retries with the next one. All three models draw from independent quota pools.

---

## 📡 API Reference

| Method | Route | Input | Output |
|---|---|---|---|
| `GET` | `/` | — | `login.html` |
| `GET` | `/dashboard` | — | `dashboard.html` |
| `GET` | `/profile` | — | `profile.html` |
| `POST` | `/api/extract` | `multipart/form-data: file (.pdf)` | `{ text, word_count, pages }` |
| `POST` | `/api/summary` | `{ text: string }` | `{ summary: string }` |
| `POST` | `/api/flashcards` | `{ text: string }` | `{ flashcards: [{id, front, back, ...sm2}] }` |
| `POST` | `/api/quiz` | `{ text: string }` | `{ questions: [{question, options, correct, explanation}] }` |
| `POST` | `/api/audio` | `{ text: string }` | `{ filename: string, script: string }` |
| `POST` | `/api/chat` | `{ message, document_text, history[] }` | `{ reply: string }` |
| `GET` | `/audio/<filename>` | URL param | MP3 binary stream |

---

## 🔁 Spaced Repetition Schedule (SM-2)

Each flashcard carries `interval`, `repetitions`, `easeFactor`, `nextReview`, and `status` fields updated on every review.

| Response | Next Review | Status |
|---|---|---|
| ✗ Didn't Know | 1 minute | Learning |
| ✓ Got It (1st) | 10 minutes | Learning |
| ✓ Got It (2nd) | 1 day | Learning |
| ✓ Got It (3rd) | 3 days | Learning |
| ✓ Got It (4th+) | 7 days | **Mastered** |

---

## 🏅 Achievement Badges

| Badge | Unlock Condition |
|---|---|
| 📄 First Upload | Upload your first PDF |
| 🧠 Quiz Taker | Complete your first quiz |
| 🃏 Card Creator | Generate a flashcard set |
| ⭐ Perfect Score | Score 100% on a quiz |
| 📚 Bookworm | Upload 5 PDFs |
| 🏆 Quiz Master | Complete 10 quizzes |
| 🎯 High Achiever | Score 90%+ on 3 quizzes |
| 🔥 On Fire | Maintain a 3-day study streak |
| ⚔️ Week Warrior | Maintain a 7-day study streak |
| 🦉 Night Owl | Study after 10 PM |
| 🌅 Early Bird | Study before 7 AM |
| ⚡ Power User | Upload 10 PDFs |

---

## ☁️ Deployment

### Render.com (Free — Recommended)

1. Add `gunicorn` to `requirements.txt`

2. Create `render.yaml` in project root:
```yaml
services:
  - type: web
    name: studybuddy
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
```

3. Update the last line of `app.py`:
```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
```

4. Push to GitHub → [render.com](https://render.com) → New Web Service → connect repo → add `GROQ_API_KEY` environment variable → Deploy.

**Your live URL:** `https://studybuddy.onrender.com`

### Railway.app

Create a `Procfile` (no extension):
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub → add `GROQ_API_KEY` → Generate Domain.

### Instant Demo Link (ngrok)

```bash
# Terminal 1
python app.py

# Terminal 2
ngrok http 5000
# Prints: https://abc123.ngrok-free.app
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | **Yes** | Groq Cloud API key — free at [console.groq.com/keys](https://console.groq.com/keys) |
| `FLASK_DEBUG` | No | Set to `0` to disable debug mode in production |
| `PORT` | No | Override default port (5000). Set automatically by Render/Railway. |

---

## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ValueError: GROQ_API_KEY not set` | Key not in current terminal session | Set the env variable in the same terminal as `python app.py` |
| `Address already in use (port 5000)` | Another process on port 5000 | Change to `app.run(port=5001)` and update fetch URLs in HTML files |
| `ModuleNotFoundError: No module named flask` | Dependencies not installed / venv not active | Run `pip install -r requirements.txt` with venv activated |
| Empty text from PDF extraction | Scanned image-only PDF — no text layer | Use a digital/typed PDF; OCR the file first with Adobe or PDF24 |
| `JSONDecodeError` on flashcards/quiz | LLM returned JSON wrapped in markdown | Retry — `strip_fences()` handles most cases; different model may respond cleaner |
| `429 Too Many Requests` | Groq free tier daily quota exceeded | Wait until midnight UTC for reset, or upgrade Groq plan |
| Audio fails / gTTS timeout | No internet connection | Check connection — gTTS requires internet for Google TTS API call |
| Profile heatmap empty | No activity recorded yet | Use the dashboard to generate content; activity logs automatically |

---

## 🔮 Future Enhancements

- [ ] **OCR support** — Tesseract for scanned image-only PDFs
- [ ] **Real Google OAuth** — OAuth 2.0 PKCE flow replacing localStorage auth
- [ ] **PostgreSQL database** — persistent cross-device data via SQLAlchemy
- [ ] **Concept mind map** — auto-generated D3.js topic graph from keywords
- [ ] **Daily review emails** — Flask-APScheduler for SM-2 due-card reminders
- [ ] **React Native mobile app** — iOS/Android wrapper around the existing API
- [ ] **Multilingual audio** — gTTS supports 40+ languages; add language selector
- [ ] **Study group sharing** — deck sharing via short URL with Redis

---

## 📚 Research Foundation

This project is grounded in peer-reviewed learning science:

| Reference | Relevance |
|---|---|
| Roediger & Karpicke (2006) | Testing effect — retrieval practice improves retention by 50% |
| Wozniak (1990) | SM-2 spaced repetition algorithm |
| Mayer (2001) | Cognitive Theory of Multimedia Learning |
| Ebbinghaus (1885) | Forgetting curve and spacing effect |
| Kasneci et al. (2023) | LLMs in education — summarisation, assessment, tutoring |
| Yang et al. (2021) | AI-generated MCQs match instructor quality at 78% less time |

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes and commit
git commit -m "Add: brief description of your change"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

Please make sure your code:
- Follows the existing style (Flask routes in `app.py`, no frontend frameworks)
- Does not commit any API keys or `.env` files
- Includes a brief PR description of what changed and why

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, copy, modify, merge, publish, and distribute this software with attribution.

---

## 👩‍💻 Author

**Samreen Begum**
B.Tech — Computer Science and Engineering
Shadan Women's College of Engineering & Technology
Affiliated to JNTUH · Hyderabad, Telangana · 2026

---

<div align="center">

Made with ❤️ for students everywhere

**⭐ Star this repo if StudyBuddy helped you study smarter!**

</div>
