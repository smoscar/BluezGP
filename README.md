# BluezGP
Turns any Keyboard and Gamepad into Bluetooth HID devices using a Raspberry Pi (could work with other Linux systems).

## Features
  - Intercepts key and button events from USB devices (keyboards, mice, controllers, etc).
  - Advertises itself as a keyboard or as a Bluetooth gamepad.
  - Sends key and button events to connected Bluetooth devices.
  - Support for analog joysticks and triggers.
  - Includes Retropie menu integration.
![Raspberry Pi Zero W](https://ezway-imagestore.s3.amazonaws.com/files/2019/07/17133308891562479901.png)
  
## Installation
```
sudo apt-get update
sudo apt-get install bluetooth bluez blueman pi-bluetooth python-bluez python-pip
sudo pip install evdev
cd
git clone https://github.com/smoscar/BluezGP.git
sudo reboot now
```

## Configuration
Disable all bluetooth plugins except 'time' by editing these files:
```
sudo vi /etc/systemd/system/dbus-org.bluez.service
```
Make sure bluetoothd is executed with the time plugin only by editing its line to look like the following:
```
ExecStart=/usr/lib/bluetooth/bluetoothd -p time
```
Edit the bluetooth init file too:
```
sudo vi /etc/init.d/bluetooth
```
And make sure the bluetoothd daemon line looks like this:
```
DAEMON=/usr/sbin/bluetoothd -p time
```
Copy the DBUS profile included:
```
sudo cp ~/BluezGP/dbus/org.bluezgp.btservice.conf /etc/dbus-1/system.d/.
```
Copy your Bluetooth's chip address:
```
sudo hciconfig hcio
```
...paste it in line 18 and reboot:
```
vi ~/BluezGP/Bluetooth.py
sudo reboot now
```

## Pairing devices
Connect through SSH to your device and run:
```
sudo python ~/BluezGP/Main.py
```
On a new terminal do:
```
sudo bluetoothctl
>agent on
>default-agent
>scan on
>scan off
>discoverable on
```
On your device search for "BT Keyboard" or "BT Gamepad" and connect to it.

Back on bluetoothctl, accept device and trust device
```
>Confirm passkey 291141 (yes/no): yes
>[CHG] Device YOUR_DEVICE_ADDRESS Modalias: bluetooth:v00E0p1200d1436
>...
>trust YOUR_DEVICE_ADDRESS
```
Your device should now be paired and connected.

## Retropie config
This optional config will run the script for you without manually SSH-ing into the Pi.
```
cp ~/BluezGP/retropie/gamepad-mode.sh /home/pi/RetroPie/retropiemenu/
cp ~/BluezGP/retropie/gamepad.png /home/pi/RetroPie/retropiemenu/icons/
```
Add the following entry to the gamelist XML
```
vi /opt/retropie/configs/all/emulationstation/gamelists/retropie/gamelist.xml
```
```
        <game>
                <path>./gamepad-mode.sh</path>
                <name>Gamepad BT Mode</name>
                <desc>Enables a Bluetooth server to use the VMU as a BT Gamepad.</desc>
                <image>/home/pi/RetroPie/retropiemenu/icons/gamepad.png</image>
                <playcount>7</playcount>
                <lastplayed>20190704T182042</lastplayed>
        </game>
```
After rebooting you should see the option in Settings.

## Final notes
If the script finds a device connected to the Pi with the name established in lines 17/25 of Main.py, it'll advertise itself as a Gamepad or it'll show itself as a keyboard.
