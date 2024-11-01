import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class main(QMainWindow):

    signals = ["signal instance", "signal instance"]
    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeUI()
        self.connectingUI()


    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()

    def createUIElements(self):
        print("Elements created")

    def layoutSet(self):
        print("layout set")

    def connectingUI(self):
        print("UI panels is connected to each other")
        self.connectImport()
        self.connectLinkControls()
        self.connectPolar()
        self.connectGlue()
    def connectImport(self):
        print("Toolbar import button is connecting to its method")
    def connectLinkControls(self):
        print("Toolbar Controls is connecting to viewers")
    def connectGlue(self):
        print("Glue window is connected")
    def connectPolar(self):
        print("Polar window is connected")
    def ConnectLive(self):
        print("show live Signal")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_())