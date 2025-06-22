from flask import Flask, request, jsonify, render_template
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.analysis import analyze_content
from app.entities import recognize_entities

app = Flask(__name__, template_folder="../templates")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.form.get("content", "")
    print("📥 Received Content:", content)

    if not content:
        return render_template("index.html", error="Please enter some content")

    structure = analyze_content(content)
    entities = recognize_entities(content)

    print("✅ Structure Result:", structure)
    print("✅ Entities Result:", entities)

    return render_template("index.html",
        score=structure.get("summary_score"),
        summary=structure.get("summary_candidate"),
        suggestions=structure.get("suggestions"),
        entities=entities.get("entities"),
        types=entities.get("types")
    )

if __name__ == '__main__':
    app.run(debug=True)
