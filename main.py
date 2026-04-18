import os
import json
import uuid
import time
import tempfile
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

AUDIO_DIR = tempfile.mkdtemp()

# ── Groq helper ────────────────────────────────────────────────────────────────
# Model fallback chain — fastest/cheapest first, most capable last
GROQ_MODEL_FALLBACK = [
    "llama-3.3-70b-versatile",   # primary: best balance of speed + quality
    "llama3-70b-8192",            # fallback 1
    "llama3-8b-8192",             # fallback 2: smallest, almost always available
]

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. "
                         "Get your free key at https://console.groq.com/keys")
    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except ImportError:
        raise ImportError("groq SDK not installed. Run: pip install groq")

def generate_content(prompt: str, system: str = "You are a helpful study assistant.") -> str:
    """Send a prompt to Groq and return the text response, with model fallback."""
    client = get_groq_client()
    for model in GROQ_MODEL_FALLBACK:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt},
                ],
                max_tokens=4096,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq model {model} failed: {e}")
            continue
    raise RuntimeError("All Groq models failed. Check your GROQ_API_KEY and rate limits.")

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

# ── API: Extract PDF text ──────────────────────────────────────────────────────
@app.route("/api/extract", methods=["POST"])
def extract_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()
        if not text:
            return jsonify({"error": "Could not extract text from PDF"}), 400
        word_count = len(text.split())
        return jsonify({"text": text, "pages": len(reader.pages), "word_count": word_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── API: Summary ───────────────────────────────────────────────────────────────
@app.route("/api/summary", methods=["POST"])
def generate_summary():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    prompt = f"""Create a comprehensive study summary of the following text.
Structure it with:
1. **Key Concepts** (bullet points of the most important ideas)
2. **Main Summary** (3-4 paragraphs covering the core content)
3. **Important Terms** (a glossary of key terms and definitions)
4. **Key Takeaways** (5 bullet points of what to remember)

Text to summarize:
{text[:8000]}"""
    try:
        summary = generate_content(prompt)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── API: Flashcards ────────────────────────────────────────────────────────────
@app.route("/api/flashcards", methods=["POST"])
def generate_flashcards():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    prompt = f"""Create exactly 10 high-quality flashcards from the following text.
Return ONLY a valid JSON array with no extra text, markdown, or code fences.
Each flashcard must have exactly these fields:
{{"front": "question or term", "back": "answer or definition"}}

Make questions that test deep understanding, not just memorization.
Vary question types: definitions, applications, comparisons, cause-effect.

Text:
{text[:6000]}

Return only the JSON array:"""
    try:
        result = generate_content(prompt)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        cards = json.loads(result.strip())
        if not isinstance(cards, list):
            raise ValueError("Expected a list")
        for i, card in enumerate(cards):
            card["id"] = str(uuid.uuid4())
            card["created"] = int(time.time() * 1000)
            # Spaced repetition fields
            card["interval"] = 0
            card["repetitions"] = 0
            card["easeFactor"] = 2.5
            card["nextReview"] = int(time.time() * 1000)
            card["status"] = "new"
        return jsonify({"flashcards": cards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── API: Quiz ──────────────────────────────────────────────────────────────────
@app.route("/api/quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    prompt = f"""Create exactly 10 multiple-choice quiz questions from the following text.
Return ONLY a valid JSON array with no extra text, markdown, or code fences.
Each question must have exactly these fields:
{{
  "question": "the question text",
  "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
  "correct": 0,
  "explanation": "brief explanation of why this is correct"
}}
"correct" is the 0-based index of the correct option.
Make questions challenging but fair. Cover different topics from the text.

Text:
{text[:6000]}

Return only the JSON array:"""
    try:
        result = generate_content(prompt)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        questions = json.loads(result.strip())
        if not isinstance(questions, list):
            raise ValueError("Expected a list")
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── API: Audio ─────────────────────────────────────────────────────────────────
@app.route("/api/audio", methods=["POST"])
def generate_audio():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    # First summarise for audio
    prompt = f"""Create a clear, engaging audio script from the following text.
Write it as if you're explaining it to a student out loud.
Keep it under 500 words. Use natural spoken language, no markdown or special characters.

Text:
{text[:5000]}"""
    try:
        script = generate_content(prompt)
        from gtts import gTTS
        filename = f"audio_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts = gTTS(text=script[:3000], lang="en", slow=False)
        tts.save(filepath)
        return jsonify({"filename": filename, "script": script})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

# ── API: Chat ──────────────────────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    document_text = data.get("document_text", "")
    history = data.get("history", [])
    if not message:
        return jsonify({"error": "No message provided"}), 400

    if document_text:
        system = (
            "You are a helpful study assistant. The student is studying the following document:\n\n"
            f"---\n{document_text[:4000]}\n---\n\n"
            "Answer questions about this document clearly and helpfully. "
            "If asked something not in the document, use your general knowledge but mention it."
        )
    else:
        system = "You are a helpful study assistant. Help the student with their questions clearly and concisely."

    # Build proper multi-turn messages array for Groq
    messages = [{"role": "system", "content": system}]
    for msg in history[-8:]:   # last 8 turns for context
        role = msg.get("role", "user")
        if role in ("user", "assistant"):
            messages.append({"role": role, "content": msg.get("content", "")})
    messages.append({"role": "user", "content": message})

    try:
        client = get_groq_client()
        for model in GROQ_MODEL_FALLBACK:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                return jsonify({"reply": reply})
            except Exception as e:
                print(f"Chat model {model} failed: {e}")
                continue
        raise RuntimeError("All Groq models failed for chat")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)