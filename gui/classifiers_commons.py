import string
import re

def clearTextList(texts: list()):
    my_regex = re.compile("^[A-zÀ-ú]+$")
    cleaned_text_list = []

    for text in texts:
        cleaned_text = ""

        # remove hiperlinks
        text = re.sub(r'http\S+', '', text)
        
        # remove mentions
        text = re.sub(r'@\S+', '', text)
        
        # remove hashtags
        text = re.sub(r'#\S+', '', text)

        # remove punctuaction
        text = text.translate(str.maketrans('', '', string.punctuation))

        for word in text.split(" "):
            if my_regex.match(word):
                cleaned_text = cleaned_text + word + " "
        text = cleaned_text.strip()
        cleaned_text_list.append(text)
    
    return cleaned_text_list