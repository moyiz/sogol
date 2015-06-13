__author__ = 'moyiz'

import random


class Game(object):
    def __init__(self):
        self.board = Board()

    def fill_random(self, max_x, max_y, cells):
        """
        Fills random cells between the range specified.

        :param max_x: Maximum x range
        :type max_x: int
        :param max_y: Maximum y range
        :type max_y: int
        :param cells: The number of cells to generate
        :type cells: int
        :return: None
        """
        for _ in xrange(cells):
            self.board.set_cell(random.randint(0, max_x),
                                random.randint(0, max_y))

    def do_turn(self):
        """
        Does one turn in the game, and returns the current
        board state
        :return: The current board
        :type: Board
        """
        new_board = Board()
        for x, y in self.board.get_cells():
            if self.board.get_cell(x, y) and \
               self.board.count_living_neigh(x, y) in [2, 3]:
                new_board.set_cell(x, y)
            elif not self.board.get_cell(x, y) and \
                 self.board.count_living_neigh(x, y) == 3:
                new_board.set_cell(x, y)
        self.board = new_board
        return new_board


class Board(object):
    def __init__(self):
        self._board = {}

    def get_cells(self):
        """
        Returns a list of relevant cells (living and their neighbours).

        :return: List(int, int)
        """
        cells = self._board.keys()
        for x, y in self._board.keys():
            cells += Board.get_neighs(x, y)
        return cells

    def get_living_cells(self):
        """
        Returns a list of coords of the living cells in the board
        :return: List(int, int)
        """
        return self._board.keys()

    def set_cell(self, x, y, alive=True):
        """
        Sets the specified cell.

        :param x: x coord of the cell
        :type x: int
        :param y: y coord of the cell
        :type y: int
        :param alive: status of cell
        :type alive: bool
        :return: None
        """
        self._board[(x, y)] = alive

    def get_cell(self, x, y):
        if (x, y) not in self._board:
            return False
        return True

    @staticmethod
    def get_neighs(x, y):
        """
        Returns a list of the current cell's neighbours.

        :param x: x coord of the cell
        :type x: int
        :param y: y coord of the cell
        :type y: int
        :return: List(int, int)
        """
        return [(i, j) for i in xrange(x - 1, x + 2)
                for j in xrange(y - 1, y + 2)
                if (i, j) != (x, y)]

    def count_living_neigh(self, x, y):
        """
        Returns the number of living neighbours of the
        specified cell.

        :param x: x coord of the cell
        :type x: int
        :param y: y coord of the cell
        :type y: int
        :return: int
        """
        return len([1 for i in xrange(x - 1, x + 2)
                    for j in xrange(y - 1, y + 2)
                    if self.get_cell(i, j) and (i, j) != (x, y)])
