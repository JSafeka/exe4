import sys
import os
import math
import numpy as np
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
    QLabel
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

        # Bonus feature (Ai assisted)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        graph_container = QWidget()
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        content_layout.addWidget(graph_container, stretch=3)

        stats_card = QWidget()
        stats_card.setObjectName("statsCard")
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(16, 16, 16, 16)
        stats_layout.setSpacing(10)

        stats_title = QLabel("Data Summary")
        stats_title.setObjectName("statsTitle")
        self.max_rev_label = QLabel("Max Revenue: --")
        self.max_rev_label.setObjectName("averageValue")
        self.min_rev_label = QLabel("Min Revenue: --")
        self.min_rev_label.setObjectName("averageValue")
        self.avg_temp_label = QLabel("Avg Temp: --")
        self.avg_temp_label.setObjectName("averageValue")

        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(self.max_rev_label)
        stats_layout.addWidget(self.min_rev_label)
        stats_layout.addWidget(self.avg_temp_label)
        stats_layout.addStretch()

        content_layout.addWidget(stats_card, stretch=1)
        main_layout.addLayout(content_layout)

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
            m, b = np.polyfit(self.temperatures, self.revenues, 1)
            y_line = [m * x + b for x in self.temperatures]
            self.axes.plot(self.temperatures, y_line, color="red", linewidth=1.5)

            equation_text = f"y = {m:.2f}x + {b:.2f}"
            self.axes.text(
                0.05,
                0.92,
                equation_text,
                transform=self.axes.transAxes,
                color="red",
                fontsize=11,
                fontweight="bold",
            )

            self.axes.set_title("Ice Cream Profits vs. Temperature")
            self.axes.set_xlabel("Temperature (°C)")
            self.axes.set_ylabel("Ice Cream Profits ($)")
            self.axes.spines["top"].set_visible(False)
            self.axes.spines["right"].set_visible(False)

            max_rev = max(self.revenues)
            min_rev = min(self.revenues)
            avg_temp = sum(self.temperatures) / len(self.temperatures)

            self.max_rev_label.setText(f"Max Revenue: ${max_rev:.1f}")
            self.min_rev_label.setText(f"Min Revenue: ${min_rev:.1f}")
            self.avg_temp_label.setText(f"Avg Temp: {avg_temp:.1f}°C")

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