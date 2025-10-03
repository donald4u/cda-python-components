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

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

class DeviceDataManager(IDataMessageListener):
	"""
	Central data manager for the Constrained Device Application.
	Coordinates all sensor, actuator, and system performance management.
	"""
	
	def __init__(self):
		self.configUtil = ConfigUtil()
		
		self.enableSystemPerf = \
			self.configUtil.getBoolean(
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.ENABLE_SYSTEM_PERF_KEY)
			
		self.enableSensing = \
			self.configUtil.getBoolean(
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.ENABLE_SENSING_KEY)
		
		# NOTE: this can also be retrieved from the configuration file
		self.enableActuation = True
		
		self.sysPerfMgr = None
		self.sensorAdapterMgr = None
		self.actuatorAdapterMgr = None
		
		# Caches for data
		self.actuatorResponseCache = {}
		self.sensorDataCache = {}
		self.systemPerformanceDataCache = {}
		
		# NOTE: The following aren't used until Part III
		self.mqttClient = None
		self.coapClient = None
		
		if self.enableSystemPerf:
			self.sysPerfMgr = SystemPerformanceManager()
			self.sysPerfMgr.setDataMessageListener(self)
			logging.info("Local system performance tracking enabled")
		
		if self.enableSensing:
			self.sensorAdapterMgr = SensorAdapterManager()
			self.sensorAdapterMgr.setDataMessageListener(self)
			logging.info("Local sensor tracking enabled")
			
		if self.enableActuation:
			self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener = self)
			logging.info("Local actuation capabilities enabled")
		
		self.handleTempChangeOnDevice = \
			self.configUtil.getBoolean(
				ConfigConst.CONSTRAINED_DEVICE, 
				ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
			
		self.triggerHvacTempFloor = \
			self.configUtil.getFloat(
				ConfigConst.CONSTRAINED_DEVICE, 
				ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
				
		self.triggerHvacTempCeiling = \
			self.configUtil.getFloat(
				ConfigConst.CONSTRAINED_DEVICE, 
				ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)
		
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		"""
		if name in self.actuatorResponseCache:
			return self.actuatorResponseCache[name]
		return None
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		"""
		if name in self.sensorDataCache:
			return self.sensorDataCache[name]
		return None
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		"""
		if name in self.systemPerformanceDataCache:
			return self.systemPerformanceDataCache[name]
		return None
	
	def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
		"""
		Callback for incoming actuator command messages.
		"""
		logging.info("Actuator data: " + str(data))
		
		if data:
			logging.info("Processing actuator command message.")
			return self.actuatorAdapterMgr.sendActuatorCommand(data)
		else:
			logging.warning("Incoming actuator command is invalid (null). Ignoring.")
			return None
	
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		"""
		Callback for actuator command responses.
		"""
		if data:
			logging.debug("Incoming actuator response received (from actuator manager): " + str(data))
			
			# Store the data in the cache
			self.actuatorResponseCache[data.getName()] = data
			
			# TODO: In Part III, convert to JSON and send upstream
			
			return True
		else:
			logging.warning("Incoming actuator response is invalid (null). Ignoring.")
			return False
	
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		Callback for incoming string-based messages.
		"""
		logging.info("Incoming message received: " + msg)
		
		# TODO: Implement message parsing and handling in Part III
		
		return True
	
	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		Callback for incoming sensor messages.
		"""
		if data:
			logging.debug("Incoming sensor data received (from sensor manager): " + str(data))
			
			# Store in cache
			self.sensorDataCache[data.getName()] = data
			
			# Analyze sensor data
			self._handleSensorDataAnalysis(data = data)
			
			# TODO: In Part III, send upstream
			
			return True
		else:
			logging.warning("Incoming sensor data is invalid (null). Ignoring.")
			return False
	
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		"""
		Callback for incoming system performance messages.
		"""
		if data:
			logging.debug("Incoming system performance message received (from sys perf manager): " + str(data))
			
			# Store in cache
			self.systemPerformanceDataCache[data.getName()] = data
			
			# TODO: In Part III, send upstream
			
			return True
		else:
			logging.warning("Incoming system performance data is invalid (null). Ignoring.")
			return False
	
	def startManager(self):
		"""
		Starts all managed components.
		"""
		logging.info("Starting DeviceDataManager...")
		
		if self.sysPerfMgr:
			self.sysPerfMgr.startManager()
		
		if self.sensorAdapterMgr:
			self.sensorAdapterMgr.startManager()
			
		logging.info("Started DeviceDataManager.")
		
	def stopManager(self):
		"""
		Stops all managed components.
		"""
		logging.info("Stopping DeviceDataManager...")
		
		if self.sysPerfMgr:
			self.sysPerfMgr.stopManager()
		
		if self.sensorAdapterMgr:	
			self.sensorAdapterMgr.stopManager()
			
		logging.info("Stopped DeviceDataManager.")
		
	def _handleIncomingDataAnalysis(self, msg: str):
		"""
		Analyzes incoming messages and takes action if needed.
		"""
		# TODO: Implement in Part III
		pass
		
	def _handleSensorDataAnalysis(self, data: SensorData):
		"""
		Analyzes sensor data and triggers actuator commands if needed.
		"""
		if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
			logging.info("Handle temp change: %s - type ID: %s", str(self.handleTempChangeOnDevice), str(data.getTypeID()))
			
			ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
			ad.setLocationID(data.getLocationID())
			
			if data.getValue() > self.triggerHvacTempCeiling:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempCeiling)
			elif data.getValue() < self.triggerHvacTempFloor:
				ad.setCommand(ConfigConst.COMMAND_ON)
				ad.setValue(self.triggerHvacTempFloor)
			else:
				ad.setCommand(ConfigConst.COMMAND_OFF)
				
			self.handleActuatorCommandMessage(ad)
		
	def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
		"""
		Sends messages upstream to GDA or cloud.
		"""
		# TODO: Implement in Part III
		pass