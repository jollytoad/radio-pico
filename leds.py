from machine import Pin
from neopixel import NeoPixel
from random import randint, randrange
import rots
import status
import hsv

# total leds
_N = const(59)

# all usable leds
_all = range(1,58+1)

# range of leds in each ring
_ring = [
  range(2, 23+1),
  range(23, 40+1),
  range(42, 52+1),
  range(53, 58+1)
]

_np = NeoPixel(Pin(8), _N)

_fade_random: bool = False
_fade_level: int = 10

def _fade():
  if status.leds_lit:
    status.leds_lit = False
    # reduce the levels of status.leds_lit leds evenly or with a slight randomness
    for j in range(_N):
      if _np[j] != (0,0,0):
        if _fade_level > 0:
          fade_amount = randint(_fade_level // 2, _fade_level) if _fade_random else _fade_level
          _np[j] = tuple(map(lambda a : max(a - fade_amount, 0), _np[j]))
        status.leds_lit = True
    if _fade_level > 0:
      _np.write()

def _fireworks(i):
  global _fade_level, _fade_random

  chance: int = rots.side_rot.value() // 2
  brightness: int = rots.front_rot.value()
  _fade_level = rots.side_rot.value()
  _fade_random = True

  # should we light a new led?
  if randrange(0,100) < chance:
    # pick a random led
    p = _all[randrange(len(_all))]

    # only light it if it's off
    if (_np[p] == (0,0,0)):
      # set a random hue and saturation
      _np[p] = hsv.to_rgb(randint(0, 359), randint(128, 255), brightness)
      _np.write()
      status.leds_lit = True

def _pulse(i):
  global _fade_level, _fade_random

  freq: int = max((100-rots.side_rot.value()) // 30, 1)
  brightness: int = rots.front_rot.value() // 4
  _fade_level = 5
  _fade_random = False

  if (i % freq == 0):
    r = int(i/freq) % (len(_ring)*3)
    if (r < len(_ring)):
      c = hsv.to_rgb(randint(0, 359), randint(200, 255), brightness)
      for p in _ring[len(_ring)-1-r]:
        _np[p] = c
      _np.write()
      status.leds_lit = True

def _spiral(i):
  global _fade_level, _fade_random

  brightness = rots.front_rot.value() // 3
  _fade_level = 10
  _fade_random = False

  p = _all[i % len(_all)]
  _np[p] = hsv.to_rgb(i % 360, 255, brightness)
  _np.write()
  status.leds_lit = True

def _static(i):
  global _fade_level, _fade_random

  chance = rots.side_rot.value() // 2
  v = rots.front_rot.value() // 4
  _fade_level = 0
  _fade_random = False

  for p in _all:
    _np[p] = (v, v, v) if randrange(0,100) < chance else (0,0,0)
  _np.write()
  status.leds_lit = True

_pattern: int = 0

_patterns = [
  _static,
  _pulse,
  _spiral,
  _fireworks
]

def init():
  print('START')
  rots.side_btn.init(Pin.IN, Pin.PULL_UP)
  rots.front_btn.init(Pin.IN, Pin.PULL_UP)
  _np.fill((0,0,0))
  _np.write()

def loop(i):
  global _pattern, _fade_level, _fade_random

  _fade()

  if status.audio_active:
    _patterns[_pattern](i)
  else:
    _fade_level = 8
    _fade_random = True

  if (rots.side_down and rots.side_btn()):
    print('side click')
    _pattern = (_pattern+1) % len(_patterns)
    print('pattern', _pattern)

  if (rots.front_down and rots.front_btn()):
    print('front click')
    _pattern = (_pattern-1) % len(_patterns)

  rots.side_down = not rots.side_btn()
  rots.front_down = not rots.front_btn()

def done():
  _np.fill((0,0,0))
  _np.write()
