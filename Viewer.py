from PyQt5.QtGui import QFont
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

from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5 import QtGui
import pyqtgraph as pg
import numpy as np
from Signal import Signal

class Viewer(QWidget):
    rangeChanged = pyqtSignal(pg.PlotWidget)  # Emit the PlotWidget for synchronization

    def __init__(self):

        super().__init__()
        self.selected_region = None
        print(f"{self} initialized")
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()

    def initializeAttributes(self):
        print("Attributes")
        self.selected_signal_data = []  # Store selected data
        self.selected_region = None

        self.id = 0

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
        self.viewerTitle = QLabel(f"Channel {self.id}")
        self.viewerTitleEditButton = QPushButton()
        self.timeLabel = QLabel("00:00")
        self.pauseButton = QPushButton()
        self.playButton = QPushButton()
        self.backwardButton = QPushButton()
        self.forwardButton = QPushButton()
        self.rewindButton = QPushButton()
        self.rewindButton.setCheckable(True)
        # self.addSignalButton = QPushButton("Add Signal", self.signalViewer) #trial adding signal button
        self.panSlider = QSlider(Qt.Horizontal)
        self.panSlider.setRange(0, 100)
        self.panSlider.setValue(0)
        self.speedSliderLabel = QLabel("Speed")
        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setRange(0, 100)
        self.speedSlider.setValue(50)
        self.plot_widget = pg.PlotWidget()

    def stylingUI(self):
        self.setStyleSheet("background-color: #2D2D2D;")
        self.signalViewer.setStyleSheet(background)
        self.viewerTitleEditButton.setIcon(QtGui.QIcon("Assets/Graph controls/edit.png"))
        self.viewerTitleEditButton.setFixedSize(20, 20)
        self.pauseButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/pause.png"))
        self.playButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/play.png"))
        self.backwardButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/backward.png"))
        self.forwardButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/forward.png"))
        self.rewindButton.setIcon(QtGui.QIcon("Assets/ControlsButtons/rewindOff.png"))
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.panSlider.setMinimumWidth(100)
        self.panSlider.setMaximumWidth(400)
        self.speedSlider.setMinimumWidth(100)
        self.speedSlider.setMaximumWidth(400)
        self.plot_widget.setBackground('#242424')
        self.signalViewer.setFrameShape(QFrame.StyledPanel)
        self.signalPlotLayout.setContentsMargins(5, 5, 5, 5)
        self.viewerTitle.setStyleSheet(labelStyle)
        self.timeLabel.setStyleSheet(labelStyle)
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.forwardButton.setStyleSheet(signalControlButtonStyle)
        self.backwardButton.setStyleSheet(signalControlButtonStyle)
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.panSlider.setStyleSheet(panSliderStyle)
        self.speedSliderLabel.setStyleSheet(labelStyle)
        self.speedSlider.setStyleSheet(panSliderStyle)
        print("Elements are styled")

    def layoutSet(self):
        self.signalPlotLayout = QVBoxLayout(self.signalViewer)
        self.titleToolbarLayout = QHBoxLayout()
        self.titleToolbarLayout.addWidget(self.viewerTitle)
        self.titleToolbarLayout.addWidget(self.viewerTitleEditButton)
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
        self.SignalbuttonsLayout.addWidget(self.speedSliderLabel)
        self.SignalbuttonsLayout.addWidget(self.speedSlider)
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
        self.speedSlider.valueChanged.connect(self.updatePlotSpeed)
        self.panSlider.valueChanged.connect(self.updatePanSlider)
        self.pan_update_timer.timeout.connect(self.syncPanSlider)
        self.plot_widget.sigXRangeChanged.connect(self.startPanUpdate)
        # self.plot_widget.sigXRangeChanged.connect(self.adjustPlotLimits)
        # self.plot_widget.sigYRangeChanged.connect(self.adjustPlotLimits)
        self.plot_widget.sigXRangeChanged.connect(self.emitRangeChange)

        print("UI panels are connected to each other")

    def addSignal(self, signal: Signal):
        if signal.isShown and signal not in self.signals:
            self.signals.append(signal)

            # Store the current X-range (i.e., the current visible time range)
            current_x_range = self.plot_widget.viewRange()[0]

            # Adjust signal data based on the current X-range to make it start from current_x_range[0]
            signal_start_time = signal.data[0, 0]
            if current_x_range[0] != 0:
                signal.shift_time = current_x_range[1]

            # Check if the signal already has a plot curve; if not, create it
            existing_curve = next((curve for curve in self.plot_curves if curve.opts.get('name') == signal.location),
                                  None)
            if not existing_curve:
                # Create the plot curve for the signal if it doesn't exist
                plot_curve = self.plot_widget.plot(pen=pg.mkPen(signal.colors[self.id]))
                plot_curve.setData(signal.getShitedTime(), signal.data[:, 1])

                # Assign the signal name to the plot curve for later identification
                plot_curve.opts['name'] = signal.location

                # Store the plot curve in the list
                self.plot_curves.append(plot_curve)

            self.current_indices[signal.location] = 0
            print(f"Signal '{signal.name}' added with color {signal.colors[1]}")

    def removeSignal(self, signal: Signal):
        if signal.isShown and signal in self.signals:
            # Remove the signal from the list
            self.signals.remove(signal)

            # Find the plot curve associated with the signal and remove it
            for plot_curve in self.plot_curves:
                # Check if the plot curve's name matches the signal's name
                if plot_curve.opts.get('name') == signal.location:
                    self.plot_widget.removeItem(plot_curve)  # Remove the curve from the plot
                    self.plot_curves.remove(plot_curve)  # Remove the curve from the list
                    break

            # Reset the signal index
            signal.shift_time = 0
            self.current_indices[signal.location] = 0
            print(f"Signal '{signal.name}' removed")

    def updateSignalColor(self, signal: Signal):
        for plot_curve in self.plot_curves:
            if plot_curve.opts.get('name') == signal.location:
                plot_curve.setPen(pg.mkPen(signal.colors[self.id]))

    def updatePlot(self):
        if self.is_playing and self.signals:
            max_time = 0

            for signal, plot_curve in zip(self.signals, self.plot_curves):
                if signal.isLive:
                    current_index = self.current_indices[signal.location]
                else:
                    current_index = signal.currentIndex[self.id]
                time_data = signal.getShitedTime()
                amplitude_data = signal.data[:, 1]

                if current_index < len(time_data):
                    plot_curve.setData(time_data[:current_index + 1], amplitude_data[:current_index + 1])
                    max_time = max(max_time, time_data[current_index])
                    current_index += 1
                else:
                    if self.is_rewinding:
                        current_index = 0
                    else:
                        current_index = len(time_data) - 1

                signal.currentIndex[self.id] = current_index
                self.current_indices[signal.location] = current_index

            # Update time label with the maximum time
            self.timeLabel.setText(f"{int(max_time // 60):02}:{int(max_time % 60):02}.{int((max_time % 1) * 1000):03}")

            # Adjust the visible range to simulate sliding
            visible_duration = .5  # Duration of the visible window in seconds
            time_min = max(0, max_time - visible_duration)  # Ensure the minimum time is never negative
            time_max = max(max_time, visible_duration)  # Extend the range to include the visible duration initially
            self.plot_widget.setXRange(time_min, time_max, padding=0)

            self.adjustPlotLimits()

    def toggleHide(self, signal):
        for plot_curve in self.plot_curves:
            curve_name = plot_curve.opts.get('name')
            print(f"Checking curve: {curve_name}")
            if curve_name == signal.location:
                plot_curve.setVisible(signal.isShown[self.id])

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
            current_index = self.current_indices[signal.location]
            new_index = current_index + int(self.time_jump / (signal.data[1, 0] - signal.data[0, 0]))
            if new_index < len(signal.data):
                self.current_indices[signal.location] = new_index
            else:
                self.current_indices[signal.location] = len(signal.data) - 1
                print("Reached the end of the signal")

        self.updatePlot()

    def backward(self):
        print("Viewer is moving 5 seconds backward")
        for signal in self.signals:
            current_index = self.current_indices[signal.location]
            new_index = current_index - int(self.time_jump / (signal.data[1, 0] - signal.data[0, 0]))
            if new_index >= 0:
                self.current_indices[signal.location] = new_index
            else:
                self.current_indices[signal.location] = 0
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
            current_index = self.current_indices[signal.location]
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

    def emitRangeChange(self):
        # Emit the plot_widget itself when the range changes
        self.rangeChanged.emit(self.plot_widget)

    def glue_rectangle(self):
        """Add a rectangle to select a region on the plot."""
        if self.selected_region:
            # If a region already exists, remove it first
            self.plot_widget.removeItem(self.selected_region)

        # Create a LinearRegionItem (rectangle) with an initial range
        self.selected_region = pg.LinearRegionItem(
            values=[self.plot_widget.viewRange()[0][0] + 50, self.plot_widget.viewRange()[0][0] + 150],
            movable=True,
            bounds=self.plot_widget.viewRange()[0]
        )
        self.selected_region.sigRegionChangeFinished.connect(self.handle_region_change)
        self.plot_widget.addItem(self.selected_region)  # Add the rectangle to the plot

    def handle_region_change(self):
        """Handle updates to the region and capture the selected data."""
        self.selected_signal_data = []  # Reset selected data

        # Get the selected region's x-axis limits
        selected_x_min, selected_x_max = self.selected_region.getRegion()

        # Get the visible x and y data within the current plot range
        visible_x_data, visible_y_data = self.get_visible_frame()

        # Filter data points within the selected region and the visible plot range
        for x_data, y_data in zip(visible_x_data, visible_y_data):
            # Only consider data that falls within both the selected region and visible range
            selected_indices = np.where((x_data >= selected_x_min) & (x_data <= selected_x_max))[0]

            if selected_indices.size > 0:
                # Extract the x and y data for the selected indices
                selected_x = x_data[selected_indices]
                selected_y = y_data[selected_indices]

                # Append the filtered data (overlapping with both the selected region and visible region)
                self.selected_signal_data.append((selected_x, selected_y))

    def get_selected_data(self):
        """Return the data selected within the region."""
        return self.selected_signal_data

    def mouseDoubleClickEvent(self, event):
        """Handle double-click event on the plot widget."""
        if self.plot_widget.geometry().contains(event.pos()):
            self.glue_rectangle()        #trial
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


