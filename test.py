import utils.preprocessing as preprocessing
import api.youtube as youtube

videos = [
    "eJwXivMnxcY",
    "9Y4rRFjtqpU",
    "pJU2y5R1VQk",
    "Sd-dYAsXABM",
    "RG8YSMUZ2Nk",
]

if __name__ == "__main__":
    youtube.download_comments([videos[0]], language="es")