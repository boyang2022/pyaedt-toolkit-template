import logging
import os
import sys
import time

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
import qdarkstyle
import requests

logger = logging.getLogger("Global")

# Create a handler and set logging level for the handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

# link handler to logger
logger.addHandler(c_handler)
logging.basicConfig(level=logging.DEBUG)


class ui_common(object):
    def __init__(self, main_window, url):
        self.main_window = main_window
        self.url = url
        self.main_window.setupUi(self.main_window)

        # Load toolkit icon
        self.images_path = os.path.join(os.path.dirname(__file__), "images")
        icon = self._load_icon(self.images_path)
        self.main_window.setWindowIcon(icon)

        # Set font style
        self.set_font(self.main_window)

        # UI Logger
        self.log_text = self.main_window.log_text
        XStream.stdout().messageWritten.connect(lambda value: self.write_log_line(value))
        XStream.stderr().messageWritten.connect(lambda value: self.write_log_line(value))

    def set_title(self, toolkit_title):
        # Toolkit name
        self.main_window.setWindowTitle(toolkit_title)
        return True

    def write_log_line(self, value):
        self.log_text.insertPlainText(value + "\n")
        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)

    def update_progress(self, value):
        self.main_window.progress_bar.setValue(value)
        if self.main_window.progress_bar.isHidden():
            self.main_window.progress_bar.setVisible(True)

    def check_connection(self):
        try:
            count = 0
            response = False
            while not response and count < 2:
                time.sleep(1)
                response = requests.get(self.url + "/health")
                count += 1
            if response.ok:
                self.write_log_line(f"Backend running: {self.url}")
                self.write_log_line(response.json())
                return True
            return False

        except requests.exceptions.RequestException as e:
            logger.error("Backend not running")
            return False

    def installed_versions(self):
        try:
            response = requests.get(self.url + "/installed_versions")
            if response.ok:
                versions = response.json()
                return versions
        except requests.exceptions.RequestException:
            self.write_log_line("Get AEDT installed versions failed")
            return False

    def get_properties(self):
        try:
            response = requests.get(self.url + "/get_properties")
            if response.ok:
                properties = response.json()
                return properties
        except requests.exceptions.RequestException:
            self.write_log_line("Get properties failed")

    def set_properties(self, data):
        try:
            response = requests.put(self.url + "/set_properties", json=data)
            if response.ok:
                response.json()
        except requests.exceptions.RequestException:
            self.write_log_line(f"Set properties failed")

    def browse_for_project(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontConfirmOverwrite, True)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        fileName, _ = dialog.getOpenFileName(
            self.main_window,
            "Open or create new aedt file",
            "",
            "Aedt Files (*.aedt)",
        )
        if fileName:
            self.main_window.project_name.setText(fileName)
            properties = self.get_properties()
            properties["project_name"] = fileName
            self.set_properties(properties)

    def find_process_ids(self):
        self.main_window.process_id_combo.clear()
        self.main_window.process_id_combo.addItem("Create New Session")
        try:
            # Modify selected version
            properties = self.get_properties()
            properties["aedt_version"] = self.main_window.aedt_version_combo.currentText()
            self.set_properties(properties)

            response = requests.get(self.url + "/aedt_sessions")
            if response.ok:
                sessions = response.json()
                for session in sessions:
                    if session[1] == -1:
                        self.main_window.process_id_combo.addItem(
                            "Process {}".format(session[0], session[1])
                        )
                    else:
                        self.main_window.process_id_combo.addItem(
                            "Process {} on Grpc {}".format(session[0], session[1])
                        )
            return True
        except requests.exceptions.RequestException:
            self.write_log_line(f"Find AEDT sessions failed")
            return False

    def launch_aedt(self):
        properties = self.get_properties()
        properties["aedt_version"] = self.main_window.aedt_version_combo.currentText()
        properties["non_graphical"] = True
        if self.main_window.non_graphical_combo.currentText() == "False":
            properties["non_graphical"] = False
        if self.main_window.process_id_combo.currentText() == "Create New Session":
            properties["selected_process"] = 0
        else:
            text_splitted = self.main_window.process_id_combo.currentText().split(" ")
            if len(text_splitted) == 5:
                properties["use_grpc"] = True
                properties["selected_process"] = int(text_splitted[4])
            else:
                properties["use_grpc"] = False
                properties["selected_process"] = int(text_splitted[1])
        self.set_properties(properties)

        self.update_progress(25)
        self.write_log_line("Connecting to AEDT...")
        response = requests.post(self.url + "/launch_aedt", json=properties)
        self.update_progress(50)
        self.write_log_line(response.json())

        if response.ok and self.find_process_ids():
            if properties["project_name"]:
                self.update_progress(75)
                response = requests.put(self.url + "/open_project", json=properties)
                self.write_log_line(response.json())
        else:
            self.write_log_line("Launch AEDT failed")
            return
        self.update_progress(100)

    def release_only(self):
        """Release desktop."""

        properties = {"close_projects": False, "close_on_exit": False}

        response = requests.post(self.url + "/close_aedt", json=properties)
        if response.ok:
            self.main_window.close()

    def release_and_close(self):
        """Release and close desktop."""

        properties = {"close_projects": True, "close_on_exit": True}

        response = requests.post(self.url + "/close_aedt", json=properties)
        if response.ok:
            self.main_window.close()

    def on_cancel_clicked(self):
        self.main_window.close()

    @staticmethod
    def set_font(ui_obj):
        ui_obj._font = QtGui.QFont()
        ui_obj._font.setPointSize(12)
        ui_obj.setFont(ui_obj._font)
        ui_obj.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
        ui_obj.top_menu_bar.setFont(ui_obj._font)

    @staticmethod
    def _load_icon(images_path):
        icon = QtGui.QIcon()
        icon.addFile(
            os.path.join(images_path, "logo_cropped.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        icon.addFile(
            os.path.join(images_path, "logo_cropped.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On,
        )
        return icon


class XStream(QtCore.QObject):
    """User interface message streamer."""

    _stdout = None
    _stderr = None

    messageWritten = QtCore.Signal(str)

    def flush(self):
        """Pass."""
        pass

    def fileno(self):
        """File."""
        return -1

    def write(self, msg):
        """Write a message."""
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        """Info logger."""
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        """Error logger."""
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr
