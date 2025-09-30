import logging
from apscheduler.schedulers.background import BackgroundScheduler
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

class SystemPerformanceManager:
    def __init__(self):
        configUtil = ConfigUtil()
        
        # Polling rate for telemetry collection
        self.pollRate = configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES
        )
        
        # Device location ID
        self.locationID = configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET
        )
        
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
        
        # Placeholder for data message listener
        self.dataMsgListener = None
        
        # APScheduler setup
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        
        # CPU and memory utilization tasks
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()

    # Setter for data message listener
    def setDataMessageListener(self, listener):
        self.dataMsgListener = listener

    # Telemetry handling method
    def handleTelemetry(self):
        cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        memUtilPct = self.memUtilTask.getTelemetryValue()
        
        logging.debug(
            'CPU utilization is %s percent, and memory utilization is %s percent.',
            str(cpuUtilPct), str(memUtilPct)
        )

    # Start the performance manager
    def startManager(self):
        logging.info("Starting SystemPerformanceManager...")
        
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Started SystemPerformanceManager.")
        else:
            logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")

    # Stop the performance manager
    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager...")
        
        try:
            self.scheduler.shutdown()
            logging.info("Stopped SystemPerformanceManager.")
        except:
            logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")
