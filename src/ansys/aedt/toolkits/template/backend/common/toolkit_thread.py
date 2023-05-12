import logging
import threading

logger = logging.getLogger(__name__)


class ToolkitThread(object):
    def __init__(self):
        pass

    @staticmethod
    def launch_thread(func):
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()

        return wrapper

    @property
    def running_threads(self):
        threads_list = [t for t in threading.enumerate() if type(t) == threading.Thread]
        return threads_list

    # def is_thread_running(self, step_name):
    #     """
    #     check if the thread is running for the specified step and the current project
    #     """
    #     if not global_settings.UseThreads:
    #         return False
    #     thread_name = properties.project_name + "_" + step_name
    #     running_threads_names = [t.name for t in self.running_threads]
    #     if thread_name in running_threads_names:
    #         return True
    #     else:
    #         return False
