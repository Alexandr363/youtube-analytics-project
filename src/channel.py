from googleapiclient.discovery import build
import json
import os

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """
    Класс для ютуб-канала
    """

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут
        подтягиваться по API
        """
        self.__channel_id = channel_id

        response = (self.get_service().channels().
                    list(id=self.__channel_id,
                    part='snippet,statistics').execute().get('items')[0])

        self.title = response.get('snippet').get('title')
        self.description = response.get('snippet').get('description')
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriberCount = (response.get('statistics').
                                get('subscriberCount'))
        self.video_count = response.get('statistics').get('videoCount')
        self.viewCount = response.get('statistics').get('viewCount')

    def __str__(self):
        return f"'{self.title} {self.url}'"

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3',
                        developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале
        """
        channel = (self.get_service().channels().
                   list(id=self.__channel_id,
                        part='snippet,statistics').execute())
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        channel_data = {
            'id': self.__channel_id,
            'name': self.title,
            'link': self.url,
            'description': self.description,
            'view_count': self.viewCount,
            'subscriber_count': self.subscriberCount
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_data, file, ensure_ascii=False, indent=4)
