class Signal:
    def __init__(self):
        self.name = ""
        self.location = ""
        self.data = ""
        self.channels = [1,0]
        self.colors = ["red", "#242424"] #color in channel1 , color in channel 2
        self.isLive = False
        self.isShown = True