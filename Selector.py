import sys

import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QTableWidgetItem, QPushButton

from Signal import Signal


class Selector(QWidget):

    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()


    def initializeAttributes(self):
        self.signals = []
    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        self.selectorNameLabel = QLabel("Selector name")
        #Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["","name","location","",""])



        print("Elements created")
    def stylingUI(self):
        #Table
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        print("Elements is styled")

    def layoutSet(self):
        self.mainLayout = QVBoxLayout()
        self.titleRow = QHBoxLayout()
        self.tableLayout = QHBoxLayout()

        self.titleRow.addWidget(self.selectorNameLabel)
        self.tableLayout.addWidget(self.table)

        self.mainLayout.addLayout(self.titleRow)
        self.mainLayout.addLayout(self.tableLayout)
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        print("layout set")

    def connectingUI(self):
        print("UI panels is connected to each other")


    def createSignalElement(self, signal):
        print("signal is created into ui")
    def  placeSignalElements(self):
        self.table.setRowCount(len(self.signals))
        for row ,signal in enumerate(self.signals):
            self.table.setItem(row, 0, QTableWidgetItem(signal.colors[0]))
            self.table.setItem(row, 1, QTableWidgetItem(signal.name))
            self.table.setItem(row, 2, QTableWidgetItem(signal.location))
            self.table.setCellWidget(row, 3, QPushButton("h"))
            self.table.setCellWidget(row, 4, QPushButton("S"))

        print("signals is placed")

    def connectProperties(self):
        print("selected signal is now on properties panel")

    def connectViewer(self):
        print("selected signal is now on viewer")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QMainWindow()
    heartSignal = Signal()
    heartSignal.name = "Heart Rate Monitor"
    heartSignal.location = "E/newFolder"
    time = np.arange(0, 10, 0.1)  # Time from 0 to 10 seconds, sampled every 0.1 second
    value = 75 + 5 * np.sin(0.5 * time)  # Simulated heart rate fluctuating around 75 bpm
    heartSignal.data = np.column_stack((time, value))
    heartSignal.channels = [1, 0]
    heartSignal.colors = ["red", "#242424"]  # color in channel 1, color in channel 2
    heartSignal.isLive = True
    heartSignal.isShown = True

    tempSignal = Signal()
    tempSignal.name = "Temperature Sensor"
    tempSignal.location = "D/dataFolder"
    time = np.arange(0, 24, 1)  # Time from 0 to 24 hours, sampled every hour
    value = 20 + 3 * np.sin(0.3 * time) + np.random.normal(0, 0.5,
                                                           len(time))  # Temperature fluctuating around 20°C with slight noise
    tempSignal.data = np.column_stack((time, value))
    tempSignal.channels = [1,0]
    tempSignal.colors = ["blue", "#Efefef"]  # color for channel 1
    tempSignal.isLive = False
    tempSignal.isShown = True

    selector = Selector()

    selector.signals.append(heartSignal)
    selector.signals.append(tempSignal)

    selector.placeSignalElements()

    main.setCentralWidget(selector)

    main.resize(int(1440/3), 720)
    main.show()
    sys.exit(app.exec_())

