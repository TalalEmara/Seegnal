import sys
from ImportWindow import ImportWindow
from Selector import Selector
from  Signal import Signal
from Viewer import Viewer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget


class main(QMainWindow):

    signals = []
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

        self.importButton = QPushButton("Import test") #For testing only

        self.selectorChannel1 = Selector()
        self.selectorChannel1.selectorId = 0
        self.selectorChannel2 = Selector()
        self.selectorChannel2.selectorId = 1

        self.viewerChannel1 = Viewer()
        self.viewerChannel2 = Viewer()



        print("Elements created")

    def layoutSet(self):
        self.mainLayout = QVBoxLayout()

        self.toolbarLayout = QHBoxLayout()
        self.workspaceLayout =QHBoxLayout()

        self.channelsLayout =QVBoxLayout()
        self.propertiesLayout =QVBoxLayout()

        self.channel1Layout = QHBoxLayout()
        self.channel2Layout = QHBoxLayout()


        self.channel1Layout.addWidget(self.selectorChannel1)
        self.channel1Layout.addWidget(self.viewerChannel1)

        self.channel2Layout.addWidget(self.selectorChannel2)
        self.channel2Layout.addWidget(self.viewerChannel2)

        self.toolbarLayout.addWidget(self.importButton)


        self.channelsLayout.addLayout(self.channel1Layout)
        self.channelsLayout.addLayout(self.channel2Layout)

        self.workspaceLayout.addLayout(self.channelsLayout)
        self.workspaceLayout.addLayout(self.propertiesLayout)

        self.mainLayout.addLayout(self.toolbarLayout)
        self.mainLayout.addLayout(self.workspaceLayout)


        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)
        print("layout set")

    def connectingUI(self):
        print("UI panels is connected to each other")
        self.connectImport()
        self.connectLinkControls()
        self.connectPolar()
        self.connectGlue()
    def connectImport(self):
        self.importButton.clicked.connect(self.openImportWindow)

        print("Toolbar import button is connecting to its method")
    def openImportWindow(self):
        self.import_window = ImportWindow()
        self.import_window.show()
        self.import_window.signalCreated.connect(self.addSignal)
        print("ImportWindow opened")

    def addSignal(self, signal):
        self.signals.append(signal)
        self.updateSelector(self.selectorChannel1)
        self.updateSelector(self.selectorChannel2)
        print(f"Signal added to main signals array: {signal} channels: {signal.channels}")

    def updateSelector(self, selector):
        selector.signals.clear()

        for signal in self.signals:
            if signal.channels[selector.selectorId] == 1:
                selector.signals.append(signal)
        print("Updated selector signals:", selector.signals, len(selector.signals))
        selector.placeSignalElements()

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