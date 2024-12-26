import sys
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget, QMainWindow, \
    QFileDialog, QApplication, QComboBox
import pyqtgraph as pg
from fpdf import FPDF
import pyqtgraph.exporters
from scipy import interpolate
from scipy.interpolate import BSpline, interp1d, Rbf


class SignalCanvas(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackground("#242424")
        self.getAxis("left").setPen(pg.mkPen(color="#EFEFEF"))
        self.getAxis("bottom").setPen(pg.mkPen(color="#EFEFEF"))
        self.showGrid(x=True, y=True, alpha=0.1)
        self.signal_plot = self.plot([], [], pen=pg.mkPen(color="#D55877", width=2))

    def update_plot(self, t, signal):
        self.signal_plot.setData(t, signal)


class GlueWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Glued Signal")
        self.setStyleSheet("background-color:#242424;")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.snapshots = []
        self.signal1 = []
        self.signal2 = []
        self.signal = []
        self.time = []

        # Two canvases: one for original signals, the other for interpolated signals
        self.signal_canvas_original = SignalCanvas(self)
        self.signal_canvas_interpolated = SignalCanvas(self)

        self.title_toolbar_layout = QHBoxLayout()
        self.title = QLabel("Gluing Signals")
        self.title.setStyleSheet("color: #EFEFEF; font-size: 20px; font-weight: bold;")
        self.title.setFixedHeight(70)
        self.title_toolbar_layout.addWidget(self.title)

        self.snapshot_button = QPushButton("SnapShot", self)
        self.snapshot_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.snapshot_button.setStyleSheet("background-color: #EFEFEF; border-radius: 10px; padding: 10px;")
        self.snapshot_button.clicked.connect(self.take_snapshot)
        self.title_toolbar_layout.addWidget(self.snapshot_button)

        self.export_pdf_button = QPushButton("Export to PDF", self)
        self.export_pdf_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.export_pdf_button.setStyleSheet("background-color: #EFEFEF; border-radius: 10px; padding: 10px;")
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        self.title_toolbar_layout.addWidget(self.export_pdf_button)

        # Dropdown for interpolation methods
        self.interpolation_combobox = QComboBox(self)
        self.interpolation_combobox.addItem("Linear")
        self.interpolation_combobox.addItem("RBF")
        self.interpolation_combobox.addItem("Nearest Neighbor")
        self.interpolation_combobox.currentIndexChanged.connect(self.update_interpolation_method)

        self.title_toolbar_layout.addWidget(self.interpolation_combobox)

        graph_row = QHBoxLayout()
        graph_row.addWidget(self.signal_canvas_original)
        graph_row.addWidget(self.signal_canvas_interpolated)

        button_row = QHBoxLayout()
        self.backward_button = QPushButton("Backward")
        self.backward_button.setStyleSheet("background-color: #EFEFEF; padding: 10px; border-radius: 10px;")
        self.backward_button.setFixedSize(150, 70)
        self.backward_button.clicked.connect(self.backward)

        self.forward_button = QPushButton("Forward")
        self.forward_button.setStyleSheet("background-color: #EFEFEF; padding: 10px; border-radius: 10px;")
        self.forward_button.setFixedSize(150, 70)
        self.forward_button.clicked.connect(self.forward)

        button_row.addStretch()
        button_row.addWidget(self.backward_button)
        button_row.addWidget(self.forward_button)
        button_row.addStretch()

        main_layout.addLayout(self.title_toolbar_layout)
        main_layout.addLayout(graph_row)
        main_layout.addLayout(button_row)

        self.setMinimumSize(1000, 700)
        self.show()

    def init_plot(self, frame1_x, frame1_y, frame2_x, frame2_y):
        self.signal_canvas_original.clear()
        self.signal_canvas_interpolated.clear()
        self.signal1 = [frame1_x[0], frame1_y[0]]
        self.signal2 = [frame2_x[0], frame2_y[0]]

        self.signal_canvas_original.plot(frame1_x[0], frame1_y[0], pen=pg.mkPen(color="blue", width=2))
        self.signal_canvas_original.plot(frame2_x[0], frame2_y[0], pen=pg.mkPen(color="red", width=2))

        # Initial interpolation using the original signals
        t_interpolated, signal_interpolated = self.interpolate_signals(self.signal1, self.signal2)
        self.signal = [t_interpolated, signal_interpolated]
        self.signal_canvas_interpolated.plot(t_interpolated, signal_interpolated, pen=pg.mkPen(color="green", width=2))

    def forward(self):
        # Move the second signal forward
        self.signal2[0] = self.signal2[0] + 1
        self.update_plots()

    def backward(self):
        # Move the second signal backward
        self.signal2[0] = self.signal2[0] - 1
        self.update_plots()

    def update_plots(self):
        # Update the original signal canvas
        self.signal_canvas_original.clear()
        self.signal_canvas_original.plot(self.signal1[0], self.signal1[1], pen=pg.mkPen(color="blue", width=2))
        self.signal_canvas_original.plot(self.signal2[0], self.signal2[1], pen=pg.mkPen(color="red", width=2))

        # Update the interpolated signal canvas
        t_interpolated, signal_interpolated = self.interpolate_signals(self.signal1, self.signal2)
        self.signal_canvas_interpolated.clear()
        self.signal_canvas_interpolated.plot(t_interpolated, signal_interpolated, pen=pg.mkPen(color="green", width=2))

    from scipy.interpolate import interp1d, BSpline

    def interpolate_signals(self, signal1, signal2):
        # Select interpolation method based on user choice
        interpolation_method = self.interpolation_combobox.currentText()  # Assuming you have a combo box to select the interpolation method

        # Combine time points from both signals
        t_combined = np.unique(np.concatenate((signal1[0], signal2[0])))

        if interpolation_method == "Linear":
            # Linear interpolation
            f1 = interp1d(signal1[0], signal1[1], kind="linear", fill_value="extrapolate")
            f2 = interp1d(signal2[0], signal2[1], kind="linear", fill_value="extrapolate")
            signal_combined = f1(t_combined) + f2(t_combined)

        elif interpolation_method == "RBF":
            # Radial Basis Function interpolation (using Multiquadric function)
            f1 = Rbf(signal1[0], signal1[1], function="multiquadric")
            f2 = Rbf(signal2[0], signal2[1], function="multiquadric")
            signal_combined = f1(t_combined) + f2(t_combined)

        elif interpolation_method == "Nearest Neighbor":
            # Nearest Neighbor interpolation
            indices1 = np.searchsorted(signal1[0], t_combined, side="left")
            indices2 = np.searchsorted(signal2[0], t_combined, side="left")

            # Ensure indices are within bounds
            indices1 = np.clip(indices1, 0, len(signal1[0]) - 1)
            indices2 = np.clip(indices2, 0, len(signal2[0]) - 1)

            # Nearest Neighbor interpolation
            signal_combined = signal1[1][indices1] + signal2[1][indices2]

        return t_combined, signal_combined

    def update_interpolation_method(self):
        # Interpolate the original signals based on the selected method
        t_interpolated, signal_interpolated = self.interpolate_signals(self.signal1, self.signal2)

        # Update the original signal canvas (this will show the original signals)
        self.signal_canvas_original.clear()
        self.signal_canvas_original.plot(self.signal1[0], self.signal1[1], pen=pg.mkPen(color="blue", width=2))
        self.signal_canvas_original.plot(self.signal2[0], self.signal2[1], pen=pg.mkPen(color="red", width=2))

        # Update the interpolated signal canvas (this will show the interpolated signal)
        self.signal_canvas_interpolated.clear()
        self.signal_canvas_interpolated.plot(t_interpolated, signal_interpolated, pen=pg.mkPen(color="green", width=2))

    def take_snapshot(self):
        # Capture statistics for the interpolated signal
        snapshot = {
            "mean": np.mean(self.signal[1]),
            "std": np.std(self.signal[1]),
            "min": np.min(self.signal[1]),
            "max": np.max(self.signal[1]),
            "duration": self.signal[0][-1] - self.signal[0][0],
            "image_path": f'snapshot_{len(self.snapshots)}.png'
        }

        # Save the interpolated plot as an image
        exporter = pg.exporters.ImageExporter(self.signal_canvas_interpolated.scene())
        exporter.parameters()['width'] = 800  # Set the resolution of the saved image
        exporter.export(snapshot["image_path"])

        # Append the snapshot to the list
        self.snapshots.append(snapshot)

    def export_to_pdf(self):
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")

        if save_path:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            table_col_width = 40
            table_total_width = 2 * table_col_width
            page_width = 210
            x_offset = (page_width - table_total_width) / 2
            image_width = 180
            image_x_offset = (page_width - image_width) / 2

            for idx, snapshot in enumerate(self.snapshots):
                pdf.add_page()

                pdf.set_font("Arial", "B", 16)
                title_width = pdf.get_string_width(f"Snapshot {idx + 1}")
                pdf.set_x((page_width - title_width) / 2)
                pdf.cell(0, 10, f"Snapshot {idx + 1}", ln=True)

                pdf.ln(10)

                pdf.set_font("Arial", "B", 12)
                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, "Statistic", 1, 0, "C")
                pdf.cell(table_col_width, 10, "Value", 1, 1, "C")

                pdf.set_font("Arial", "", 12)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, "Mean", 1)
                pdf.cell(table_col_width, 10, f"{snapshot['mean']:.4f}", 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, "Std Dev", 1)
                pdf.cell(table_col_width, 10, f"{snapshot['std']:.4f}", 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, "Min", 1)
                pdf.cell(table_col_width, 10, f"{snapshot['min']:.4f}", 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, "Max", 1)
                pdf.cell(table_col_width, 10, f"{snapshot['max']:.4f}", 1, 1)

                pdf.set_x(x_offset)
                pdf.cell(table_col_width, 10, "Duration", 1)
                pdf.cell(table_col_width, 10, f"{snapshot['duration']:.4f}", 1, 1)

                pdf.ln(10)
                pdf.set_x(image_x_offset)
                pdf.image(snapshot["image_path"], w=image_width)

            pdf.output(save_path)
            print(f"PDF Report saved to {save_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlueWindow()
    sys.exit(app.exec_())
