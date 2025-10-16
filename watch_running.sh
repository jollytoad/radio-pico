#!/bin/sh

# Find the squeezelite shared memory file
SHM_FILE=$(ls /dev/shm/squeezelite-??:??:??:??:??:?? 2>/dev/null | head -n 1)
LED_FILE=$(ls /sys/class/leds/input?::scrolllock/brightness 2>/dev/null | head -n 1)

if [ -z "$SHM_FILE" ]; then
  echo "Error: No squeezelite shared memory file found in /dev/shm/"
  exit 1
fi

if [ -z "$LED_FILE" ]; then
  echo "Error: No usb keyboard leds found in /sys/class/leds/"
  exit 1
fi

echo "Monitoring: $SHM_FILE"
echo "Watching 'running' flag for changes..."
echo ""

OFFSET=64  # 0x40 - offset of the running flag (56 bytes rwlock + 4 buf_size + 4 buf_index)

previous=""

while true; do
  # Read 1 byte at offset 64
  current=$(od -An -t u1 -N 1 -j $OFFSET "$SHM_FILE" 2>/dev/null | tr -d ' ')

  if [ -n "$current" ] && [ "$current" != "$previous" ]; then
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    if [ "$current" = "0" ]; then
      echo "[$timestamp] running: false (stopped)"
      sudo sh -c "echo 0 > $LED_FILE"
    else
      echo "[$timestamp] running: true (playing)"
      sudo sh -c "echo 1 > $LED_FILE"
    fi
    previous="$current"
  fi

  sleep 1
done
