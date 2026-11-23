import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QVBoxLayout, QSpinBox, QFileDialog, QTableWidgetItem

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

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["Student Id", "Original Grade", "Corrected Grade"])
        main_layout.addWidget(self.table)

        control_layout = QHBoxLayout()

        self.select_button = QPushButton("Select File")
        self.update_button = QPushButton("Update fixed grades")
        self.about_button = QPushButton("About")
        self.select_button.clicked.connect(self.load_file)

        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(0, 100)
        self.bonus_input.lineEdit().returnPressed.connect(self.update_bonus)

        control_layout.addWidget(self.select_button)
        control_layout.addWidget(self.update_button)
        control_layout.addWidget(self.about_button)
        control_layout.addWidget(self.bonus_input)
        control_layout.addWidget(QLabel("Bonus:"))

        main_layout.addLayout(control_layout)


    # AI generated method for updating the table! 
    def load_file(self):
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Select Grades File", "", "CSV Files (*.csv)"
            )
            if file_name:
                self.selected_file = file_name
                self.student_ids = []
                self.original_grades = []
                self.corrected_grades = []

                with open(file_name, "r", encoding="utf-8") as f:
                    next(f)  # Skip header row
                    for line in f:
                        parts = line.strip().split(",")
                        student_id = parts[0]
                        grade = int(parts[1])
                        self.student_ids.append(student_id)
                        self.original_grades.append(grade)
                        self.corrected_grades.append(grade)

                self.update_table()
                
    # AI generated method for updating the table! 
    def update_table(self):
        self.table.setRowCount(len(self.student_ids))
        for row, (s_id, orig, corr) in enumerate(
            zip(self.student_ids, self.original_grades, self.corrected_grades)
            ):
            self.table.setItem(row, 0, QTableWidgetItem(str(s_id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(orig)))
            self.table.setItem(row, 2, QTableWidgetItem(str(corr)))


    def update_bonus(self):
        bonus = self.bonus_input.value()
        self.corrected_grades = []
        for origin in self.original_grades:
            new_grade = origin + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades.append(new_grade)
        self.update_table()



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()