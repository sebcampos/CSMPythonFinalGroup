import time
import uuid
from json import dumps
import xml.etree.ElementTree as et
from typing import Self


class SongSerializer:
    def serialize(self, song):
        raise NotImplementedError('serialize method not implemented')


class JsonSerializer(SongSerializer):
    def serialize(self, song):
        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return dumps(payload)


class XmlSerializer(SongSerializer):
    def serialize(self, song):
        song_info = et.Element('song', attrib={'id': song.song_id})
        title = et.SubElement(song_info, 'title')
        title.text = song.title
        artist = et.SubElement(song_info, 'artist')
        artist.text = song.artist
        return et.tostring(song_info, encoding='unicode')


class SongSerializerFactory:
    serializer_options: tuple = ('json', 'xml')

    def __new__(cls, *args, **kwargs) -> SongSerializer:
        s = kwargs.get('serializer_type')
        if s is None:
            raise ValueError('required field "serializer_type" was not provided')
        if s.lower() not in cls.serializer_options:
            raise NotImplementedError(f'serializer "{s}" Has not been implemented')
        return cls.get_serializer(s)

    @staticmethod
    def get_serializer(serializer_type) -> SongSerializer:
        if serializer_type == 'json':
            return JsonSerializer()
        elif serializer_type == 'xml':
            return XmlSerializer()
        else:
            raise ValueError('Unsupported serializer type: %s' % serializer_type)


class Song:
    _string: str

    def __init__(self, title, artist, duration):
        self.song_id = str(uuid.uuid4())
        self.title = title
        self.artist = artist
        self.duration = duration
        minutes, seconds = duration.split(":")
        self.minutes, self.seconds = int(minutes), int(seconds)
        self.total_seconds = int(self.minutes) * 60 + int(self.seconds)

    def serialize(self, s_format: str) -> str:
        """
        :param s_format: desired format either json or xml
        """
        return SongSerializerFactory(serializer_type=s_format).serialize(self)

    def __eq__(self, other: Self):
        equal = True
        for key, item in self.__dict__.items():
            if other.__dict__.get(key) != item:
                equal = False
        return equal

    # def __str__(self) -> str:
    #     # building string table representation
    #     self._string = "{:>20} {:>20} {:>20}\n" \
    #         .format('Title', 'Artist', 'Duration')
    #     self._string += "{:>20} {:>20} {:>20}\n" \
    #         .format(self.title, self.artist, str(self.minutes)+":"+str(self.seconds))
    #     return self._string


    def __repr__(self) -> str:
        string = f'Song(song_id={self.song_id}, title="{self.title}", artist="{self.artist}")\n\n'
        return string
