# jesseBLab11_state_v3.py
# Student Name: Jesse Burden
# Course: CIS 502 Applied Python Programming
# Lab # 11 - Design Patterns
# Application: Music Service.
# Description: Jukebox using just one Class with if/elif/else conditionals.
# Testing Validation: .
# Development Environment: Anaconda + VS Code / Pycharm + Miniconda
# Version: Python 3.9.15 / 3.11.3
# Solution File: jesseBLab11_state_v3.py
# Date: 04/27/23

import time
from os import system, name
from queue import Queue
from library import Library, Song
from threading import Thread


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
        options_str = 'Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]'
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
                print(self.lib.serialize('xml'))
                print(self.lib.serialize('json'))
                selection = None



            elif selection == 'q':
                global stop_threads
                stop_threads = True
                self.thread.join()
                print("Thank you an goodbye!")
                return


if __name__ == '__main__':
    stop_threads = False
    jukebox = Jukebox()
    jukebox.interface()
