import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode
from machine import Pin
import neopixel

KEYS = (
    # Screen buttons left
    (Pin.cpu.GPIO2, KeyCode.A, 3),
    (Pin.cpu.GPIO3, KeyCode.B, 4),
    (Pin.cpu.GPIO4, KeyCode.C, 5),

    # Screen buttons right
    (Pin.cpu.GPIO7, KeyCode.D, 2),
    (Pin.cpu.GPIO6, KeyCode.E, 1),
    (Pin.cpu.GPIO5, KeyCode.F, 0),

    # Rotary encoder button - side
    (Pin.cpu.GPIO13, KeyCode.X, -1),

    # Rotary encoder button - front right
    (Pin.cpu.GPIO18, KeyCode.Y, -2),
)

np = neopixel.NeoPixel(Pin(9), 6)

k = KeyboardInterface()

def init():
    # Initialise all the pins as active-low inputs with pullup resistors
    for pin, _, _ in KEYS:
        pin.init(Pin.IN, Pin.PULL_UP)

    # Register the keyboard interface and re-enumerate
    usb.device.get().init(k, builtin_driver=True)

    np.fill((0,255,0))
    np.write()

keys = []  # Keys held down, reuse the same list object
prev_keys = [None]  # Previous keys, starts with a dummy value so first

def loop():
    if k.is_open():
        keys.clear()
        for pin, code, led in KEYS:
            pressed = not pin() # active-low
            if pressed:
                keys.append(code)
            if led >= 0:
                np[led] = (100,100,100) if pressed else (0,0,0)

        if keys != prev_keys:
            # print(keys)
            k.send_keys(keys)
            prev_keys.clear()
            prev_keys.extend(keys)
            np.write()

    return keys

def done():
    np.fill((0,0,0))
    np.write()
