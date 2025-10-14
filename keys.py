import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode
from machine import Pin
import neopixel

KEYS = (
    # Screen buttons
    (Pin.cpu.GPIO2, KeyCode.A, 2), # 4 (physical pin)
    (Pin.cpu.GPIO3, KeyCode.B, 1), # 5
    (Pin.cpu.GPIO4, KeyCode.C, 0), # 6
    (Pin.cpu.GPIO5, KeyCode.D, 3), # 7
    (Pin.cpu.GPIO6, KeyCode.E, 4), # 9
    (Pin.cpu.GPIO7, KeyCode.F, 5), # 10

    # Rotary encoder buttons
    (Pin.cpu.GPIO10, KeyCode.X, -1), # 13
    (Pin.cpu.GPIO11, KeyCode.Y, -1), # 14
)

np = neopixel.NeoPixel(Pin(21), 6)

k = KeyboardInterface()

def init():
    # Initialise all the pins as active-low inputs with pullup resistors
    for pin, _, _ in KEYS:
        pin.init(Pin.IN, Pin.PULL_UP)

    # Register the keyboard interface and re-enumerate
    usb.device.get().init(k, builtin_driver=True)

keys = []  # Keys held down, reuse the same list object
prev_keys = [None]  # Previous keys, starts with a dummy value so first

def loop():
    activate = False
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
            activate = True

        np.write()

    return activate

def done():
    np.fill((0,0,0))
    np.write()
