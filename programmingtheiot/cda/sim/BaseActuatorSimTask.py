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

from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
	"""
	Base class for simulating actuator tasks.
	"""

	def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
		self.latestActuatorResponse = ActuatorData(typeID = typeID, name = name)
		self.latestActuatorResponse.setAsResponse()
		
		self.name = name
		self.typeID = typeID
		self.simpleName = simpleName
		self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
		self.lastKnownValue = ConfigConst.DEFAULT_VAL
		self.lastKnownState = ""
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		"""
		Returns the latest actuator response.
		
		@return ActuatorData The latest actuator response.
		"""
		return self.latestActuatorResponse
	
	def getSimpleName(self) -> str:
		"""
		Returns the simple name of this actuator.
		
		@return str The simple name.
		"""
		return self.simpleName
	
	def updateActuator(self, data: ActuatorData) -> ActuatorData:
		"""
		Updates the actuator based on the command in the ActuatorData.
		
		@param data The ActuatorData containing the command.
		@return ActuatorData The response, or None if invalid.
		"""
		if data and self.typeID == data.getTypeID():
			statusCode = ConfigConst.DEFAULT_STATUS
			
			curCommand = data.getCommand()
			curVal     = data.getValue()
			curState   = data.getStateData()
			
			# check if the command, value and state are repeats from previous
			# if so, ignore the command and return None to caller
			if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue and curState == self.lastKnownState:
				logging.debug(
					"New actuator command, value and state are repeats. Ignoring: %s %s",
					str(curCommand), str(curVal))
			else:
				logging.debug(
					"New actuator command and value to be applied: %s %s",
					str(curCommand), str(curVal))
				
				if curCommand == ConfigConst.COMMAND_ON:
					logging.info("Activating actuator...")
					statusCode = self._activateActuator(val = data.getValue(), stateData = data.getStateData())
				elif curCommand == ConfigConst.COMMAND_OFF:
					logging.info("Deactivating actuator...")
					statusCode = self._deactivateActuator(val = data.getValue(), stateData = data.getStateData())
				else:
					logging.warning("ActuatorData command is unknown. Ignoring: %s", str(curCommand))
					statusCode = -1
				
				# update the last known actuator command and value
				self.lastKnownCommand = curCommand
				self.lastKnownValue = curVal
				self.lastKnownState = curState
				
				# create the ActuatorData response from the original command
				actuatorResponse = ActuatorData()
				actuatorResponse.updateData(data)
				actuatorResponse.setStatusCode(statusCode)
				actuatorResponse.setAsResponse()
				
				self.latestActuatorResponse.updateData(actuatorResponse)
				
				return actuatorResponse
			
		return None
		
	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Simulates activating the actuator (ON command).
		
		@param val The actuation value.
		@param stateData The string state data.
		@return int Status code (0 for success).
		"""
		msg = "\n*******"
		msg = msg + "\n* O N *"
		msg = msg + "\n*******"
		msg = msg + "\n" + self.name + " VALUE -> " + str(val) + "\n======="
			
		logging.info("Simulating %s actuator ON: %s", self.name, msg)
		
		return 0
		
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Simulates deactivating the actuator (OFF command).
		
		@param val The actuation value.
		@param stateData The string state data.
		@return int Status code (0 for success).
		"""
		msg = "\n*******"
		msg = msg + "\n* OFF *"
		msg = msg + "\n*******"
		
		logging.info("Simulating %s actuator OFF: %s", self.name, msg)
				
		return 0