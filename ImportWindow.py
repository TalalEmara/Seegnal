from PyQt5.QtWidgets import QMainWindow
import numpy as np
import pandas as pd
from Signal import Signal
import os

class ImportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print(f"{self}initialized")
        self.initializeUI()
        self.connectingUI()

    def initializeUI(self):
        print("UI initialized")
        self.createUIElements()
        self.layoutSet()

    def createUIElements(self):
        print("Elements created")

    def layoutSet(self):
        print("layout set")

    def connectingUI(self):
        print("UI panels is connected to each other")

    def createSignal(self, file_path):
        try:
            # get signal data
            data = pd.read_csv(file_path)
            data = data.apply(pd.to_numeric, errors='coerce').to_numpy()
            
            # get signal name
            file_name = os.path.basename(file_path)

            # Create signal instance
            self.signal = Signal(file_name, file_path, data)

            print("Data loaded successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def sendData(self,SignalInstance):
        return self.signal # returns signal instance
        print("signal is sent")

