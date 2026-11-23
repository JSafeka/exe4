import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QVBoxLayout, QSpinBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__    ()

        self.student_id = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        self.setWindowTitle("Grade Correction")
        self.setGeometry(500, 300, 700, 600)

        center_widg = QWidget(self)
        self.setCentralWidget(center_widg)
        main_layout = QVBoxLayout(center_widg)

        self.table = QTableWidget(50, 30)
        self.table.setHorizontalHeaderLabels(["Student Id", "Original Grade", "Corrected Grade"])

        self.select_button = QPushButton("Select File")
        self.update_button = QPushButton("Update fixed grades")
        self.about_button = QPushButton("About")

        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(0, 100)
        self.bonus_input.lineEdit.returnPressed.connect(self.update_bonus)