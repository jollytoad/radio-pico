#!/bin/sh

CMD="/home/tc/watch_running.sh"

echo $CMD
$CMD > /dev/null 2>&1 &
