#!/bin/sh

# This script does two things:
# 1. Start pigpiod and sbpd to handle volume control rotary encoder
# 2. Start a script that watches the squeezelite shared memory for
#    the 'running' flag, and notifies the pico usb keypad via an 'led'

# start pigpiod daemon
sudo pigpiod -t 0 -f -l -s 10

# wait for pigpiod to initialize - indicated by 'pigs t' exit code of zero

count=10 # approx time limit in seconds
while ! pigs t >/dev/null 2>&1 ; do
	if [ $((count--)) -le 0 ]; then
		printf "\npigpiod failed to initialize within time limit\n"
		exit 1
	fi
#	printf "\nWaiting for pigpiod to initialize\n"
	sleep 1
done
printf "\npigpiod is running\n"

# load uinput module - required to be able to send keystrokes
# then set the permission to group writable, so you don't need to run sbpd with root permissions
sudo modprobe uinput
sudo chmod g+w /dev/uinput

# The full list of Jivelite key commands can be found here:
# https://github.com/ralph-irving/tcz-lirc/blob/master/jivekeys.csv

CMD="sbpd -v e,23,24,VOLU,2 b,27,KEY:KEY_U"

echo $CMD
$CMD > /dev/null 2>&1 &

CMD="/home/tc/watch-running.sh"

echo $CMD
$CMD > /dev/null 2>&1 &
