import logging
import psutil

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemMemUtilTask(BaseSystemUtilTask):
    """
    System memory utilization task.
    """

    def __init__(self):
        super(SystemMemUtilTask, self).__init__(
            name=ConfigConst.MEM_UTIL_NAME, 
            typeID=ConfigConst.MEM_UTIL_TYPE
        )

    def getTelemetryValue(self) -> float:
        """
        Return the current memory utilization as a percentage.
        """
        return psutil.virtual_memory().percent
