import usb.device # type: ignore
from usb.device.keyboard import KeyboardInterface, KeyCode, LEDCode # type: ignore
from machine import Pin
from micropython import const
from neopixel import NeoPixel
import status

KEYS = ( # (Pin, KeyCode, Led, Colour)
  # Screen buttons left
  (Pin.cpu.GPIO2, KeyCode.N, 3, (0,255,0)), # Home/Now Playing
  (Pin.cpu.GPIO3, KeyCode.F, 4, (255,0,0)), # Favourites
  (Pin.cpu.GPIO4, KeyCode.C, 5, (0,0,255)), # Pause

  # Screen buttons right
  (Pin.cpu.GPIO7, KeyCode.N1, 2, (255,127,0)), # Preset 1
  (Pin.cpu.GPIO6, KeyCode.N2, 1, (0,255,127)), # Preset 2
  (Pin.cpu.GPIO5, KeyCode.N3, 0, (127,0,255)), # Preset 3
)

FADE = const(10)

N = const(6)
np = NeoPixel(Pin(9), N)

class Keyboard(KeyboardInterface):
  def on_led_update(self, led_mask):
    status.audio_active = bool(led_mask & LEDCode.SCROLL_LOCK)
    status.leds_lit = True
    status.keys_lit = True

k = Keyboard()

def fade():
  if status.keys_lit:
    lit = False
    # reduce the levels of leds evenly
    for j in range(N):
      if np[j] != (0,0,0):
        np[j] = tuple(map(lambda a : max(a - FADE, 0), np[j]))
        lit = True
    np.write()
    status.keys_lit = lit

def init():
  # Initialise all the pins as active-low inputs with pullup resistors
  for pin, _, led, clr in KEYS:
    pin.init(Pin.IN, Pin.PULL_UP)
    np[led] = clr

  np.write()
  status.keys_lit = True

  # Register the keyboard interface and re-enumerate
  usb.device.get().init(k, builtin_driver=True)

keys = []  # Keys held down, reuse the same list object
prev_keys = [None]  # Previous keys, starts with a dummy value so first

def loop(i):
  fade()

  if k.is_open():
    keys.clear()
    for pin, code, led, clr in KEYS:
      if not pin(): # active-low
        keys.append(code)
        np[led] = clr
        np.write()
        status.keys_lit = True

    if keys != prev_keys:
      # print(keys)
      k.send_keys(keys)
      prev_keys.clear()
      prev_keys.extend(keys)

def done():
  np.fill((0,0,0))
  np.write()
