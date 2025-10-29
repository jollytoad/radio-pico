import usb.device # type: ignore
from usb.device.keyboard import KeyboardInterface, KeyCode, LEDCode # type: ignore
from machine import Pin
from neopixel import NeoPixel
import status

_KEYS = ( # (Pin, KeyCode, Led, Colour)
  # Screen buttons left
  (Pin.cpu.GPIO2, KeyCode.N, 3, (0,255,0)), # Home/Now Playing
  (Pin.cpu.GPIO3, KeyCode.F, 4, (255,0,0)), # Favourites
  (Pin.cpu.GPIO4, KeyCode.C, 5, (0,0,255)), # Pause

  # Screen buttons right
  (Pin.cpu.GPIO7, KeyCode.N1, 2, (255,127,0)), # Preset 1
  (Pin.cpu.GPIO6, KeyCode.N2, 1, (0,255,127)), # Preset 2
  (Pin.cpu.GPIO5, KeyCode.N3, 0, (127,0,255)), # Preset 3
)

_FADE = const(10)

_N = const(6)
_np = NeoPixel(Pin(9), _N)

class Keyboard(KeyboardInterface):
  def on_led_update(self, led_mask):
    status.audio_active = bool(led_mask & LEDCode.SCROLL_LOCK)
    status.leds_lit = True
    status.keys_lit = True

_k = Keyboard()

def _fade():
  if status.keys_lit:
    status.keys_lit = False
    # reduce the levels of leds evenly
    for j in range(_N):
      if _np[j] != (0,0,0):
        _np[j] = tuple(map(lambda a : max(a - _FADE, 0), _np[j]))
        status.keys_lit = True
    _np.write()

def init():
  # Initialise all the pins as active-low inputs with pullup resistors
  for pin, _, led, clr in _KEYS:
    pin.init(Pin.IN, Pin.PULL_UP)
    _np[led] = clr

  _np.write()
  status.keys_lit = True

  # Register the keyboard interface and re-enumerate
  usb.device.get().init(_k, builtin_driver=True)

_keys = []  # Keys held down, reuse the same list object
_prev_keys = [None]  # Previous keys, starts with a dummy value so first

def loop(i):
  _fade()

  if _k.is_open():
    _keys.clear()
    for pin, code, led, clr in _KEYS:
      if not pin(): # active-low
        _keys.append(code)
        _np[led] = clr
        _np.write()
        status.keys_lit = True

    if _keys != _prev_keys:
      _k.send_keys(_keys)
      _prev_keys.clear()
      _prev_keys.extend(_keys)

def done():
  _np.fill((0,0,0))
  _np.write()
