import time

from PySide6 import QtCore
import requests


class FrontendThread(QtCore.QThread):
    statusChanged = QtCore.Signal(str)

    def __int__(self):
        pass

    def run(self):
        self.launch_thread()

    def launch_thread(self):
        while True:
            response = requests.get(self.url + "/get_status")

            # Emit the signal to update the status label
            self.statusChanged.emit(response)
            if response.ok and response.json() != "Backend running":
                break
            time.sleep(1)

        self.find_process_ids()
        self.update_progress(100)
