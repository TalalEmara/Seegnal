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
    panSliderStyle
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
        self.plot_speed = 150
        self.time_jump=5
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(self.plot_speed)
        self.signals = [] 
        self.plot_curves = []  
        self.current_indices = {}
        
        self.pan_update_timer = QTimer()
        self.pan_update_timer.setInterval(100)  
        self.is_panning = False


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
        self.panSlider = QSlider(Qt.Horizontal, self.signalViewer)
        self.panSlider.setRange(0, 100)
        self.panSlider.setValue(0)
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
        self.panSlider.setMinimumWidth(100)
        self.panSlider.setMaximumWidth(400)
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
        self.panSlider.setStyleSheet(panSliderStyle)
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
        self.SignalbuttonsLayout.addWidget(self.panSlider)
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
        self.panSlider.valueChanged.connect(self.updatePanSlider)
        self.pan_update_timer.timeout.connect(self.syncPanSlider)
        self.plot_widget.sigXRangeChanged.connect(self.startPanUpdate)
        # self.plot_widget.sigXRangeChanged.connect(self.adjustPlotLimits)
        # self.plot_widget.sigYRangeChanged.connect(self.adjustPlotLimits)

        print("UI panels are connected to each other")

   
        
    def addSignal(self, signal: Signal):
        if signal.isShown: 
            self.signals.append(signal)
            
            #choose color based on channel number 
            
            #color = signal.colors[0] if signal.channels[0] == 1 else signal.colors[1]
            #plot_curve = self.plot_widget.plot(pen=pg.mkPen(color))

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


    #button functions 
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

    #limits
    def adjustPlotLimits(self):
        time_min, time_max = self.plot_widget.viewRange()[0]

        # Ensure time_min is not less than zero
        if time_min < 0:
            time_min = 0

        current_times = []
        current_amplitudes=[]
        for signal in self.signals:
            current_index = self.current_indices[signal.name]
            if current_index < len(signal.data):  
                current_time = signal.data[current_index, 0]
                current_times.append(current_time)

                amplitude_data = signal.data[:current_index, 1]
                current_amplitudes.extend(amplitude_data)


        # Update time_max based on current times from signals
        if current_times:
            current_max_time = max(current_times)
            time_max = max(time_max, current_max_time)

        if current_amplitudes:
            y_min = min(current_amplitudes)
            y_max = max(current_amplitudes)
            padding = 0.1 * (y_max - y_min)
            self.plot_widget.setYRange(y_min - padding, y_max + padding)


        # Set the x-range of the plot widget
        self.plot_widget.setXRange(time_min, time_max, padding=0)


    #pan slider functions 
    def updatePanSlider(self):
        if not self.signals:
            return
    
        max_time = max(signal.data[-1, 0] for signal in self.signals if len(signal.data) > 0)

        slider_position = self.panSlider.value() / 100  

        time_range_span = self.plot_widget.viewRange()[0][1] - self.plot_widget.viewRange()[0][0]
        time_start = slider_position * (max_time - time_range_span)
        time_start = max(0, time_start)  
        time_end = time_start + time_range_span

        self.plot_widget.setXRange(time_start, time_end, padding=0)    
    
    def startPanUpdate(self):
        if not self.is_panning:
            self.is_panning = True
            self.pan_update_timer.start()

    def stopPanUpdate(self):
        self.is_panning = False
        self.pan_update_timer.stop()

    def syncPanSlider(self):
        if not self.signals:
            return

        time_start, time_end = self.plot_widget.viewRange()[0]
        max_time = max(signal.data[-1, 0] for signal in self.signals if len(signal.data) > 0)
        time_range_adjusted = max_time - (time_end - time_start)
        if time_range_adjusted > 0: 
            slider_position = (time_start / time_range_adjusted) * 100
            self.panSlider.setValue(int(max(0, min(100, slider_position)))) 
        else:
            self.panSlider.setValue(0)
        self.adjustPlotLimits()

    def get_visible_frame(self):
        """Get the currently visible frame (x and y data) based on the x-axis limits of the plot."""
        if not self.signals or not self.plot_widget:
            return None, None

        # Get current x-axis limits from the PlotWidget
        x_min, x_max = self.plot_widget.viewRange()[0]  # viewRange()[0] gives the x-axis range

        visible_x_data = []
        visible_y_data = []

        for signal, plot_curve in zip(self.signals, self.plot_curves):
            time_data = signal.data[:, 0]  # Assuming first column is time (x-axis)
            amplitude_data = signal.data[:, 1]  # Assuming second column is amplitude (y-axis)

            # Get indices of x data within the visible range
            indices = np.where((time_data >= x_min) & (time_data <= x_max))[0]

            if indices.size > 0:  # Ensure there is data within the range
                visible_x_data.append(time_data[indices])
                visible_y_data.append(amplitude_data[indices])

        # Combine visible data for all signals
        return visible_x_data, visible_y_data

    #trial
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

