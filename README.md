# SOGOL
*Sound of Game of Life* is the simple game of life you all know, but instead of showing the state of the board for every turn, it will be played for you!

### Why?
Because it is freaking awesome! And it will make you think about an alien who is trying to communicate with you.

### Installation
Simply, by using the install command of setup.py:

```sh
$ git clonehttps://github.com/moyiz/sogol.git
$ cd sogol
$ python2 setup.py install
```

### Usage
Using this is pretty simple, just run sogolife.py from your terminal.

By default, it will randomly generate 7 cells within a 3x3 matrix, and play each generation with a delay of 0.5 seconds. 
This behaviour can be changed, please run the script with the ```--help``` parameter for further information.
```
usage: sogolife.py [-h] [--max-x X] [--max-y Y] [--cells CELLS]
                   [--delay DELAY]

The Sound Of Life. Listen to a board Game Of Life as it is beinggenerated

optional arguments:
  -h, --help     show this help message and exit
  --max-x X      Maximum x value of randomly generated cells
  --max-y Y      Maximum y value of randomly generated cells
  --cells CELLS  Number of cells to randomly generate
  --delay DELAY  The delay between each generation
```

### Version
0.1

### License
BSD
