import usb.device # type: ignore
from usb.device.keyboard import KeyboardInterface, KeyCode # type: ignore
from machine import Pin
from micropython import const
from neopixel import NeoPixel

KEYS = ( # (Pin, KeyCode, Led, Colour)
  # Screen buttons left
  (Pin.cpu.GPIO2, KeyCode.N, 3, (0,255,0)), # Home/Now Playing
  (Pin.cpu.GPIO3, KeyCode.F, 4, (255,0,0)), # Favourites
  (Pin.cpu.GPIO4, KeyCode.C, 5, (0,0,255)), # Pause

  # Screen buttons right
  (Pin.cpu.GPIO7, KeyCode.N0, 2, (255,127,0)), # Preset 0
  (Pin.cpu.GPIO6, KeyCode.N1, 1, (0,255,127)), # Preset 1
  (Pin.cpu.GPIO5, KeyCode.N2, 0, (127,0,255)), # Preset 2
)

N = const(6)
np = NeoPixel(Pin(9), N)

k = KeyboardInterface()

def fadeEven(fade):
  # reduce the levels of lit leds evenly
  for j in range(N):
    if np[j] != (0,0,0):
      np[j] = tuple(map(lambda a : max(a - fade, 0), np[j]))

def init():
  # Initialise all the pins as active-low inputs with pullup resistors
  for pin, _, led, clr in KEYS:
    pin.init(Pin.IN, Pin.PULL_UP)
    np[led] = clr

  np.write()

  # Register the keyboard interface and re-enumerate
  usb.device.get().init(k, builtin_driver=True)

keys = []  # Keys held down, reuse the same list object
prev_keys = [None]  # Previous keys, starts with a dummy value so first

def loop(i):
  fadeEven(10)

  if k.is_open():
    keys.clear()
    for pin, code, led, clr in KEYS:
      pressed = not pin() # active-low
      if pressed:
        keys.append(code)
        np[led] = clr

    if keys != prev_keys:
      # print(keys)
      k.send_keys(keys)
      prev_keys.clear()
      prev_keys.extend(keys)

  np.write()

def done():
  np.fill((0,0,0))
  np.write()
