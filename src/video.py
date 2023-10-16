import os
from googleapiclient.discovery import build


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

        self.request = self.get_service().videos().list(part="snippet,statistics", id=self.video_id)
        response = self.request.execute()

        if response['items']:
            video_data = response['items'][0]
            self.name_video = video_data['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.video_view = int(video_data['statistics']['viewCount'])
            self.video_like = int(video_data['statistics']['likeCount'])

    def __str__(self):
        return self.name_video


class PLVideo(Video):
    def __init__(self, video_id: str, plist_id: str) -> None:
        """Инициализирует 'id видео' и 'id плейлиста"""
        super().__init__(video_id)
        self.plist_id = plist_id
