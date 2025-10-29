# Installing the piCorePlayer

## SDCard

- Burn piCorePlayer OS to SD with the Raspberry Pi Imager
- Mount the SD
- Create `wpa_supplicant.conf`:

```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=staff
country=GB
update_config=1

network={
        ssid="SET THIS"
        psk="SET THIS"
        key_mgmt=WPA-PSK
        auth_alg=OPEN
}
```

- Put the SD into the Pi and boot

## Guided setup

- Open the pcp server page and follow the guided setup...
- Host name: `radio`
- Enable SSH
- NTP server: `pool.ntp.org`, 'Set and Enable'
- Enable Lyrion Server
- Select audio device: `DigiAMP`
- Resize partition 2 to the `Whole SD Card`

- After it's rebooted, from the main pcp pages:

## Lyrion Music Server setup:

- Select `Lyrion` tab
- Click `Install LMS`, then after it's installed...
- `Start LMS`
- `Configure LMS`, this opens in a new tab with a setup wizard...
- Select `TIDAL`, and complete the wizard
- Update LMS if an update is available
- Add the following plugins:
- `AirPlay bridge`, `BBC Sounds`, `Chromecast bridge`
- Enable plugin auto update
- Set Presets:
- 1. `BBC Radio 2`: `sounds://_LIVE_bbc_radio_two`
- 2. 
- 3.

## Tweaks:

- Broadcast .local: `No` (doesn't seem to work on our network)
- HDMI power: `Off`

## Jivelite setup:

- Ensure VC4 graphics driver is `No`
- `Install Vis`

- From the physical radio screen, in Jivelite:
- Select language `English`
- Select `Grid Skin`

## Volume/Pico setup

- Install extensions:
- `git.tcz`, `pigpio.tcz`, `pcp-sbpd.tcz`, `python3.11.tcz`, `python3.11-pip.tcz`

- `ssh tc@...`

```sh
git clone https://github.com/jollytoad/radio-pico.git
cd radio-pico
pip install mpremote
./install.sh
```

- In pcp `Tweaks` tab; 'User commands'...
- User command #1: `/home/tc/start.sh`
- Reboot

## Bluetooth

- In `Wifi Settings` tab...
- RPi built-in Bluetooth: `On`
- In `Main Page` tab...
- Click `Bluetooth` and `Install`
- Reboot
- In `Tweaks` tab...
- `setStreamer` to `Yes`
- In `Bluetooth` page...
- Enable `Discoverable`
- Pair your phone with `radio`
