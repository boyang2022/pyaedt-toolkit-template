import atexit
import json
import os
import signal
import sys
import threading
import time

import psutil
import requests

from ansys.aedt.toolkits.template import backend
from ansys.aedt.toolkits.template import ui

with open(os.path.join(os.path.dirname(__file__), "ui", "common", "general_properties.json")) as fh:
    general_settings = json.load(fh)

url = general_settings["backend_url"]
port = general_settings["backend_port"]
url_call = "http://" + url + ":" + str(port)

is_linux = os.name == "posix"

if is_linux:
    import subprocessdotnet as subprocess
else:
    import subprocess

# Path to Python interpreter with Flask and Pyside6 installed
python_path = sys.executable

# Define the command to start the Flask application
backend_file = os.path.join(backend.__path__[0], "backend.py")
backend_command = [python_path, backend_file]


# Define the command to start the PySide6 UI
frontend_file = os.path.join(ui.__path__[0], "frontend.py")
frontend_command = [python_path, frontend_file]


# Clean up python processes
def clean_python_processes():
    # Terminate all remaining Python processes
    current_process = psutil.Process()
    for process in current_process.children(recursive=True):
        if process.name() == "python.exe" or process.name() == "python":
            process.terminate()


# Define a function to run the subprocess command
def run_command(*command):
    CREATE_NO_WINDOW = 0x08000000
    process = subprocess.Popen(
        " ".join(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=CREATE_NO_WINDOW,
    )
    stdout, stderr = process.communicate()
    print(stdout.decode())
    print(stderr.decode())


# Define the Flask process variable
flask_process = None


# Define a function to terminate the Flask process
def terminate_flask_process():
    if flask_process and flask_process.poll() is None:
        if is_linux:
            os.killpg(os.getpgid(flask_process.pid), signal.SIGTERM)
        else:
            flask_process.terminate()
        flask_process.wait()
        clean_python_processes()


# Create a thread to run the Flask application
flask_thread = threading.Thread(target=run_command, args=backend_command)
flask_thread.daemon = True
flask_thread.start()

# Wait for the Flask application to start
response = requests.get(url_call + "/get_status")
while response.json() != "Backend free":
    time.sleep(1)
    response = requests.get(url_call + "/get_status")

# User can pass the desktop ID and version
if len(sys.argv) == 3:
    desktop_pid = sys.argv[1]
    desktop_version = sys.argv[2]
    properties = {
        "selected_process": int(desktop_pid),
        "aedt_version": desktop_version,
        "use_grpc": False,
    }
    requests.put(url_call + "/set_properties", json=properties)
    requests.post(url_call + "/launch_aedt", json=properties)

    response = requests.get(url_call + "/get_status")
    while response.json() != "Backend free":
        time.sleep(1)
        response = requests.get(url_call + "/get_status")
    requests.put(url_call + "/connect_aedt")


# Create a thread to run the PySide6 UI
ui_thread = threading.Thread(target=run_command, args=frontend_command)
ui_thread.start()


# Wait for the UI thread to complete
ui_thread.join()

# Register the cleanup function to be called on script exit
atexit.register(clean_python_processes)
