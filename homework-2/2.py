import json
import os

from googleapiclient.discovery import build


class Channel:
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def dict_to_print(self) -> None:
        channel_id = 'UCwHL6WHUarjGfUM_586me8w'
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        Channel.printj(channel)
