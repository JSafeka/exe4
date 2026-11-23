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
        self.setMinimumSize(980, 650)
        self.resize(1100, 720)

        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        title = QLabel("Ice Cream Profits")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Explore the relationship between temperature and revenue.")
        subtitle.setObjectName("pageSubtitle")
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        self.figure = Figure(figsize=(8, 5), facecolor="#111827")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setObjectName("chartCanvas")
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setObjectName("chartToolbar")
        self.figure.subplots_adjust(left=0.10, right=0.98, top=0.93, bottom=0.12)
        self.axes = self.figure.add_subplot(111, facecolor="#1f2937")

        # Bonus feature (Ai assisted)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        graph_container = QWidget()
        graph_container.setObjectName("graphCard")
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(10, 8, 10, 10)
        graph_layout.setSpacing(6)
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
        controls_layout.setContentsMargins(14, 12, 14, 12)
        controls_layout.setSpacing(10)
        self.select_button = QPushButton("Select File")
        self.about_button = QPushButton("About")
        self.select_button.setObjectName("primaryButton")
        self.about_button.setObjectName("secondaryButton")
        self.select_button.clicked.connect(self.load_file)
        self.about_button.clicked.connect(self.open_about)

        controls_layout.addWidget(self.select_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.about_button)
        controls_card = QWidget()
        controls_card.setObjectName("controlCard")
        controls_card.setLayout(controls_layout)
        main_layout.addWidget(controls_card)

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
        self.axes.set_facecolor("#1f2937")
        if self.temperatures:
            self.axes.scatter(
                self.temperatures,
                self.revenues,
                s=1,
                c="#60a5fa",
                edgecolors="#bfdbfe",
                linewidths=0.7,
                alpha=0.92,
            )
            m, b = np.polyfit(self.temperatures, self.revenues, 1)
            x_sorted = sorted(self.temperatures)
            y_line = [m * x + b for x in x_sorted]
            self.axes.plot(x_sorted, y_line, color="#fb7185", linewidth=2.2)

            equation_text = f"y = {m:.2f}x + {b:.2f}"
            self.axes.text(
                0.05,
                0.92,
                equation_text,
                transform=self.axes.transAxes,
                color="#fda4af",
                fontsize=11,
                fontweight="bold",
                bbox={"boxstyle": "round,pad=0.5", "facecolor": "#111827", "edgecolor": "#374151", "alpha": 0.95},
            )

            self.axes.set_title("Ice Cream Profits vs. Temperature")
            self.axes.set_xlabel("Temperature (°C)")
            self.axes.set_ylabel("Ice Cream Profits ($)")
            self.axes.spines["top"].set_visible(False)
            self.axes.spines["right"].set_visible(False)
            self.axes.spines["left"].set_color("#4b5563")
            self.axes.spines["bottom"].set_color("#4b5563")
            self.axes.tick_params(colors="#d1d5db")
            self.axes.xaxis.label.set_color("#d1d5db")
            self.axes.yaxis.label.set_color("#d1d5db")
            self.axes.title.set_color("#f9fafb")
            self.axes.grid(True, color="#374151", linewidth=0.8, alpha=0.75)

            max_rev = max(self.revenues)
            min_rev = min(self.revenues)
            avg_temp = sum(self.temperatures) / len(self.temperatures)

            self.max_rev_label.setText(f"Max Revenue: ${max_rev:.1f}")
            self.min_rev_label.setText(f"Min Revenue: ${min_rev:.1f}")
            self.avg_temp_label.setText(f"Avg Temp: {avg_temp:.1f}°C")
        else:
            self.axes.set_title("Load a CSV to view the revenue graph")
            self.axes.set_xlabel("Temperature (°C)")
            self.axes.set_ylabel("Ice Cream Profits ($)")
            self.axes.spines["left"].set_color("#4b5563")
            self.axes.spines["bottom"].set_color("#4b5563")
            self.axes.tick_params(colors="#d1d5db")
            self.axes.xaxis.label.set_color("#d1d5db")
            self.axes.yaxis.label.set_color("#d1d5db")
            self.axes.title.set_color("#f9fafb")
            self.axes.grid(True, color="#374151", linewidth=0.8, alpha=0.75)

        self.canvas.draw()

    def open_about(self):
        self.about_window = About()
        self.about_window.show()

def main():
    app = QApplication(sys.argv)
    style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()