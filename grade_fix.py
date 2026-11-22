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
        