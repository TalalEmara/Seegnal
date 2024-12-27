import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QLabel, QPushButton, QCheckBox, QLineEdit, QVBoxLayout, \
    QHBoxLayout, QApplication, QFileDialog
import numpy as np
import pandas as pd
from Signal import Signal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
url_live = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'
import requests
from datetime import datetime
import matplotlib.dates as mdates

from Styles.ImportWindowStyles import importButtonStyle,browseButtonStyle

class ImportWindow(QMainWindow):
    signalCreated = pyqtSignal(Signal)
    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeUI()
        self.connectingUI()

    def initializeUI(self):
        self.setWindowTitle("Import a Signal")
        self.resize(400, 100)
        self.createUIElements()
        self.stylingUI()
        self.layoutSet()
        print("UI initialized")

    def createUIElements(self):
        self.tabs = QTabWidget()
        self.fileTab = QWidget()
        self.fileTabLabel = QLabel("Upload Signal File")
        self.signalName = QLabel("Signal has not been uploaded yet")
        self.browseButton = QPushButton("Browse")
        self.channel1CheckBox = QCheckBox("Channel 1")
        self.channel2CheckBox = QCheckBox("Channel 2")
        self.importButton = QPushButton("Import")

        self.liveTab = QWidget()
        self.liveTabLabel = QLabel("Live Signal")
        self.liveInput = QLineEdit('https://services.swpc.noaa.gov/json/planetary_k_index_1m.json')

        self.plotButton = QPushButton("Plot")
        print("Elements created")

    def stylingUI(self):
        self.setStyleSheet("background-color:#2D2D2D; color:#EFEFEF; font-family: Sofia sans; font-weight: semiBold;")
        self.tabs.setStyleSheet("color:#2D2D2D;")
        self.fileTab.setStyleSheet("background-color:#2D2D2D; color:#EFEFEF; font-family: Sofia sans; font-weight: "
                                   "semiBold;")
        self.fileTabLabel.setStyleSheet("font-size:18px; color:#76D4D4;")

        self.signalName.setStyleSheet("font-size:12px; ")
        self.signalName.setFixedWidth(300)

        self.browseButton.setStyleSheet(browseButtonStyle)
        self.importButton.setFixedWidth(400)
        self.importButton.setStyleSheet(importButtonStyle)

        self.liveTabLabel.setStyleSheet("font-size:18px; color:#76D4D4;")
        self.liveInput.setStyleSheet("color:white;font-size:13px; padding:2px; border: .5px solid #76D4D4;;")
        self.liveInput.setPlaceholderText("Put the link")

        self.plotButton.setStyleSheet(importButtonStyle)

        print("UI is styled")
    def layoutSet(self):
        self.setCentralWidget(self.tabs)
        self.fileMainLayout = QVBoxLayout()
        self.fileMainLayout.setAlignment(Qt.AlignCenter)
        self.browseLayout = QHBoxLayout()
        self.browseLayout.addWidget(self.signalName)
        self.browseLayout.addWidget(self.browseButton)

        self.checkBoxesLayout = QHBoxLayout()
        self.checkBoxesLayout.addWidget(self.channel1CheckBox)
        self.checkBoxesLayout.addWidget(self.channel2CheckBox)

        self.fileMainLayout.addWidget(self.fileTabLabel)
        self.fileMainLayout.addLayout(self.browseLayout)
        self.fileMainLayout.addLayout(self.checkBoxesLayout)
        self.fileMainLayout.addStretch()
        self.fileMainLayout.addWidget(self.importButton)

        self.fileTab.setLayout(self.fileMainLayout)
        self.tabs.addTab(self.fileTab, "File")

        self.liveMainLayout = QVBoxLayout()
        self.liveMainLayout.addWidget(self.liveTabLabel)
        self.liveMainLayout.addWidget(self.liveInput)
        self.liveMainLayout.addWidget(self.plotButton)

        self.liveTab.setLayout(self.liveMainLayout)

        self.tabs.addTab(self.liveTab, "Live")



        print("layout set")

    def connectingUI(self):
        self.browseButton.clicked.connect(self.open_file_dialog)
        self.importButton.clicked.connect(lambda: (self.createSignal(self.file_path) if self.file_path else print("No file selected."), self.close()))
        self.plotButton.clicked.connect(lambda: (self.plotLiveSignal(self.liveInput.text()), self.close()))
        print("UI panels are connected to each other")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open Signal File", "",
                                                        "CSV Files (*.csv);;All Files (*)", options=options)
        if self.file_path:
            self.signalName.setText(os.path.basename(self.file_path))
            print(f"File selected: {self.file_path}")
    def createSignal(self, file_path):
        try:
            # get signal data
            data = pd.read_csv(file_path)
            data = data.apply(pd.to_numeric, errors='coerce').to_numpy()

            # get signal name
            file_name = os.path.basename(file_path)

            # Create signal instance
            self.signal = Signal(file_name, file_path, data)

            if self.channel1CheckBox.isChecked():
                self.signal.channels[0] = 1
            if self.channel2CheckBox.isChecked():
                self.signal.channels[1] = 1

            self.signalCreated.emit(self.signal)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def plotLiveSignal(self, url):
        self.signal = Signal("Live Signal", url,self.live_signal_processing(url))
        self.signal.isLive = True
        self.signalCreated.emit(self.signal)
        print("Live Signal plotted")

    def live_signal_processing(self, url):
        response = requests.get(url)
        data = response.json()

        # Initialize lists for storing extracted data
        time_numbers = []  # For numerical time representation
        kp_values = []
        date = []

        for entry in data:
            # Extracting the full datetime object
            full_time = datetime.strptime(entry['time_tag'], '%Y-%m-%dT%H:%M:%S')

            # Convert datetime to a numerical format (for plotting)
            time_number = mdates.date2num(full_time)  # Convert to numerical format

            # Extracting date part (y-m-d)
            date_part = full_time.date()

            # Appending results
            time_numbers.append(time_number)
            date.append(date_part)
            kp_values.append(entry['estimated_kp'])  # Appending the kp value

            print(np.column_stack((time_numbers, kp_values)))

        # Return numerical time representation and kp values
        return  np.column_stack((time_numbers, kp_values))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = ImportWindow()
    test.show()
    sys.exit(app.exec_())
