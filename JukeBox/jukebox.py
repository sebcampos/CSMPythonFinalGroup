# jukebox.py
# Students Name: Jesse Burden, Sebastian Campos
# Course: CIS 502 Applied Python Programming
# Lab # 11 - Design Patterns
# Application: Music Service.
# Description: Jukebox.
# Testing Validation: .
# Development Environment: Anaconda + VS Code / Pycharm + Miniconda
# Version: Python 3.9.15 / 3.11.3
# Solution File: jukebox.py
# Date: 05/01/23


import time
import uuid
from os import system, name
from queue import Queue
from json import dumps
import xml.etree.ElementTree as et
from threading import Thread


# Factory Method Pattern
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

    def __eq__(self, other: object):
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
    
# Iterator Pattern
class Node:
    _next: object or None = None
    _song: Song

    def __init__(self, song: object):
        self._song = song

    def __eq__(self, other: object or Song):
        if other.__dict__.get('song'):
            return self.song == other.song
        return self.song == other

    def __repr__(self):
        return self._song.__repr__()

    def __str__(self):
        return self._song.__str__()

    @property
    def song(self):
        return self._song

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node: object):
        self._next = node


class DummyNode:
    _next: Node or None

    def __init__(self):
        self._next = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node: Node):
        self._next = node


# Iterator and Chain of Responsibility patterns
class LinkedList:
    _root: DummyNode
    _current_node: Node or DummyNode

    def __init__(self):
        self._root = DummyNode()
        self._current_node = self._root

    def __iter__(self):
        self._current_node = self._root
        return self

    def __next__(self):
        if self._current_node.next is None:
            raise StopIteration()
        self._current_node = self._current_node.next
        return self._current_node


# Factory Method pattern
class Library(LinkedList):
    _size = 0

    @property
    def size(self):
        return self._size

    def build_library(self):
        self.add(Song("G Minor", "Bach", "2:47"))
        self.add(Song("Marriage of Figaro", "Mozart", "4:00"))
        self.add(Song("Mayonakano Door", "Tanaka Yuri", "5:10"))
        self.add(Song("Rasputin", "Boney M.", "5:50"))
        self.add(Song("Coffee Cold", "Galt MacDermot", "4:01"))
        self.add(Song("Shark Smile", "Big Thief", "3:58"))
        self.add(Song("Here Goes Something", "Nada Surf", "2:06"))
        self.add(Song("Scarecrow", "Wand", "5:18"))

    def get(self, index) -> Node:
        if index < 0 or index > self._size:
            raise IndexError(f'{index} out of bounds')
        counter = 0
        for node in self:
            if counter == index:
                return node
            counter += 1

    def search(self, song_id=False, title=False, artist=False, song: Song = False) -> Node:
        result = None
        if song_id and not title and not artist:
            result = next((node for node in self if node.song.song_id == song_id), None)
        elif title and not song_id and not artist:
            result = next((node for node in self if node.song.title == title), None)
        elif artist and not song_id and not title:
            result = next((node for node in self if node.song.artist == artist), None)
        elif song_id and title and not artist:
            result = next((node for node in self if node.song.song_id == song_id and node.song.title == title), None)
        elif song_id and artist and not title:
            result = next((node for node in self if node.song.song_id == song_id and node.song.artist == artist), None)
        elif artist and title and not song_id:
            result = next((node for node in self if node.song.artist == artist and node.song.title == title), None)
        elif song_id and title and artist:
            for node in self:
                if node.song.song_id == song_id and node.song.title == title and node.song.artist == artist:
                    result = node
                    break
        elif song:
            for node in self:
                if node.song == song:
                    result = node
                    break
        return result

    def add(self, song: Song) -> None:
        new_node = Node(song)
        self._current_node.next = new_node
        self._current_node = new_node
        self._size += 1

    def remove(self, song_id):
        if self._root.next and self._root.next.song.song_id == song_id:
            self._root.next = self._root.next.next
            self._size -= 1
            return
        for node in self:
            next_node = node.next
            if next_node and next_node.song.song_id == song_id:
                node.next = next_node.next
                self._size -= 1

    def insert_after(self, song_id, song):
        curr_node = None
        for node in self:
            if node.song.song_id == song_id:
                curr_node = node
                break
        if curr_node:
            if curr_node.next is None:
                curr_node.next = Node(song)
            else:
                tmp_node = curr_node.next
                curr_node.next = Node(song)
                curr_node.next.next = tmp_node
            return True
        return False

    def __str__(self):
        string = "Playlist:\n"
        string += "{:>20} {:>20} {:>20}\n"\
            .format('Number', 'Title', 'Artist')
        for i, node in enumerate(self):
            song = node.song
            string += "{:>20} {:>20} {:>20}\n" \
                .format(str(i), song.title, song.artist)
        return string

    def serialize(self, format):
        if format == 'json':
            return '{"playlist" :[\n\t' + ',\n\t'.join(node.song.serialize(format) for node in self) + '\n]}'
        if format == 'xml':
            return '<playlist>\n\t' + '\n\t'.join(node.song.serialize(format) for node in self) + '\n</playlist>'



