#!/bin/sh

cp -v watch_running.sh ~/
cp -v watch_running_daemon.sh ~/

echo "Installing to Pico..."

mpremote reset 2>/dev/null
mpremote fs cp *.py :
mpremote reset
