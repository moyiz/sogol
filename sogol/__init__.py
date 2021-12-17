"""
Sound of Game of Life.
Listen to an audio interpretation of each generation.

Usage:
    sogol [--max-column=X] [--max-row=Y] [--cells=N] [-d DELAY] [-w WAVE]
    sogol (--from-lexicon=PATH|--from-json=PATH) [-d DELAY] [-w WAVE]

Options:
    -x NUM, --max-column=NUM  Maximum column of randomly generated cells [default: 3]
    -y NUM, --max-row=NUM     Maximum row of randomly generated cells [default: 3]
    -c CELLS, --cells=CELLS   Maximum number of cells to randomly generate [default: 7]
    --from-json=PATH          Load a JSON file or stdin (-)
    --from-lexicon=PATH       Load a lexicon formatted file or stdin (-)
    -d DELAY, --delay=DELAY   Delay in seconds between each generation [default: 0.5]
    -w (sine|square|sawtooth) Select a wave to generate [default: sine]
"""
import sys
import time

from docopt import docopt

from sogol.game import BoardBuilder, SoundOfLife
from sogol.sound import SawtoothWave, SineWave, SquareWave

wave_map = {"sine": SineWave, "square": SquareWave, "sawtooth": SawtoothWave}


def _read_file_or_stdin(path):
    if path == "-":
        return sys.stdin.read()
    with open(path) as f:
        return f.read()


def main():
    args = docopt(__doc__)
    if args["--from-json"]:
        board = BoardBuilder.from_json(_read_file_or_stdin(args["--from-json"]))
    elif args["--from-lexicon"]:
        board = BoardBuilder.from_lexicon(_read_file_or_stdin(args["--from-lexicon"]))
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
