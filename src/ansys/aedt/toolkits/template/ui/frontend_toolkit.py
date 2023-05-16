import logging

import requests

from ansys.aedt.toolkits.template.ui.common.frontend_generic import FrontendGeneric
from ansys.aedt.toolkits.template.ui.common.thread_manager import FrontendThread

logger = logging.getLogger("Global")

# Create a handler and set logging level for the handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# link handler to logger
logger.addHandler(c_handler)
logging.basicConfig(level=logging.DEBUG)


class ToolkitFrontend(FrontendGeneric, FrontendThread):
    def __init__(self):
        FrontendThread.__init__(self)
        FrontendGeneric.__init__(self)

    def create_geometry_toolkit(self):
        properties = self.get_properties()
        properties["multiplier"] = float(self.multiplier.text())
        properties["geometry"] = self.geometry_combo.currentText()
        self.set_properties(properties)
        response = requests.get(self.url + "/get_status")

        if self.progress_bar.value() < 100 or (
            response.ok and response.json() == "Backend running"
        ):
            self.write_log_line("Waiting for the previous process to terminate.")
            return

        self.update_progress(0)

        response = requests.post(self.url + "/connect_hfss", json=properties)

        if response.ok:
            response = requests.post(self.url + "/create_geometry")
            if response.ok:
                self.start()
                self.write_log_line("Creating geometry process launched.")
            else:
                self.write_log_line(f"Failed backend call: {self.url}")
                self.update_progress(100)
        else:
            self.write_log_line(response.json())
            self.update_progress(100)
