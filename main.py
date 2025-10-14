import time
import leds
import keys
from usb.device.keyboard import KeyCode

DELAY = 20

def main():
  i = 0
  pattern = 0

  keys.init()
  leds.init()

  while True:
    try:
      pressed = keys.loop()
      if (pressed == [KeyCode.X]):
        pattern = (pattern + 1) % 4
      leds.loop(i, pattern)
      time.sleep_ms(DELAY)
      i += 1
    except KeyboardInterrupt:
      break
  
  keys.done()
  leds.done()

main()
