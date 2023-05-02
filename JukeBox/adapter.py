
from song import Song, SongSerializerFactory


class SongSerializerAdapter:
    def __init__(self, serializer):
        self.serializer = serializer

    def to_payload(self, song):
        return self.serializer.serialize(song)


class HtmlAdapter:
    def __init__(self, song_list):
        self.song_list = song_list
        

    def to_html(self):
        song_html = ""
        for song in self.song_list:
            json_serializer_adapter = SongSerializerAdapter(SongSerializerFactory.get_serializer('json'))
            json_payload = json_serializer_adapter.to_payload(song)

            xml_serializer_adapter = SongSerializerAdapter(SongSerializerFactory.get_serializer('xml'))
            xml_payload = xml_serializer_adapter.to_payload(song)

            song_html += f'<div class="song">' \
                         f'<h2>{song.title}</h2>' \
                         f'<h3>{song.artist}</h3>' \
                         f'<p class="json">{json_payload}</p>' \
                         f'<p class="xml"><!--\n{xml_payload}\n--></p>' \
                         f'</div>'
        html = f'<html>' \
               f'<head><title>Songs</title></head>' \
               f'<body>{song_html}</body>' \
               f'</html>'

        return html


if __name__ == '__main__':

    adapter = HtmlAdapter(songs)
    html = adapter.to_html()

    with open('songs-adapter.html', 'w') as f:
        f.write(html)
