import sys

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication, QMainWindow, QVBoxLayout
from Styles.toolBarStyle import labelStyle, signalControlButtonStyle


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
        self.logoLabel = QLabel("Seegnal |")
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

        self.importButton.setStyleSheet(signalControlButtonStyle)
        self.pauseButton.setStyleSheet(signalControlButtonStyle)
        self.playButton.setStyleSheet(signalControlButtonStyle)
        self.backwardButton.setStyleSheet(signalControlButtonStyle)
        self.forwardButton.setStyleSheet(signalControlButtonStyle)
        self.rewindButton.setStyleSheet(signalControlButtonStyle)
        self.linkedButton.setStyleSheet(signalControlButtonStyle)
        self.glueButton.setStyleSheet(signalControlButtonStyle)
        self.polarButton.setStyleSheet(signalControlButtonStyle)
        print("Elements is styled")


    def layoutSet(self):
        self.mainLayout = QHBoxLayout()

        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.addWidget(self.pauseButton)
        self.controlsLayout.addWidget(self.playButton)
        self.controlsLayout.addWidget(self.backwardButton)
        self.controlsLayout.addWidget(self.forwardButton)
        self.controlsLayout.addWidget(self.rewindButton)

        self.mainLayout.addWidget(self.logoLabel)
        self.mainLayout.addWidget(self.importButton)
        self.mainLayout.addLayout(self.controlsLayout)
        self.mainLayout.addWidget(self.linkedButton)
        self.mainLayout.addWidget(self.glueButton)
        self.mainLayout.addWidget(self.polarButton)



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
        main_window.resize(800, 50)

        # Apply the background color to the main window
        main_window.setStyleSheet("background-color: #2d2d2d;")

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
