import leds
import keys
import status
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

      if status.audio_active or status.keys_lit or status.leds_lit:
        sleep_ms(DELAY)
        i += 1
      else:
        sleep_ms(DELAY * 10)

    except KeyboardInterrupt:
      break
  
  keys.done()
  leds.done()

main()
