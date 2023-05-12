import logging

import requests

logger = logging.getLogger("Global")

# Create a handler and set logging level for the handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# link handler to logger
logger.addHandler(c_handler)
logging.basicConfig(level=logging.DEBUG)


class ui_toolkit(object):
    def __init__(self, common_frontend, url):
        self.ui_common = common_frontend
        self.url = url

    def create_geometry(self):
        properties = self.ui_common.get_properties()
        properties["multiplier"] = float(self.ui_common.main_window.multiplier.text())
        properties["geometry"] = self.ui_common.main_window.geometry_combo.currentText()
        self.ui_common.set_properties(properties)

        if self.ui_common.main_window.progress_bar.value() < 100:
            self.ui_common.write_log_line("Waiting for the previous process to terminate.")
            return

        self.ui_common.update_progress(0)

        response = requests.post(self.url + "/connect_hfss", json=properties)

        if response.ok:
            self.ui_common.update_progress(50)
            response = requests.post(self.url + "/create_geometry", json=properties)
            self.ui_common.write_log_line(response.json())
            self.ui_common.update_progress(100)
        else:
            self.ui_common.write_log_line(response.json())
            self.ui_common.update_progress(100)
