from bluetooth import *
from BluezProfile import *
import dbus
import dbus.service
import dbus.mainloop.glib
import sys
import os

from dbus.mainloop.glib import DBusGMainLoop

class Bluetooth(dbus.service.Object):
    """docstring for Gamepad"""
    HOST = 0
    PORT = 1
    P_CTRL = 17
    P_INTR = 19
    UUID = "1f16e7c0-b59b-11e3-95d2-0002a5d5c51b"
    ADDRESS = "B8:27:EB:5C:C9:33"
    def __init__(self, sdp, classname, devname, debug = False):
        self.DEBUG = debug
        
        # Set up as a DBus service
        DBusGMainLoop(set_as_default=True)
        self.bus_name = dbus.service.BusName("org.bluezgp.btservice",bus=dbus.SystemBus())
        dbus.service.Object.__init__(self,self.bus_name,"/org/bluezgp/btservice")
        
        # Inits device
        self.classname = classname
        self.devname = devname
        os.system("sudo hciconfig hci0 class "+self.classname)
        os.system("sudo hciconfig hci0 name "+self.devname)
        os.system("sudo hciconfig hci0 lm master")
        os.system("sudo hciconfig hci0 piscan")
        
        # Inits profile
        try:
            fh = open(sdp,"r")
        except Exception, e:
            sys.exit("Cannot open sdp_record file, " + str(e))

        self.service_record = fh.read()
        opts = {
            "ServiceRecord":self.service_record,
            "Role":"server",
            "RequireAuthentication":False,
            "RequireAuthorization":False
        }
        
        # Gets proxy for the bluez interface
        self.bus = dbus.SystemBus()
        self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")
        
        self.profile = BluezProfile(self.bus, "/bluez/bluezgp/bt_profile")
        self.manager.RegisterProfile("/bluez/bluezgp/bt_profile", self.UUID, opts)
        
        fh.close()
        
    def debug(self, message):
        if self.DEBUG:
            print message

    def listen(self):
        try:
            self.soccontrol = BluetoothSocket(L2CAP)
            self.sockinter = BluetoothSocket(L2CAP)

            self.soccontrol.bind((Bluetooth.ADDRESS, Bluetooth.P_CTRL))
            self.sockinter.bind((Bluetooth.ADDRESS, Bluetooth.P_INTR))
            
            self.soccontrol.listen(1)
            self.sockinter.listen(1)
            print "waiting for connection"
            self.ccontrol, self.cinfo = self.soccontrol.accept()
            print "Control channel connected to "+self.cinfo[Bluetooth.HOST]
            self.cinter, self.cinfo = self.sockinter.accept()
            print "Interrupt channel connected to "+self.cinfo[Bluetooth.HOST]
            print "\n                        MMM\n                        MMMMMM\n                        MMM  MM\n                 MMM    MMM   MMM               MMM\n                   MMM  MMM  MMMM              MMM\n                     MMMMMMMMMM               MMM\n                       MMMMMM        MM      MMM\n                       MMMMMM         MMM  MMM\n                     MMMMMMMMMM         MMMM\n                   MMM  MMM  MMMM        MM\n                 MMM    MMM   MMM\n                        MMM  MMM\n                        MMMMMM\n                        MMM\n"
        except Exception, e:
            sys.exit("Cannot listen to bluetooth, " + str(e))
    
    #@dbus.service.method('org.bluezgp.btservice', in_signature='yay')
    def sendInput(self, inp):
        str_inp = ""
        self.debug(inp)
        for elem in inp:
            if type(elem) is list:
                tmp_str = ""
                for tmp_elem in elem:
                    tmp_str += str(tmp_elem)
                for i in range(0,len(tmp_str)/8):
                    if((i+1)*8 >= len(tmp_str)):
                        str_inp += chr(int(tmp_str[i*8:],2))
                        #self.debug(tmp_str[i*8:] + ' -> ' + str(int(tmp_str[i*8:],2)))
                    else:
                        str_inp += chr(int(tmp_str[i*8:(i+1)*8],2))
                        #self.debug(tmp_str[i*8:(i+1)*8] + ' -> ' + str(int(tmp_str[i*8:(i+1)*8],2)))
            else:
                str_inp += chr(elem)

        self.cinter.send(str_inp)
