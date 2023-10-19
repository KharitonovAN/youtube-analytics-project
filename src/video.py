import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class APIKEY:
    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)


class Video(APIKEY):
    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.name_video = ""
        self.url_video = ""
        self.video_view = None
        self.video_like = None
        self._init_from_api()

    def _init_from_api(self):
        youtube = self.get_service()

        try:
            video = youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()

            if 'items' in video and video['items']:
                snippet = video['items'][0]['snippet']
                statistics = video['items'][0]['statistics']

                self.title = snippet['title']
                self.url = f'https://youtu.be/{self.video_id}'
                self.view_count = statistics['viewCount']
                self.like_count = statistics['likeCount']
            else:
                self.title = None
                self.url = None
                self.view_count = None
                self.like_count = None

        except HttpError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.name_video


class PLVideo(Video):
    def __init__(self, video_id: str, plist_id: str) -> None:
        """Инициализирует 'id видео' и 'id плейлиста"""
        super().__init__(video_id)
        self.plist_id = plist_id
