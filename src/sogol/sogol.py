import time
import os
from uuid import uuid1

from game import Game
from sound import *


class SoundOfLife(object):
    """
    A game of sound.
    This class manages the entire game and combines it
    with sound making.

    Use `start` to listen to The Sound Of Life.
    """
    def __init__(self):
        """
        Receives a number of cells to generate randomly.

        :param cells: The number of cells to generate.
        :type cells: int
        :return: None
        """
        self.game = Game()
        self.game.fill_random(3, 3, 7)

    def single_turn(self):
        """
        Does a single turn and plays the board state.

        """
        wav = self.generate_sound()
        self._play(wav)
        os.remove(wav)
        self.game.do_turn()

    def _play(self, wav):
        """
        Plays the specified wave file.

        :param wav: A path to the wav file
        :type wav: str
        :return: None
        """
        os.system("mplayer {}".format(wav))

    def start(self, delay=0.5):
        """
        Run until no living cells remain, and play each turn.

        :param delay: The amount of seconds to wait between turns.
        :type delay: int
        :return: None
        """
        while len(self.game.board.get_living_cells()) > 0:
            self.single_turn()
            time.sleep(delay)

    def generate_sound(self):
        """
        Generates a sound out of the board and saves it into a
        temporary file.

        :return: A path to the wave file
        :rtype: str
        """
        board = self.game.board.get_living_cells()
        sounds = []
        for x, y in board:
            sounds.append(SineWave(440 + (12 ** 0.5) ** x, 44100,
                          self._normalize(y)).duration(0.2))
        c1 = Channel(sounds[:len(sounds) / 2])
        c2 = Channel(sounds[len(sounds) / 2:])
        w = WaveFile([c1.generator, c2.generator], 2)
        wav_name = str(uuid1())[:10] + '.wav'
        w.dump(wav_name)
        return wav_name

    def _normalize(self, x, low=-1, high=1):
        """
        Used to normalize x to a value between low and high.

        :param x: The value to normalize
        :type x: int
        :param low: The lower bound
        :type low: int
        :param high: The upper bound
        :type high: int
        :return: The normalized value
        ;rtype: int
        """
        if x == 0:
            return 0
        return (high - low) / x


if __name__ == '__main__':
    pass
