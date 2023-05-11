import os
import sys

from PySide6 import QtWidgets
import frontend_generic

from ansys.aedt.toolkits.template.ui.common.frontend_ui import Ui_MainWindow

os.environ["QT_API"] = "pyside6"

# User inputs
toolkit_title = "PyAEDT Toolkit Template Wizard"

if len(sys.argv) != 2:
    url = "http://127.0.0.1"
    port = "5000"
else:
    url = sys.argv[0]
    port = sys.argv[1]


class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Initial configuration
        super(ApplicationWindow, self).__init__()

        # UI init
        self.ui_obj = frontend_generic.ui_common(self, url + ":" + port)

        # Set title
        self.ui_obj.set_title(toolkit_title)

        # Check backend connection
        self.backend = self.ui_obj.check_connection()

        if not self.backend:
            raise "Backend not running"

        # General Settings

        # Get default properties
        default_properties = self.ui_obj.get_properties()

        # Get AEDT installed versions
        installed_versions = self.ui_obj.installed_versions()

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
            self.ui_obj.find_process_ids()

        # Select AEDT project
        self.browse_project.clicked.connect(self.ui_obj.browse_for_project)

        # Close toolkit button
        self.release_button.clicked.connect(self.ui_obj.release_only)

        # Close toolkit and AEDT button
        self.release_and_exit_button.clicked.connect(self.ui_obj.release_and_close)

        # Find active AEDT sessions
        self.aedt_version_combo.currentTextChanged.connect(self.ui_obj.find_process_ids)

        # Launch AEDT
        self.connect_aedtapp.clicked.connect(self.ui_obj.launch_aedt)

        # Toolkit Settings

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(
            self, "QUIT", "Confirm quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.ui_obj.release_only()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
