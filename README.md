# StudyBuddy 📚

AI-powered study platform — converts any PDF into a full study pack.

## Setup

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
python app.py
```

Visit: http://localhost:5000

## File Structure

```
studybuddy/
├── app.py
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── profile.html
└── static/        ← (empty, add CSS/JS if you split them later)
```

## Features

### Dashboard
- Drag-and-drop PDF upload
- Generate **Summary** / **Flashcards** / **Quiz** / **Audio Notes** individually or all at once
- Flashcards auto-saved to localStorage for spaced repetition
- Floating AI chatbot (document-aware)

### Profile — 5 Tabs

| Tab | What's inside |
|-----|--------------|
| 📊 Overview | GitHub-style heatmap, quiz performance chart + trend, Weak Area Detector, Pomodoro timer, activity feed |
| 🃏 Review Cards | SM-2 spaced repetition — Due Now / Learning / Mastered counts, flip-card review session |
| 🏅 Achievements | 12 badges (First Upload, Quiz Master, Perfect Score, streaks, Night Owl, etc.) |
| 📂 Files | Full file library with word counts, dates, delete |
| 📈 Progress | Animated progress bars + full quiz score history |

## AI Models (Gemini fallback chain)
1. `models/gemini-2.0-flash-lite`
2. `models/gemini-1.5-flash`
3. `models/gemini-1.5-flash-8b`

## Spaced Repetition Schedule (SM-2 inspired)

| Result | Next review |
|--------|------------|
| ✗ Wrong | 1 minute |
| ✓ 1st correct | 10 minutes |
| ✓ 2nd correct | 1 day |
| ✓ 3rd correct | 3 days |
| ✓ Mastered | 7 days |