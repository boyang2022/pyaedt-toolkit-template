import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QPushButton
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 300, 50)

        self.button = QPushButton("Click me", self)
        self.button.setGeometry(50, 150, 100, 50)
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        response = requests.get("http://localhost:5000/")
        if response.ok:
            self.label.setText(response.json()["message"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
