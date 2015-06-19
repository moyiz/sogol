__author__ = 'moyiz'

from game import Game
from sound import *
import time
import os


class SoundOfLife(object):
    def __init__(self):
        self.game = Game()
        self.game.fill_random(3, 3, 7)

    def turn_and_play(self):
        seconds = self.generate_sound()
        self.play()
        self.game.do_turn()

    def generate_sound(self):
        board = self.game.board.get_living_cells()
        sounds = []
        for x, y in board:
            sounds.append(SineWave(440 + (12 ** 0.5) ** x, 44100, self._normalize(y)).duration(0.2))
        c1 = Channel(sounds[:len(sounds) / 2])
        c2 = Channel(sounds[len(sounds) / 2:])
        w = WaveFile([c1.generator, c2.generator], 2)
        w.dump("tmp.wav")

    def play(self):
        os.system("mplayer tmp.wav")

    def _normalize(self, x, low=-1, high=1):
        if x == 0:
            return 0
        return (high - low) / x

if __name__ == '__main__':
    pass
