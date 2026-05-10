import re
import nltk
from nltk.corpus import stopwords

try:
    STOPWORDS = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    STOPWORDS = set(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))


def clean_text(text):

    # lowercase
    text = text.lower()

    # remove URLs
    text = re.sub(r'http\S+', '', text)

    # remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # tokenize
    words = text.split()

    # remove stopwords
    words = [word for word in words if word not in STOPWORDS]

    return " ".join(words)