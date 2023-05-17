import pyaedt


class RunnerDesktop(object):
    """Open project AEDT.

    Examples
    --------
    >>> from ansys.aedt.toolkits.template.backend.common.service_aedt import RunnerDesktop
    >>> aedt_runner = RunnerDesktop()
    >>> aedt_runner.launch_aedt()
    >>> aedt_runner.release_desktop()

    """

    def __init__(self):
        self.desktop = None

    def launch_aedt(self, version="2023.1", non_graphical=False, selected_process=0, use_grpc=True):
        """Launch AEDT.

        Parameters
        ----------
        version : str, optional
            AEDT version. The default is ``"2023.1"``.
        non_graphical : bool, optional
            AEDT version. The default is ``False``.
        selected_process : int, optional
            AEDT process to connect. The default is ``0``.
        use_grpc : bool, optional
            Use Grpc. The default is ``True``.

        """
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
        """Release AEDT.

        Parameters
        ----------
        close_projects : bool, optional
            Whether to close the AEDT projects that are open in the session.
            The default is ``True``.
        close_on_exit : bool, optional
            Whether to close the active AEDT session on exiting AEDT.
            The default is ``True``.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """

        if self.desktop:
            self.desktop.release_desktop(close_projects, close_on_exit)
            self.desktop = None
            return True
        else:
            return False

    def open_project(self, project_name=None):
        """Open project AEDT.

        Parameters
        ----------
        project_name : str, optional
            Project path to open.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if self.desktop and project_name:
            self.desktop.odesktop.OpenProject(project_name)
            return True
        else:
            return False
