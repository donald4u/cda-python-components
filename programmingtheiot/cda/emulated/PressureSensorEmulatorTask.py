#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from pisense import SenseHAT

class PressureSensorEmulatorTask(BaseSensorSimTask):
    """
    Pressure sensor emulator using SenseHAT.
    """
    
    def __init__(self, dataSet=None):
        super(PressureSensorEmulatorTask, self).__init__(
            name=ConfigConst.PRESSURE_SENSOR_NAME,
            typeID=ConfigConst.PRESSURE_SENSOR_TYPE
        )
        
        self.sh = SenseHAT(emulate=True)
    
    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(name=self.getName(), typeID=self.getTypeID())
        sensorVal = self.sh.environ.pressure
        
        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData
        
        return sensorData