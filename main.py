import api.reddit as reddit

if __name__ == "__main__":
    # reddit.download_posts(limit=2)
    print(reddit.fetch_all_posts())