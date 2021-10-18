"""
Sound of Game of Life.
Listen to an audio interpretation of each generation.

Usage:
    sogol [--max-column=X] [--max-row=Y] [--cells=N] [-d DELAY] [-w WAVE]
    sogol (--from-json=PATH|--from-string=BOARD) [-d DELAY] [-w WAVE]

Options:
    -x NUM, --max-column=NUM   Maximum column of randomly generated cells [default: 3]
    -y NUM, --max-row=NUM      Maximum row of randomly generated cells [default: 3]
    -c CELLS, --cells=CELLS    Maximum number of cells to randomly generate [default: 7]
    -j FILE, --from-json=FILE  Load board from JSON file
    -d DELAY, --delay=DELAY    Delay in seconds between each generation [default: 0.5]
    -w (sine|square|sawtooth)  Select a wave to generate [default: sine]
"""
import json
import sys
import time

from docopt import docopt

from sogol.game import BoardBuilder, SoundOfLife
from sogol.sound import SawtoothWave, SineWave, SquareWave

wave_map = {"sine": SineWave, "square": SquareWave, "sawtooth": SawtoothWave}


def main():
    args = docopt(__doc__)
    if args["--from-json"]:
        with open(args["--from-json"]) as fp:
            board = tuple(tuple(cell) for cell in json.load(fp))
    elif args["--from-string"]:
        board = tuple(tuple(cell) for cell in json.loads(args["--from-string"]))
    else:
        board = BoardBuilder.generate_random_board(
            max_column=int(args["--max-column"]),
            max_row=int(args["--max-row"]),
            max_cells=int(args["--cells"]),
        )

    delay = float(args["--delay"])
    try:
        while board:
            board = SoundOfLife.do_turn(board, wave=wave_map.get(args["-w"]))
            time.sleep(delay)
    except KeyboardInterrupt:
        sys.exit(1)
