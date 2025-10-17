import leds
import keys
import status
from time import sleep_ms

DELAY = const(20)
LOW_POWER_DELAY = const(100)

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
        sleep_ms(LOW_POWER_DELAY)

    except KeyboardInterrupt:
      break
  
  keys.done()
  leds.done()

main()
