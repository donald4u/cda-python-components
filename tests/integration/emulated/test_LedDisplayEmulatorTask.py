import unittest
import logging
import time

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.emulated.LedDisplayEmulatorTask import LedDisplayEmulatorTask

class LedDisplayEmulatorTaskTest(unittest.TestCase):
    
    HELLO_WORLD_A = "Hello, world!"
    HELLO_WORLD_B = "Welcome to Connected Devices!"
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Testing LedDisplayEmulatorTask class [using SenseHAT emulator]...")
        
        self.lddSimTask = LedDisplayEmulatorTask()
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testUpdateEmulator(self):
        ad = ActuatorData(typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setStateData(self.HELLO_WORLD_A)
        
        adr = self.lddSimTask.updateActuator(ad)
        logging.info("ActuatorData: %s", adr)
        
        print(f"\n>>> Message 1: '{self.HELLO_WORLD_A}' - Watch emulator for 30 sec!")
        time.sleep(30)
        
        ad.setStateData(self.HELLO_WORLD_B)
        adr = self.lddSimTask.updateActuator(ad)
        logging.info("ActuatorData: %s", adr)
        
        print(f"\n>>> Message 2: '{self.HELLO_WORLD_B}' - Watch emulator for 30 sec!")
        time.sleep(30)
        
        ad.setCommand(ConfigConst.COMMAND_OFF)
        adr = self.lddSimTask.updateActuator(ad)
        logging.info("ActuatorData: %s", adr)
        
        print("\n>>> Display cleared!")
        time.sleep(5)

if __name__ == "__main__":
    unittest.main()