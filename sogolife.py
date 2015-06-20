import sys
import argparse

from sogol import SoundOfLife


def argument_parsing():
    parser = argparse.ArgumentParser(description="The Sound Of Life. Listen " +
                                     "to a board Game Of Life as it is being" +
                                     "generated")
    parser.add_argument("--max-x", type=int, default=3, dest='x',
                        help="Maximum x value of randomly generated cells")
    parser.add_argument("--max-y", type=int, default=3, dest='y',
                        help="Maximum y value of randomly generated cells")
    parser.add_argument("--cells", type=int, default=7,
                        help="Number of cells to randomly generate")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="The delay between each generation")
    return parser.parse_args()


def main():
    args = argument_parsing()
    sol = SoundOfLife(args.cells, args.x, args.y)
    sol.start(args.delay)


if __name__ == "__main__":
    main()
