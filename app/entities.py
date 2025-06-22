import spacy
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

def recognize_entities(html_content):
    # Strip HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text(separator=' ', strip=True)

    # Run spaCy
    doc = nlp(plain_text)

    # Extract unique entities
    entities = list({ent.text.strip() for ent in doc.ents if len(ent.text.strip()) > 1})
    types = list({ent.label_ for ent in doc.ents})

    return {
        "entities": entities,
        "types": types
    }

