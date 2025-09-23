# programmingtheiot/cda/system/DeviceDataManager.py
# Minimal placeholder so ConstrainedDeviceApp can start/stop cleanly.

import logging

class DeviceDataManager:
    def __init__(self):
        logging.info("DeviceDataManager initialized.")
        self._running = False

    def startManager(self):
        logging.info("DeviceDataManager starting...")
        self._running = True
        logging.info("DeviceDataManager started.")

    def stopManager(self):
        logging.info("DeviceDataManager stopping...")
        self._running = False
        logging.info("DeviceDataManager stopped.")
