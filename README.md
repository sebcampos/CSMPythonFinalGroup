# Group Project

- Factory Method
- State
- Iterator


### How to
- Clone the repo
- From repo directory run command `python JukeBox`

Example run

```
$ python JukeBox
Main interface:
Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> i
Coin inserted
Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> s
Enter song number to add to queue:
Playlist:
              Number                Title               Artist
                   0              G Minor                 Bach
                   1   Marriage of Figaro               Mozart
                   2      Mayonakano Door          Tanaka Yuri
                   3             Rasputin             Boney M.

>>> 3
Song Selected
Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> i
Coin inserted
Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> s
Enter song number to add to queue:
Playlist:
              Number                Title               Artist
                   0              G Minor                 Bach
                   1   Marriage of Figaro               Mozart
                   2      Mayonakano Door          Tanaka Yuri
                   3             Rasputin             Boney M.

>>> 0
Song Selected
Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> v
Rasputin 05:43
On Deck:
         G Minor 2:47
Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> v
Rasputin 05:36
On Deck:
         G Minor 2:47

Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> d
<playlist>
        <song id="007085be-5797-4204-b100-535f5d4ba8dc"><title>G Minor</title><artist>Bach</artist></song>
        <song id="3a2ea3af-4745-4b5a-85c1-a09c08d26a6f"><title>Marriage of Figaro</title><artist>Mozart</artist></song>
        <song id="8774e4cb-53d7-4187-9f80-90e2b2718edf"><title>Mayonakano Door</title><artist>Tanaka Yuri</artist></song>
        <song id="730a878c-7f37-4128-95b5-7afb30d424d6"><title>Rasputin</title><artist>Boney M.</artist></song>
</playlist>
{"playlist" :[
        {"id": "007085be-5797-4204-b100-535f5d4ba8dc", "title": "G Minor", "artist": "Bach"},
        {"id": "3a2ea3af-4745-4b5a-85c1-a09c08d26a6f", "title": "Marriage of Figaro", "artist": "Mozart"},
        {"id": "8774e4cb-53d7-4187-9f80-90e2b2718edf", "title": "Mayonakano Door", "artist": "Tanaka Yuri"},
        {"id": "730a878c-7f37-4128-95b5-7afb30d424d6", "title": "Rasputin", "artist": "Boney M."}
]}



Options: "i" to insert coin, "s" to select a song, "v" to view the queue, "q" to quit ["d" to serialize]
>>> q
Thank you an goodbye!

```