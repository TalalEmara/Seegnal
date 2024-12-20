import sys
import numpy as np
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy, QHBoxLayout, QComboBox, QSlider, QLineEdit, QLabel, QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from Styles.PolarStyle import  signalControlButtonStyle,rewindOffButtonStyle,rewindOnButtonStyle,sliderStyle,labelStyle


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='polar')
        fig.patch.set_facecolor('#242424')
        self.ax.set_facecolor('#242424')
        self.ax.spines['polar'].set_color('#EFEFEF')
        self.ax.grid(color='#EFEFEF', linestyle='dashed', linewidth=0.2)
        self.ax.tick_params(axis='x', colors='#EFEFEF')
        self.ax.tick_params(axis='y', colors='#EFEFEF')
        super(MplCanvas, self).__init__(fig)


class NonRectangularWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:#2D2D2D; color: #efefef;")
        self.setWindowTitle("Polar view")

        self.polarLabel = QLabel("Polar View")
        self.polarLabel.setStyleSheet("""color: #76D4D4;
                                    font-family: Sofia sans;
                                    font-weight: 600;
                                    font-size:25px;""")
        self.polarLabel.setAlignment(Qt.AlignCenter)
        self.polarLabel.setMargin(20)

        self.rewind_active = False

        self.csv_file_path = 'D:/Faculty/SBE 24-25/DSP/Seegnal/signals_data/ECG_Normal.csv'
        self.data = pd.read_csv(self.csv_file_path)
        self.data = self.data.apply(pd.to_numeric, errors='coerce').to_numpy()

        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.init_plot()

        self.is_panning = False
        self.last_mouse_position = None

        self.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.colorChoosen = "#76D4D4"
        self.signalColorLabel = QLabel("Signal Color")
        self.signalColorLabel.setStyleSheet(labelStyle)

        self.signalColorChooseSquare = QPushButton()
        self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
        self.signalColorChooseSquare.setFixedHeight(20)
        self.signalColorChooseSquare.setFixedWidth(20)
        self.signalColorChooseSquare.clicked.connect(self.openColorDialog)

        self.signalColorChooseList = QComboBox()
        self.signalColorChooseList.setStyleSheet("""
QComboBox{
    background-color: #242424;
    color: #EFEFEF;
    border: none;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 12px;
    height:26px;
}
QComboBox::drop-down {
    border: none
}
QComboBox::down-arrow {
    image: url(Assets/RightPanel/dropdownArrowWhite.png);
    
}

QComboBox QAbstractItemView {
    background-color: #242424;
    color: #EFEFEF;
    selection-background-color: rgba(0,0,0,0);
    selection-color: #76D4D4;
    border: none;
    padding: 5px;
    margin: 2px;
}
""")
        self.signalColorChooseList.addItem("#76D4D4", "#76D4D4")
        self.signalColorChooseList.addItem("#D55877", "#D55877")
        self.signalColorChooseList.addItem("Add New Color")
        self.signalColorChooseList.currentIndexChanged.connect(self.changeSignalColor)

        self.thicknessLabel = QLabel("Line Thickness")

        self.thicknessLabel.setStyleSheet(labelStyle)

        self.thicknessSlider = QSlider(Qt.Horizontal)
        self.thicknessSlider.setMinimum(1)
        self.thicknessSlider.setMaximum(10)
        self.thicknessSlider.setSingleStep(1)
        self.thicknessSlider.setValue(1)  # Default thickness
        self.thicknessSlider.setStyleSheet(sliderStyle)
        self.thicknessSlider.valueChanged.connect(self.updateThicknessValue)

        self.thicknessValueBox = QLineEdit("1")
        self.thicknessValueBox.setFixedWidth(40)
        self.thicknessValueBox.setAlignment(Qt.AlignCenter)
        self.thicknessValueBox.setStyleSheet("""
                                                QLineEdit{
                                                    color: #76D4D4;
                                                    padding:2px;
                                                    border: 2px solid #76D4D4;
                                                    border-radius: 5px;
                                                    font-weight: 600;
                                                }""")


        self.speedLabel = QLabel("Animation Speed")
        self.speedLabel.setStyleSheet(labelStyle)

        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setMinimum(5)
        self.speedSlider.setMaximum(100)
        self.speedSlider.setSingleStep(5)
        self.speedSlider.setValue(10)
        self.speedSlider.setStyleSheet(sliderStyle)
        self.speedSlider.valueChanged.connect(self.updateSpeedValue)

        self.speedValueBox = QLineEdit("10")
        self.speedValueBox.setFixedWidth(40)
        self.speedValueBox.setAlignment(Qt.AlignCenter)
        self.speedValueBox.setStyleSheet("""
                                                QLineEdit{
                                                    color: #76D4D4;
                                                    padding:2px;
                                                    border: 2px solid #76D4D4;
                                                    border-radius: 5px;
                                                    font-weight: 600;
                                                }""")

        propertiesPanel = QVBoxLayout()

        colorPropertyRow1 = QHBoxLayout()
        colorPropertyRow1.addWidget(self.signalColorLabel)
        colorPropertyRow2 = QHBoxLayout()
        colorPropertyRow2.addWidget(self.signalColorChooseSquare)
        colorPropertyRow2.addWidget(self.signalColorChooseList)

        thicknessPropertyRow1 = QHBoxLayout()
        thicknessPropertyRow1.addWidget(self.thicknessLabel)
        thicknessPropertyRow2 = QHBoxLayout()
        thicknessPropertyRow2.addWidget(self.thicknessSlider)
        thicknessPropertyRow2.addWidget(self.thicknessValueBox)

        speedPropertyRow1 = QHBoxLayout()
        speedPropertyRow1.addWidget(self.speedLabel)
        speedPropertyRow2 = QHBoxLayout()
        speedPropertyRow2.addWidget(self.speedSlider)
        speedPropertyRow2.addWidget(self.speedValueBox)

        propertiesPanel.addLayout(colorPropertyRow1)
        propertiesPanel.addLayout(colorPropertyRow2)
        propertiesPanel.addLayout(thicknessPropertyRow1)
        propertiesPanel.addLayout(thicknessPropertyRow2)
        propertiesPanel.addLayout(speedPropertyRow1)
        propertiesPanel.addLayout(speedPropertyRow2)

        self.pauseButton = QPushButton()
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseIcon = QIcon("Assets/ControlsButtons/pause.png")
        self.pauseButton.setIcon(self.pauseIcon)
        self.pauseButton.clicked.connect(self.pause)

        self.playButton = QPushButton()
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playIcon = QIcon("Assets/ControlsButtons/play.png")
        self.playButton.setIcon(self.playIcon)
        self.playButton.clicked.connect(self.play)

        self.zoomInButton = QPushButton()
        self.zoomInButton.setStyleSheet(signalControlButtonStyle)
        self.zoomInButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomInIcon = QIcon("Assets/ControlsButtons/zoomInPolar.png")
        self.zoomInButton.setIcon(self.zoomInIcon)
        self.zoomInButton.clicked.connect(self.zoom_in)

        self.zoomOutButton = QPushButton()
        self.zoomOutButton.setStyleSheet(signalControlButtonStyle)
        self.zoomOutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoomOutIcon = QIcon("Assets/ControlsButtons/zoomOutPolar.png")
        self.zoomOutButton.setIcon(self.zoomOutIcon)
        self.zoomOutButton.clicked.connect(self.zoom_out)

        self.rewindButton = QPushButton()
        self.rewindButton.setStyleSheet(rewindOffButtonStyle)
        self.rewindButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.rewindIcon = QIcon("Assets/ControlsButtons/rewindOff.png")
        self.rewindButton.setIcon(self.rewindIcon)
        self.rewindButton.clicked.connect(self.rewind)

        signalControl = QWidget()
        signalControlLayout = QHBoxLayout()
        signalControl.setLayout(signalControlLayout)

        signalControlLayout.addWidget(self.pauseButton)
        signalControlLayout.addWidget(self.playButton)
        signalControlLayout.addWidget(self.zoomInButton)
        signalControlLayout.addWidget(self.zoomOutButton)
        signalControlLayout.addWidget(self.rewindButton)

        layout = QVBoxLayout()
        layout.addWidget(self.polarLabel)
        layout.addWidget(self.canvas)
        layout.addWidget(signalControl)
        layout.addLayout(propertiesPanel)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.running = True
        self.current_index = 0
        self.batch_size = 10

        # Initialize animation with blit=True for optimization
        self.ani = FuncAnimation(self.canvas.figure, self.update_plot, frames=1000000, interval=100, blit=False)

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorChoosen = color.name()
            self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
            color_exists = False
            for i in range(self.signalColorChooseList.count()):
                if self.signalColorChooseList.itemText(i) == self.colorChoosen:
                    color_exists = True
                    break
            if not color_exists:
                self.signalColorChooseList.insertItem(self.signalColorChooseList.count() - 1, self.colorChoosen, self.colorChoosen)
            self.signalColorChooseList.setCurrentIndex(self.signalColorChooseList.count() - 2)
            self.changeSignalColor()

    def changeSignalColor(self):
        if self.signalColorChooseList.currentText() == "Add New Color":
            self.signalColorChooseList.blockSignals(True)
            self.openColorDialog()
            self.signalColorChooseList.setCurrentIndex(self.signalColorChooseList.count() - 2)
            self.signalColorChooseList.blockSignals(False)
        else:
            self.colorChoosen = self.signalColorChooseList.currentData()
            if self.colorChoosen:
                self.signalColorChooseSquare.setStyleSheet(f"background-color: {self.colorChoosen}")
                self.polar_line.set_color(self.colorChoosen)
                self.canvas.draw()

    def updateThicknessValue(self, value):
        self.thicknessValueBox.setText(str(value))
        self.polar_line.set_linewidth(value)
        self.canvas.draw()

    def init_plot(self):
        self.polar_line, = self.canvas.ax.plot([], [], marker='.', color="#76D4D4")
        # self.canvas.ax.set_title('Polar Plot of Signal Data')
        if self.data is not None:
            r_min = np.min(self.data[:, 1])
            r_max = np.max(self.data[:, 1])
            self.canvas.ax.set_ylim(r_min, r_max * 1.1)

    def update_plot(self, frame):
        if self.running and self.data is not None and self.canvas is not None:
            end_index = min(self.current_index + self.batch_size, len(self.data))
            batch_data = self.data[self.current_index:end_index]
            time = batch_data[:, 0]
            max_time = self.data[:, 0].max()
            theta = 2 * np.pi * time / max_time
            r = batch_data[:, 1]

            if self.current_index == 0:
                self.polar_line.set_data(theta, r)
            else:
                self.polar_line.set_data(np.concatenate((self.polar_line.get_xdata(), theta)),
                                         np.concatenate((self.polar_line.get_ydata(), r)))

            self.current_index += self.batch_size
            self.canvas.draw()
            if self.current_index >= len(self.data):
                if self.rewind_active:
                    self.current_index = 0
                    self.polar_line.set_data([], [])
                    self.canvas.draw()
                    self.running = True

    def on_scroll(self, event):
        if event.inaxes == self.canvas.ax:
            r_min, r_max = self.canvas.ax.get_ylim()
            zoom_factor = 0.2
            if event.button == 'up':
                r_min *= (1 - zoom_factor)
                r_max *= (1 - zoom_factor)
            elif event.button == 'down':
                r_min *= (1 + zoom_factor)
                r_max *= (1 + zoom_factor)
            r_min = max(r_min, 0)
            r_max = min(r_max, np.max(self.data[:, 1]) * 1.5)
            if r_min < r_max:
                self.canvas.ax.set_ylim(r_min, r_max)
                self.canvas.draw_idle()

    def updateSpeedValue(self, value):
        self.speedValueBox.setText(str(value))
        speed_factor = value / 100
        new_interval = max(1, 50 - int(40 * speed_factor))
        new_batch_size = max(1, int(10 + 90 * speed_factor))
        self.batch_size = new_batch_size
        self.ani.event_source.interval = new_interval
        self.ani.event_source.start()

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def zoom_in(self):
        current_ylim = self.canvas.ax.get_ylim()
        new_ylim = (current_ylim[0] / 2, current_ylim[1] / 2)
        r_min, r_max = new_ylim
        self.canvas.ax.set_ylim(r_min, r_max)
        self.canvas.ax.set_yticks(np.linspace(r_min, r_max, num=5))
        self.canvas.draw()

    def zoom_out(self):
        current_ylim = self.canvas.ax.get_ylim()
        new_ylim = (current_ylim[0] * 2, current_ylim[1] * 2)
        r_min, r_max = new_ylim
        self.canvas.ax.set_ylim(r_min, r_max)
        self.canvas.ax.set_yticks(np.linspace(r_min, r_max, num=5))
        self.canvas.draw()

    def rewind(self):
            self.rewind_active = not self.rewind_active
            if self.rewind_active:
                self.rewindButton.setStyleSheet(rewindOnButtonStyle)
            else:
                self.rewindButton.setStyleSheet(rewindOffButtonStyle)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NonRectangularWindow()
    window.show()
    sys.exit(app.exec_())
