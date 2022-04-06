import string
import re
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

def clearTextList(texts: list()):
    words_to_remove = stopwords.words('portuguese')
    stemmer = RSLPStemmer()

    my_regex = re.compile("^[A-zÀ-ú]+$")
    cleaned_text_list = []

    for text in texts:
        cleaned_text = ""

        text = text.lower()

        # remove hiperlinks
        text = re.sub(r'http\S+', '', text)
        
        # remove mentions
        text = re.sub(r'@\S+', '', text)
        
        # remove hashtags
        text = re.sub(r'#\S+', '', text)

        # remove punctuaction
        text = text.translate(str.maketrans('', '', string.punctuation))

        for word in text.split():
            if my_regex.match(word) and word not in words_to_remove:
                cleaned_text = cleaned_text + stemmer.stem(word) + " "
        text = cleaned_text.strip()
        cleaned_text_list.append(text)
    
    return cleaned_text_list