import sys

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QTableWidgetItem, QPushButton, QHeaderView, QComboBox, QSpinBox, QColorDialog

from Signal import Signal


class Properties(QWidget):


    def __init__(self):
        super().__init__()
        self.signal = Signal("heart","d/dd/d",[1,0,1,1,0])
        self.signal.colors[0] = "white"
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()
        print(f"{self}initialized")

    def initializeAttributes(self):
        print("Initialize Attributes")
    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        self.propertiesLabel = QLabel("Properties")
        self.signalNameLabel = QLabel(self.signal.name) #should be signal name
        self.colorChannel1Label = QLabel("ch1 color")
        # self.colorChannel1combo = QComboBox()
        self.colorChannel1Input = QPushButton()
        self.colorChannel2Label = QLabel("ch2 color")
        # self.colorChannel2combo = QComboBox()
        self.colorChannel2Input = QPushButton()
        self.lineThicknessLabel = QLabel("Line thickness")
        self.thicknessInput = QSpinBox()



        print("Elements created")

    def stylingUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#242424;color: #76D4D4; font-family: Sofia sans;")
        self.propertiesLabel.setStyleSheet("""color: #76D4D4;
                                                font-family: Sofia sans;
                                                font-weight: 600;
                                                font-size: 18px;
                                                margin-bottom:10px;
                                                """)
        self.signalNameLabel.setStyleSheet("""color: #76D4D4;
                                                font-family: Sofia sans;
                                                font-weight: 500;
                                                font-size: 16px;
                                                Padding-left:10px;;
                                                """)
        self.colorChannel1Label.setStyleSheet("""color: #EFEFEF;
                                                font-family: Sofia sans;
                                                font-weight: 400;
                                                font-size: 14px;
                                                padding-left: 15px;""")

        self.colorChannel2Label.setStyleSheet("""color: #EFEFEF;
                                                font-family: Sofia sans;
                                                font-weight: 400;
                                                font-size: 14px;
                                                padding-left: 15px;""")

        # should take color of the signal
        self.colorChannel1Input.setStyleSheet(f"""
                                                background-color:{self.signal.colors[0]}; 
                                                """)
        self.colorChannel2Input.setStyleSheet(f"""
                                                background-color:{self.signal.colors[1]};
                                                """)

        self.lineThicknessLabel.setStyleSheet("""color: #EFEFEF;
                                                font-family: Sofia sans;
                                                font-weight: 400;
                                                font-size: 14px;
                                                padding-left: 15px;""")

        self.thicknessInput.setButtonSymbols(QSpinBox.NoButtons)
        self.thicknessInput.setAlignment(Qt.AlignCenter)
        self.thicknessInput.setStyleSheet("""
                                                QSpinBox{
                                                    color: #76D4D4;
                                                    padding:2px;
                                                    border: 2px solid #76D4D4;
                                                    border-radius: 5px; 
                                                    font-size:16px;
                                                    font-weight: 600;
                                                    margin: 0 15px 0 15px ;
                                                }""")



        print("Elements is styled")

    def layoutSet(self):
        self.mainLayout = QVBoxLayout()
        self.color1Layout = QHBoxLayout()
        self.color1Layout.addWidget(self.colorChannel1Label)
        # self.color1Layout.addWidget(self.colorChannel1combo)
        self.color1Layout.addWidget(self.colorChannel1Input)

        self.color2Layout = QHBoxLayout()
        self.color2Layout.addWidget(self.colorChannel2Label)
        # self.color2Layout.addWidget(self.colorChannel2combo)
        self.color2Layout.addWidget(self.colorChannel2Input)

        self.mainLayout.addWidget(self.propertiesLabel)
        self.mainLayout.addWidget(self.signalNameLabel)
        self.mainLayout.addLayout(self.color1Layout)
        self.mainLayout.addLayout(self.color2Layout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.lineThicknessLabel)
        self.mainLayout.addWidget(self.thicknessInput)

        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        print("layout set")

    def connectingUI(self):
        self.colorChannel1Input.clicked.connect(self.open_color_dialog)
        self.colorChannel2Input.clicked.connect(self.open_color_dialog)
        print("UI panels is connected to each other")

    def setSignal(self, signal):
        self.signal = signal
        self.signalNameLabel.setText(self.signal.name)
        self.colorChannel1Input.setStyleSheet(f"background-color:{self.signal.colors[0]};")
        self.colorChannel2Input.setStyleSheet(f"background-color:{self.signal.colors[1]};")
    def open_color_dialog(self):

        color = QColorDialog.getColor()
        sender = self.sender()
        if color.isValid():
            if sender == self.colorChannel1Input:
                self.signal.changeChannel1Color(color.name())
                print("1" + color.name())
            else:
                self.signal.changeChannel2Color(color.name())
                print("2" + color.name())

            sender.setStyleSheet(f"background: {color.name()};")

            print(f"Selected color: {color.name()}")


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

    props = Properties()
    props.setSignal(heartSignal)


    main.setCentralWidget(props)

    main.resize(480, 720)
    main.show()
    sys.exit(app.exec_())

