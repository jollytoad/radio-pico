# Pi/Pico Radio

This is my kitchen radio project.

Case: A 40s bakelite Bush DAC90
Hardware: Raspberry Pi 3b+, DigiAmp+, Waveshare touchscreen, Pico 2
Software: PiCorePlayer (LMS + Squeezelite + Jivelite), Micropython

The Pico acts as a 6-key backlit usb keyboard to control Jivelite,
and also runs a funky led display (~60 leds in 4 concentric rings),
with a couple or rotary encoders to control the led effects.

This is mainly the Micropython program for the Pico.

## Installing to the Pico from the Pi:

```sh
git clone https://github.com/jollytoad/radio-pico.git
cd radio-pico
pip install mpremote
./install.sh
```
