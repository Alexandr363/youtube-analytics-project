import os
import isodate
import datetime
from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """
    Класс для плейлиста
    """
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        response = youtube.playlists().list(id=playlist_id,
                                            part='contentDetails,snippet',
                                            maxResults=50,
                                            ).execute().get('items')[0]

        self.title = response.get('snippet').get('title')
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def _get_videos(self):
        """
        Получаем из плейлиста информацию о всех видео
        """
        playlist_videos = youtube.playlistItems().list(playlistId=self.
                                                       playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,'
                                                    'statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        return video_response

    @property
    def total_duration(self):
        """
        Получаем общую длительность видео
        """
        video_response = self._get_videos()
        total_duration = datetime.timedelta()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Получаем видео из плейлиста с максимальным количеством лайков
        """
        video_response = self._get_videos()
        best_video = max(video_response['items'], key=lambda video:
                         video['statistics']['likeCount'])
        best_video_id = best_video['id']
        best_video_link = f"https://youtu.be/{best_video_id}"
        return best_video_link
