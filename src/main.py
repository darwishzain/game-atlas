import json, os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtGui import QFont, QColor, QBrush

class GameAtlas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.config = self.openjson('config.json')
        self.setWindowTitle(self.config['title'])

        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)

        self.header = QHBoxLayout()
        self.layout.addLayout(self.header)

        game = QComboBox()
        game.addItems(['select game','albiononline','honorofkings'])
        self.header.addWidget(game)
        game.currentIndexChanged.connect(lambda: self.selectgame(game.currentText()))

        self.content = QVBoxLayout()
        self.layout.addLayout(self.content)

    def selectgame(self, game):
        if game == 'albiononline':
            self.albiononline()
        elif game == 'honorofkings':
            self.honorofkings()
    def albiononline(self):
        print("AO")
    def honorofkings(self):
        print("HOK")
    def openjson(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
        return jsondata

if __name__ == "__main__":
    app = QApplication([])
    window = GameAtlas()
    window.show()
    app.exec()
