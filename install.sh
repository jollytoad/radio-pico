#!/bin/sh

echo "Installing shell scripts to Pico..."

cp -v pico-scripts/*.sh ~/

echo "Installing MicroPython code to Pico..."

mpremote reset 2>/dev/null
mpremote mip install usb-device-keyboard
mpremote mip install github:miketeachman/micropython-rotary
mpremote fs cp *.py :
mpremote reset
