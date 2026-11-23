import sys
import os
import subprocess
from About import About
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QVBoxLayout, QSpinBox, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__    ()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        self.setWindowTitle("Grade Correction")
        self.setMinimumSize(860, 620)
        self.setGeometry(500, 300, 860, 620)

        center_widg = QWidget(self)
        center_widg.setObjectName("centralWidget")
        self.setCentralWidget(center_widg)
        main_layout = QVBoxLayout(center_widg)
        main_layout.setContentsMargins(24, 20, 24, 24)
        main_layout.setSpacing(16)

        title = QLabel("Grade Correction")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Load a CSV, apply a bonus, and export the corrected grades.")
        subtitle.setObjectName("pageSubtitle")
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        self.table = QTableWidget(0, 3)
        self.table.setObjectName("gradesTable")
        self.table.setHorizontalHeaderLabels(["Student Id", "Original Grade", "Corrected Grade"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 220)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Bonus: average calculation (Ai assisted)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)
        content_layout.addWidget(self.table, stretch=3)

        stats_card = QWidget()
        stats_card.setObjectName("statsCard")
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(16, 16, 16, 16)
        stats_layout.setSpacing(10)

        stats_title = QLabel("Class Averages")
        stats_title.setObjectName("statsTitle")
        self.orig_avg_label = QLabel("Original: --")
        self.orig_avg_label.setObjectName("averageValue")
        self.corr_avg_label = QLabel("Corrected: --")
        self.corr_avg_label.setObjectName("averageValue")

        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(self.orig_avg_label)
        stats_layout.addWidget(self.corr_avg_label)
        stats_layout.addStretch()

        content_layout.addWidget(stats_card, stretch=1)
        main_layout.addLayout(content_layout)

        control_card = QWidget()
        control_card.setObjectName("controlCard")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(14, 12, 14, 12)
        control_layout.setSpacing(10)

        self.select_button = QPushButton("Select File")
        self.update_button = QPushButton("Update fixed grades")
        self.about_button = QPushButton("About")
        self.select_button.setObjectName("primaryButton")
        self.update_button.setObjectName("successButton")
        self.about_button.setObjectName("secondaryButton")
        self.select_button.clicked.connect(self.load_file)
        self.update_button.clicked.connect(self.update_file)
        self.about_button.clicked.connect(self.open_about)

        self.bonus_input = QSpinBox()
        self.bonus_input.setObjectName("bonusInput")
        self.bonus_input.setRange(0, 100)
        self.bonus_input.lineEdit().returnPressed.connect(self.update_bonus)
        self.bonus_input.valueChanged.connect(self.update_bonus)

        bonus_label = QLabel("Bonus")
        bonus_label.setObjectName("bonusLabel")

        control_layout.addWidget(bonus_label)
        control_layout.addWidget(self.bonus_input)
        control_layout.addStretch()
        control_layout.addWidget(self.select_button)
        control_layout.addWidget(self.about_button)
        control_layout.addWidget(self.update_button)

        control_card.setLayout(control_layout)
        main_layout.addWidget(control_card)


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

        if self.original_grades:
            orig_avg = sum(self.original_grades) / len(self.original_grades)
            corr_avg = sum(self.corrected_grades) / len(self.corrected_grades)
            self.orig_avg_label.setText(f"Original: {orig_avg:.1f}")
            self.corr_avg_label.setText(f"Corrected: {corr_avg:.1f}")
        else:
            self.orig_avg_label.setText("Original: --")
            self.corr_avg_label.setText("Corrected: --")

    def update_bonus(self, _value=None):
        if not hasattr(self, "student_ids") or not self.original_grades:
            return
        bonus = self.bonus_input.value()
        self.corrected_grades = []
        for origin in self.original_grades:
            new_grade = origin + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades.append(new_grade)
        self.update_table()

    # AI generated method for updating the table!         
    def update_file(self):
        if not self.selected_file:
            return

        with open(self.selected_file, "r", encoding="utf-8") as f:
            header = f.readline()

        with open(self.selected_file, "w", encoding="utf-8") as f:
            f.write(header)
            for s_id, corr in zip(self.student_ids, self.corrected_grades):
                f.write(f"{s_id},{corr}\n")

        if sys.platform == "win32":
            os.startfile(self.selected_file)
        elif sys.platform == "darwin":
            subprocess.run(["open", self.selected_file])
        else:
            subprocess.run(["xdg-open", self.selected_file])

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