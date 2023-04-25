import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.service = Channel.get_service()
        self.channel = self.service.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.channel_description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта класса Channel.
        """
        return f"'{self.title} ({self.url})'"

    def __add__(self, other) -> int:
        """
        Метод для операции сложения
        """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other) -> int:
        """
        Метод для операции вычитания
        """
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other) -> bool:
        """
        Метод для операции сравнения больше
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other) -> bool:
        """
        Метод для операции сравнения больше или равно
        """
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other) -> bool:
        """
        Метод для операции сравнения меньше
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other) -> bool:
        """
        Метод для операции сравнения меньше или равно
        """
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other) -> bool:
        """
        Метод для операции сравнения равенства
        """
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.__channel_id)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump({
                'title': self.title,
                'description': self.channel_description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count
            }, file)
