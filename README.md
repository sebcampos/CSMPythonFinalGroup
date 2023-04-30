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
>>> q
Thank you an goodbye!

```