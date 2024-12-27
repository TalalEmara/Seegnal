from PyQt5.QtCore import pyqtSignal, QObject


class Signal(QObject):
    nameChanged = pyqtSignal(object)
    colorChanged = pyqtSignal(object)
    hideToggled = pyqtSignal(object,int)
    def __init__(self, name, location, data):
        super().__init__()
        self.name = name
        self.location = location
        self.data = data
        self.channels = [0,0]
        self.colors = ["#D55877", "red"] #color in channel1 , color in channel 2
        self.isLive = False
        self.isShown = [True , True]
        self.shift_time = 0 # maybe need one for each channel
        self.currentIndex = [0,0]

    def changeName(self,name):
        self.name = name
        self.nameChanged.emit(self)
    def changeChannel1Color(self,color):
        self.colors[0] = color
        self.colorChanged.emit(self)
        print("emited")
    def changeChannel2Color(self,color):
        self.colors[1] = color
        self.colorChanged.emit(self)

    def toggleHide(self, id):
        self.isShown[id] = not self.isShown[id]
        self.hideToggled.emit(self,id)


    def getShitedTime(self):
        return self.data[:, 0] + self.shift_time



        