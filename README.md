# Pi/Pico Radio

This is my kitchen radio project.

- Case: A 1940s Bakelite [Bush DAC90](https://collections.vam.ac.uk/item/O372024/bush-dac90-radio-middleditch-frank-e/)
- Hardware:
  - [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/)
  - [DigiAmp+](https://www.raspberrypi.com/products/digiamp-plus/) and [power supply](https://thepihut.com/products/pi-digiamp-plus-power-brick-15v-3-33a-50w)
  - [Waveshare 4.3inch touchscreen](https://www.waveshare.com/wiki/4.3inch_DSI_LCD)
  - [Raspberry Pi Pico 2](https://www.raspberrypi.com/products/raspberry-pi-pico-2/)
  - 3 x [KY-040 Rotary Encoder](https://www.amazon.co.uk/dp/B07SV5HHM5)
  - 6 x [Mx key switches](https://www.amazon.co.uk/dp/B0CNSZJJJS) with [NeoKey](https://thepihut.com/products/neokey-socket-breakout-for-mechanical-key-switches-with-neopixel-for-mx-compatible-switches) led sockets
  - A strip of 60 NeoPixel compatible leds
  - Some [Dupont wires](https://thepihut.com/products/thepihuts-jumper-bumper-pack-120pcs-dupont-wire)
  - 3D parts printed using a [Creality Ender-3 V3 SE](https://www.creality.com/products/creality-ender-3-v3-se)
- Software:
  - [PiCorePlayer](https://www.picoreplayer.org/) (LMS + Squeezelite + Jivelite)
  - [MicroPython](https://micropython.org)

One day I may post some photos.

The Pico acts as a 6-key backlit usb keyboard to control Jivelite,
and also runs a funky led display (~60 leds in 4 concentric rings),
with a couple of rotary encoders to control the led effects.

This is mainly the MicroPython program for the Pico.

## Installing to the Pico from the Pi:

```sh
git clone https://github.com/jollytoad/radio-pico.git
cd radio-pico
pip install mpremote
./install.sh
```
