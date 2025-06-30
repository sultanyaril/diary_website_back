import re
from transformers import pipeline, AutoTokenizer
from googletrans import Translator
import asyncio
from numpy import average


# Load the emotion classifier
tokenizer = AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-go-emotion")
classifier = pipeline("text-classification",
                      model="bhadresh-savani/bert-base-go-emotion",
                      top_k=None)


# Function to return all emotions provided by model
def get_list_of_emotions():
    return [classifier.model.config.id2label[i] for i in range(len(classifier.model.config.id2label))]


# Function to split text into chunks
def split_into_token_chunks(text, max_tokens=500):
    # TODO: Split on sentences or paragraphs for better accuracy but slower performance
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks


# Run emotion analysis
def analyze_emotion(text):
    chunks = split_into_token_chunks(text)
    chunk_lengths = [len(tokenizer.encode(chunk, add_special_tokens=False)) for chunk in chunks]
    scores = {}
    for chunk in chunks:
        probs = classifier(chunk)[0]
        for emotion in probs:
            scores[emotion['label']] = scores.get(emotion['label'], []) + [emotion['score']]
    for emotion in scores:
        scores[emotion] = average(scores[emotion], weights=chunk_lengths)
    return scores


# Extract entries based on date lines
def extract_entries_from_text(text):
    entries = []
    pattern = r'(\d{2}/\d{2}/\d{4})'
    parts = re.split(pattern, text)

    for i in range(1, len(parts), 2):
        date = parts[i].strip()
        content = parts[i + 1].strip().replace('\n', ' ')
        entries.append({'date': date, 'journal_entry': content})
    return entries


async def translate(text):
    async with Translator() as translator:
        translation = await translator.translate(text)
    return translation


def predict_emotion(text):
    """
    Predicts the emotion (sentiment) of the given text.
    Returns emotion
    """
    translated = asyncio.run(translate(text)).text

    emotions = analyze_emotion(translated)
    sorted_emotions = dict(sorted(emotions.items(), key=lambda item: -item[1]))
    most_probable_emotion = max(sorted_emotions, key=sorted_emotions.get)
    return most_probable_emotion
