import re
import html
import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    """
    Clean and normalize job-description text.
    """

    if not isinstance(text, str):
        return ""

    # 1. Convert HTML entities
    text = html.unescape(text)

    # 2. Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # 3. Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # 4. Convert text to lowercase
    text = text.lower()

    # 5. Replace special characters with spaces
    text = re.sub(r"[^a-z0-9+#.\-/ ]", " ", text)

    # 6. Normalize multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_text(text):
    """
    Perform NLP preprocessing using spaCy.
    """

    cleaned = clean_text(text)

    doc = nlp(cleaned)

    tokens = []

    for token in doc:

        # Remove stopwords and punctuation
        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if token.is_space:
            continue

        tokens.append(token.text)

    return " ".join(tokens)


if __name__ == "__main__":

    sample_text = """
    We are looking for a Data Scientist with experience in
    Python, SQL, Machine Learning, Pandas and TensorFlow.
    Visit https://example.com for more information.
    """

    print("Original text:")
    print(sample_text)

    print("\nCleaned text:")
    print(clean_text(sample_text))

    print("\nPreprocessed text:")
    print(preprocess_text(sample_text))