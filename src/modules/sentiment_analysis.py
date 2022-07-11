from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
from collections import Counter

_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

_model = TFAutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

_classifier = pipeline(task="sentiment-analysis", model=_model, tokenizer=_tokenizer)


def predict_net_sentiment(text: list):
    """
    Returns the net sentiment (mode) of the list of texts
    text: list\tList of texts
    returns: tuple\tMode predicted label and count from all the texts
    """
    results = predict_sentiment(text)
    labels = []
    for result in results:
        labels.append(result["label"])

    counter = Counter(labels)

    return counter.most_common(1)[0]


def predict_sentiment(text: str or list):
    """
    Returns a list of dictionaries containing label, and score
    text:str or list\t Value to pass to the classifier
    returns: list
    """
    result = _classifier(text)
    return result
