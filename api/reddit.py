from datetime import datetime
import time
from dotenv import load_dotenv
import praw
import os
from langdetect import detect, LangDetectException
import sqlite3
load_dotenv()

client = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

client.read_only = True

# DB_PATH = "data/reddit_posts.db"
DB_PATH = "reddit.db"

def get_posts(subreddit="offmychest", limit=100, language="en"):
    posts = []
    try:
        sub = client.subreddit(subreddit)
        for submission in sub.new(limit=limit):
            time.sleep(1)

            if submission.author and submission.selftext:
                # Detectar idioma del post
                try:
                    detected_language = detect(submission.title + " " + submission.selftext)
                except LangDetectException:
                    detected_language = "unknown"

                if detected_language == language:
                    posts.append((
                        submission.id,
                        submission.title,
                        submission.selftext,
                        detected_language,
                        datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        submission.author.name,
                        datetime.utcfromtimestamp(submission.author.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        submission.author.link_karma,
                        submission.author.comment_karma,
                        int(submission.author.is_mod)
                    ))  

    except Exception as e:
        print(f"❌ Error al acceder al subreddit '{subreddit}': {e}")
    
    return posts

def create_table_if_not_exists(conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id TEXT PRIMARY KEY,
            title TEXT,
            body TEXT,
            language TEXT,
            post_created TEXT,
            author TEXT,
            account_created TEXT,
            link_karma INTEGER,
            comment_karma INTEGER,
            is_mod INTEGER
        )
    """)
    conn.commit()

def insert_many_posts(conn, cursor, posts):
    cursor.executemany("""
        INSERT OR IGNORE INTO posts (
            post_id, title, body, language,
            post_created, author, account_created,
            link_karma, comment_karma, is_mod
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, posts)
    conn.commit()

def fetch_all_posts(limit=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT post_id, title, body, language, post_created, author, account_created, link_karma, comment_karma, is_mod
        FROM posts
        ORDER BY post_created DESC
    """
    if limit is not None:
        query += f" LIMIT {limit}"

    cursor.execute(query)

    rows = cursor.fetchall()

    conn.close()

    # return rows
    return [dict(row) for row in rows]

def save_to_db(posts):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_table_if_not_exists(conn=conn, cursor=cursor)

    cursor.execute("SELECT COUNT(*) FROM posts")
    count_before = cursor.fetchone()[0]

    insert_many_posts(conn=conn, cursor=cursor, posts=posts)

    cursor.execute("SELECT COUNT(*) FROM posts")
    count_after = cursor.fetchone()[0]
    
    inserted_count = count_after - count_before

    conn.close()
    
    return inserted_count

def download_posts(subreddit="all", limit=100, language="en", interval_seconds=1800):
    print(f"🔄 Comenzando descarga periódica de publicaciones de r/{subreddit} cada {interval_seconds // 60} minutos...")
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')

        print(f"\n📥 Obteniendo publicaciones a las {timestamp}...")
        posts = get_posts(subreddit=subreddit, limit=limit, language=language)

        if posts:
            inserted_count = save_to_db(posts=posts)
            print(f"✅ Se insertaron {inserted_count} posts nuevos (de {len(posts)} intentos).")
        else:
            print("⚠️ No se encontraron publicaciones válidas.")
        
        print(f"⏳ Esperando {interval_seconds} segundos...\n")
        time.sleep(interval_seconds)