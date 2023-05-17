import logging

from PySide6 import QtWidgets
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


class ToolkitFrontend(FrontendThread, FrontendGeneric):
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
            self.write_log_line("Please wait, toolkit running")
            return

        self.update_progress(0)

        response = requests.post(self.url + "/connect_hfss", json=properties)

        if response.ok:
            response = requests.post(self.url + "/create_geometry")
            if response.ok:
                self.update_progress(50)
                self.toolkit_running_led.setText("Toolkit busy")
                self.toolkit_running_led.adjustSize()
                self.toolkit_running_led.setStyleSheet("background-color: red;")

                # Start the thread
                self.running = True
                self.start()
                self.write_log_line("Creating geometry process launched")
            else:
                self.write_log_line(f"Failed backend call: {self.url}")
                self.update_progress(100)
        else:
            self.write_log_line(response.json())
            self.update_progress(100)

    def save_project(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontConfirmOverwrite, True)
        file_name, _ = dialog.getSaveFileName(
            self,
            "Save new aedt file",
            "",
            "Aedt Files (*.aedt)",
        )

        if file_name:
            self.project_name.setText(file_name)
            properties = self.get_properties()
            properties["new_project_name"] = file_name
            self.set_properties(properties)
            self.update_progress(0)

            response = requests.post(self.url + "/connect_hfss", json=properties)

            if response.ok and response.json() != "Toolkit not connected to AEDT":
                response = requests.post(self.url + "/save_project", json=properties)
                if response.ok:
                    self.update_progress(50)
                    self.toolkit_running_led.setText("Toolkit busy")
                    self.toolkit_running_led.adjustSize()
                    self.toolkit_running_led.setStyleSheet("background-color: red;")

                    # Start the thread
                    self.running = True
                    self.start()
                    self.write_log_line("Saving project process launched")
                else:
                    self.write_log_line(f"Failed backend call: {self.url}")
                    self.update_progress(100)
            else:
                self.write_log_line(response.json())
                self.update_progress(100)
