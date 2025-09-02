import csv
import re
import sys
import langdetect
from deep_translator import GoogleTranslator
from transformers import pipeline


sys.stdout.reconfigure(encoding="utf-8")

# HuggingFace sentiment model (multilingual)
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Translator
translator = GoogleTranslator(source="auto", target="en")


def detect_language(text):
    try:
        return langdetect.detect(text)
    except:
        return "en"

def is_hinglish(text):
    """ Check if text looks English but has many non-English words. """
    words = text.split()
    non_english_like = sum(1 for w in words if not re.match("^[a-zA-Z]+$", w))
    return (non_english_like / max(1, len(words))) > 0.3

def smart_translate(text):
    lang = detect_language(text)
    if lang != "en" or is_hinglish(text):
        try:
            return translator.translate(text)
        except:
            return text
    return text

def custom_sentiment(text, model_output):
    """ Override Neutral if text looks like a problem/complaint """
    label = model_output["label"]
    problem_keywords = [
        "not", "no", "issue", "problem", "can't", "cannot",
        "fail", "error", "doesn't", "isn't", "missing", "slow", "bad"
    ]
    if label == "Neutral":
        lower_text = text.lower()
        if any(word in lower_text for word in problem_keywords):
            return "Negative"
    return label

# ---- Main Processing ----
input_file = r"C:\Users\Haris\Atomberg\Data\youtube_comments_labeled.csv"
output_file = r"C:\Users\Haris\Atomberg\Data\youtube_comments_sentiment.csv"

with open(input_file, newline="", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8-sig") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Translated", "RawSentiment", "FinalSentiment"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        brand = row.get("brand", "").strip()
        comment = str(row.get("comment", "")).strip()  

        if not comment:
            # keep track of empty comments 
            print(f"Skipping empty comment for brand: {brand}")
            continue

        # Translate if needed
        translated = smart_translate(comment) or comment
        translated = str(translated)

        #  Transformer sentiment
        if translated.strip():
            try:
                result = pipe(translated[:512])[0]  
                raw_sentiment = result.get("label", "Unknown")
            except Exception:
                raw_sentiment = "Error"
                result = {"label": "Neutral"}  #  fallback
        else:
            raw_sentiment = "Unknown"
            result = {"label": "Neutral"}

        
        final_sentiment = custom_sentiment(translated, result)

        
        row["Translated"] = translated
        row["RawSentiment"] = raw_sentiment
        row["FinalSentiment"] = final_sentiment
        writer.writerow(row)

       
        print(
            f"Processed brand: {brand} | Comment: {comment[:40]}... | "
            f"Translated: {translated[:40]}... | "
            f"Raw: {raw_sentiment} | Final: {final_sentiment}"
        )
