from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap
import os


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(360, 500)
        self.setObjectName("aboutWindow")

        self.pic_label = QLabel()
        self.pic_label.setObjectName("aboutImage")
        self.pic_label.setScaledContents(True)
        pixmap = QPixmap("pic.png")
        self.pic_label.setPixmap(pixmap)

        self.github_label = QLabel('<a href="https://github.com/JSafeka/exe4.git">GitHub Repository</a>')
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setObjectName("aboutLink")

        self.name_label = QLabel("Jonathan Samia")
        self.name_label.setObjectName("aboutName")
        self.email_label = QLabel("jonatan.samia@s.afeka.ac.il")
        self.email_label.setObjectName("aboutEmail")
        self.game_label = QLabel('<a href="https://ageofwargame.io/">Age of War</a>')
        # Sorry but i don't have a LinkedIn page so I replaced it with a link to a good game instead, Tnx.
        self.game_label.setOpenExternalLinks(True)
        self.game_label.setObjectName("aboutLink")

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        layout.addWidget(self.pic_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.game_label)
        layout.addWidget(self.github_label)
        layout.addStretch()
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication()
    style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as style_file:
            app.setStyleSheet(style_file.read())
    window = About()
    window.show()
    app.exec()