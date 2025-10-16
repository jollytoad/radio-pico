#!/bin/sh

cp -v watch_running.sh ~/watch_running.sh

mpremote reset
mpremote fs cp *.py :
mpremote reset
