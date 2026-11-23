import sys
import os
import math
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from About import About

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.temperatures = []
        self.revenues = []
        self.selected_file = ""

        self.setWindowTitle("Ice Cream Profits")
        self.setMinimumSize(800, 600)

        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.axes = self.figure.add_subplot(111)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        controls_layout = QHBoxLayout()
        self.select_button = QPushButton("Select File")
        self.about_button = QPushButton("About")
        self.select_button.clicked.connect(self.load_file)
        self.about_button.clicked.connect(self.open_about)

        controls_layout.addWidget(self.select_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.about_button)
        main_layout.addLayout(controls_layout)

        self.draw_graph()

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Ice Cream File", "", "CSV Files (*.csv)"
        )
        if file_name:
            self.selected_file = file_name
            self.temperatures = []
            self.revenues = []

            with open(file_name, "r", encoding="utf-8") as f:
                next(f)
                for line in f:
                    parts = line.strip().split(",")
                    self.temperatures.append(float(parts[0]))
                    self.revenues.append(float(parts[1]))

            self.draw_graph()

    def draw_graph(self):
        self.axes.clear()
        if self.temperatures:
            self.axes.scatter(self.temperatures, self.revenues, s=1)
            self.axes.set_title("Ice Cream Profits vs. Temperature")
            self.axes.set_xlabel("Temperature (°C)")
            self.axes.set_ylabel("Ice Cream Profits ($)")
            self.axes.spines["top"].set_visible(False)
            self.axes.spines["right"].set_visible(False)
        self.canvas.draw()

    def open_about(self):
        self.about_window = About()
        self.about_window.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()