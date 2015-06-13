__author__ = 'moyiz'

from math import sin, pi
from itertools import cycle, islice, izip, chain
import wave
import struct
import copy


class Wave(object):
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
    def __init__(self, freq, rate, amp):
        self._freq = freq
        self._rate = rate
        self._amp = amp
        self._period = int(float(rate) / freq)
        self._cache = {}
        self._seconds = 0
        super(SineWave, self).__init__(self._wave())
        
    def _wave(self):
        return (self._calc(i) for i in cycle(xrange(self._period)))

    def _calc(self, t):
        if t not in self._cache:
            self._cache[t] = self._amp * sin(2 * pi * self._freq *
                                             (float(t) / self._rate))
        return self._cache[t]
    
    def duration(self, seconds=1):
        return islice(cycle(self.wave()), self._rate * seconds)


class Channel(object):
    def __init__(self, waves=list()):
        self._waves = waves

    def add(self, wav):
        self._waves.append(copy.deepcopy(wav))

    def __iter__(self):
        return self._waves

    @property
    def generator(self):
        return chain(*self._waves)


class WaveFile(object):
    def __init__(self, channels, sample_width):
        self._channels = channels
        self._nchannels = len(channels)
        self._swidth = sample_width

    def dump(self, filename, framerate=44100, seconds=0):
        w = wave.open(filename, "w")
        w.setparams((self._nchannels, self._swidth, framerate, seconds * framerate,
                    'NONE', 'not compressed'))
        max_amp = float(2 ** (self._swidth * 7)) - 1
        data = ''.join(''.join(struct.pack('h', max_amp * s) for s in channel)
                       for channel in self._samples())
        w.writeframesraw(data)
        w.close()

    def play(self, filename):
        pass

    def _samples(self):
        return izip(*self._channels)


a = SineWave(freq=440, rate=44100, amp=0.5).duration(1)
c = SineWave(freq=262.0, rate=44100, amp=0.5).duration(1)
e = SineWave(freq=329.0, rate=44100, amp=0.5).duration(2)
left = Channel([a, c])
right = Channel([e])
w = WaveFile([left.generator, right.generator], 2)
w.dump("bah.wav")
