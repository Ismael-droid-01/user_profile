import re
import emoji

def normalize_text(text):
    # Eliminar emojis
    text = emoji.replace_emoji(text, replace="")

    # Eliminar las URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Menciones y Hastags: Quitar @ y # pero conservar el texto
    text = re.sub(r'@(\w+)', r'\1', text)
    text = re.sub(r'#(\w+)', r'\1', text)

    # Convertir a minúsculas
    text = text.lower()

    # Eliminar múltiple espacios
    text = re.sub(r'\s+', ' ', text).strip()

    return text