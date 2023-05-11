import os
import signal
import sys
import threading

import psutil

is_linux = os.name == "posix"
script_name = os.path.splitext(os.path.basename(__file__))[0]

if is_linux:
    import subprocessdotnet as subprocess
else:
    import subprocess

# User or tool could pass the desktop ID and version
desktop_pid = None
desktop_version = None
if len(sys.argv) == 2:
    desktop_pid = sys.argv[1]
    desktop_version = sys.argv[2]

# Path to Python interpreter with Flask and Pyside6 installed
python_path = sys.executable

# Define the command to start the Flask application
backend_command = [python_path, "backend\\backend.py"]

# Define the command to start the PySide6 UI
frontend_command = [python_path, "ui\\frontend.py"]


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


# Create a thread to run the Flask application
flask_thread = threading.Thread(target=run_command, args=backend_command)
flask_thread.daemon = True
flask_thread.start()

# Create a thread to run the PySide6 UI
ui_thread = threading.Thread(target=run_command, args=frontend_command)
ui_thread.start()


# Wait for the UI thread to complete
ui_thread.join()

# Terminate the Flask process
terminate_flask_process()

# Wait for the Flask thread to complete
flask_thread.join()

# Terminate all remaining Python processes
current_process = psutil.Process()
for process in current_process.children(recursive=True):
    if process.name() == "python.exe" or process.name() == "python":
        process.terminate()
