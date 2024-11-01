from PyQt5.QtWidgets import QMainWindow
class ImportWindow(QMainWindow):
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

    def createSignal(self,name, data, channelsAccess):
        print("signal created")
    def sendData(self,SignalInstance):
        print("signal is sent")
