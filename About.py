from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        self.pic_label = QLabel()
        pixmap = QPixmap("pic.png")
        self.pic_label.setPixmap(pixmap)

        self.name_label = QLabel("Jonathan Samia")
        self.email_label = QLabel("jonatan.samia@s.afeka.ac.il")
        self.game_label = QLabel('<a href="https://ageofwargame.io/">Age of War</a>')
        # Sorry but i don't have a LinkedIn page so I replaced it with a link to a good game instead, Tnx.
        self.game_label.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(self.pic_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.game_label)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication()
    window = About()
    window.show()
    app.exec()