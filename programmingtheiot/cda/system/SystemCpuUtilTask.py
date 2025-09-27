#####
# This class is part of the Programming the Internet of Things project.
#####

import logging
import psutil

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemCpuUtilTask(BaseSystemUtilTask):
    """
    CPU Utilization task for ConstrainedDeviceApp.
    """

    def __init__(self):
        super().__init__()
        logging.info("SystemCpuUtilTask initialized.")

    def getSystemData(self):
        """
        Returns CPU utilization as a dictionary.
        """
        return {"cpu_percent": psutil.cpu_percent(interval=1)}
