from src.channel import Channel

if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    """добавил вызов сюда, если вызвать в конце файла - json не создаётся
    причины этого не понял + кодировку utf-8 указал, но кириллица почему-то 
    не отображается корректно
    """
    moscowpython.to_json('moscowpython.json')

    # получаем значения атрибутов
    print(moscowpython.title)  # MoscowPython
    print(moscowpython.video_count)  # 685 (может уже больше)
    print(moscowpython.url)
    # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

    # менять не можем
    moscowpython.channel_id = 'Новое название'
    # AttributeError: property 'channel_id' of 'Channel' object has no setter

    # можем получить объект для работы с API вне класса
    print(Channel.get_service())
    # <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>

    # создаем файл 'moscowpython.json' в данными по каналу
    # moscowpython.to_json('moscowpython.json')

    moscowpython.to_json('moscowpython.json')
