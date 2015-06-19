import wave
import struct
import copy
from math import sin, pi
from itertools import cycle, islice, izip, chain

"""
An usage example:

a = SineWave(freq=440, rate=44100, amp=0.5).duration(1)
c = SineWave(freq=262.0, rate=44100, amp=0.5).duration(1)
e = SineWave(freq=329.0, rate=44100, amp=0.5).duration(2)
left = Channel([a, c])
right = Channel([e])
w = WaveFile([left.generator, right.generator], 2)
w.dump("bah.wav")
"""


class Wave(object):
    """
    Base class for waves.
    Waves are based on generators.
    Provides an implementation of addition and substraction of waves.
    """
    def __init__(self, gen):
        self._gen = gen

    def wave(self):
        return self._gen

    def __add__(self, y):
        return Wave(i + j for i, j in izip(self.wave(), y.wave()))

    def __sub__(self, y):
        return Wave(i - j for i, j in izip(self.wave(), y.wave()))

    def __iter__(self):
        return self.wave()

    def duration(self, seconds=1):
        raise NotImplementedError


class SineWave(Wave):
    """
    A sine wave.
    """
    def __init__(self, freq, rate, amp):
        """
        Create a sine wave out of the parameters.

        :param freq: The frequency of the wave.
        :type freq: int or float
        :param rate: The frame rate of the wave.
        :type rate: int or float
        :param amp: The amplitude of the wave.
        :type amp: int or float
        """
        self._freq = freq
        self._rate = rate
        self._amp = amp
        self._period = int(float(rate) / freq)
        self._cache = {}
        self._seconds = 0
        super(SineWave, self).__init__(self._wave())

    def _wave(self):
        """
        Returns a generator for the wave
        """
        return (self._calc(i) for i in cycle(xrange(self._period)))

    def _calc(self, t):
        """
        Calculates the value of the wave at the specific index.
        Uses a cache mechanism for optimizations.
        """
        if t not in self._cache:
            self._cache[t] = self._amp * sin(2 * pi * self._freq *
                                             (float(t) / self._rate))
        return self._cache[t]

    def duration(self, seconds=1):
        """
        Returns a wave in length of the specified seconds.

        :param seconds: The amount of time for the wave.
        :type seconds: int or float
        :return: A generator that generates a `seconds` length wave.
        :rtype: generator
        """
        return islice(cycle(self.wave()), self._rate * seconds)


class Channel(object):
    """
    Used to represent a channel.
    Contains a list of wave to produce a chain.
    """
    def __init__(self, waves=list()):
        self._waves = waves

    def add(self, wav):
        """
        Add a wave into the channel.

        :param wav: The wave to add.
        :type wav: Wave
        """
        self._waves.append(copy.deepcopy(wav))

    def __iter__(self):
        return self._waves

    @property
    def generator(self):
        """
        A generator of the chain produced from the waves in this channel.
        """
        return chain(*self._waves)


class WaveFile(object):
    """
    A wave file.
    """
    def __init__(self, channels, sample_width):
        """
        :param channels: A list of channel.
        :type channels: list(Channel)
        :param sample_width: The width of the sound
        :type sample_width: int
        """
        self._channels = channels
        self._nchannels = len(channels)
        self._swidth = sample_width

    def dump(self, filename, framerate=44100, seconds=0):
        """
        Dumps the content of this instance's channels into a file.

        :param filename: The name of the file to create.
        :type filename: str
        :param framerate: The frame rate to use (default: 44100)
        :type framerate: int
        :param seconds: The amount of seconds to dump.
        :type seconds: int or float
        """
        w = wave.open(filename, "w")
        w.setparams((self._nchannels, self._swidth, framerate,
                     seconds * framerate, 'NONE', 'not compressed'))
        max_amp = float(2 ** (self._swidth * 7)) - 1
        data = ''.join(''.join(struct.pack('h', max_amp * s) for s in channel)
                       for channel in self._samples())
        w.writeframesraw(data)
        w.close()

    def _samples(self):
        return izip(*self._channels)
