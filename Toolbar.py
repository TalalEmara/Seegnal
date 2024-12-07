import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication, QMainWindow, QVBoxLayout, QGroupBox
from Styles.toolBarStyle import labelStyle, signalControlButtonStyle, groupBoxStyle


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeAttributes()
        self.initializeUI()
        self.connectingUI()


    def initializeAttributes(self):
        #should have viewers
        print("Attributes")


    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()


    def createUIElements(self):
        self.logoLabel = QLabel("Seegnal|")
        self.importButton = QPushButton("import")
        #Control Buttons
        self.pauseButton = QPushButton()
        self.playButton = QPushButton()
        self.backwardButton = QPushButton()
        self.forwardButton = QPushButton()
        self.rewindButton = QPushButton()
        #Linked
        self.linkedButton = QPushButton("Linked")
        #Glue
        self.glueButton = QPushButton("Glue")
        #Polar
        self.polarButton = QPushButton("Polar")
        print("Elements created")


    def stylingUI(self):
        self.logoLabel.setStyleSheet(labelStyle)
        self.logoLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.importButton.setStyleSheet(signalControlButtonStyle + "QPushButton{ background-color: #76D4D4; color: #2d2d2d;}")

        self.controlsGroupBox.setStyleSheet(groupBoxStyle)
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.backwardButton.setStyleSheet(signalControlButtonStyle)
        self.forwardButton.setStyleSheet(signalControlButtonStyle)
        self.rewindButton.setStyleSheet(signalControlButtonStyle)
        self.glueButton.setStyleSheet(signalControlButtonStyle)
        self.polarButton.setStyleSheet(signalControlButtonStyle)
        self.linkedButton.setStyleSheet(signalControlButtonStyle)

        self.pauseButton.setMaximumWidth(50)
        self.playButton.setMaximumWidth(50)
        self.backwardButton.setMaximumWidth(50)
        self.forwardButton.setMaximumWidth(50)
        self.rewindButton.setMaximumWidth(50)
        self.linkedButton.setMaximumWidth(150)

        print("Elements is styled")


    def layoutSet(self):
        self.mainLayout = QHBoxLayout()

        self.controlsGroupBox = QGroupBox("Controls")
        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.addWidget(self.pauseButton)
        self.controlsLayout.addWidget(self.playButton)
        self.controlsLayout.addWidget(self.backwardButton)
        self.controlsLayout.addWidget(self.forwardButton)
        self.controlsLayout.addWidget(self.rewindButton)
        self.controlsLayout.addWidget(self.linkedButton)
        self.controlsGroupBox.setLayout(self.controlsLayout)

        self.mainLayout.addWidget(self.logoLabel, 1)
        self.mainLayout.addWidget(self.importButton, 1)
        self.mainLayout.addWidget(self.controlsGroupBox, 3)
        self.mainLayout.addWidget(self.glueButton, 1)
        self.mainLayout.addWidget(self.polarButton, 1)
        self.mainLayout.addStretch(1)

        self.setLayout(self.mainLayout)




        print("layout set")


    def connectingUI(self):
        print("UI panels is connected to each other")

    def importSignal(self):
        print("open import window")

    def initializePolar(self):
        print("open import window")

    def linkViewers(self, viewer1, viewer2):
        print("link viewer")


if __name__ == "__main__":
        app = QApplication(sys.argv)
        # Set up the main window
        main_window = QMainWindow()
        main_window.setWindowTitle("Toolbar Test")
        main_window.resize(1600, 50)

        # Apply the background color to the main window
        main_window.setStyleSheet("background-color: #242424;")

        # Create a central widget and layout
        central_widget = QWidget()
        main_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add the ToolBar widget
        toolbar = ToolBar()
        layout.addWidget(toolbar)

        # Show the main window
        main_window.show()

        # Run the application loop
        sys.exit(app.exec_())
