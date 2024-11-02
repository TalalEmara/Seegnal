from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QSpacerItem, QSizePolicy, QSlider, QApplication,
    QMainWindow
)
import sys


from Styles.viewerStyles import (
    signalControlButtonStyle,
    rewindOffButtonStyle,
    rewindOnButtonStyle,
    labelStyle,
    background,
    panSlider
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtGui
import pyqtgraph as pg
import numpy as np

from Signal import Signal

class Viewer(QWidget):
    def __init__(self):
        super().__init__()
        print(f"{self} initialized")
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()

    def initializeAttributes(self):
        print("Attributes")
        self.viewer_name = "Channel 1"
        #self.plot_color = "#87EDF1"  # NOT Viewer Attribute it is Signal Attribute
        self.plot_speed = 50
        #self.plot_thickness = 2 # NOT Viewer Attribute it is Signal Attribute
        self.time_data = np.linspace(0, 10, 1000)
       # self.amplitude_data = np.sin(self.time_data) # NOT Viewer Attribute it is Signal Attribute
        self.current_index = 0
        self.is_playing = True
        self.is_rewinding = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(self.plot_speed)

    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        print("Elements created")


        self.signalViewer = QFrame(self)
        self.signalTitle = QLabel(self.viewer_name, self.signalViewer)
        self.signalTitleEditButton = QPushButton(self.signalViewer)
        self.timeLabel = QLabel("00:00", self.signalViewer)
        self.pauseButton = QPushButton(self.signalViewer)
        self.playButton = QPushButton(self.signalViewer)
        self.backwardButton = QPushButton(self.signalViewer)
        self.forwardButton = QPushButton(self.signalViewer)
        self.rewindButton = QPushButton(self.signalViewer)
        self.slider = QSlider(Qt.Horizontal, self.signalViewer)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.plot_widget = pg.PlotWidget()









    def stylingUI(self):
        self.setStyleSheet("background-color: #2D2D2D;")
        self.signalViewer.setStyleSheet(background)
        self.signalTitleEditButton.setIcon(QtGui.QIcon("Assets/Graph controls/edit.png"))
        self.signalTitleEditButton.setFixedSize(20, 20)
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.backwardButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/backward.png"))
        self.forwardButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/forward.png"))
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOn.png"))
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.slider.setMinimumWidth(100)
        self.slider.setMaximumWidth(400)
        self.plot_widget.setBackground('#242424')
        self.signalViewer.setFrameShape(QFrame.StyledPanel)
        self.signalPlotLayout.setContentsMargins(5, 5, 5, 5)
        self.signalTitle.setStyleSheet(labelStyle)
        self.timeLabel.setStyleSheet(labelStyle)
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.forwardButton.setStyleSheet(signalControlButtonStyle)
        self.backwardButton.setStyleSheet(signalControlButtonStyle)
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.slider.setStyleSheet(panSlider)
        print("Elements are styled")

    def layoutSet(self):
        self.signalPlotLayout = QVBoxLayout(self.signalViewer)
        self.titleToolbarLayout = QHBoxLayout()
        self.titleToolbarLayout.addWidget(self.signalTitle)
        self.titleToolbarLayout.addWidget(self.signalTitleEditButton)
        self.titleToolbarLayout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.SignalbuttonsLayout = QHBoxLayout()
        self.SignalbuttonsLayout.addWidget(self.timeLabel)
        self.SignalbuttonsLayout.addSpacing(10)
        self.SignalbuttonsLayout.addWidget(self.pauseButton)
        self.SignalbuttonsLayout.addWidget(self.playButton)
        self.SignalbuttonsLayout.addWidget(self.backwardButton)
        self.SignalbuttonsLayout.addWidget(self.forwardButton)
        self.SignalbuttonsLayout.addWidget(self.rewindButton)
        self.SignalbuttonsLayout.addStretch(1)
        self.SignalbuttonsLayout.addWidget(self.slider)
        self.SignalbuttonsLayout.addStretch(1)
        self.signalPlotLayout.addLayout(self.titleToolbarLayout)
        self.signalPlotLayout.addWidget(self.plot_widget)
        self.signalPlotLayout.addLayout(self.SignalbuttonsLayout)




        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.signalViewer)
        self.setLayout(mainLayout)
        print("Layout set")

    def connectingUI(self):
        self.timer.timeout.connect(self.updatePlot)
        self.pauseButton.clicked.connect(self.pause)
        self.playButton.clicked.connect(self.play)
        self.forwardButton.clicked.connect(self.forward)
        self.backwardButton.clicked.connect(self.backward)
        self.rewindButton.toggled.connect(self.toggleRewind)
        self.plot_widget.sigXRangeChanged.connect(self.adjustPlotLimits)
        print("UI panels are connected to each other")

    def updatePlot(self): # IT Should TAKE SIGNAL AS ARGUMENT TO TAKE DATA AND COLOR AND ALL ATTRIBUTES
        if self.is_playing:  
            self.plot_curve.setData(self.time_data[:self.current_index], self.amplitude_data[:self.current_index])
            self.current_index += 1
            if self.current_index >= len(self.time_data):
                self.current_index = len(self.time_data)
            self.adjustPlotLimits()
            self.updateTimeLabel()

    def updateTimeLabel(self):
        if self.current_index < len(self.time_data):
            elapsed_time = self.time_data[self.current_index]
            minutes, seconds = divmod(elapsed_time, 60)  
            milliseconds = int((elapsed_time % 1) * 1000) 
            self.timeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{milliseconds:03}")

    def loadData(self, time_data, amplitude_data):  # ALL DATA IS INSIDE SIGNAL CLASS signal_name.data| signal.color[0] | I discarded the thicknes for Now Review All structrue First
        self.time_data = time_data
        self.amplitude_data = amplitude_data
        self.current_index = 0

    def setSignalProperties(self, color=None, speed=None, thickness=None):
        if color:
            self.plot_color = color
            self.plot_curve.setPen(pg.mkPen(color=self.plot_color, width=self.plot_thickness))
        if speed:
            self.plot_speed = speed
            self.timer.setInterval(self.plot_speed)
        if thickness:
            self.plot_thickness = thickness
            self.plot_curve.setPen(pg.mkPen(color=self.plot_color, width=self.plot_thickness))

    def control(self):
        self.play()
        self.pause()
        self.backward()
        self.forward()
        self.toggleRewind()
        self.changeSpeed()

    def play(self):
        if not self.is_playing:  
            self.is_playing = True
            self.timer.start(self.plot_speed) 
            print("Viewer is played")

    def pause(self):
        if self.is_playing:  
            self.is_playing = False
            self.timer.stop()
            print("Viewer is stopped")

    def forward(self):
        print("Viewer is forward")
        self.current_index = len(self.time_data)  
        self.updatePlot()  

    def backward(self):
        print("Viewer is backward")
        self.current_index = 0  
        self.updatePlot() 

    def toggleRewind(self):
        print("Viewer is rewinding")

    def updatePlotSpeed(self, value):
        self.plot_speed = max(1, 100 - value)  
        self.timer.setInterval(self.plot_speed)
        print("Speed is changed")
            
    def adjustPlotLimits(self):
        time_min, time_max = self.plot_widget.viewRange()[0]

        if time_min < 0:
            time_min = 0

        if self.current_index > 0:  
            current_time = self.time_data[self.current_index - 1]
            time_max = max(current_time, time_max) 

        self.plot_widget.setXRange(time_min, time_max, padding=0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QMainWindow()
    signal = Signal()
    signal.name = "Heart Rate Monitor"
    signal.location = "E/newFolder"
    time = np.arange(0, 10, 0.1)  # Time from 0 to 10 seconds, sampled every 0.1 second
    value = 75 + 5 * np.sin(0.5 * time)  # Simulated heart rate fluctuating around 75 bpm
    signal.data = np.column_stack((time, value))
    signal.channels = [1, 2]
    signal.colors = ["red", "#242424"]  # color in channel 1, color in channel 2
    signal.isLive = True
    signal.isShown = True

viewer = Viewer()
    main.setCentralWidget(viewer)

    main.resize(750, 400)
    main.show()
    sys.exit(app.exec_())

