import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init()

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
        