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

from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
	Humidifier actuator simulator task.
	"""

	def __init__(self):
		super(HumidifierActuatorSimTask, self).__init__(
			name = ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
			typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE,
			simpleName = "HUMIDIFIER")