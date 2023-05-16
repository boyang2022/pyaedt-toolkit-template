from functools import wraps
import logging
import threading
import time

from ansys.aedt.toolkits.template.backend.common.properties import properties

logger = logging.getLogger(__name__)


class ThreadManager(object):
    """Class to control toolkit threads."""

    def __init__(self):
        pass

    @classmethod
    def process_exe(cls, process, *args):
        """Execute process."""
        # process_name = process.__name__

        # set the variable at process start
        properties.is_toolkit_busy = True

        # start
        process(*args)

        # waits for the thread closure
        time.sleep(2)

        # set the variable at process end
        properties.is_toolkit_busy = False

    @classmethod
    def launch_thread(cls, process):
        """Launch process."""

        @wraps(process)
        def inner_function(*args):
            # process_name = process.__name__
            thread_name = "Toolkit_Thread"
            if not properties.is_toolkit_busy:
                logger.debug("Starting thread: {}".format(thread_name))
                running_thread = threading.Thread(
                    target=cls.process_exe,
                    name=thread_name,
                    args=(
                        process,
                        *args,
                    ),
                    daemon=True,
                )
                running_thread.start()
                return True
            else:
                return False

        return inner_function

    @property
    def running_threads(self):
        threads_list = [t for t in threading.enumerate() if type(t) == threading.Thread]
        return threads_list

    def is_thread_running(self):
        """
        Check if the thread is running
        """

        thread_name = "Toolkit_Thread"
        running_threads_names = [t.name for t in self.running_threads]
        if thread_name in running_threads_names:
            return True
        else:
            return False
