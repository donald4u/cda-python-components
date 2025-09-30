"""
SystemCpuUtilTask module

This class extends BaseSystemUtilTask and provides CPU utilization telemetry.
"""

import logging
import psutil

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemCpuUtilTask(BaseSystemUtilTask):
    """
    System CPU utilization task class.
    """

    def __init__(self):
        """
        Constructor for SystemCpuUtilTask.
        Initializes the task with the name and type defined in ConfigConst.
        """
        super(SystemCpuUtilTask, self).__init__(
            name=ConfigConst.CPU_UTIL_NAME,
            typeID=ConfigConst.CPU_UTIL_TYPE
        )
        logging.info(f"Initialized SystemCpuUtilTask with name: {self.name}, typeID: {self.typeID}")

    def getTelemetryValue(self) -> float:
        """
        Returns the current CPU utilization percentage.
        """
        cpu_percent = psutil.cpu_percent()
        logging.debug(f"CPU Utilization: {cpu_percent}%")
        return cpu_percent
