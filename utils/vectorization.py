from collections import Counter
from datetime import datetime
from utils.preprocessing import normalize_text, parse_and_tokenize
import tkinter as tk
from tkinter import ttk
import api.reddit as reddit
import api.youtube as youtube

def standardize_social_data(data, source):
    standardized = []

    for record in data:
        user_id = None
        text = None
        account_created = None
        popularity_score = 0
        engagement_score = 0
        reach_score = 0
        language = record.get("language")

        if source == "reddit":
            user_id = record.get("author")
            text = record.get("title") + " " +  record.get("body")

            account_created = record.get("account_created")
            popularity_score = record.get("link_karma") + record.get("comment_karma")
            engagement_score = record.get("comment_karma")
            reach_score = 0

            content_meta = {
                "is_mod": record.get("is_mod"),
            }

        elif source == "youtube":
            user_id = record.get("channel_name")
            text = record.get("text")

            account_created = record.get("channel_created")
            popularity_score = record.get("subscriber_count")
            engagement_score = record.get("like_count")
            reach_score = record.get("view_count")

            content_meta = {
                "video_title": record.get("video_title"),
                "country": record.get("country")
            }

        account_created = datetime.strptime(account_created, "%Y-%m-%d %H:%M:%S")
        account_age_days = (datetime.now() - account_created).days
        
        standardized.append({
            "user_id": user_id,
            "text": text,
            "language": language,
            "account_age_days": account_age_days,
            "popularity_score": popularity_score,
            "engagement_score": engagement_score,
            "reach_score": reach_score,
            "content_meta": content_meta
        })

    return standardized

def build_bow(data, language="en"):
    bow = {}
    for record in data:
        user_id = record["user_id"]
        clean_text, _ = normalize_text(record["text"], language=language)
        tokens = parse_and_tokenize(clean_text, language=language)
        # Actualizar bolsa de palabras en caso de obtener una segunda publicación de un usuario existente
        if user_id not in bow:
            bow[user_id] = Counter(tokens)
        else:
            bow[user_id].update(Counter(tokens))
    
    # Añadir la bolsa de palabras al vector
    for record in data:
        user_id = record["user_id"]
        record["bow"] = dict(bow[user_id])
        #record["bow"] = bow[user_id]

    return data

def generate_vector(source="reddit", limit=10, language="en"):
    # 1. Obtener los datos
    if source == "reddit":
        posts = reddit.fetch_all_posts(limit=limit, language=language)
    elif source == "youtube":
        posts = youtube.fetch_all_comments(limit=limit, language=language)

    # 2. Estandarizar los datos
    data = standardize_social_data(posts, source=source)

    # 3. Construir la bolsa de palabras
    data = build_bow(data, language=language)

    return data