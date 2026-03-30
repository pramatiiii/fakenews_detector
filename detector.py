from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
import requests
import re
from datetime import datetime

import os
API_KEY = os.getenv("GROQ_API_KEY") # Replace with your actual key

app = Flask(__name__, static_folder='.')
client = Groq(api_key=API_KEY)
history_log = []


def fetch_url_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        text = response.text
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 200:
            return text[:3000]
        return None
    except:
        return None


def parse_result(result):
    lines = result.strip().split("\n")
    verdict = ""
    confidence = ""
    reasons = []
    advice = ""
    reading_reasons = False
    for line in lines:
        if line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            confidence = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("REASONS:"):
            reading_reasons = True
        elif line.startswith("ADVICE:"):
            reading_reasons = False
            advice = line.replace("ADVICE:", "").strip()
        elif reading_reasons and line.strip().startswith("-"):
            reasons.append(line.strip()[1:].strip())
    return verdict, confidence, reasons, advice


def get_score(verdict, confidence):
    base = {"LIKELY REAL": 10, "SUSPICIOUS": 50, "LIKELY FAKE": 90}
    modifier = {"High": 0, "Medium": 10, "Low": 20}
    score = base.get(verdict.upper().strip(), 50)
    if "FAKE" in verdict.upper():
        score += modifier.get(confidence, 10)
    elif "REAL" in verdict.upper():
        score -= modifier.get(confidence, 10)
    return max(0, min(100, score))


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    url = data.get('url', '')

    if url.strip():
        fetched = fetch_url_text(url.strip())
        if fetched:
            text = fetched
        else:
            return jsonify({"error": "Could not fetch article from that URL. Try pasting the text directly."})

    if not text.strip():
        return jsonify({"error": "Please enter some text or a URL to analyze."})

    prompt = f"""You are an expert fact-checker and misinformation analyst.

Analyze the following news text and determine if it is:
- LIKELY REAL: Credible, factual, measured language
- SUSPICIOUS: Some red flags, needs verification
- LIKELY FAKE: Clear misinformation, fabricated, or extremely misleading

News text:
\"\"\"{text[:2000]}\"\"\"

Respond in this EXACT format and nothing else:
VERDICT: [LIKELY REAL / SUSPICIOUS / LIKELY FAKE]
CONFIDENCE: [High / Medium / Low]
REASONS:
- [Reason 1]
- [Reason 2]
- [Reason 3]
ADVICE: [One sentence telling the user what to do]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    result = response.choices[0].message.content
    verdict, confidence, reasons, advice = parse_result(result)
    score = get_score(verdict, confidence)

    history_log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "text": text.strip()[:80],
        "verdict": verdict,
        "score": score,
    })

    return jsonify({
        "verdict": verdict,
        "confidence": confidence,
        "reasons": reasons,
        "advice": advice,
        "score": score,
        "history": history_log[-10:]
    })


if __name__ == '__main__':
    print("\n✓ Server running! Open this in your browser:")
    print("  http://127.0.0.1:5000\n")
    app.run(debug=False, port=5000)