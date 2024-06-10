
from urllib.request import urlopen
import vlc
import httpx
import threading
import os
import sys
import time

DEFAULT_BUFFER_FILE = '/home/lmar/radio/stream'

class InternetRadioStream:

    def __init__(self, url, buffer_file: str = DEFAULT_BUFFER_FILE):
        self.url = url
        self.buffer_file = buffer_file

    def set_stream_url(self, url):
        self.stream_url = url

    def _get_stream(self):
        with open(self.buffer_file, 'wb') as buff:
            with httpx.stream('GET', self.url) as r:
                for data in r.iter_raw():
                    buff.write(data)

    @property
    def _get_info(self):
        """
        Redefine in child class for specific web scraping
        """
        return False

    def _display_info(self):
        if self._get_info:
            self._get_info()
            info_string = '   + + +   '.join([self._info[key] for key in self._info]) + '   + + +   '
        else:
            info_string = self.url + '   + + +   '

        while True:
            columns = os.get_terminal_size().columns
            sys.stdout.write('\r'+info_string[:columns])
            info_string = info_string[1:] + info_string[0]
            time.sleep(0.3)
            sys.stdout.flush()


    def _stream_vlc(self):
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new(self.buffer_file)
        self.vlc_player.play()

    def _init_buffer(self):
        if not os.path.exists(self.buffer_file):
            os.mknod(path)

    def start(self):

        self._init_buffer()

        stream_thread = threading.Thread(target=self._get_stream,)
        vlc_thread = threading.Thread(target=self._stream_vlc,)
        info_thread = threading.Thread(target=self._display_info,)

        stream_thread.start()
        time.sleep(2)
        vlc_thread.start()
        info_thread.start()
