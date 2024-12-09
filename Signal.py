class Signal:
    def __init__(self, name, location, data):
        self.name = name
        self.location = location
        self.data = data
        self.channels = [0,0]
        self.colors = ["#D55877", "red"] #color in channel1 , color in channel 2
        self.isLive = False
        self.isShown = True

    def changeChannel1Color(self,color):
        self.colors[0] = color
    def changeChannel2Color(self,color):
        self.colors[1] = color




        