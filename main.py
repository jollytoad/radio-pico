import time
import leds
import keys

DELAY = 20

def main():
  i = 0
  pattern = 0

  keys.init()

  while True:
    try:
      activate = keys.loop()
      if (activate):
        pattern = (pattern + 1) % 4
      leds.loop(i, pattern)
      time.sleep_ms(DELAY)
      i += 1
    except KeyboardInterrupt:
      break
  
  keys.done()
  leds.done()

main()
