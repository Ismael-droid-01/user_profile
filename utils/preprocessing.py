import re
import emoji
import contractions
import string
import spacy

# Modelos de tokenización
_npl_models = {
    "es": spacy.load("es_core_news_sm"),
    "en": spacy.load("en_core_web_sm")
}

def normalize_text(text, language="en"):
    original_text = text

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

    # Eliminar signos de puntuación
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)

    # Eliminar múltiple espacios
    text = re.sub(r'\s+', ' ', text).strip()

    # Calcular el porcentaje de cambio
    total_chars = max(len(original_text), 1)
    changed_chars = sum(1 for o, n in zip(original_text, text) if o != n) # + abs(len(original_text) - len(text))
    change_percentage = (changed_chars / total_chars) * 100

    return text, round(change_percentage, 2)

def parse_and_tokenize(text, language="en"):
    if language not in _npl_models:
        return None
    
    doc = _npl_models[language](text)

    tokens = []
    for token in doc:
        # is_stop: Stopword ("y", "el", "la")
        # is_punct: Signos de puntuación ("-", "?", ".")
        # is_alpha: Solo letras ("perro", "comer")
        if (not token.is_stop and not token.is_punct and token.is_alpha):
            tokens.append(token.lemma_.lower())
    
    return tokens