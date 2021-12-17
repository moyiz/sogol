import json
from functools import lru_cache
from itertools import product
from random import randint
from typing import Dict, Tuple

from .sound import Channel, SineWave, Wave, play

Cell = Tuple[int, int]
Board = Tuple[Cell]
ExpandedBoard = Dict[Cell, bool]
LexiconBoard = str


class BoardBuilder:
    @staticmethod
    def generate_random_board(max_column: int, max_row: int, max_cells: int) -> Board:
        return tuple(
            set((randint(0, max_column), randint(0, max_row)) for _ in range(max_cells))
        )

    @staticmethod
    def from_lexicon(lexicon_board: LexiconBoard) -> Board:
        return tuple(
            (x, y)
            for y, row in enumerate(lexicon_board.strip().split()[::-1])
            for x, cell in enumerate(row)
            if cell in "oO*"
        )

    @staticmethod
    def from_json(json_board: str) -> Board:
        return tuple(tuple(cell) for cell in json.loads(json_board))


class GameOfLife:
    @classmethod
    def do_turn(cls, living_cells: Board) -> Board:
        """
        Returns the next state of the board.
        """
        expanded_board = cls._get_expanded_board(living_cells)
        next_generation_set = {
            cell
            for cell, state in expanded_board.items()
            if cls._living_neighbours(living_cells, cell) == 3
            or expanded_board.get(cell)
            and cls._living_neighbours(living_cells, cell) == 2
        }
        return tuple(next_generation_set)

    @classmethod
    @lru_cache()
    def _living_neighbours(cls, living_cells: Board, cell: Cell) -> int:
        x, y = cell
        neighbours = (
            neigh
            for neigh in product(range(x - 1, x + 2), range(y - 1, y + 2))
            if cell != neigh
        )
        return len([neigh for neigh in neighbours if neigh in living_cells])

    @staticmethod
    def _get_expanded_board(living_cells: Board) -> ExpandedBoard:
        """
        Get a board that includes the neighbours of the given cells.
        """
        board = {cell: True for cell in living_cells}
        return {
            cell: board.get(cell, False)
            for (x, y) in board.keys()
            for cell in product(range(x - 1, x + 2), range(y - 1, y + 2))
        }


class SoundOfLife(GameOfLife):
    """
    A game of sound.
    Creates a game, generates & plays generation of each turn.
    """

    @classmethod
    def do_turn(cls, living_cells: Board, wave: Wave = SineWave) -> Board:
        """
        Plays the given board and returns the next generation.
        """
        cls.generate_sound(living_cells, wave)
        return super().do_turn(living_cells)

    @classmethod
    def generate_sound(cls, board: Board, wave: Wave):
        sounds = [
            wave(
                freq=440 + (12 ** 0.5) ** x,
                rate=44100,
                amp=cls._normalize(y),
            ).duration(0.2)
            for (x, y) in board
        ]
        lower_mid = len(sounds) // 2
        c1 = Channel(sounds[:lower_mid])
        c2 = Channel(sounds[lower_mid:])
        play(channels=[c1.generator, c2.generator], sample_width=2)

    @staticmethod
    def _normalize(x, low=-1, high=1) -> float:
        return 0 if x == 0 else (high - low) / x
