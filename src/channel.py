import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.channel_info = self.get_channel_info()

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def get_channel_info(self):
        """Собирает информацию о канале"""
        youtube = self.get_service()
        response = youtube.channels().list(part='snippet,statistics', id=self.channel_id).execute()
        if 'items' in response:
            channel_data = response['items'][0]
            snippet = channel_data['snippet']
            statistics = channel_data['statistics']
            channel_info = {
                "id канала": self.channel_id,
                "Название канала": snippet['title'],
                "Описание канала": snippet['description'],
                "Ссылка на канал": f"https://www.youtube.com/channel/{self.channel_id}",
                "Количество подписчиков": statistics['subscriberCount'],
                "Количество видео": statistics['videoCount'],
                "Общее количество просмотров": statistics['viewCount']}
            return channel_info

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале"""
        if self.channel_info:
            print("Информация о канале:")
            print(f"id канала: {self.channel_info['id канала']}")
            print(f"Название канала: {self.channel_info['Название канала']}")
            print(f"Описание канала: {self.channel_info['Описание канала']}")
            print(f"Ссылка на канал: {self.channel_info['Ссылка на канал']}")
            print(f"Количество подписчиков: {self.channel_info['Количество подписчиков']}")
            print(f"Количество видео: {self.channel_info['Количество видео']}")
            print(f"Общее количество просмотров: {self.channel_info['Общее количество просмотров']}")

    def to_json(self, filename: str):
        """Сохраняющий в файл JSON значения атрибутов экземпляра"""
        if self.channel_info:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.channel_info, file, ensure_ascii=False, indent=2)
