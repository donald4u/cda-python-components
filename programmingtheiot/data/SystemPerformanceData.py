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

class SystemPerformanceData(BaseIotData):
	"""
	Representation of system performance data including CPU and memory utilization.
	"""
	
	def __init__(self, d = None):
		super(SystemPerformanceData, self).__init__(name = ConfigConst.SYSTEM_PERF_MSG, typeID = ConfigConst.SYSTEM_PERF_TYPE, d = d)
		
		self.cpuUtil = ConfigConst.DEFAULT_VAL
		self.memUtil = ConfigConst.DEFAULT_VAL
	
	def getCpuUtilization(self):
		"""
		Returns the CPU utilization value.
		
		@return float The CPU utilization percentage.
		"""
		return self.cpuUtil
	
	def getMemoryUtilization(self):
		"""
		Returns the memory utilization value.
		
		@return float The memory utilization percentage.
		"""
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		"""
		Sets the CPU utilization value and updates the timestamp.
		
		@param cpuUtil The CPU utilization percentage.
		"""
		self.cpuUtil = cpuUtil
		self.updateTimeStamp()
	
	def setMemoryUtilization(self, memUtil):
		"""
		Sets the memory utilization value and updates the timestamp.
		
		@param memUtil The memory utilization percentage.
		"""
		self.memUtil = memUtil
		self.updateTimeStamp()
	
	def _handleUpdateData(self, data):
		"""
		Updates the values from another SystemPerformanceData instance.
		
		@param data The SystemPerformanceData instance to copy from.
		"""
		if data and isinstance(data, SystemPerformanceData):
			self.cpuUtil = data.getCpuUtilization()
			self.memUtil = data.getMemoryUtilization()