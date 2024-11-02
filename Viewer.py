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
        
        self.current_index = 0
        self.is_playing = True
        self.is_rewinding = False
        self.plot_speed = 200
        self.time_jump=5
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(self.plot_speed)
        self.signals = [] 
        self.plot_curves = []  
        self.current_indices = {}

    def initializeUI(self):
    
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        print("Elements created")

        self.signalViewer = QFrame(self)
        self.signalTitle = QLabel("channel1")
        self.signalTitleEditButton = QPushButton(self.signalViewer)
        self.timeLabel = QLabel("00:00", self.signalViewer)
        self.pauseButton = QPushButton(self.signalViewer)
        self.playButton = QPushButton(self.signalViewer)
        self.backwardButton = QPushButton(self.signalViewer)
        self.forwardButton = QPushButton(self.signalViewer)
        self.rewindButton = QPushButton(self.signalViewer)
        self.rewindButton.setCheckable(True)
        # self.addSignalButton = QPushButton("Add Signal", self.signalViewer) #trial adding signal button
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
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
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
        # self.SignalbuttonsLayout.addWidget(self.addSignalButton) #trial adding signal button
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
        self.rewindButton.clicked.connect(self.toggleRewind)
        # self.addSignalButton.clicked.connect(self.addNewSignal)  #trial adding signal button
        self.plot_widget.sigXRangeChanged.connect(self.adjustPlotLimits)
        print("UI panels are connected to each other")

    def addSignal(self, signal: Signal):
        if signal.isShown: 
            self.signals.append(signal)
            plot_curve = self.plot_widget.plot(pen=pg.mkPen(signal.colors[1])) 
            self.plot_curves.append(plot_curve)
            self.current_indices[signal.name] = 0 
            print(f"Signal '{signal.name}' added with color {signal.colors[1]}")

    def updatePlot(self):
        if self.is_playing and self.signals:
            max_time = 0

            for signal, plot_curve in zip(self.signals, self.plot_curves):
                current_index = self.current_indices[signal.name]
                time_data = signal.data[:, 0]
                amplitude_data = signal.data[:, 1]

                if self.is_rewinding:
                    if current_index < len(time_data):  
                        plot_curve.setData(time_data[:current_index + 1], amplitude_data[:current_index + 1])  
                        max_time = max(max_time, time_data[current_index])
                        current_index += 1  
                    else:
                        current_index = 0 
                else:
                
                    if current_index < len(time_data):  
                        plot_curve.setData(time_data[:current_index], amplitude_data[:current_index]) 
                        max_time = max(max_time, time_data[current_index])
                        current_index += 1  
                    else:
                        self.current_indices[signal.name] = len(time_data)

                self.current_indices[signal.name] = current_index
                
        

            # Update time label with the maximum time
            self.timeLabel.setText(f"{int(max_time // 60):02}:{int(max_time % 60):02}.{int((max_time % 1) * 1000):03}")
            self.adjustPlotLimits()


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
        print("Viewer is moving 5 seconds forward")
        for signal in self.signals:
            current_index = self.current_indices[signal.name]
            new_index = current_index + int(self.time_jump / (signal.data[1, 0] - signal.data[0, 0])) 
            if new_index < len(signal.data):
                self.current_indices[signal.name] = new_index
            else:
                self.current_indices[signal.name] = len(signal.data) - 1 
                print("Reached the end of the signal")

        self.updatePlot()

    def backward(self):
        print("Viewer is moving 5 seconds backward")
        for signal in self.signals:
            current_index = self.current_indices[signal.name]
            new_index = current_index - int(self.time_jump / (signal.data[1, 0] - signal.data[0, 0]))  
            if new_index >= 0:
                self.current_indices[signal.name] = new_index
            else:
                self.current_indices[signal.name] = 0
                print("At the start of the signal")

        self.updatePlot()

    def toggleRewind(self):
        self.is_rewinding = not self.is_rewinding
        if self.is_rewinding:
            self.rewindButton.setStyleSheet(rewindOnButtonStyle)  
            print("Rewind is ON")
        else:
            self.rewindButton.setStyleSheet(rewindOffButtonStyle) 
            print("Rewind is OFF")
        self.updatePlot()

    def updatePlotSpeed(self, value):
        self.plot_speed = max(1, 100 - value)  
        self.timer.setInterval(self.plot_speed)
        print("Speed is changed")
            
    def adjustPlotLimits(self):
        time_min, time_max = self.plot_widget.viewRange()[0]

        if time_min < 0:
            time_min = 0

        current_times = []
        for signal in self.signals:
            current_index = self.current_indices[signal.name]
            if current_index < len(signal.data):  
                current_time = signal.data[current_index, 0]
                current_times.append(current_time)

        if current_times:
            current_max_time = max(current_times)
            time_max = max(time_max, current_max_time)

        self.plot_widget.setXRange(time_min, time_max, padding=0)

    
    # def addNewSignal(self): #Trial , to add multiple signals and test with it
    #     new_signal = Signal()
    #     new_signal.name = f"Signal {len(self.signals) + 1}" 
    #     new_signal.location = "E/newFolder" 
    #     endpoint = np.random.uniform(10, 20) 
    #     time = np.arange(0, endpoint, 0.1) 
    #     np.random.seed(len(self.signals))  
    #     value = np.random.rand(len(time)) * 100 
    #     new_signal.data = np.column_stack((time, value))
    #     new_signal.channels = [1, 2]
    #     new_signal.colors = ["#D55877", "#76D4D4"] 
    #     new_signal.isLive = True
    #     new_signal.isShown = True
    #     self.addSignal(new_signal) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QMainWindow()
    viewer = Viewer()

    signal1 = Signal()
    signal1.name = "Heart Rate Monitor"
    signal1.location = "E/newFolder"
    time = np.arange(0, 10, 0.1)
    value = 75 + 5 * np.sin(0.5 * time)
    signal1.data = np.column_stack((time, value))
    signal1.channels = [1, 2]
    signal1.colors = ["#D55877", "#76D4D4"] 
    signal1.isLive = True
    signal1.isShown = True


    signal2 = Signal()
    signal2.name = "Temperature Sensor"
    time = np.arange(0, 10, 0.1)
    value = 25 + 2 * np.sin(0.3 * time)
    signal2.data = np.column_stack((time, value))
    signal1.colors = ["#D55877", "#76D4D4"] 
    signal1.isLive = True
    signal1.isShown = True

    viewer.addSignal(signal1)
    viewer.addSignal(signal2)
    main.setCentralWidget(viewer)

    main.resize(750, 400)
    main.show()
    sys.exit(app.exec_())

