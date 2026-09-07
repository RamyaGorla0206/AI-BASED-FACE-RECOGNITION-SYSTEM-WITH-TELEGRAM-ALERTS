import requests
from config import API_TOKEN, CHAT_ID


def send_telegram_photo(photo_path):

    url = f"https://api.telegram.org/bot{API_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": "🚨 UNKNOWN PERSON DETECTED"
            },
            files={
                "photo": photo
            }
        )


def send_telegram_video(video_path):

    url = f"https://api.telegram.org/bot{API_TOKEN}/sendVideo"

    with open(video_path, "rb") as video:

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": "🎥 Intruder Video"
            },
            files={
                "video": video
            }
        )