import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv(
        'YOUTUBE_API_KEY')  # YOUTUBE_API_KEY скопирован из гугла и вставлен в переменные окружения

    youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2,
                         ensure_ascii=False))  # Выводит словарь в json-подобном удобном формате с отступами

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name):
        """Сохраняет в Json файл значения атрибутов экземпляра - информацию о канале"""
        data = {'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count
                }
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)
