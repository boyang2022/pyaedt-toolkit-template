# -*- coding: utf-8 -*-
import os
from pathlib import Path
import sys

sys.path.append(str(Path(os.path.dirname(os.path.realpath(__file__))).parents[3]))
from ansys.aedt.toolkits.template.common_ui import RunnerDesktop
from ansys.aedt.toolkits.template.common_ui import XStream
from ansys.aedt.toolkits.template.common_ui import active_sessions
from ansys.aedt.toolkits.template.common_ui import handler
from ansys.aedt.toolkits.template.common_ui import logger

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
package_path = current_path.parents[3]
sys.path.append(os.path.abspath(package_path))
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from pyaedt import Desktop
from pyaedt import Hfss
from pyaedt.misc import list_installed_ansysem
import qdarkstyle

from ansys.aedt.toolkits.template.backend.template_script import TemplateBackend
from ansys.aedt.toolkits.template.ui.ui_main import Ui_MainWindow

images_path = os.path.join(os.path.dirname(__file__), "ui", "images")
os.environ["QT_API"] = "pyside6"

import logging

handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)


class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, desktop_pid=None, desktop_version=None):
        # Initial configuration
        super(ApplicationWindow, self).__init__()
        self.__thread = QtCore.QThreadPool()
        self.__thread.setMaxThreadCount(4)
        self.parameters = {}
        self.setupUi(self)
        self._font = QtGui.QFont()
        self._font.setPointSize(12)
        self.setFont(self._font)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
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

        # Settings configuration

        self.setWindowIcon(icon)
        self.top_menu_bar.setFont(self._font)
        self.setWindowTitle("PyAEDT Toolkit Template Wizard")
        # Close toolkit and release AEDT button
        self.release_and_exit_button.clicked.connect(self.release_and_close)
        # Close toolkit button
        self.release_button.clicked.connect(self.release_only)
        # Detect existing AEDT installation
        for ver in list_installed_ansysem():
            ver = "20{}.{}".format(
                ver.replace("ANSYSEM_ROOT", "")[:2], ver.replace("ANSYSEM_ROOT", "")[-1]
            )
            self.aedt_version_combo.addItem(ver)
        # Find active AEDT sessions
        self.aedt_version_combo.currentTextChanged.connect(self.find_process_ids)
        # Browse AEDT project if needed
        self.browse_project.clicked.connect(self.browse_for_project)
        # Launch AEDT or connect to existing AEDT project
        self.aedtapp = None
        self.connect_aedtapp.clicked.connect(self.launch_aedtapp)
        # Send message to the log
        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)
        XStream.stdout().messageWritten.connect(lambda value: self.write_log_line(value))
        XStream.stderr().messageWritten.connect(lambda value: self.write_log_line(value))
        self.find_process_ids()

        # Design configuration

        # Push button action
        self.create_geometry_buttom.clicked.connect(self.crate_geometry)

        # Push top bar action
        self.action_export_model.triggered.connect(lambda checked: self.export_model())

        # Detect existing AEDT installation
        if desktop_pid or desktop_version:
            self.launch_aedtapp(desktop_pid, desktop_version)

    # General methods

    def write_log_line(self, value):
        self.log_text.insertPlainText(value)
        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)

    def browse_for_project(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontConfirmOverwrite, True)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        fileName, _ = dialog.getOpenFileName(
            self,
            "Open or create new aedt file",
            "",
            "Aedt Files (*.aedt)",
        )
        if fileName:
            self.project_name.setText(fileName)

    def find_process_ids(self):
        self.process_id_combo.clear()
        self.process_id_combo.addItem("Create New Session")
        sessions = active_sessions(version=self.aedt_version_combo.currentText())
        for session in sessions:
            if session[1] == -1:
                self.process_id_combo.addItem("Process {}".format(session[0], session[1]))
            else:
                self.process_id_combo.addItem(
                    "Process {} on Grpc {}".format(session[0], session[1])
                )

    def launch_aedtapp(self, pid=None, version=None):
        non_graphical = eval(self.non_graphical_combo.currentText())
        if version is None:
            version = self.aedt_version_combo.currentText()
        if pid:
            selected_process = "Process {}".format(pid)
        else:
            selected_process = self.process_id_combo.currentText()
        projectname = self.project_name.text()
        process_id_combo_splitted = selected_process.split(" ")
        args = {
            "non_graphical": non_graphical,
            "version": version,
            "selected_process": selected_process,
            "projectname": projectname,
            "process_id_combo_splitted": process_id_combo_splitted,
        }
        if self.aedtapp:
            try:
                self.aedtapp.release_desktop(False, False)
            except:
                pass
        worker_1 = RunnerDesktop()
        worker_1.aedtapp_args = args
        worker_1.signals.progressed.connect(lambda value: self.update_progress(value))
        worker_1.signals.completed.connect(lambda: self.update_aedtapp(worker_1, version))

        self.__thread.start(worker_1)
        pass

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if self.progress_bar.isHidden():
            self.progress_bar.setVisible(True)

    def update_aedtapp(
        self,
        worker_1,
        version=None,
    ):
        if worker_1.pid != -1:
            module = sys.modules["__main__"]
            try:
                del module.COMUtil
            except AttributeError:
                pass
            try:
                del module.oDesktop
            except AttributeError:
                pass
            try:
                del module.pyaedt_initialized
            except AttributeError:
                pass
            try:
                del module.oAnsoftApplication
            except AttributeError:
                pass
            if version is None:
                version = self.aedt_version_combo.currentText()

            self.aedtapp = Desktop(
                specified_version=version,
                aedt_process_id=worker_1.pid,
                new_desktop_session=False,
            )
        else:
            self.aedtapp = worker_1.aedtapp
        self.update_progress(100)

    def add_status_bar_message(self, message):
        """Add a status bar message.

        Parameters
        ----------
        message : str

        """
        myStatus = QtWidgets.QStatusBar()
        myStatus.showMessage(message, 3000000)
        self.setStatusBar(myStatus)

    def add_image(self, image_path):
        """Add the image to antenna settings."""
        line_0 = QtWidgets.QHBoxLayout()
        line_0.setObjectName("line_0")

        line_0_spacer = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )

        line_0.addItem(line_0_spacer)

        antenna_image = QtWidgets.QLabel()
        antenna_image.setObjectName("image")

        antenna_image.setMaximumHeight(self.centralwidget.height() / 3)
        antenna_image.setScaledContents(True)
        _pixmap = QtGui.QPixmap(image_path)
        _pixmap = _pixmap.scaled(
            antenna_image.width(),
            antenna_image.height(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        antenna_image.setPixmap(_pixmap)

        line_0.addWidget(antenna_image)

        line_0_spacer = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        line_0.addItem(line_0_spacer)
        return line_0

    def add_header(self, image_name):
        top_spacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )

        self.layout_settings.addItem(top_spacer, 2, 0, 1, 1)

        image = self.add_image(os.path.join(images_path, image_name))
        self.layout_settings.addLayout(image, 0, 0, 1, 1)

    def release_only(self):
        """Release desktop."""
        if self.aedtapp:
            self.aedtapp.release_desktop(False, False)
        self.close()

    def release_and_close(self):
        """Release and close desktop."""
        if self.aedtapp:
            self.aedtapp.release_desktop(True, True)
        self.close()

    def closeEvent(self, event):
        """Close UI."""
        close = QtWidgets.QMessageBox.question(
            self, "QUIT", "Confirm quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            app.quit()
        else:
            event.ignore()

    # Toolkit specific methods

    def crate_geometry(self):
        """Create a box or sphere in a random position."""
        if self.progress_bar.value() < 100:
            self.add_status_bar_message("Waiting for the previous process to terminate.")
            return
        self.progress_bar.setValue(0)
        if isinstance(self.aedtapp, type(Desktop())):
            if not self.aedtapp.design_list():
                # If no design exist then create a new HFSS design
                self.add_status_bar_message("Adding an HFSS design to the project.")
                self.aedtapp = Hfss(
                    specified_version=self.aedtapp.aedt_version_id,
                    aedt_process_id=self.aedtapp.aedt_process_id,
                    new_desktop_session=False,
                )
            else:
                oproject = self.aedtapp.odesktop.GetActiveProject()
                projectname = oproject.GetName()
                activedesign = oproject.GetActiveDesign().GetName()
                self.aedtapp = self.aedtapp[[projectname, activedesign]]

        multiplier = self.multiplier.text()
        if not multiplier.isdigit():
            multiplier = 1.0

        app = TemplateBackend(self.aedtapp, multiplier=float(multiplier))
        if self.geometry_combo.currentText() == "Box":
            comp = app.draw_box()
        else:
            comp = app.draw_sphere()
        self.write_log_line("Component {} added.".format(comp.name))
        self.update_progress(100)

    def export_model(self):
        """Export picture and show in the UI."""
        if self.progress_bar.value() < 100:
            self.add_status_bar_message("Waiting for the previous process to terminate.")
            return
        self.progress_bar.setValue(0)

        if isinstance(self.aedtapp, type(Desktop())):
            if not self.aedtapp.design_list():
                # If no design exist then create a new HFSS design
                self.add_status_bar_message("Adding an HFSS design to the project.")
                self.aedtapp = Hfss(
                    specified_version=self.aedtapp.aedt_version_id,
                    aedt_process_id=self.aedtapp.aedt_process_id,
                    new_desktop_session=False,
                )
            else:
                oproject = self.aedtapp.odesktop.GetActiveProject()
                projectname = oproject.GetName()
                activedesign = oproject.GetActiveDesign().GetName()
                self.aedtapp = self.aedtapp[[projectname, activedesign]]
        # Export picture
        path = os.path.join(self.aedtapp.working_directory, "picture.png")
        self.aedtapp.plot(show=False, export_path=path)

        w = self.picture.geometry().width()
        h = self.picture.geometry().height()

        self.picture.setFixedSize(w, h)
        pixmap = QtGui.QPixmap(path)
        pixmap = pixmap.scaled(w, h)
        self.picture.setPixmap(pixmap)
        self.picture.resize(w, h)

        self.update_progress(100)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    desktop_pid = None
    desktop_version = None
    if len(sys.argv) > 2:
        desktop_pid = sys.argv[1]
        desktop_version = sys.argv[2]
    w = ApplicationWindow(desktop_pid, desktop_version)
    w.show()
    sys.exit(app.exec())
