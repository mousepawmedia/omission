import os
from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QIcon

from omission.data.data_loader import DataLoader

class OmissionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Omission"
        self.icon = os.path.join(os.path.dirname(__file__), os.pardir, "resources", "icons", "omission_icon.png")

        # Create our score loader.
        self.dataloader = DataLoader()

        # Initialize the window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.show()