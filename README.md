# AI-Content-Analyzer
✅ A summary score (0–100) based on Google AI summary patterns

🧠 Structure and readability feedback

🏷️ Entity extraction (ORG, GPE, PERSON, etc.)

📌 Specific suggestions to improve summary-worthiness

🚀 Features ✅ Accepts raw HTML/text input via POST ✅ Calculates content summary potential ✅ Identifies summary-worthy sentences ✅ Suggests improvements (if score < 95) ✅ Extracts named entities with spaCy ✅ Returns a complete JSON analysis

project-root/ ├── api.py # Main Flask API ├── README.md # This file ├── requirements.txt # Python dependencies

# 🔧 Setup Instructions

1. Clone the repository git clone 
  https://github.com/yourname/ai-summary-analyzer.git cd ai-summary-analyzer

2. Create a virtual environment (optional) python -m venv venv source venv/bin/activate # On Windows
 venv\Scripts\activate

3. Install dependencies 
  pip install -r requirements.txt

Download spaCy model python -m spacy download en_core_web_sm

# ▶️ Run the API
   python api.py
   http://127.0.0.1:5000/analyze

# Limitations & Challenges:
1. spaCy may miss short or generic entities like "AI".
2. Rule-based scoring lacks real AI learning or accuracy.
3. Only works on English HTML/text content — no media or multilingual support.
