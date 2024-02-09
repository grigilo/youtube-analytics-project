import json
import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id
        response = self.get_service().videos().list(part="snippet,contentDetails,statistics", id=video_id).execute()
        self.title = response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/channel/{response['items'][0]['snippet']['channelId']}'
        self.view_count = response['items'][0]['statistics']['viewCount']
        self.like_count = response['items'][0]['statistics']['likeCount']

    def get_response(self):
        response = self.get_service().videos().list(part="snippet,contentDetails,statistics", id=video_id).execute()
        return response

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """

        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2,
                         ensure_ascii=False))  # Выводит словарь в json-подобном удобном формате с отступами

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        return youtube


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        # self.video_id = video_id
        # response = self.get_service().videos().list(part="snippet,contentDetails,statistics", id=video_id).execute()
        super().__init__(video_id)
        self.playlist_id = playlist_id
        # self.title = response['items'][0]['snippet']['title']
        # self.url = f'https://www.youtube.com/channel/{response['items'][0]['snippet']['channelId']}'
        # self.view_count = response['items'][0]['statistics']['viewCount']
        # self.like_count = response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title
