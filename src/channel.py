from googleapiclient.discovery import build
import os
import json


class Channel:

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}]'
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = int(channel["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f'{self.title} ({self.url})'

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        return: объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        data = {
            'Channel ID': self.__channel_id,
            'Name channel': self.title,
            'description': self.description,
            'URL': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def __add__(self, other):
        return self.view_count + other.view_count

    def __sub__(self, other):
        return self.view_count - other.view_count

    def __gt__(self, other):
        return self.view_count > other.view_count

    def __ge__(self, other):
        return self.view_count >= other.view_count

    def __lt__(self, other):
        return self.view_count < other.view_count

    def __le__(self, other):
        return self.view_count <= other.view_count
