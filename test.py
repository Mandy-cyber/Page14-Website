import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re

def text_pre_processing(text):
    """ preprocesses text to be used in recommendation engine.
        e.g removes stop words, lemmatizes text, lowercase, etc
    
    Args:
        text (str): text to be processed
    Returns:
        processed_text (list): a list of valuable & formatted words from the text
    """
    text = re.sub(r'[0-9]', '', text)
    # remove punctuation 
    text = text.translate(str.maketrans('', '', string.punctuation))

    # lowercase the text
    text = text.lower()

    # remove duplicate spaces + newline characters
    text = " ".join(text.split())

    # remove default stopwords
    stop_words = set(stopwords.words('english'))
    new_text = []

    for word in text.split():
        if word not in stop_words:
            new_text.append(word)
        else:
            continue

    # lemmatization
    lemma = WordNetLemmatizer()
    lemma_text = list()

    for word in new_text:
        word = lemma.lemmatize(word)
        lemma_text.append(word)

    processed_text = lemma_text
    return processed_text


text = "OMG where do123 4i even77 start bro, i love biking and bAking and reading (like duh). OH!! And sometimes i like to go swimming in the river"
print(text_pre_processing(text))