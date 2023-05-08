import os
import sys
import threading

is_linux = os.name == "posix"
script_name = os.path.splitext(os.path.basename(__file__))[0]

if is_linux:
    import subprocessdotnet as subprocess
else:
    import subprocess

# User or tool could pass the desktop ID and version
desktop_pid = None
desktop_version = None
if len(sys.argv) > 2:
    desktop_pid = sys.argv[1]
    desktop_version = sys.argv[2]

# Path to Python interpreter with Flask and Pyside6 installed
python_path = sys.executable

# Define the command to start the Flask application
backend_command = "backend\\backend.py"

# Define the command to start the PySide6 UI
frontend_command = "ui\\frontend.py"


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


if desktop_pid and desktop_version:
    flask_thread = threading.Thread(
        target=run_command, args=[python_path, backend_command, desktop_pid, desktop_version]
    )
    ui_thread = threading.Thread(
        target=run_command, args=[python_path, frontend_command, desktop_pid, desktop_version]
    )
else:
    flask_thread = threading.Thread(target=run_command, args=[python_path, backend_command])
    ui_thread = threading.Thread(target=run_command, args=[python_path, frontend_command])

# Create a thread to run the Flask application
flask_thread.start()
# Create a thread to run the PySide6 UI
ui_thread.start()

# Wait for both threads to complete
flask_thread.join()
ui_thread.join()
