import time
from evdev import *

class Gamepad:
    """docstring for Gamepad"""
    def __init__(self, dev, debug = False):
        self.DEBUG = debug
        # EvCodes comming in from controller
        self.gamepadmap = {}
        #Circuit Gem codes
        self.gamepadmap[105] = (6,0) # KEY_LEFT
        self.gamepadmap[103] = (6,1) # KEY_UP
        self.gamepadmap[106] = (6,2) # KEY_RIGHT
        self.gamepadmap[108] = (6,3) # KEY_DOWN
        self.gamepadmap[31] = (6,4) # KEY_Y
        self.gamepadmap[30] = (6,5) # KEY_X
        self.gamepadmap[44] = (6,6) # KEY_B
        self.gamepadmap[45] = (6,7) # KEY_A
        self.gamepadmap[28] = (7,7) # KEY_START
        self.gamepadmap[01] = (7,6) # KEY_SELECT
        self.gamepadmap[02] = (7,5) # KEY_L
        self.gamepadmap[04] = (7,4) # KEY_R
        # Dreamcast controller codes
        self.gamepadmap[310] = (6,0) # KEY_LEFT
        self.gamepadmap[308] = (6,1) # KEY_UP
        self.gamepadmap[311] = (6,2) # KEY_RIGHT
        self.gamepadmap[309] = (6,3) # KEY_DOWN
        self.gamepadmap[314] = (6,4) # KEY_X
        self.gamepadmap[313] = (6,5) # KEY_Y
        self.gamepadmap[305] = (6,6) # KEY_B
        self.gamepadmap[306] = (6,7) # KEY_A
        self.gamepadmap[307] = (7,7) # KEY_ENTER

        self.axes = {}
        self.axes['ABS_X'] = 2
        self.axes['ABS_Y'] = 3
        self.axes['ABS_RUDDER'] = 4
        self.axes['ABS_THROTTLE'] = 5
        
        self.state = [
            0xA1,	# input report
            0x01,	# usage id (1)
            0x00,       # x axe 
            0x00,       # y axe
            0x00,       # l trigger
            0x00,       # r trigger
            [           # (0-7) buttons
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            [           # (8-15) buttons
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            0x00,0x00,0x00]
            
        self.dev = dev
        print "Controller detected: "+str(self.dev)
            
    def debug(self, message):
        if self.DEBUG:
            print message

    def change_state(self, event):
        if self.gamepadmap.has_key(event.code):
            evdev_byte = self.gamepadmap[event.code][0]
            evdev_bit = self.gamepadmap[event.code][1]
            if event.value == 1:
                self.state[evdev_byte][evdev_bit] = 1
            else:
                self.state[evdev_byte][evdev_bit] = 0

    def handle_axes(self, absevent):
        axe_name = ecodes.bytype[absevent.event.type][absevent.event.code]
        if self.axes.has_key(axe_name):
            state_index = self.axes[axe_name]
            # Ugly fix to account for (0,1) sliders instead of (-1,-1)
            if axe_name == 'ABS_RUDDER':
                self.state[state_index] = int((absevent.event.value - 128) * 2)
            else:
                self.state[state_index] = int(absevent.event.value)

    def event_loop(self,bt):
        for event in self.dev.read_loop():
            self.debug(event)
            #Button presses
            if event.type == ecodes.EV_KEY:
                self.change_state(event)
                bt.sendInput(self.state)
            #Analog stick
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                self.handle_axes(absevent)
                bt.sendInput(self.state)
