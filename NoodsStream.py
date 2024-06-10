from urllib.request import urlopen
import vlc
import httpx
import threading
import os
import time

from InternetRadioStream import InternetRadioStream

DEFAULT_BUFFER_FILE = '/home/lmar/radio/stream'

class NoodsStream(InternetRadioStream):

    def __init__(self, buffer_file: str = DEFAULT_BUFFER_FILE):
        self.stream_url = 'https://noodsradio.out.airtime.pro/noodsradio_a'
        super().__init__(self.stream_url, DEFAULT_BUFFER_FILE)


if __name__ == "__main__":
    stream = NoodsStream()
    stream.start()
