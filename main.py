import sys

from PyQt5.QtCore import Qt

from ImportWindow import ImportWindow
from Properties import Properties
from Selector import Selector
from  Signal import Signal
from Viewer import Viewer
from Toolbar import ToolBar
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from Polar import NonRectangularWindow
from glue import GlueWindow


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
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#2D2D2D;")

    def createUIElements(self):

        self.toolbar = ToolBar()

        # self.importButton = QPushButton("Import test") #For testing only

        self.selectorChannel1 = Selector()
        self.selectorChannel1.selectorId = 0
        self.selectorChannel2 = Selector()
        self.selectorChannel2.selectorId = 1

        self.viewerChannel1 = Viewer()
        self.viewerChannel2 = Viewer()

        self.propertiesPanel = Properties()


        print("Elements created")

    def layoutSet(self):
        self.mainLayout = QVBoxLayout()

        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.addWidget(self.toolbar)

        self.workspaceLayout =QHBoxLayout()

        self.channelsLayout =QVBoxLayout()
        self.propertiesLayout =QVBoxLayout()

        self.propertiesLayout.addWidget(self.propertiesPanel)

        self.channel1Layout = QHBoxLayout()
        self.channel2Layout = QHBoxLayout()


        self.channel1Layout.addWidget(self.selectorChannel1,30)
        self.channel1Layout.addWidget(self.viewerChannel1,70)

        self.channel2Layout.addWidget(self.selectorChannel2,30)
        self.channel2Layout.addWidget(self.viewerChannel2,70)

        # self.toolbarLayout.addWidget(self.importButton)


        self.channelsLayout.addLayout(self.channel1Layout)
        self.channelsLayout.addLayout(self.channel2Layout)

        self.workspaceLayout.addLayout(self.channelsLayout,80)
        self.workspaceLayout.addLayout(self.propertiesLayout,20)

        self.mainLayout.addLayout(self.toolbarLayout)
        self.mainLayout.addLayout(self.workspaceLayout)


        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)
        print("layout set")

    def connectingUI(self):
        self.connectImport()
        self.selectorChannel1.properties = self.propertiesPanel
        self.selectorChannel2.properties = self.propertiesPanel
        self.selectorChannel1.channelChanged.connect(self.updateSelectors)
        self.selectorChannel2.channelChanged.connect(self.updateSelectors)
        self.connectLinkControls()
        self.connectPolar()
        # self. connectGlue()
        self.toolbar.glueButton.clicked.connect(self.connectGlue)
        print("UI panels is connected to each other")
    def connectImport(self):
        self.toolbar.importButton.clicked.connect(self.openImportWindow)

        print("Toolbar import button is connecting to its method")
    def openImportWindow(self):
        self.import_window = ImportWindow()
        self.import_window.show()
        self.import_window.signalCreated.connect(self.addSignal)
        print("ImportWindow opened")

    def addSignal(self, signal):
        self.signals.append(signal)
        if signal.channels[0] == 1:
            self.viewerChannel1.addSignal(signal)
        if signal.channels[1] == 1:
            self.viewerChannel2.addSignal(signal)
        self.updateSelectors()
        print(f"Signal added to main signals array: {signal} channels: {signal.channels}")

    def updateSelectors(self):
        self.updateSelector(self.selectorChannel1)
        self.updateSelector(self.selectorChannel2)
        print("Selectors updated")

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
        frame1_x, frame1_y =self.viewerChannel1.get_visible_frame()
        frame2_x, frame2_y = self.viewerChannel2.get_visible_frame()

        # Process the captured frames as needed
        print("Frame from Viewer 1 - X:", frame1_x, "Y:", frame1_y)
        print("Frame from Viewer 2 - X:", frame2_x, "Y:", frame2_y)
        self.glueview = GlueWindow()
        self.glueview.init_plot(frame1_x, frame1_y, frame2_x, frame2_y)  # Pass the frame data
        self.glueview.show()

        print("Glue window is connected")
    def connectPolar(self):
        self.toolbar.polarButton.clicked.connect(lambda: NonRectangularWindow().show())
        print("Polar window is connected")
    def ConnectLive(self):
        print("show live Signal")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_())