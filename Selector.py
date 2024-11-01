from PyQt5.QtWidgets import QWidget


class Selector(QWidget):

    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()


    def initializeAttributes(self):
        self.signals ["signal instance","signal instance"]
    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        print("Elements created")
    def stylingUI(self):
        print("Elements is styled")

    def layoutSet(self):
        print("layout set")

    def connectingUI(self):
        print("UI panels is connected to each other")


    def createSignalElement(self, signal):
        print("signal is created into ui")
    def  placeSignalElements(self , signals):
        print("signals is placed")

    def connectProperties(self):
        print("selected signal is now on properties panel")

    def connectViewer(self):
        print("selected signal is now on viewer")
