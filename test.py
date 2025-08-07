import utils.preprocessing as preprocessing
import api.reddit as reddit

if __name__ == "__main__":
    posts = reddit.fetch_all_posts(limit=2)
    preprocessed_text = []
    for post in posts:
        preprocessed_text.append(preprocessing.normalize_text(post["body"], language="en"))
    
    for post, text in zip(posts, preprocessed_text):
        print("Texto original:", post["body"])
        print("Texto normalizado:", text)
        print("---"*100)