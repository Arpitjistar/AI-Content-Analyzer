import re
from bs4 import BeautifulSoup

def analyze_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True).lower()

    # Headings
    h1 = len(soup.find_all('h1'))
    h2 = len(soup.find_all('h2'))
    h3 = len(soup.find_all('h3'))

    # Paragraphs
    paragraphs = soup.find_all('p')
    paragraph_lengths = [len(p.get_text(strip=True).split()) for p in paragraphs]

    # Lists
    lists = soup.find_all(['ul', 'ol'])

    # Sentences
    total_words = len(text.split())
    sentences = re.split(r'[.!?]', text)
    short_sentences = [s.strip() for s in sentences if 5 <= len(s.strip().split()) <= 15]
    qa_keywords = ['what is', 'how to', 'why', 'does', 'can', 'should', '?']
    has_qa = any(q in text for q in qa_keywords)
    direct_answers = [s for s in sentences if ' is ' in s or ' means ' in s or ' refers to ' in s]

    # Start scoring
    score = 0

    # Headings = 25
    score += min(h1 * 5, 10)
    score += min(h2 * 3, 10)
    score += min(h3 * 2, 5)

    # Paragraphs = 15
    if len(paragraphs) >= 3:
        score += 10
    elif len(paragraphs) == 2:
        score += 5
    else:
        score -= 5
    if any(pl < 30 for pl in paragraph_lengths):
        score += 5

    # Lists = 10
    score += 10 if lists else -5

    # Q&A = 15
    if has_qa: score += 15

    # Direct answer = 15
    if len(direct_answers) >= 2: score += 15

    # Clarity = 10
    score += min(len(short_sentences) * 2, 10)

    # Keywords = 5
    keywords = ['guide', 'example', 'benefits', 'steps', 'comparison', 'vs']
    if any(kw in text for kw in keywords):
        score += 5

    # Penalty
    if total_words < 50: score -= 10

    # Clamp
    score = max(min(score, 100), 0)

    # Summary-worthy sentence
    best_line = max(short_sentences, key=len) if short_sentences else sentences[0] if sentences else ""

    # Suggestions
    suggestions = []
    if score == 100:
        suggestions.append("✅ Your content is well-structured and summary-ready! Great job!")
    else:
        if h1 == 0:
            suggestions.append("Add an H1 heading for the main topic.")
        if h2 + h3 < 2:
            suggestions.append("Use more subheadings (H2/H3) for structure.")
        if len(paragraphs) < 3:
            suggestions.append("Add more paragraphs for depth.")
        if not lists:
            suggestions.append("Use bullet or numbered lists to highlight key points.")
        if not has_qa:
            suggestions.append("Include a question-answer format (e.g. 'What is...?').")
        if len(direct_answers) < 2:
            suggestions.append("Add direct answer sentences (e.g. 'X is Y').")
        if total_words < 50:
            suggestions.append("Increase word count to improve richness.")
    
    if not suggestions and score < 100:  # Fallback if no specific suggestions were added but score isn't 100
        suggestions.append("Review content structure and clarity for better summarization.")

    return {
        "summary_score": score,
        "summary_candidate": best_line.strip().capitalize(),
        "suggestions": suggestions
    }