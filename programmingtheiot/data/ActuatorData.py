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

class ActuatorData(BaseIotData):
	"""
	Representation of actuator data with support for commands, float values, and state data.
	"""

	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = ""
		self.isResponse = False
	
	def getCommand(self) -> int:
		"""
		Returns the command value.
		
		@return int The command value.
		"""
		return self.command
	
	def getStateData(self) -> str:
		"""
		Returns the state data string.
		
		@return str The state data.
		"""
		return self.stateData
	
	def getValue(self) -> float:
		"""
		Returns the actuator value.
		
		@return float The actuator value.
		"""
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		"""
		Returns whether this is a response message.
		
		@return bool True if this is a response, False otherwise.
		"""
		return self.isResponse
	
	def setCommand(self, command: int):
		"""
		Sets the command value and updates the timestamp.
		
		@param command The command value.
		"""
		self.command = command
		self.updateTimeStamp()
	
	def setAsResponse(self):
		"""
		Marks this as a response message and updates the timestamp.
		"""
		self.isResponse = True
		self.updateTimeStamp()
		
	def setStateData(self, stateData: str):
		"""
		Sets the state data string and updates the timestamp.
		
		@param stateData The state data string.
		"""
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()
	
	def setValue(self, val: float):
		"""
		Sets the actuator value and updates the timestamp.
		
		@param val The actuator value.
		"""
		self.value = val
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		"""
		Updates the values from another ActuatorData instance.
		
		@param data The ActuatorData instance to copy from.
		"""
		if data and isinstance(data, ActuatorData):
			self.command = data.getCommand()
			self.stateData = data.getStateData()
			self.value = data.getValue()
			self.isResponse = data.isResponseFlagEnabled()