import logging

from PySide6 import QtCore
import requests

logger = logging.getLogger("Global")

# Create a handler and set logging level for the handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# link handler to logger
logger.addHandler(c_handler)
logging.basicConfig(level=logging.DEBUG)


class FrontendThread(QtCore.QThread):
    status_changed = QtCore.Signal(bool)
    running = True

    def __int__(self):
        pass

    def run(self):
        while self.running:
            response = requests.get(self.url + "/get_status")
            if response.ok and response.json() != "Backend running":
                self.running = False
                # Emit the status_changed signal if the status changes
                self.status_changed.emit(self.running)

            # Sleep for a certain amount of time before checking again
            self.msleep(500)
