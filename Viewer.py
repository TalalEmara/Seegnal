from PyQt5.QtWidgets import QWidget


class Viewer(QWidget):
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

    def plot(self):
        print("signal is plotted")

    def control(self):
        self.play()
        self.stop()
        self.backward()
        self.forward()
        self.rewind()
        self.changeSpeed()
    def play(self):
        print("viewer is played")
    def stop(self):
        print("viewer is played")

    def backward(self):
        print("viewer is played")

    def forward(self):
        print("viewer is played")
    def rewind(self):
        print("viewer is played")
    def changeSpeed(self):
        print("Speed is changed")
