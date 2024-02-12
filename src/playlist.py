import isodate
import datetime
from src.video import Video
import os
from googleapiclient.discovery import build


class PlayList():
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, pl_id):
        """
        иниуиализируем id плейлиста
        """
        self.pl_id = pl_id
        self.response = self.get_service().playlistItems().list(playlistId=self.pl_id, part='contentDetails, snippet',
                                                                maxResults=50).execute()
        pl_response = self.get_service().playlists().list(id=self.pl_id, part='contentDetails,snippet',
                                                          maxResults=50).execute()
        self.title = pl_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.response['items'][0]['snippet']['playlistId']
        self.ids_video = [video['contentDetails']['videoId'] for video in
                          self.response['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.ids_video)
                                                               ).execute()

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        return youtube

    @property
    def total_duration(self):
        """
        Считаем общую продолжительность видео в плейлисте
        Получаем из плейлиста id video, далее длительность каждого видео, и в итоге складываем.
        @return:
        """
        # playlist_videos_part_contentdetails = self.get_service().playlistItems().list(playlistId=self.pl_id,
        #                                                                               part='contentDetails',
        #                                                                               maxResults=50).execute()
        # video_ids: list[str] = [video['contentDetails']['videoId'] for video in
        #                         self.response['items']]
        # video_response = self.get_service().videos().list(part='contentDetails,statistics',
        #                                                   id=','.join(self.ids_video)
        #                                                   ).execute()
        total_duration = 0
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format

            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration.total_seconds()

        return datetime.timedelta(seconds=total_duration)

    def show_best_video(self):
        # playlist_videos_part_contentdetails = self.get_service().playlistItems().list(playlistId=self.pl_id,
        #                                                                               part='contentDetails',
        #                                                                               maxResults=50).execute()
        # video_ids: list[str] = [video['contentDetails']['videoId'] for video in
        #                         self.response['items']]
        # video_response = self.get_service().videos().list(part='contentDetails,statistics',
        #                                                   id=','.join(self.ids_video)
        #                                                   ).execute()

        max_like = 0
        video_w_max_like = 0
        for video in self.video_response['items']:
            count_like = video['statistics']['likeCount']
            count_video = video['id']
            if int(count_like) > int(max_like):
                video_w_max_like = count_video
        return "https://youtu.be/" + video_w_max_like
