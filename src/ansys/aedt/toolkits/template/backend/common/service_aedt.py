import pyaedt


class RunnerDesktop(object):
    def __init__(self):
        self.desktop = None

    def launch_aedt(self, version="2023.1", non_graphical=False, selected_process=0, use_grpc=True):
        try:
            pyaedt.settings.use_grpc_api = use_grpc
            if selected_process == 0:  # pragma: no cover
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    new_desktop_session=True,
                )
            elif use_grpc:
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    port=selected_process,
                    new_desktop_session=False,
                )
            else:  # pragma: no cover
                self.desktop = pyaedt.Desktop(
                    specified_version=version,
                    non_graphical=non_graphical,
                    aedt_process_id=selected_process,
                    new_desktop_session=False,
                )
        except:  # pragma: no cover
            self.desktop = None

    def release_desktop(self, close_projects=False, close_on_exit=False):
        if self.desktop:
            self.desktop.release_desktop(close_projects, close_on_exit)
            self.desktop = None
            return True
        else:
            return False

    def open_project(self, project_name=None):
        if self.desktop and project_name:
            self.desktop.odesktop.OpenProject(project_name)
        else:
            return False
