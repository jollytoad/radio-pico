from machine import Pin
from micropython import const
from neopixel import NeoPixel
from random import randint, randrange
from rots import side_btn, side_down, side_rot, front_btn, front_down, front_rot
import status
import hsv

# total leds
N = const(59)

# all usable leds
all = range(1,58+1)

# range of leds in each ring
ring = [
  range(2, 23+1),
  range(23, 40+1),
  range(42, 52+1),
  range(53, 58+1)
]

np = NeoPixel(Pin(8), N)

fade_random = False
fade_level = 10

def fade():
  if status.leds_lit:
    lit = False
    # reduce the levels of status.leds_lit leds evenly or with a slight randomness
    for j in range(N):
      if np[j] != (0,0,0):
        if fade_level > 0:
          fade_amount = randint(fade_level // 2, fade_level) if fade_random else fade_level
          np[j] = tuple(map(lambda a : max(a - fade_amount, 0), np[j]))
        lit = True
    if fade_level > 0:
      np.write()
    status.leds_lit = lit

def fireworks(i):
  global fade_level, fade_random
  chance = side_rot.value() // 2
  brightness = front_rot.value()
  fade_level = side_rot.value()
  fade_random = True

  # should we light a new led?
  if randrange(0,100) < chance:
    # pick a random led
    p = all[randrange(len(all))]

    # only light it if it's off
    if (np[p] == (0,0,0)):
      # set a random hue and saturation
      np[p] = hsv.to_rgb(randint(0, 359), randint(128, 255), brightness)
      np.write()
      status.leds_lit = True

def pulse(i):
  global fade_level, fade_random
  freq = max((100-side_rot.value()) // 30, 1)
  brightness = front_rot.value() // 4
  fade_level = 5
  fade_random = False

  if (i % freq == 0):
    r = int(i/freq) % (len(ring)*3)
    if (r < len(ring)):
      c = hsv.to_rgb(randint(0, 359), randint(200, 255), brightness)
      for p in ring[len(ring)-1-r]:
        np[p] = c
      np.write()
      status.leds_lit = True

def spiral(i):
  global fade_level, fade_random
  brightness = front_rot.value() // 3
  fade_level = 10
  fade_random = False

  p = all[i % len(all)]
  np[p] = hsv.to_rgb(i % 360, 255, brightness)
  np.write()
  status.leds_lit = True

def static(i):
  global fade_level, fade_random
  chance = side_rot.value() // 2
  v = front_rot.value() // 4
  fade_level = 0
  fade_random = False

  for p in all:
    np[p] = (v, v, v) if randrange(0,100) < chance else (0,0,0)
  np.write()
  status.leds_lit = True

pattern: int = 0

patterns = [
  static,
  pulse,
  spiral,
  fireworks
]

def init():
  print('START')
  side_btn.init(Pin.IN, Pin.PULL_UP)
  front_btn.init(Pin.IN, Pin.PULL_UP)
  np.fill((0,0,0))
  np.write()

def loop(i):
  global pattern, side_down, front_down, fade_level, fade_random

  fade()

  if status.audio_active:
    patterns[pattern](i)
  else:
    fade_level = 8
    fade_random = True

  if (side_down and side_btn()):
    print('side click')
    pattern = (pattern+1) % len(patterns)
    print('pattern', pattern)

  if (front_down and front_btn()):
    print('front click')
    pattern = (pattern-1) % len(patterns)

  side_down = not side_btn()
  front_down = not front_btn()

def done():
  np.fill((0,0,0))
  np.write()
