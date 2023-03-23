import unicodedata
import re



def clean(text):
    # Replace non-BMP characters with a replacement character
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub(r'', text)

    normalized_text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')

    return text

text = clean("This dog 😂")
print(text)
