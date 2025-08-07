# import api.reddit as reddit
import api.youtube as youtube

def youtube_robot():
    video_ids = [
        'sOnqjkJTMaA', # Thriller
        '4NRXx6U8ABQ', # Blindig Lights
        'kXYiU_JCYtU', # Numb
        'SBjQ9tuuTJQ', # The Pretender
        'ocGJWc2F1Yk', # Tonight Show
        '6gTmyhRM6k0', 
        'g-pZ7WXuBSs',
        '6i0a7RDPkM8',
        'G_sBOsh-vyI',
        'ewOPQZZn4SY',
        'pyNfB24Eo4A',
    ]
    youtube.download_comments(video_ids=video_ids)

if __name__ == "__main__":
    # reddit.download_posts(limit=100, interval_seconds=900)
    youtube_robot()