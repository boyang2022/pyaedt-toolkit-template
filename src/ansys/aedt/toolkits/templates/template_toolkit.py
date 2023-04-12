# -*- coding: utf-8 -*-
import os
from pathlib import Path
import sys
import json

import ansys.aedt.toolkits.templates.common_ui
from ansys.aedt.toolkits.templates.common_ui import RunnerHfss
from ansys.aedt.toolkits.templates.common_ui import XStream
from ansys.aedt.toolkits.templates.common_ui import active_sessions
from ansys.aedt.toolkits.templates.common_ui import handler
from ansys.aedt.toolkits.templates.common_ui import logger

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
package_path = current_path.parents[3]
sys.path.append(os.path.abspath(package_path))
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from pyaedt import Hfss
from pyaedt.misc import list_installed_ansysem
import qdarkstyle


from ansys.aedt.toolkits.templates.ui.ui_main import Ui_MainWindow

images_path = os.path.join(os.path.dirname(__file__), "ui", "images")
os.environ["QT_API"] = "pyside6"

import logging

handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)


class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, desktop_pid=None, desktop_version=None):
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
        self.setWindowIcon(icon)

        self.menubar.setFont(self._font)
        self.setWindowTitle("PyAEDT Toolkit Template Wizard")
        self.length_unit = ""
        self.create_button = None

        self.release_and_exit_button.clicked.connect(self.release_and_close)
        self.release_button.clicked.connect(self.release_only)
        self.hfss = None
        self.connect_hfss.clicked.connect(self.launch_hfss)
        for ver in list_installed_ansysem():
            ver = "20{}.{}".format(
                ver.replace("ANSYSEM_ROOT", "")[:2], ver.replace("ANSYSEM_ROOT", "")[-1]
            )
            self.aedt_version_combo.addItem(ver)
        self.aedt_version_combo.currentTextChanged.connect(self.find_process_ids)
        self.browse_project.clicked.connect(self.browse_for_project)

        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)
        XStream.stdout().messageWritten.connect(lambda value: self.write_log_line(value))
        XStream.stderr().messageWritten.connect(lambda value: self.write_log_line(value))
        self.find_process_ids()

        if desktop_pid or desktop_version:
            self.launch_hfss(desktop_pid, desktop_version)


    def value_changed(self):
        self.slider_value.setText(str(self.sweep_slider.value()))

    def write_log_line(self, value):
        self.log_text.insertPlainText(value)
        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)

    def update_project(self):
        sel = self.property_table.selectedItems()
        if sel and self.oantenna:
            sel_key = self.property_table.item(self.property_table.row(sel[0]), 0).text()
            key = self.oantenna.synthesis_parameters.__getattribute__(sel_key).hfss_variable
            val = self.property_table.item(self.property_table.row(sel[0]), 1).text()
        else:
            return
        if self.hfss and sel and key in self.hfss.variable_manager.independent_variable_names:
            if self.oantenna.length_unit not in val:
                val = val + self.oantenna.length_unit
            self.hfss[key] = val
            ansys.aedt.toolkits.antennas.common_ui.logger.info(
                "Key {} updated to value {}.".format(key, val)
            )
            self.add_status_bar_message("Project updated.")

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

    def launch_hfss(self, pid=None, version=None):
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
        if self.hfss:
            try:
                self.hfss.release_desktop(False, False)
            except:
                pass
        worker_1 = RunnerHfss()
        worker_1.hfss_args = args
        worker_1.signals.progressed.connect(lambda value: self.update_progress(value))
        worker_1.signals.completed.connect(lambda: self.update_hfss(worker_1))

        self.__thread.start(worker_1)
        pass

    def update_progress(self, value):
        self.progressBar.setValue(value)
        if self.progressBar.isHidden():
            self.progressBar.setVisible(True)

    def update_hfss(self, worker_1):
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
            version = self.aedt_version_combo.currentText()

            self.hfss = Hfss(
                specified_version=version,
                projectname=worker_1.projectname,
                designname=worker_1.designname,
                aedt_process_id=worker_1.pid,
            )
        else:
            self.hfss = worker_1.hfss
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

    def release_only(self):
        """Release Desktop."""
        if self.hfss:
            self.hfss.release_desktop(False, False)
        self.close()

    def release_and_close(self):
        """Release Desktop."""
        if self.hfss:
            self.hfss.release_desktop(True, True)
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
