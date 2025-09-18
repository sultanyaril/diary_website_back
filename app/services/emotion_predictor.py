import re
import asyncio
from transformers import pipeline
from googletrans import Translator

# Define candidate emotions (extend/modify as needed)
CANDIDATE_EMOTIONS = [
    "joy", "sadness", "anger", "fear", "disgust",
    "surprise", "neutral", "love", "confusion", "pride"
]

# Load zero-shot classifier
classifier = pipeline("zero-shot-classification", 
                      model="facebook/bart-large-mnli",
                      device=0)

def get_list_of_emotions():
    """Return the list of candidate emotions."""
    return CANDIDATE_EMOTIONS


def extract_entries_from_text(text):
    """
    Split diary text into individual entries based on date lines (MM/DD/YYYY).
    Returns list of dicts with 'date' and 'journal_entry'.
    """
    entries = []
    pattern = r'(\d{2}/\d{2}/\d{4})'
    parts = re.split(pattern, text)

    for i in range(1, len(parts), 2):
        date = parts[i].strip()
        content = parts[i + 1].strip().replace('\n', ' ')
        entries.append({'date': date, 'journal_entry': content})
    return entries


async def translate_text(text, target_lang="en"):
    """
    Translate text to English (if needed).
    """
    async with Translator() as translator: 
        translation = await translator.translate(text) 
    return translation


def analyze_emotion(text, top_n=1):
    """
    Run zero-shot emotion classification.
    Returns top-N emotions with their probabilities.
    """
    result = classifier(text, candidate_labels=CANDIDATE_EMOTIONS, multi_label=True)
    labels, scores = result["labels"], result["scores"]

    # Sort by score
    emotions = sorted(zip(labels, scores), key=lambda x: -x[1])

    if top_n == 1:
        return emotions[0][0]  # just the best label
    return emotions[:top_n]    # list of (label, score)


def predict_emotion(text, top_n=1, translate=True):
    """
    Predicts the most probable emotions of the given diary entry.
    If translate=True, translates entry into English first.
    """
    if translate:
        text = asyncio.run(translate_text(text)).text

    return analyze_emotion(text, top_n=top_n)
