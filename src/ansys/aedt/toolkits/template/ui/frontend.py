import logging
import os
import sys

from PySide6 import QtWidgets

from ansys.aedt.toolkits.template.ui.common.frontend_ui import Ui_MainWindow
from ansys.aedt.toolkits.template.ui.frontend_toolkit import ToolkitFrontend

logger = logging.getLogger("Global")

# Create a handler and set logging level for the handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# link handler to logger
logger.addHandler(c_handler)
logging.basicConfig(level=logging.DEBUG)


os.environ["QT_API"] = "pyside6"

# User inputs
toolkit_title = "PyAEDT Toolkit Template Wizard"

if len(sys.argv) != 2:
    url = "http://127.0.0.1"
    port = "5000"
else:
    url = sys.argv[0]
    port = sys.argv[1]


class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow, ToolkitFrontend):
    def __init__(self):
        # Initial configuration
        super(ApplicationWindow, self).__init__()
        ToolkitFrontend.__init__(self)

        self.url = url + ":" + port

        # Set title
        self.set_title(toolkit_title)

        # Check backend connection
        self.backend = self.check_connection()

        if not self.backend:
            raise "Backend not running"

        # General Settings

        # Update toolkit running flag
        self.toolkit_running_led.setStyleSheet(
            "text-align: center; qproperty-alignment: 'AlignCenter';"
        )

        if self.backend_busy():
            self.toolkit_running_led.setText("Toolkit busy")
            self.toolkit_running_led.adjustSize()
            self.toolkit_running_led.setStyleSheet("background-color: red;")
        else:
            self.toolkit_running_led.setText("")
            self.toolkit_running_led.adjustSize()
            self.toolkit_running_led.setStyleSheet("background-color: green;")

        # Get default properties
        default_properties = self.get_properties()

        # Get AEDT installed versions
        installed_versions = self.installed_versions()

        # Add versions to the UI
        if installed_versions:
            for ver in installed_versions:
                self.aedt_version_combo.addItem(ver)
        elif self.backend:
            self.aedt_version_combo.addItem("AEDT not installed")

        if (
            "aedt_version" in default_properties.keys()
            and default_properties["aedt_version"] in installed_versions
        ):
            self.aedt_version_combo.setCurrentText(default_properties["aedt_version"])
            self.find_process_ids()

        # Add default properties
        self.non_graphical_combo.setCurrentText(str(default_properties["non_graphical"]))
        self.numcores.setText(str(default_properties["core_number"]))

        # Thread signal
        self.status_changed.connect(self.change_thread_status)

        # Select AEDT project
        self.browse_project.clicked.connect(self.browse_for_project)

        # Close toolkit button
        self.release_button.clicked.connect(self.release_only)

        # Close toolkit and AEDT button
        self.release_and_exit_button.clicked.connect(self.release_and_close)

        # Find active AEDT sessions
        self.aedt_version_combo.currentTextChanged.connect(self.find_process_ids)

        # Launch AEDT
        self.connect_aedtapp.clicked.connect(self.launch_aedt)

        # Toolkit Settings

        # Create geometry
        self.create_geometry_buttom.clicked.connect(self.create_geometry_toolkit)

        # Save project
        self.action_save_project.triggered.connect(lambda checked: self.save_project())

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(
            self, "QUIT", "Confirm quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
