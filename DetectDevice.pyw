import winreg
import time
from datetime import datetime
from pymata4 import pymata4


class DeviceDetect:

    def __init__(self):
        self.REG_KEY = winreg.HKEY_CURRENT_USER

        self.DIGITAL_PINS = {5,7} # 2,3, 5,6, 8,9
        self.ACTIVE_PINS = set()
        # self.ACTIVE_HOURS = {8,9,10,11,12,13,14,15,16,17,18,19}

        self.board = pymata4.Pymata4()

        for i in self.DIGITAL_PINS:
            self.board.set_pin_mode_digital_output(i)

        self.devices = {
            "microphone": {
                "cfg": self.getConf("microphone"),
                "status": False,
                "pins": {5}
            },
            "webcam": {
                "cfg": self.getConf("webcam"),
                "status": False,
                "pins": {7}
            }
        }
        self.TIMESTAMP_VALUE_NAME = "LastUsedTimeStop"

        while True:
            self.detect()

    def getConf(self, device):
        REG_SUBKEY = f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\{device}\\NonPackaged"
        return {
            "_regKey": winreg.OpenKey( self.REG_KEY, REG_SUBKEY ),
            "REG_SUBKEY": REG_SUBKEY
        }

    def getActiveApps(self, device):
        activeApps = []
        _regKey = self.devices[device]["cfg"]["_regKey"]
        REG_SUBKEY = self.devices[device]["cfg"]['REG_SUBKEY']
        # Enumerate over the subkeys of the webcam key
        subkeyCnt, valueCnt, lastModified = winreg.QueryInfoKey( _regKey )
        for idx in range(subkeyCnt):
            subkeyName = winreg.EnumKey( _regKey, idx )
            subkeyFullName = f"{REG_SUBKEY}\\{subkeyName}"

            # Open each subkey and check the 'stopped' timestamp value. A value of 0 implies the camera is in use.
            subkey = winreg.OpenKey( self.REG_KEY, subkeyFullName )
            stoppedTimestamp, _ = winreg.QueryValueEx( subkey, self.TIMESTAMP_VALUE_NAME )
            if 0 == stoppedTimestamp:
                activeApps.append( subkeyName.replace("#", "/" ) )

        return activeApps

    def isActive(self, device):
        return len(self.getActiveApps(device)) > 0

    def setStatus(self):
        for device in self.devices:
            self.devices[device]["status"] = self.isActive(device)

    def digitalOutput(self, pins):
        if pins == self.ACTIVE_PINS:
            pass
        else:
            for pin in self.ACTIVE_PINS:
                self.board.digital_pin_write(pin, 0)
            for pin in pins:
                self.board.digital_pin_write(pin, 1)
        self.ACTIVE_PINS = pins.copy()

    def detect(self):
        pin_set = {}
        self.setStatus()

        if self.devices["webcam"]["status"]:
                pin_set = self.devices["webcam"]["pins"]
        elif self.devices["microphone"]["status"]:
                pin_set = self.devices["microphone"]["pins"]
        # elif datetime.now().hour not in self.ACTIVE_HOURS:
        #     pin_set = {}

        self.digitalOutput(pin_set)
        time.sleep(0.5)

if __name__ == "__main__":
    detect = DeviceDetect()