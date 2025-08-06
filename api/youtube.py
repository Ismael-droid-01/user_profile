import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from langdetect import detect, LangDetectException
from datetime import datetime
from dateutil.parser import parse
import os
import sqlite3

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
client = build('youtube', 'v3', developerKey=API_KEY)

DB_PATH = "data/youtube_comments.db"

def get_channel_info(channel_id):
    try:
        request = client.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        items = response.get("items", [])

        if not items:
            return "unknown", "unknown", "unknown", "unknown", "unknown"
        
        channel = items[0]
        snippet = channel.get("snippet", {})
        stats = channel.get("statistics", {})

        channel_name = snippet.get("title") or "unknown"
        
        published_at = snippet.get("publishedAt", "")
        try:
            dt = parse(published_at)
            channel_created = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            channel_created = "unknown"
        
        subscriber_count = stats.get("subscriberCount")
        subscriber_count = int(subscriber_count) if subscriber_count and subscriber_count.isdigit() else "unknown"

        view_count = stats.get("viewCount")
        view_count = int(view_count) if view_count and view_count.isdigit() else "unknown"

        country = snippet.get('country', 'unknown')

        return channel_name, channel_created, subscriber_count, view_count, country
    except Exception as e:
        print(f"❌ Error al obtener información del canal '{channel_id}': {e}")
        return "unknown", "unknown", "unknown", "unknown", "unknown"
    
def get_comments(video_id, max_results=100, language="en"):
    comments = []
    channel_cache = {}
    try:
        request = client.commentThreads().list(
            part="snippet",
            videoId = video_id,
            maxResults = max_results,
            textFormat = "plainText"
        )
        response = request.execute()
    except Exception as e:
        print(f"❌ Error al obtener comentarios del video {video_id}: {e}")
        return comments

    try:
        video_request = client.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()
        items = video_response.get("items", [])
        video_title = items[0]["snippet"]["title"] if items else "unknown"
    except Exception as e:
        video_title = "unknown"

    for item in response.get("items", []):
        top_comment = item["snippet"]["topLevelComment"]
        comment_id = top_comment["id"]
        snippet = top_comment["snippet"]
        
        text = snippet.get("textDisplay", "")

        try:
            comment_published = datetime.strptime(snippet.get("publishedAt", ""), "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            comment_published = "unknown"

        like_count = snippet.get("likeCount", 0) 

        try:
            detected_language = detect(text)
        except LangDetectException:
            detected_language = "unknown"

        channel_id = snippet.get('authorChannelId', {}).get('value')

        # Cache para ahorrar peticiones
        if channel_id in channel_cache:
            channel_info = channel_cache[channel_id]
        else:
            channel_info = get_channel_info(channel_id)
            channel_cache[channel_id] = channel_info

        channel_name, channel_created, subscriber_count, view_count, country = channel_info

        if detected_language == language:
            comments.append((
                comment_id,
                text,
                detected_language,
                comment_published,
                like_count,
                video_id,
                video_title,
                channel_name,
                channel_created,
                subscriber_count, 
                view_count,
                country
            ))

    return comments

def create_table_if_not_exists(conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id VARCHAR(50) PRIMARY KEY,
            text TEXT,
            language TEXT,
            comment_published TEXT,
            like_count INTEGER,
            video_id VARCHAR(50),
            video_title TEXT,
            channel_name TEXT,
            channel_created TEXT,
            subscriber_count INTEGER,
            view_count INTEGER,
            country VARCHAR(50)
        )
    """)
    conn.commit()

def insert_many_comments(conn, cursor, comments):
    cursor.executemany("""
        INSERT OR IGNORE INTO comments (
            comment_id, text, language, comment_published,
            like_count, video_id, video_title, channel_name,
            channel_created, subscriber_count, view_count, country
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, comments)
    conn.commit()

def fetch_all_comments():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT comment_id, text, language, comment_published, like_count,
        video_id, video_title, channel_name, channel_created, subscriber_count, view_count, country
        FROM comments
        ORDER BY comment_published DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def save_to_db(comments):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_table_if_not_exists(conn=conn, cursor=cursor)
    
    cursor.execute("SELECT COUNT(*) FROM comments")
    count_before = cursor.fetchone()[0]

    insert_many_comments(conn=conn, cursor=cursor, comments=comments)

    cursor.execute("SELECT COUNT(*) FROM comments")
    count_after = cursor.fetchone()[0]

    inserted_count = count_after - count_before

    conn.close()

    return inserted_count

def download_comments(video_ids, max_results=100, language="en", interval_seconds=60):
    for video_id in video_ids:
        print(f"🔄 Comenzando descarga periódica de comentarios del video {video_id} cada {interval_seconds // 60} minutos...")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')

        print(f"\n📥 Obteniendo comentarios a las {timestamp}...")
        comments = get_comments(video_id=video_id, max_results=max_results, language=language)

        if comments:
            inserted_count = save_to_db(comments=comments)
            print(f"✅ Se insertaron {inserted_count} comentarios nuevos (de {len(comments)} intentos).")
        else:
            print("⚠️ No se encontraron comentarios.")
        
        print(f"⏳ Esperando {interval_seconds} segundos...\n")
        time.sleep(interval_seconds)