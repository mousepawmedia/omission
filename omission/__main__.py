"""
Main Class [Omission]
"""

import sys
from omission.interface.window import OmissionWindow
from PySide2.QtWidgets import QApplication

def main():
    """
    Run Omission
    """
    app = QApplication(sys.argv)
    window = OmissionWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
