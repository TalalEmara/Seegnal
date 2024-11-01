from PyQt5.QtWidgets import QWidget


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()


    def initializeAttributes(self):
        print("Attributes")


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

    def importSignal(self):
        print("open import window")

    def initializePolar(self):
        print("open import window")

    def linkViewers(self, viewer1, viewer2):
        print("link viewer")