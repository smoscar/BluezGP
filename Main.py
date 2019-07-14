from Bluetooth import *
from Gamepad import *
from Keyboard import *
from evdev import *
bt = Bluetooth("/home/pi/BluezGP/sdp_record_gamepad.xml","000508", "BT\ Gamepad")
device = False
i = 0

print 'Looking for connected devices...'
print '--------------------------------'

# Check for connected devices
while True:
    try:
        dev = InputDevice("/dev/input/event"+str(i))
        print "Device found, " + str(dev)
        # Check for USB Controller's identifier
        if "Dreamcast" in str(dev):
            device = False
            bt.listen()
            gp = Gamepad(dev)
            gp.event_loop(bt)
            break
        # Emulated keyboard's identifier
        if "circuitsword" in str(dev):
            device = dev
    except Exception, e:
        #print "Error while reading for devices." 
        break
    i += 1
    
#If all we found was the Circuit gem
if device != False:
    bt.listen()
    kb = Gamepad(device)
    kb.event_loop(bt)
