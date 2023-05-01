import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.service = Video.get_service()
        self.video = self.service.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=self.video_id).execute()
        self.title = self.video['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.views = int(self.video['items'][0]['statistics']['viewCount'])
        self.likes = int(self.video['items'][0]['statistics']['commentCount'])

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def __str__(self) -> str:
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self) -> str:
        return f'{super().__str__()}'
