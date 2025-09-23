import argparse
import logging
import traceback
from time import sleep

from programmingtheiot.common.ConfigConst import DEFAULT_CONFIG_FILE_NAME
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.system.DeviceDataManager import DeviceDataManager


logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.DEBUG
)

class ConstrainedDeviceApp:
    """
    CDA main application class.
    """

    def __init__(self):
        logging.info("Initializing CDA...")
        self.ddm = DeviceDataManager()
        self.isStarted = False

    def isAppStarted(self) -> bool:
        return self.isStarted

    def startApp(self):
        logging.info("Starting CDA...")
        self.ddm.startManager()
        self.isStarted = True
        logging.info("CDA started.")

    def stopApp(self, code: int):
        logging.info("CDA stopping...")
        self.ddm.stopManager()
        self.isStarted = False
        logging.info("CDA stopped with exit code %s.", str(code))


def main():
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

    configUtil = ConfigUtil(configFile or DEFAULT_CONFIG_FILE_NAME)
    cda = None

    try:
        cda = ConstrainedDeviceApp()
        cda.startApp()

        runForever = configUtil.getBoolean('ConstrainedDevice', 'runForever')

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
