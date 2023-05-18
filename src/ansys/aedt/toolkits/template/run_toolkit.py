import atexit
import os
import signal
import sys
import threading
import time

import psutil
import requests

from ansys.aedt.toolkits.template import backend
from ansys.aedt.toolkits.template import ui

is_linux = os.name == "posix"

if is_linux:
    import subprocessdotnet as subprocess
else:
    import subprocess

# Path to Python interpreter with Flask and Pyside6 installed
python_path = sys.executable

# Define the command to start the Flask application
backend_file = os.path.join(backend.__path__[0], "run.py")
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
response = requests.get("http://localhost:5000/get_status")
while response.json() != "Backend free":
    time.sleep(1)
    response = requests.get("http://localhost:5000/get_status")

# User or tool could pass the desktop ID and version
if len(sys.argv) == 3:
    desktop_pid = sys.argv[1]
    desktop_version = sys.argv[2]
    properties = {
        "selected_process": int(desktop_pid),
        "aedt_version": desktop_version,
        "use_grpc": False,
    }
    requests.put("http://localhost:5000/set_properties", json=properties)
    requests.post("http://localhost:5000/launch_aedt", json=properties)

    response = requests.get("http://localhost:5000/get_status")
    while response.json() != "Backend free":
        time.sleep(1)
        response = requests.get("http://localhost:5000/get_status")
    requests.put("http://localhost:5000/connect_aedt")

# Create a thread to run the PySide6 UI
ui_thread = threading.Thread(target=run_command, args=frontend_command)
ui_thread.start()


# Wait for the UI thread to complete
ui_thread.join()

# Terminate the Flask process
terminate_flask_process()

# Wait for the Flask thread to complete
flask_thread.join()

# Register the cleanup function to be called on script exit
atexit.register(clean_python_processes)
