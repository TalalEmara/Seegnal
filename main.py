import sys

from PyQt5.QtCore import Qt

from ImportWindow import ImportWindow
from Properties import Properties
from Selector import Selector
from  Signal import Signal
from Styles.toolBarStyle import linkedButtonOffStyle, linkedButtonOnStyle, rewindOnButtonStyle, rewindOffButtonStyle
from Viewer import Viewer, LiveViewer
from Toolbar import ToolBar
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QTabWidget, \
    QLabel
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
        self.channelsSpace.setStyleSheet("""
               QTabWidget::pane {
                   border-top: 1px solid #76D4D4;
               }
               QTabBar::tab {
                   background-color: #2d2d2d;  /* Tab background color */
                   color:#EFEFEF;
                   padding: 5px;
                   border: 1px solid #C4C4C3;
               }
               QTabBar::tab:selected {
                    color:#2d2d2d;
                   background-color: #76D4D4;  /* Background color of selected tab */
               }
               QTabBar::tab:hover {
                    color:#2d2d2d;
                   background-color: #a6f1f1;  /* Background color when hovered */
               }
           """)

    def createUIElements(self):

        self.toolbar = ToolBar()

        # self.importButton = QPushButton("Import test") #For testing only

        self.selectorChannel1 = Selector()
        self.selectorChannel1.selectorId = 0
        self.selectorChannel2 = Selector()
        self.selectorChannel2.selectorId = 1

        self.selectorChannel1.selectorNameLabel.setText(f"Channel {self.selectorChannel1.selectorId +1}")
        self.selectorChannel2.selectorNameLabel.setText(f"Channel {self.selectorChannel2.selectorId+ 1}")


        self.viewerChannel1 = Viewer()
        self.viewerChannel2 = Viewer()
        self.viewerChannel1.id = 0
        self.viewerChannel2.id = 1
        self.viewerChannel1.viewerTitle.setText(f"Channel {self.viewerChannel1.id +1}")
        self.viewerChannel2.viewerTitle.setText(f"Channel {self.viewerChannel2.id+ 1}")


        self.propertiesPanel = Properties()

        self.liveViewer = LiveViewer()
        self.liveViewer.viewerTitle.setText("Live")

        print("Elements created")

    def layoutSet(self):
        self.mainLayout = QVBoxLayout()

        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.addWidget(self.toolbar)

        self.workspaceLayout =QHBoxLayout()

        self.channelsSpace = QTabWidget()
        self.localTab = QWidget()
        self.liveTab = QWidget()

        self.localLayout =QVBoxLayout()
        self.liveLayout =QVBoxLayout()

        self.propertiesLayout =QVBoxLayout()

        self.propertiesLayout.addWidget(self.propertiesPanel)

        self.channel1Layout = QHBoxLayout()
        self.channel2Layout = QHBoxLayout()


        self.channel1Layout.addWidget(self.selectorChannel1,30)
        self.channel1Layout.addWidget(self.viewerChannel1,70)

        self.channel2Layout.addWidget(self.selectorChannel2,30)
        self.channel2Layout.addWidget(self.viewerChannel2,70)

        # self.toolbarLayout.addWidget(self.importButton)


        self.localLayout.addLayout(self.channel1Layout)
        self.localLayout.addLayout(self.channel2Layout)

        self.liveLayout.addWidget(self.liveViewer)

        self.localTab.setLayout(self.localLayout)
        self.liveTab.setLayout(self.liveLayout)

        self.channelsSpace.addTab(self.localTab, "Local")
        self.channelsSpace.addTab(self.liveTab, "Live")

        self.workspaceLayout.addWidget(self.channelsSpace,80)
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
        self.selectorChannel1.channelChanged.connect(self.handleChannelChange)
        self.selectorChannel2.channelChanged.connect(self.handleChannelChange)
        self.connectLinkControls()
        self.toolbar.pauseButton.clicked.connect(self.pauselink)
        self.toolbar.playButton.clicked.connect(self.playlink)
        self.toolbar.backwardButton.clicked.connect(self.backlink)
        self.toolbar.forwardButton.clicked.connect(self.forwardlink)
        self.toolbar.linkedButton.clicked.connect(self.toggleLinkedButton)
        self.toolbar.speedSlider.valueChanged.connect(self.update_speed)
        self.toolbar.rewindButton.clicked.connect(self.toggleRewindButton)
        self.viewerChannel1.rangeChanged.connect(lambda plot_widget: self.sync_pan(plot_widget))
        self.viewerChannel2.rangeChanged.connect(lambda plot_widget: self.sync_pan(plot_widget))

        self.connectPolar()
        # self. connectGlue()
        self.toolbar.glueButton.clicked.connect(self.connectGlue)
        print("UI panels is connected to each other")

    def toggleLinkedButton(self):
        self.toolbar.isLinked = not self.toolbar.isLinked

        if self.toolbar.isLinked:
            # Update the linked button's appearance and text
            self.toolbar.linkedButton.setStyleSheet(linkedButtonOnStyle)
            self.toolbar.linkedButton.setText("Linked")

            # Disable viewer buttons when linked, so the toolbar buttons are used instead
            self.viewerChannel1.rewindButton.setEnabled(False)
            self.viewerChannel2.rewindButton.setEnabled(False)
            self.viewerChannel1.backwardButton.setEnabled(False)
            self.viewerChannel2.backwardButton.setEnabled(False)
            self.viewerChannel1.forwardButton.setEnabled(False)
            self.viewerChannel2.forwardButton.setEnabled(False)
            self.viewerChannel1.pauseButton.setEnabled(False)
            self.viewerChannel2.pauseButton.setEnabled(False)
            self.viewerChannel1.playButton.setEnabled(False)
            self.viewerChannel2.playButton.setEnabled(False)
            self.viewerChannel1.speedSlider.setEnabled(False)
            self.viewerChannel2.speedSlider.setEnabled(False)



        else:
            # Update the linked button's appearance and text when unlinked
            self.toolbar.linkedButton.setStyleSheet(linkedButtonOffStyle)
            self.toolbar.linkedButton.setText("Link")

            # Enable viewer buttons when unlinked
            self.viewerChannel1.rewindButton.setEnabled(True)
            self.viewerChannel2.rewindButton.setEnabled(True)
            self.viewerChannel1.backwardButton.setEnabled(True)
            self.viewerChannel2.backwardButton.setEnabled(True)
            self.viewerChannel1.forwardButton.setEnabled(True)
            self.viewerChannel2.forwardButton.setEnabled(True)
            self.viewerChannel1.pauseButton.setEnabled(True)
            self.viewerChannel2.pauseButton.setEnabled(True)
            self.viewerChannel1.playButton.setEnabled(True)
            self.viewerChannel2.playButton.setEnabled(True)
            self.viewerChannel1.speedSlider.setEnabled(True)
            self.viewerChannel2.speedSlider.setEnabled(True)

    def backlink(self):
        if self.toolbar.isLinked:
            self.viewerChannel1.backward()
            self.viewerChannel2.backward()

    def forwardlink(self):
        if self.toolbar.isLinked:
            self.viewerChannel1.forward()
            self.viewerChannel2.forward()
    def pauselink(self):
        if self.toolbar.isLinked:
            self.viewerChannel1.pause()
            self.viewerChannel2.pause()

    def playlink(self):
        if self.toolbar.isLinked:
            self.viewerChannel1.play()
            self.viewerChannel2.play()

    def toggleRewindButton(self):
        print(self.toolbar.isRewind)

        if self.toolbar.isLinked:
            self.toolbar.isRewind = not self.toolbar.isRewind
            if self.toolbar.isRewind:
                    self.viewerChannel1.toggleRewind()
                    self.viewerChannel2.toggleRewind()
                    self.toolbar.rewindButton.setStyleSheet(rewindOnButtonStyle)
                    print(self.toolbar.isRewind)
            else:
                    self.toolbar.rewindButton.setStyleSheet(rewindOffButtonStyle)
                    print(self.toolbar.isRewind)

    def sync_pan(self, source_viewer):
        """Synchronize the x-range between the two viewers."""
        if self.toolbar.isLinked:  # Ensure syncing happens only when linked
            # Get the time range (x-axis view range) of the source plot_widget
            time_min, time_max = source_viewer.viewRange()[0]

            # Synchronize the other viewer's x-axis range
            if source_viewer == self.viewerChannel1.plot_widget:
                self.viewerChannel2.plot_widget.setXRange(time_min, time_max, padding=0)
            elif source_viewer == self.viewerChannel2.plot_widget:
                self.viewerChannel1.plot_widget.setXRange(time_min, time_max, padding=0)
    def update_speed(self, speed_value):
        if self.toolbar.isLinked:
            self.viewerChannel1.updatePlotSpeed(speed_value)
            self.viewerChannel2.updatePlotSpeed(speed_value)

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
        signal.colorChanged.connect(self.handleColorChanged)
        signal.hideToggled.connect(self.handleHideToggeled)
        if signal.isLive:
            self.liveViewer.addSignal(signal)
        else:
            if signal.channels[0] == 1:
                self.viewerChannel1.addSignal(signal)
            if signal.channels[1] == 1:
                self.viewerChannel2.addSignal(signal)
        self.updateSelectors()
        print(f"Signal added to main signals array: {signal} channels: {signal.channels}")

    def handleChannelChange(self, signal):
        if signal.channels == [1,0]:
            self.viewerChannel2.removeSignal(signal)
            #signal Start Time
            signal.currentIndex[0] = signal.currentIndex[1]
            print(f"Signal index{signal.currentIndex}")
            self.viewerChannel1.addSignal(signal)
        elif signal.channels == [0,1]:
            self.viewerChannel1.removeSignal(signal)
            #signal Start Time
            signal.currentIndex[1] = signal.currentIndex[0]
            print(f"Signal index{signal.currentIndex}")
            self.viewerChannel2.addSignal(signal)

        self.updateSelectors()


    def handleHideToggeled(self, signal,id):
        if id == 0:
            self.viewerChannel1.toggleHide(signal)
        else:
            self.viewerChannel2.toggleHide(signal)

    def handleColorChanged(self,signal):
        self.viewerChannel1.updateSignalColor(signal)
        self.viewerChannel2.updateSignalColor(signal)
        self.updateSelectors()

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
        """Connect glue functionality to the viewers."""


        # Access the selected data from both viewers
        frame1_x, frame1_y = zip(*self.viewerChannel1.get_selected_data())
        frame2_x, frame2_y = zip(*self.viewerChannel2.get_selected_data())

        # Process or pass the captured frames as needed
        print("Selected data from Viewer 1 - X:", frame1_x, "Y:", frame1_y)
        print("Selected data from Viewer 2 - X:", frame2_x, "Y:", frame2_y)

        # frame1_x, frame1_y =self.viewerChannel1.get_selected_data()
        # frame2_x, frame2_y = self.viewerChannel2.get_selected_data()

        # frame1_x, frame1_y =self.viewerChannel1.glue_rectangle()
        # frame2_x, frame2_y = self.viewerChannel2.glue_rectangle()

        # Process the captured frames as needed
        # print("Frame from Viewer 1 - X:", frame1_x, "Y:", frame1_y)
        # print("Frame from Viewer 2 - X:", frame2_x, "Y:", frame2_y)
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