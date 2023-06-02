import logging
import os

from PySide6 import QtCore
import requests

logger = logging.getLogger("Global")


class FrontendThread(QtCore.QThread):
    status_changed = QtCore.Signal(bool)
    running = True

    def __int__(self):
        pass

    def run(self):
        while self.running:
            response = requests.get(self.url + "/get_status")
            if response.ok and response.json() != "Backend running":
                self.running = False
                properties = self.get_properties()
                if properties["active_project_name"] and "project_aedt_combo" in self.__dir__():
                    self.project_aedt_combo.clear()
                    cont = 0
                    for project in properties["project_list"]:
                        self.project_aedt_combo.addItem(project)
                        project_name = os.path.splitext(os.path.basename(properties["active_project_name"]))[0]
                        if project_name == project:
                            self.project_aedt_combo.setCurrentIndex(cont)
                        cont += 1

                if properties["active_design_name"] and "design_aedt_combo" in self.__dir__():
                    self.design_aedt_combo.clear()
                    cont = 0
                    design_name = properties["active_design_name"]
                    for design in properties["design_list"]:
                        self.design_aedt_combo.addItem(design)
                        if design_name == design:
                            self.design_aedt_combo.setCurrentIndex(cont)
                        cont += 1

                # Emit the status_changed signal if the status changes
                self.status_changed.emit(self.running)

            # Sleep for a certain amount of time before checking again
            self.msleep(500)
