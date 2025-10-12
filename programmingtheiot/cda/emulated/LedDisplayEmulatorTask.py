#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from sense_emu import SenseHat

class LedDisplayEmulatorTask(BaseActuatorSimTask):
    """
    LED Display Emulator Task using SenseHAT.
    """

    def __init__(self):
        super(LedDisplayEmulatorTask, self).__init__(
            name=ConfigConst.NOT_SET,
            typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE
        )
        
        self.sh = SenseHat()
        logging.info("LED Display Emulator initialized.")

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        if stateData:
            msg = str(stateData)
            logging.info(f"LED Display: Showing message: {msg}")
            print(f"LED MESSAGE: {msg}")
            
            self.sh.show_message(msg, scroll_speed=0.05, text_colour=[255, 0, 0])
        return 0

    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        logging.info("LED Display: Cleared")
        print("LED DISPLAY CLEARED")
        self.sh.clear()
        return 0