from evdev import *
import keymap
from Bluetooth import *
class Keyboard:
    def __init__(self, dev, debug = False):
        self.DEBUG = debug
        self.state = [
            0xA1,
            0x01,
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00
        ]
        self.dev = dev
        print "VMU detected: "+str(self.dev)

    def debug(self, message):
        if self.DEBUG:
            print message

    def change_state(self,event):
        evdev_code = ecodes.KEY[event.code]
        modkey_element = keymap.modkey(evdev_code)
        if modkey_element > 0:
            if self.state[2][modkey_element] == 0:
                self.state[2][modkey_element] = 1
            else:
                self.state[2][modkey_element] = 0
        else:
            hex_key = keymap.convert(evdev_code)
            for i in range(4,10):
                if self.state[i] == hex_key and event.value == 0:
                    self.state[i] = 0x00
                elif self.state[i] == 0x00 and event.value == 1:
                    self.state[i] = hex_key
                break
    def event_loop(self,bt):
        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value < 2:
                self.change_state(event)
                self.debug(self.state)
                bt.sendInput(self.state)
