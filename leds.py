from machine import Pin
from time import sleep_ms
import neopixel
import random

brightness = 1.0 # 0-1
chance = 20 # 0-100, TODO: set this to audio output level

delay = 20

# total leds
n = 59

# all usable leds
all = range(1,58+1)

# range of leds in each ring
ring = [
    range(2,23+1),
    range(23, 40+1),
    range(42, 52+1),
    range(53, 58+1)
]

# usable pixels
leds = all

np = neopixel.NeoPixel(Pin(8), n)

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        r = g = b = int(v * 255)
        return (r, g, b)
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    elif i == 5:
        r, g, b = v, p, q
    return (int(r * 255), int(g * 255), int(b * 255))

def fadeRandom(fade):
    # reduce the levels of lit leds with a slight randomness
    for j in range(n):
        if np[j] != (0,0,0):
            np[j] = tuple(map(lambda a : max(a - random.randint(int(fade/2), fade), 0), np[j]))

def fadeEven(fade):
    # reduce the levels of lit leds evenly
    for j in range(n):
        if np[j] != (0,0,0):
            np[j] = tuple(map(lambda a : max(a - fade, 0), np[j]))

def fireworks():
    fadeRandom(chance * 2)

    # should we light a new led?
    if random.randrange(0,100) < chance:
        # pick a random led
        p = leds[random.randrange(len(leds))]

        # only light it if it's off
        if (np[p] == (0,0,0)):
            # set a random hue and saturation
            np[p] = hsv_to_rgb(
                random.uniform(0, 1),
                random.uniform(0.5, 1.0),
                brightness
                )

def pulse(i, x):
    fadeEven(5)

    if (i % x == 0):
        r = int(i/x) % (len(ring)*3)
        if (r < len(ring)):
            c = hsv_to_rgb(
                random.uniform(0, 1),
                random.uniform(1, 1),
                brightness/4
                )
            for p in ring[len(ring)-1-r]:
                np[p] = c

def spiral(i):
    fadeEven(10)

    p = all[i % len(all)]
    np[p] = hsv_to_rgb(i/360, 1, brightness/3)

def loop(i, pattern):
    if (pattern == 0):
        fadeEven(1)
    elif (pattern == 1):
        pulse(i,2)
    elif (pattern == 2):
        spiral(i)
    elif (pattern == 3):
        fireworks()

    # apply new led settings
    np.write()

def done():
    np.fill((0,0,0))
    np.write()
