import json
import os
from googleapiclient.discovery import build
import isodate
import datetime


api_key: str = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

playlist_id = 'PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw'
playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails, snippet',
                                               maxResults=50,
                                               ).execute()

#playlist_videos_part_contentdetails = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                                      # part='contentDetails',
                                                                                      # maxResults=50).execute()
print(playlist_videos)
# print(f"www.youtube.com/playlist?list={playlist_videos['items'][0]['snippet']['playlistId']}")

# title = playlist_videos['items'][0]['snippet']['title']
# print(playlist_videos['items'][0]['snippet']['title'].split('.')[0])

pl = youtube.playlists().list(id=playlist_id,
                              part='contentDetails,snippet',
                              maxResults=50,
                              ).execute()
# print(pl['items'][0]['snippet']['title'])
# channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'
# playlists = youtube.playlists().list(channelId=channel_id,
#                                      part='contentDetails,snippet',
#                                      maxResults=50,
#                                      ).execute()
# # printj(playlists)
# for playlist in playlists['items']:
#     print(playlist)

video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

#video_ids = ['feg3DYywNys', 'MtWXwMCAApY', 'nApYYXYL9qA', 'cUGyMzWQcGM']
video_response = youtube.videos().list(part='contentDetails,statistics',
                                       id=','.join(video_ids)
                                       ).execute()
#print(video_response)

total_duration = 0
for video in video_response['items']:
        # YouTube video duration is in ISO 8601 format

    iso_8601_duration = video['contentDetails']['duration']
    duration = isodate.parse_duration(iso_8601_duration)
    total_duration += duration.total_seconds()
#print(str(datetime.timedelta(seconds=total_duration)))







'''
получить статистику видео по его id
получить id можно из адреса видео
https://www.youtube.com/watch?v=gaoc9MPZ4bw или https://youtu.be/gaoc9MPZ4bw
'''
# video_id = 'feg3DYywNys'
# video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
#                                        id=video_id
#                                        ).execute()


video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

#video_ids = ['feg3DYywNys', 'MtWXwMCAApY', 'nApYYXYL9qA', 'cUGyMzWQcGM']
video_response = youtube.videos().list(part='contentDetails,statistics',
                                       id=','.join(video_ids)
                                       ).execute()

max_like = 0
max_video = 0
for video in video_response['items']:
    count_like = video['statistics']['likeCount']
    count_video = video['id']
    if int(count_like) > int(max_like):
        max_video = count_video
#print(f"https://youtu.be/{max_video}")




# print(video_response)
# video_title: str = video_response['items'][0]['snippet']['title']
# view_count: int = video_response['items'][0]['statistics']['viewCount']
# like_count: int = video_response['items'][0]['statistics']['likeCount']
# comment_count: int = video_response['items'][0]['statistics']['commentCount']


#print(f'{video_title},\n{view_count}, \n{like_count},\n{comment_count}')
