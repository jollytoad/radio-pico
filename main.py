import leds
import keys
from time import sleep_ms
from usb.device.keyboard import KeyCode # type: ignore

DELAY = 20

def main():
  i = 0

  keys.init()
  leds.init()

  while True:
    try:
      keys.loop(i)
      leds.loop(i)

      sleep_ms(DELAY)
      i += 1
    except KeyboardInterrupt:
      break
  
  keys.done()
  leds.done()

main()
