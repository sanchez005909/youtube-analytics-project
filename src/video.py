from googleapiclient.discovery import build
import os
from src.channel import Channel


class Video:

    youtube = Channel.get_service()

    def __init__(self, video_id):
        self.video_id = video_id
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id).execute()
        # print(video_response)
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return f'{self.video_title}'

    def __repr__(self):
        return (f'ID:{self.video_id}, Название: {self.video_title}, {self.view_count} просмотров, '
                f'{self.like_count} лайков, {self.comment_count} комментариев')

    @classmethod
    def get_service(cls):
        """
        return: объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):

    def __init__(self, video_id, plv_id):
        super().__init__(video_id)
        self.plv_id = plv_id
