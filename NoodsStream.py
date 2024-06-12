from urllib.request import urlopen

from InternetRadioStream import InternetRadioStream
from configs import DEFAULT_BUFFER_FILE

class NoodsStream(InternetRadioStream):

    def __init__(self, buffer_file: str = DEFAULT_BUFFER_FILE):
        self.stream_url = 'https://noodsradio.out.airtime.pro/noodsradio_a'
        super().__init__(self.stream_url, buffer_file)
        self.info_url = f"https://www.noodsradio.com/"

    def no_get_info(self):
        html = urlopen(self.info_url).read().decode('utf-8')
        tags = {
            'title': ('<h1 class="text-bold">', '</h1>'),
            'time': ('<h2 class="live-landing__broadcast-time">', '<'),
        }
        self._info = {
            'station': 'NTS'
        }
        bio_index = html.find('<li class="artist-slot relative block flex flex-col xl:flex-row py-2 pl-4 justify-around xl:justify-center items-start xl:items-center w-full cursor-pointer live"><a href="https://noodsradio.com/residents/crosspolar" class="absolute left-0 right-0 top-0 bottom-0"></a> <div class="xl:w-1/2 flex flex-row"><div class="on-air-tag flex items-center"><svg width="7" height="7" fill="none" xmlns="http://www.w3.org/2000/svg" class="inline flash mr-1"><path fill-rule="evenodd" clip-rule="evenodd" d="M3 6a3 3 0 100-6 3 3 0 000 6z" fill="#EE4343"></path></svg> <span>On Air</span></div> <div class="w-2/4"><p class="slot-time flex pb-0 text-sm text-black font-bold xl:text-xl"> 23:00 <svg class="time-slot-arrow" fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 14"><path d="M.984 8h15.75a.992.992 0 00.985-1c0-.552-.441-1-.985-1H.984A.992.992 0 000 7c0 .552.44 1 .984 1z"></path><path d="M10.132 12.293a1.011 1.011 0 000 1.414.974.974 0 001.392 0l5.906-6a1.011 1.011 0 000-1.414l-5.906-6a.974.974 0 00-1.392 0 1.011 1.011 0 000 1.414L15.342 7l-5.21 5.293z"></path></svg>  00:00</p></div></div> <div class="w-2/3"><h4 class="artist-slot__name pb-0 text-left inline-block">Crosspolar</h4></div></li>')
        html_post_bio = html[bio_index:]
        for key in tags:
            open_tag, close_tag = tags[key]
            open_index = html.find(open_tag) + len(open_tag)
            close_index = open_index + html[open_index:].find(close_tag)
            text = html[open_index:close_index].replace('amp;', '')
            if '<' not in text and  '>' not in text:
                self._info[key] = text


if __name__ == "__main__":
    stream = NoodsStream()
    stream.start()
