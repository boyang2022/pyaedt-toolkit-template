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
