from machine import Pin
from micropython import const
from neopixel import NeoPixel
from random import randint, randrange
from rots import side_btn, side_down, side_rot, front_btn, front_down, front_rot
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

def fadeRandom(fade):
  # reduce the levels of lit leds with a slight randomness
  for j in range(N):
    if np[j] != (0,0,0):
      np[j] = tuple(map(lambda a : max(a - randint(fade // 2, fade), 0), np[j]))

def fadeEven(fade):
  # reduce the levels of lit leds evenly
  for j in range(N):
    if np[j] != (0,0,0):
      np[j] = tuple(map(lambda a : max(a - fade, 0), np[j]))

def fireworks(i):
  chance = side_rot.value() // 2
  brightness = front_rot.value()

  fadeRandom(chance * 2)

  # should we light a new led?
  if randrange(0,100) < chance:
    # pick a random led
    p = all[randrange(len(all))]

    # only light it if it's off
    if (np[p] == (0,0,0)):
      # set a random hue and saturation
      np[p] = hsv.to_rgb(randint(0, 359), randint(128, 255), brightness)

def pulse(i):
  freq = max((100-side_rot.value()) // 30, 1)
  brightness = front_rot.value() // 4

  fadeEven(5)

  if (i % freq == 0):
    r = int(i/freq) % (len(ring)*3)
    if (r < len(ring)):
      c = hsv.to_rgb(randint(0, 359), randint(200, 255), brightness)
      for p in ring[len(ring)-1-r]:
        np[p] = c

def spiral(i):
  brightness = front_rot.value() // 3

  fadeEven(10)

  p = all[i % len(all)]
  np[p] = hsv.to_rgb(i % 360, 255, brightness)

def static(i):
  chance = side_rot.value() // 2
  v = front_rot.value() // 4

  for p in all:
    np[p] = (v, v, v) if randrange(0,100) < chance else (0,0,0)

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
  global pattern, side_down, front_down

  patterns[pattern](i)

  # TODO: switch pattern when rot btn is clicked
  if (side_down and side_btn()):
    print('side click')
    pattern = (pattern+1) % len(patterns)
    print('pattern', pattern)

  if (front_down and front_btn()):
    print('front click')
    pattern = (pattern-1) % len(patterns)

  side_down = not side_btn()
  front_down = not front_btn()

  # apply new led settings
  np.write()

def done():
  np.fill((0,0,0))
  np.write()
