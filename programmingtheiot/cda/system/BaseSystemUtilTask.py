"""
BaseSystemUtilTask module

This is the base class for all system utility tasks in the CDA project.
"""

import programmingtheiot.common.ConfigConst as ConfigConst

class BaseSystemUtilTask:
    """
    Base class for system utility tasks.
    """

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE):
        """
        Constructor for BaseSystemUtilTask.

        :param name: Name of the task.
        :param typeID: Type ID of the task.
        """
        self.name = name
        self.typeID = typeID

    def getName(self) -> str:
        """
        Getter for the task name.
        """
        return self.name

    def getTypeID(self) -> int:
        """
        Getter for the task type ID.
        """
        return self.typeID

    def getTelemetryValue(self) -> float:
        """
        Template method to get telemetry value.

        Should be implemented by subclasses.
        """
        pass
