import os

import isodate
from googleapiclient.discovery import build
import datetime


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.service = PlayList.get_service()
        self.playlist_videos = self.service.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()
        self.video_ids = [video['contentDetails']['videoId']
                          for video in self.playlist_videos['items']]
        self.video_response = self.service.videos().list(
            part='contentDetails,statistics',
            id=','.join(self.video_ids)
        ).execute()
        self.playlist_info = self.service.playlists().list(id=self.playlist_id,
                                                           part='contentDetails,snippet',
                                                           maxResults=50,
                                                           ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def total_duration(self):
        total = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        max_count = 0
        id_max_like_video = None
        for x in range(self.video_response['pageInfo']['totalResults']):
            like_count = int(self.video_response['items'][x]['statistics']['likeCount'])
            if like_count > max_count:
                max_count = like_count
                id_max_like_video = self.video_response['items'][x]['id']
        return f'https://youtu.be/{id_max_like_video}'