class LiveViewer(Viewer):
    def __init__(self):
        super().__init__()

    def layoutSet(self):
        self.signalPlotLayout = QVBoxLayout(self.signalViewer)
        self.titleToolbarLayout = QHBoxLayout()
        self.titleToolbarLayout.addWidget(self.viewerTitle)
        self.titleToolbarLayout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))


        self.signalPlotLayout.addLayout(self.titleToolbarLayout)
        self.signalPlotLayout.addWidget(self.plot_widget)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.signalViewer)
        self.setLayout(mainLayout)
        print("Layout set")

    def updatePlot(self):
        if self.is_playing and self.signals:
            max_time = 0

            # Loop over the signals and update the plot curves
            for signal, plot_curve in zip(self.signals, self.plot_curves):
                # For live signals, use the current index from the signal object
                if signal.isLive:
                    current_index = self.current_indices[signal.location]
                else:
                    current_index = signal.currentIndex[self.id]
                signal.shift_time = 0
                time_data = signal.getShitedTime()  # Get the shifted time data
                amplitude_data = signal.data[:, 1]  # Get the amplitude data

                # Update the plot curve with data up to the current index
                if current_index < len(time_data):
                    plot_curve.setData(time_data[:current_index + 1], amplitude_data[:current_index + 1])
                    max_time = max(max_time, time_data[current_index])
                    current_index += 1  # Increment to simulate real-time plotting
                else:
                    # Handle edge case: if we reach the end, we either stop or rewind based on state
                    if self.is_rewinding:
                        current_index = 0
                    else:
                        current_index = len(time_data) - 1

                # Store the updated index for this signal
                signal.currentIndex[self.id] = current_index
                self.current_indices[signal.location] = current_index

            # Update the time label based on the maximum time value
            self.timeLabel.setText(f"{int(max_time // 60):02}:{int(max_time % 60):02}.{int((max_time % 1) * 1000):03}")

            # Adjust the X-range of the plot to simulate sliding of the visible window
            visible_duration = .01  # Duration of the visible window in seconds
            time_min = max(time_data[0], max_time - visible_duration)  # Ensure the minimum time is never negative
            time_max = max_time  # Ensure the range includes the visible duration initially
            self.plot_widget.setXRange(time_min, time_max, padding=0)

            # Adjust the Y-range to fit the signal data
            # self.adjustPlotLimits()

