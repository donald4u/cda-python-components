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

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Manages actuator adapters and processes actuation commands.
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.dataMsgListener = dataMsgListener
		
		self.configUtil = ConfigUtil()
		
		self.useSimulator = \
			self.configUtil.getBoolean(
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.ENABLE_SIMULATOR_KEY)
		self.useEmulator = \
			self.configUtil.getBoolean(
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.ENABLE_EMULATOR_KEY)
		self.deviceID = \
			self.configUtil.getProperty(
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.DEVICE_LOCATION_ID_KEY, 
				defaultVal = ConfigConst.NOT_SET)
		self.locationID = \
			self.configUtil.getProperty(
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.DEVICE_LOCATION_ID_KEY, 
				defaultVal = ConfigConst.NOT_SET)
		
		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None
		
		# Initialize actuator tasks
		self._initEnvironmentalActuationTasks()

	def _initEnvironmentalActuationTasks(self):
		"""
		Initializes the environmental actuator simulator tasks.
		"""
		if not self.useEmulator:
			logging.info("Using simulators for actuator commands.")
			
			# Load the environmental tasks for simulated actuation
			self.humidifierActuator = HumidifierActuatorSimTask()
			
			# Create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()
		else:
			logging.info("Using emulators for actuator commands.")

	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		"""
		Sends an actuator command to the appropriate actuator.
		
		@param data The ActuatorData containing the command.
		@return ActuatorData The response, or None if invalid.
		"""
		if data and not data.isResponseFlagEnabled():
			# First check if the actuation event is destined for this device
			if data.getLocationID() == self.locationID:
				logging.info("Actuator command received for location ID %s. Processing...", str(data.getLocationID()))
				
				aType = data.getTypeID()
				responseData = None
				
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
					responseData = self.hvacActuator.updateActuator(data)
				elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
					responseData = self.ledDisplayActuator.updateActuator(data)
				else:
					logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())
					
				return responseData
			else:
				logging.warning("Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s", str(self.locationID), str(data.getLocationID()))
		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")
		
		return None
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		"""
		Sets the data message listener for actuator responses.
		
		@param listener The IDataMessageListener instance.
		@return bool True if set successfully.
		"""
		if listener:
			self.dataMsgListener = listener
			return True
		return False