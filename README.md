# 🔍 AI Fake News Detector

A powerful, AI-driven web application designed to analyze news articles, headlines, and URLs for misinformation. Built with a robust Python/Flask backend and a stunning, interactive glassmorphic frontend, this tool leverages the blazing-fast Groq API and the Llama 3.3 (70B) model to provide deep, structured fact-checking analysis in seconds.

## ✨ Key Features

* **URL & Text Analysis:** Paste a direct link to a news article for automatic text extraction, or paste the raw text/headline directly into the application.
* **Advanced AI Evaluation:** Powered by Groq and `llama-3.3-70b-versatile`, the app acts as an expert fact-checker to identify red flags, fabricated content, or misleading language.
* **Structured Insights:** Returns a clear verdict (`LIKELY REAL`, `SUSPICIOUS`, or `LIKELY FAKE`), a confidence metric, bulleted analytical reasons, and actionable advice.
* **Misinformation Risk Score:** Automatically calculates a risk score (0-100) based on the AI's verdict and confidence level, displayed via animated progress bars.
* **Premium UI/UX:** Features a responsive, dark-mode "glassmorphism" interface with beautiful typography (Cormorant Garamond & Inter), animated UI states, and color-coded results.
* **Session History:** Automatically logs and displays your recent analyses during your active session.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Requests, Regex
* **AI Provider:** Groq API (`llama-3.3-70b-versatile`)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)

## 📁 Project Structure

```text
├── detector.py            # Main Flask application, API routing, and AI logic
├── index.html             # Frontend UI, styling, and client-side scripts
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
