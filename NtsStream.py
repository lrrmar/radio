from urllib.request import Request, urlopen
import sys

from InternetRadioStream import InternetRadioStream
from configs import DEFAULT_BUFFER_FILE

class NtsStream(InternetRadioStream):

    def __init__(self, channel: int = 1, buffer_file: str = DEFAULT_BUFFER_FILE):
        self.channel = str(channel)
        stream_url = 'https://stream-relay-geo.ntslive.net/stream'
        if self.channel == '2':
            stream_url += '2'
        super().__init__(stream_url, buffer_file)
        self.info_url = f"https://www.nts.live/{channel}"
        self._info = {}

    @property
    def info(self):
        if self._info == {}:
            self._get_info()
        return self._info


    def _get_info(self):
        headers = {'Cache-Control': 'no-cache, no-transform'}
        req = Request(self.info_url, headers=headers)
        resp = urlopen(req)
        html = urlopen(req).read().decode('utf-8')
        tags = {
            'title': ('<h1 class="text-bold">', '</h1>'),
            'location': ('<h2>', '</h2>'),
            'time': ('<h2 class="live-landing__broadcast-time">', '<'),
            'description': ('<h3>', '</h3>')
        }
        self._info = {
            'station': 'NTS'
        }
        bio_index = html.find('<div class="bio">')
        html_post_bio = html[bio_index:]
        for key in tags:
            open_tag, close_tag = tags[key]
            open_index = html.find(open_tag) + len(open_tag)
            close_index = open_index + html[open_index:].find(close_tag)
            text = html[open_index:close_index].replace('amp;', '')
            if '<' not in text and  '>' not in text:
                self._info[key] = text


if __name__ == "__main__":

    try:
        channel = sys.argv[1]
    except:
        channel = 1

    stream = NtsStream(channel)
    stream.start()
