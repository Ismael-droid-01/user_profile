# import api.reddit as reddit
import api.youtube as youtube

def youtube_robot():
    video_ids = [
        'xy8aJw1vYHo',
        'aZXBFirj6b4',
        'ApXoWvfEYVU',
        'F5tSoaJ93ac',
        'kTJczUoc26U',
        '2fDzCWNS3ig',
    ]
    youtube.download_comments(video_ids=video_ids)

if __name__ == "__main__":
    # reddit.download_posts(limit=100, interval_seconds=900)
    youtube_robot()