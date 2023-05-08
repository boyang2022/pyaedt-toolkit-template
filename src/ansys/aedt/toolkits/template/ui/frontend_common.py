import os
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
import qdarkstyle
import requests


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
        self.log_text.insertPlainText(value)
        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)

    def check_connection(self):
        try:
            response = requests.get(self.url + "/health")
            if response.ok:
                self.write_log_line(f"Backend running: {self.url}")
                return True
        except requests.exceptions.RequestException as e:
            self.write_log_line(f"An error occurred: {e}")
            return False

    def installed_versions(self):
        try:
            response = requests.get(self.url + "/installed_versions")
            if response.ok:
                versions = eval(response.json())
                return versions
        except requests.exceptions.RequestException:
            return False

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

    def on_cancel_clicked(self):
        self.main_window.close()

    def release_only(self, event):
        """Release desktop."""
        self.main_window.close()

    def on_finished(self):
        event = QtGui.QCloseEvent()
        self.closeEvent(event)

    def closeEvent(self, event):
        """Close UI."""
        close = QtWidgets.QMessageBox.question(
            self.main_window,
            "QUIT",
            "Confirm quit?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.main_window.app.quit()
        else:
            event.ignore()

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
    """Message streamer."""

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


class RunnerSignals(QtCore.QObject):
    """Trigger."""

    progressed = QtCore.Signal(int)
    messaged = QtCore.Signal(str)
    completed = QtCore.Signal()
