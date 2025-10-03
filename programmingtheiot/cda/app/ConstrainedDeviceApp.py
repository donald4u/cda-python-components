import argparse
import logging
import traceback
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.DEBUG
)

class ConstrainedDeviceApp:
    """
    Definition of the ConstrainedDeviceApp class.
    """

    def __init__(self):
        """
        Initialization of class.
        """
        logging.info("Initializing CDA...")

        # Initialize DeviceDataManager
        self.devDataMgr = DeviceDataManager()
        self.isStarted = False

    def isAppStarted(self) -> bool:
        return self.isStarted

    def startApp(self):
        """
        Start the CDA and the DeviceDataManager.
        """
        logging.info("Starting CDA...")

        # Start device data manager
        self.devDataMgr.startManager()

        self.isStarted = True
        logging.info("CDA started.")

    def stopApp(self, code: int = 0):
        """
        Stop the CDA and the DeviceDataManager.
        """
        logging.info("CDA stopping...")

        # Stop device data manager
        self.devDataMgr.stopManager()

        self.isStarted = False
        logging.info("CDA stopped with exit code %s.", str(code))


def main():
    """
    Main function for running CDA as a standalone app.
    """
    argParser = argparse.ArgumentParser(
        description='CDA used for generating telemetry - Programming the IoT.'
    )
    argParser.add_argument('-c', '--configFile', help='Optional custom configuration file for the CDA.')

    configFile = None
    try:
        args = argParser.parse_args()
        configFile = args.configFile
        logging.info('Parsed configuration file arg: %s', configFile)
    except:
        logging.info('No arguments to parse.')

    # Initialize ConfigUtil
    configUtil = ConfigUtil(configFile)
    cda = None

    try:
        # Initialize CDA
        cda = ConstrainedDeviceApp()

        # Start CDA
        cda.startApp()

        # Check if CDA should run forever
        runForever = configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)
        if runForever:
            while True:
                sleep(5)
        else:
            if cda.isAppStarted():
                sleep(65)
                cda.stopApp(0)

    except KeyboardInterrupt:
        logging.warning('Keyboard interruption for CDA. Exiting.')
        if cda:
            cda.stopApp(-1)

    except Exception as e:
        logging.error('Startup exception caused CDA to fail. Exiting.')
        traceback.print_exception(type(e), e, e.__traceback__)
        if cda:
            cda.stopApp(-2)

    logging.info('Exiting CDA.')
    exit()


if __name__ == '__main__':
    main()