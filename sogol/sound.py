import struct
from abc import abstractmethod
from itertools import chain, cycle, islice
from math import pi, sin
from typing import Generator, Iterable, List

from simpleaudio import play_buffer


class Wave:
    """
    Base class for waves.
    Waves are based on generators.
    Provides an implementation of addition and substraction of waves.
    """

    def __init__(self, freq: int, rate: int, amp: float):
        """
        :param freq: The frequency of the wave.
        :type freq: int or float
        :param rate: The frame rate of the wave.
        :type rate: int or float
        :param amp: The amplitude of the wave.
        :type amp: int or float
        """
        self.freq = freq
        self.rate = rate
        self.amp = amp
        self._cache = {}

    def __iter__(self):
        return (
            self._cached_position(i) for i in cycle(range(int(self.rate / self.freq)))
        )

    def _cached_position(self, t):
        if t not in self._cache:
            self._cache[t] = self.position(t)
        return self._cache[t]

    @abstractmethod
    def position(self, t):
        """
        Get a specific position `t` in wave.
        """
        pass

    def duration(self, seconds: int = 1) -> Generator:
        """
        Returns a wave in length of the specified seconds.

        :return: A generator that generates a `seconds` length wave.
        """
        return islice(cycle(iter(self)), int(self.rate * seconds))


class SineWave(Wave):
    def position(self, t) -> float:
        return self.amp * sin(2 * pi * self.freq * (t / self.rate))


class SquareWave(Wave):
    def position(self, t) -> float:
        return self.amp * (-1) ** int(2 * self.freq * (t / self.rate))


class SawtoothWave(Wave):
    def position(self, t) -> float:
        return self.amp * (t * self.freq / self.rate) - (t * self.freq // self.rate)


class Channel:
    """
    Chains a list of waves.
    """

    def __init__(self, waves: Iterable = None):
        self._waves = waves or []

    def __iter__(self):
        return self._waves

    @property
    def generator(self):
        """
        A generator of the chain produced from the waves in this channel.
        """
        return chain(*self._waves)


def play(channels: List[Channel], sample_width: int, framerate: int = 44100):
    max_amp = float(2 ** (sample_width * 7)) - 1
    data = b"".join(
        b"".join(struct.pack("h", int(max_amp * sample)) for sample in channel)
        for channel in zip(*channels)
    )

    return play_buffer(
        audio_data=data,
        num_channels=len(channels),
        bytes_per_sample=sample_width,
        sample_rate=framerate,
    ).wait_done()
