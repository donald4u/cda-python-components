#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
	"""
	Representation of sensor data with support for float values.
	"""
		
	def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(SensorData, self).__init__(name = name, typeID = typeID, d = d)
		
		self.value = ConfigConst.DEFAULT_VAL
	
	def getValue(self) -> float:
		"""
		Returns the sensor value.
		
		@return float The current sensor value.
		"""
		return self.value
	
	def setValue(self, newVal: float):
		"""
		Sets the sensor value and updates the timestamp.
		
		@param newVal The new sensor value.
		"""
		self.value = newVal
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
		Updates the value from another SensorData instance.
		
		@param data The SensorData instance to copy from.
		"""
		if data and isinstance(data, SensorData):
			self.value = data.getValue()