import sys

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QTableWidgetItem, QPushButton, QHeaderView

from Properties import Properties
from Signal import Signal


class Selector(QWidget):

    channelChanged = pyqtSignal()
    def __init__(self,id = 0):
        super().__init__()
        print(f"{self}initialized")
        self.initializeAttributes(id)
        self.initializeUI()
        self.connectingUI()


    def initializeAttributes(self, id):
        self.signals = []
        self.selectorId = id
        self.properties = Properties()
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
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#242424;color: #76D4D4; font-family: Sofia sans;")

        self.selectorNameLabel.setStyleSheet("""color: #76D4D4;
                                                font-family: Sofia sans;
                                                font-weight: 600;
                                                font-size: 18px;
                                                padding-left: 15px;""")
        # Table
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setFocusPolicy(Qt.NoFocus)

        # Set the stylesheet to customize the table and headers
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #242424;
                color: #EFEFEF;
                border: none;
            }
            QTableWidget::item {
                background-color: #242424;  
                color: #EFEFEF;
                border:none;
            }
            QTableWidget::item:selected {
                background-color: #242424;  
                color: #EFEFEF;
                border:none;
            }
            QHeaderView::section {
                background-color: #242424;
                font-size: 12px; 
                color: #7c7c7c;
                border: none;
                border-bottom: 1px solid #76D4D4;
                text-align: left;
                font-weight: normal;  
            }
            QTableWidget::item:focus {
            outline: none:
        }
        """)

        self.table.setShowGrid(False)
        self.table.setColumnWidth(0, 1)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setColumnWidth(3, int(480 * .1))
        self.table.setColumnWidth(4, int(480 * .1))

        for i in range(self.table.horizontalHeader().count()):
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignLeft)

        self.table.update()
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
        self.table.itemClicked.connect(self.on_item_clicked)
        print("UI panels is connected to each other")


    def placeSignalElements(self):
        self.table.setRowCount(len(self.signals))
        for row, signal in enumerate(self.signals):
            colorPreview = QPushButton()
            colorPreview.setStyleSheet(f"background-color:{signal.colors[0]};")
            colorPreview.setFixedWidth(5)
            colorPreview.setEnabled(False)

            colorHolder = QHBoxLayout()
            colorHolder.addWidget(colorPreview)
            colorHolder.setContentsMargins(0, 0, 0, 0)

            colorWidget = QWidget()
            colorWidget.setLayout(colorHolder)

            self.table.setCellWidget(row, 0, colorWidget)
            self.table.setItem(row, 1, QTableWidgetItem(signal.name))
            self.table.setItem(row, 2, QTableWidgetItem(signal.location))

            hideButton = QPushButton()
            hideButton.setIcon(QIcon("Assets/Selector/shown.png"))
            hideButton.clicked.connect(
                lambda checked, button=hideButton, selectSignal=signal: self.toggleHide(button, selectSignal))

            switchButton = QPushButton()
            switchButton.setIcon(QIcon("Assets/Selector/swap.png"))
            switchButton.clicked.connect(
                lambda checked, button=switchButton, selectSignal=signal: self.toggleSwitch(button, selectSignal))

            self.table.setCellWidget(row, 3, hideButton)
            self.table.setCellWidget(row, 4, switchButton)

        print("signals are placed")

    def on_item_clicked(self, item):
        row = item.row()
        self.table.selectRow(row)
        selected_signal = self.signals[row]
        self.properties.setSignal(selected_signal)
        print(f"Selected row: {row}")

    def toggleSwitch(self, button, signal):
        if signal.channels == [1,1]:
            return
        else:
            signal.channels = [1,1]
            signal.channels[self.selectorId] = 0
            self.signals.remove(signal)
            self.placeSignalElements()
            self.channelChanged.emit()


        print(signal.channels)
    def toggleHide(self, button, signal):
        if signal.isShown:
            button.setIcon(QIcon("Assets/Selector/hidden.png"))
            signal.isShown = False
        else:
            button.setIcon(QIcon("Assets/Selector/shown.png"))
            signal.isShown = True

        print(signal.name)
        print(signal.isShown)


    def connectViewer(self):
        print("selected signal is now on viewer")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = QMainWindow()
    heartSignal = Signal("Heart", "E/Heart", "")
    heartSignal.name = heartSignal.name
    heartSignal.location = heartSignal.location
    time = np.arange(0, 10, 0.1)  # Time from 0 to 10 seconds, sampled every 0.1 second
    value = 75 + 5 * np.sin(0.5 * time)  # Simulated heart rate fluctuating around 75 bpm
    heartSignal.data = np.column_stack((time, value))
    heartSignal.channels = [1, 0]
    heartSignal.colors = ["red", "#242424"]  # color in channel 1, color in channel 2
    heartSignal.isLive = True
    heartSignal.isShown = True

    tempSignal = Signal("Temprature", "E/Temp", "")
    tempSignal.name = tempSignal.name
    tempSignal.location = tempSignal.location
    time = np.arange(0, 24, 1)  # Time from 0 to 24 hours, sampled every hour
    value = 20 + 3 * np.sin(0.3 * time) + np.random.normal(0, 0.5,
                                                           len(time))  # Temperature fluctuating around 20°C with slight noise
    tempSignal.data = np.column_stack((time, value))
    tempSignal.channels = [1,1]
    tempSignal.colors = ["blue", "#Efefef"]  # color for channel 1
    tempSignal.isLive = False
    tempSignal.isShown = True

    selector = Selector()

    selector.signals.append(heartSignal)
    selector.signals.append(tempSignal)

    selector.placeSignalElements()

    main.setCentralWidget(selector)

    main.resize(480, 360)
    main.show()
    sys.exit(app.exec_())

