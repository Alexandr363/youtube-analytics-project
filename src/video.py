import os
from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """
    Класс для получения информации по id видео на ютюбе
    """
    def __init__(self, id_video):
        """Экземпляр инициализируется id канала. Дальше все данные будут
        подтягиваться по API
        """

        try:
            response = youtube.videos().list(id=id_video,
                                             part='snippet, statistics'
                                             ).execute().get('items')[0]
            self.id_video = id_video
            self.title = response.get('snippet').get('title')
            self.title = response['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={self.id_video}'
            self.viewCount = response.get('statistics').get('viewCount')
            self.like_count = response.get('statistics').get('likeCount')
        except IndexError:
            self.id_video = id_video
            self.title = None
            self.url = None
            self.viewCount = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    """
    Класс для получения информации по id видео и id плейлиста на ютюбе
    """
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
