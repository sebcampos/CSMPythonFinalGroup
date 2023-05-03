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


### Creational ###
# Factory Method Pattern
class SongSerializer:
    """Serializer Base class to be implemented"""

    def serialize(self, song):
        raise NotImplementedError('serialize method not implemented')


class JsonSerializer(SongSerializer):
    """Json song serializer implements the serialize method to return json formatted song"""

    def serialize(self, song):
        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return dumps(payload)


class XmlSerializer(SongSerializer):
    """Xml song serializer implements the serialize method to return xml formatted song"""

    def serialize(self, song):
        song_info = et.Element('song', attrib={'id': song.song_id})
        title = et.SubElement(song_info, 'title')
        title.text = song.title
        artist = et.SubElement(song_info, 'artist')
        artist.text = song.artist
        return et.tostring(song_info, encoding='unicode')


class SongSerializerFactory:
    """
    This class is an example of the factory method. It builds new instances
    of the serializer classes and returns those instance to the program
    using the get_serializer method
    """
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
    """
    The song class is a representation of a Song to be used in the JukeBox
    and Library classes
    """

    def __init__(self, title, artist, duration):
        self.song_id = str(uuid.uuid4())
        self.title = title
        self.artist = artist
        self.duration = duration
        minutes, seconds = duration.split(":")
        self.minutes, self.seconds = int(minutes), int(seconds)
        self.total_seconds = int(self.minutes) * 60 + int(self.seconds)

    def __eq__(self, other: object):
        equal = True
        for key, item in self.__dict__.items():
            if other.__dict__.get(key) != item:
                equal = False
        return equal

    def __repr__(self) -> str:
        string = f'Song(song_id={self.song_id}, title="{self.title}", artist="{self.artist}")\n\n'
        return string


### Structural ###
# Iterator Pattern
class Node:
    """
    The node is part of our LinkedList / Iterator implementation
    and represents one item in the LinkedList
    """
    _next: object or None = None
    _song: Song

    def __init__(self, song: Song):
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
    """
    The Dummy Node is used in our program and the Head Node of
    the linked list
    """
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
    """
    The linked list class is a representation of our Iterator.
    It builds the basic LinkedList using the Node class by implementing
    the iter and next methods.
    """
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
    """
    The Library class inherits from the linked list and adds the abilities
    to add, remove, and search for nodes with a particular song value or index.
    It also builds a hard coded Library of Songs in the init method.
    """
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
        string += "{:>20} {:>20} {:>20}\n" \
            .format('Number', 'Title', 'Artist')
        for i, node in enumerate(self):
            song = node.song
            string += "{:>20} {:>20} {:>20}\n" \
                .format(str(i), song.title, song.artist)
        return string


class SongSerializerAdapter:

    def __init__(self, serializer):
        self.serializer = serializer

    def to_payload(self, song):
        return self.serializer.serialize(song)


# Adapter pattern
class HtmlAdapter:
    """
    The HtmlAdapter serializes the song from our Library and adapts
    them into an html page
    """

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
                         f'<p class="xml">\n{xml_payload.replace(">", "&gt").replace("<", "&lt")}\n</p>' \
                         f'</div>'
        html = f'<html>' \
               f'<head><title>Songs</title></head>' \
               f'<body>{song_html}</body>' \
               f'</html>'

        return html


### Behavioral ###
# State pattern
class Jukebox:
    """
    The JukeBox implements the Adapter, Factory, and Iterator into one program.
    This program also includes the State pattern by allowing users to play a song
    only when they have inserted a coin and by maintaining a queue of songs to play,
    removing them as they complete.
    """
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
        global clear_screen
        if clear_screen is False:
            return
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
                # for windows
                if name == 'nt':
                    _ = system('start songs-adapter.html')

                # for mac and linux(here, os.name is 'posix')
                else:
                    _ = system('open songs-adapter.html')


            elif selection == 'q':
                global stop_threads
                stop_threads = True
                self.thread.join()
                print("Thank you and goodbye!")
                return


if __name__ == '__main__':
    stop_threads = False
    clear_screen = False
    jukebox = Jukebox()
    jukebox.interface()
