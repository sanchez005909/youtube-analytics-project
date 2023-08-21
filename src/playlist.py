import datetime
import json
from src.channel import Channel
from src.video import Video
import isodate
from datetime import timedelta

class PlayList:

    youtube = Channel.get_service()

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_info_playlist()['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    def __repr__(self):
        return f'{self.title}, {self.url}'

    def get_info_playlist(self):
        playlists = self.youtube.playlists().list(part="snippet", id=self.playlist_id).execute()
        return playlists

    def get_ids_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        return video_ids

    @property
    def total_duration(self):
        durations = []
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.get_ids_video())
                                               ).execute()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations.append(duration)
        return sum(durations, datetime.timedelta())

    def show_best_video(self):
        likes = 0
        id = None
        video_ids = self.get_ids_video()
        for video_id in video_ids:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > likes:
                likes = int(like_count)
                id = video_id
        return f"https://youtu.be/{id}"
