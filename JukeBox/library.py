from song import Song
from typing import Self


class Node:
    _next: Self or None = None
    _song: Song

    def __init__(self, song: Self):
        self._song = song

    def __eq__(self, other: Self or Song):
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


if __name__ == "__main__":
    # create a playlist
    p = Library()
    # create songs for testing
    s1 = Song("G Minor", "Bach", "2:47")
    s2 = Song("Marriage of Figaro", "Mozart", "4:00")
    s3 = Song("Mayonakano Door", "Tanaka Yuri", "5:10")
    s4 = Song("Rasputin", "Boney M.", "5:50")
    # add 2 songs to the playlist
    print(s1)
    p.add(s1)
    p.add(s2)
    # serialization demo
    print('Serialization methods:\n')
    # serialize in json format
    print('Json:\n')
    print(p.serialize('json'), '\n')
    # serialize in xml format
    print('XML:\n')
    print(p.serialize('xml'), '\n')
    print('Playlist methods:\n')
    # search for song that does not exist returns None
    assert p.search(song=s3) is None
    # search yields node when it exists
    p.add(s3)
    assert p.search(song=s3) == s3
    # search via uuid
    assert p.search(song_id=s1.song_id) == s1
    # search via index
    assert p.get(0) == s1
    print(p)
    # remove a song
    print(f'Removing song: {s1.title}...')
    p.remove(s1.song_id)
    assert s1 not in p
    print(p)
    # insert a song
    print(f'Inserting song {s4.title} after {s2.title}')
    p.insert_after(s2.song_id, s4)
    assert p.get(1) == s4
    print(p)
