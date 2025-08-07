import re
import emoji
import contractions

def normalize_text(text, language="en"):
    # Eliminar emojis
    text = emoji.replace_emoji(text, replace="")

    # Eliminar las URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Menciones y Hastags: Quitar @ y # pero conservar el texto
    text = re.sub(r'@(\w+)', r'\1', text)
    text = re.sub(r'#(\w+)', r'\1', text)

    # Convertir a minúsculas
    text = text.lower()

    if language == "en":
        text = contractions.fix(text)

    # Eliminar múltiple espacios
    text = re.sub(r'\s+', ' ', text).strip()

    return text