class SongSerializerAdapter:
    def __init__(self, serializer):
        self.serializer = serializer

    def to_payload(self, song):
        return self.serializer.serialize(song)


# Adapter pattern
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

# State pattern
class Jukebox:
    lib = Library()
    _state: str = 'standby' or 'coin_inserted' or 'playing' or 'quit'
    _current_song: Song = None
    thread: Thread
    q: Queue[int] = Queue()

    def __init__(self):
        self.state = 'standby'

        # adding songs to lib
        self.lib.build_library()
        self.adapter = HtmlAdapter(tuple(n.song for n in self.lib))
        self.thread = Thread(target=self._state_monitor)
        self.thread.start()

    @staticmethod
    def clear():

        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    def _state_monitor(self):
        while True:
            global stop_threads
            if stop_threads:
                return
            if self.q.empty():
                continue
            else:
                song = self.lib.get(self.q.get()).song
                total_seconds = song.total_seconds
                while total_seconds:
                    m, s = divmod(total_seconds, 60)
                    timer = song.title + ' ' + '{:02d}:{:02d}'.format(m, s)
                    self._current_song = timer
                    time.sleep(1)
                    total_seconds -= 1
                    if total_seconds <= 0:
                        self._current_song = None
                    if stop_threads:
                        return

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, other):
        self._state = other

    def insert_coin(self):
        if self.state == 'standby' or self.state == 'playing':
            print("Coin inserted", flush=True)
            self.state = "coin_inserted"
        elif self.state == "coin_inserted":
            print("Coin has already been inserted please select a song")

    def select_song(self):
        song_selected = None
        if self.state != "coin_inserted":
            print("Please insert a coin")
            return
        print('Enter song number to add to queue:')
        print(self.lib)
        while song_selected is None:
            s = input('>>> ').strip()
            if s.isnumeric() and int(s) in range(self.lib.size):
                print('Song Selected', flush=True)
                self.q.put(int(s))
                self.state = 'playing'
                song_selected = True
                self.clear()
            else:
                self.clear()
                print("ERROR please enter a valid song number")
                print(self.lib)

    def interface(self):
        options = ('i', 's', 'v', 'd', 'q')
        self.clear()
        print('Main interface:')
        options_str = 'Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to save html]'
        selection = 0
        while True:
            print(options_str)
            while selection not in options:
                selection = input('>>> ').lower()

            if selection == 'i':
                self.clear()
                jukebox.insert_coin()
                selection = None
            elif selection == 's':
                self.clear()
                jukebox.select_song()
                selection = None
            elif selection == 'v':
                self.clear()
                if self._current_song is None:
                    print('No song actively playing [state standby]\r')
                else:
                    print(self._current_song)
                if not self.q.empty():
                    print("On Deck:")
                    for i in list(self.q.queue):
                        s = self.lib.get(i).song
                        print('\t', s.title, s.duration)
                selection = None

            elif selection == 'd':
                print('html file written "songs-adapter.html"')
                selection = None
                html = self.adapter.to_html()
                with open('songs-adapter.html', 'w') as f:
                    f.write(html)


            elif selection == 'q':
                global stop_threads
                stop_threads = True
                self.thread.join()
                print("Thank you and goodbye!")
                return



if __name__ == '__main__':
    stop_threads = False
    jukebox = Jukebox()
    jukebox.interface()
