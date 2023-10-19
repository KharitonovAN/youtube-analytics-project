import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # self.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.channel_info = self.get_channel_info()
        self.title = self.channel_info["Название канала"]
        self.description = self.channel_info['Описание канала']
        self.subscriber_count = self.channel_info['Количество подписчиков']
        self.view_count = self.channel_info['Общее количество просмотров']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.url = self.channel_info['Ссылка на канал']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def get_channel_info(self):
        """Собирает информацию о канале"""
        response = self.get_service().channels().list(part='snippet,statistics', id=self.channel_id).execute()
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

    def __str__(self):
        """Возвращающий название и ссылку на канал по шаблону - <название_канала> (<ссылка_на_канал>)"""
        return f'{self.title}: ({self.url})'

    def __add__(self, other):
        """Метод складывания двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Метод вычитание двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        """Метод сравнение (равенства ==) двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __ne__(self, other):
        """Метод сравнение (неравенства) двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) != int(other.subscriber_count)

    def __lt__(self, other):
        """Метод сравнение (оператора меньше) двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Метод сравнение (оператора меньше или равно) двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        """Метод сравнение (оператора больше) двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Метод сравнение (оператора больше или равно) двух каналов между собой по количеству подписчиков"""
        return int(self.subscriber_count) >= int(other.subscriber_count)
