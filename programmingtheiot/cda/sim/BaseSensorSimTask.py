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

import logging
import random

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

class BaseSensorSimTask():
	"""
	Base class for simulating sensor tasks with support for random or dataset-based values.
	"""

	DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
	DEFAULT_MAX_VAL = 100.0
	
	def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, dataSet: SensorDataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
		self.dataSet = dataSet
		self.name = name
		self.typeID = typeID
		self.dataSetIndex = 0
		self.useRandomizer = False
		
		self.latestSensorData = None
		
		if not self.dataSet:
			self.useRandomizer = True
			self.minVal = minVal
			self.maxVal = maxVal
	
	def generateTelemetry(self) -> SensorData:
		"""
		Generates sensor telemetry data either from a dataset or randomly.
		
		@return SensorData The generated sensor data.
		"""
		sensorData = SensorData(typeID = self.getTypeID(), name = self.getName())
		sensorVal = ConfigConst.DEFAULT_VAL
		
		if self.useRandomizer:
			sensorVal = random.uniform(self.minVal, self.maxVal)
		else:
			sensorVal = self.dataSet.getDataEntry(index = self.dataSetIndex)
			self.dataSetIndex = self.dataSetIndex + 1
			
			if self.dataSetIndex >= self.dataSet.getDataEntryCount():
				self.dataSetIndex = 0
				
		sensorData.setValue(sensorVal)
		
		self.latestSensorData = sensorData
		
		return self.latestSensorData
	
	def getTelemetryValue(self) -> float:
		"""
		Returns the current telemetry value, generating it if necessary.
		
		@return float The sensor value.
		"""
		if not self.latestSensorData:
			self.generateTelemetry()
		
		return self.latestSensorData.getValue()
	
	def getLatestTelemetry(self) -> SensorData:
		"""
		Returns the latest sensor data.
		
		@return SensorData The latest sensor data instance.
		"""
		return self.latestSensorData
	
	def getName(self) -> str:
		"""
		Returns the name of this sensor task.
		
		@return str The sensor name.
		"""
		return self.name
	
	def getTypeID(self) -> int:
		"""
		Returns the type ID of this sensor.
		
		@return int The sensor type ID.
		"""
		return self.typeID