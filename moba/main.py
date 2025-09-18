import json,os,re
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtGui import QFont, QColor, QBrush
class MOBACodex(QWidget):
    def __init__(self):
        super().__init__()
        self.configfile = os.path.abspath('config.json')
        self.config = self.openjson(self.configfile)
        self.setWindowTitle(self.config['name'])
        self.showMaximized()
        self.mainlayout = QVBoxLayout()
        #self.mainlayout.setContentsMargins(0, 0, 0, 0)  # no outer margins
        #self.mainlayout.setSpacing(5)
        self.setLayout(self.mainlayout)
        self.ui()

    def openjson(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            jsondata = json.load(f)
        return jsondata

    def ui(self):
        menu = QVBoxLayout()
        self.mainlayout.addLayout(menu)

        self.error = QLineEdit("Error: None")
        self.error.setReadOnly(True)
        self.error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error.setStyleSheet("color: red;background-color: #101010;")
        menu.addWidget(self.error)

        selectfile = QHBoxLayout()
        menu.addLayout(selectfile)

        self.fileselection = QComboBox()
        self.fileselection.addItems(os.listdir(self.config['settings']['data']))
        self.fileselection.currentTextChanged.connect(lambda text: self.loadfile())
        selectfile.addWidget(self.fileselection,stretch=1)
        #selectfile.addWidget(QLabel("or"),stretch=0)
        #self.fileinput = QLineEdit()
        #self.fileinput.setPlaceholderText("Enter path")
        #selectfile.addWidget(self.fileinput,stretch=2)
        #self.loadbtn = QPushButton("Load")
        ##self.loadbtn.clicked.connect(self.loadfile)
        #selectfile.addWidget(self.loadbtn,stretch=0)

        self.options = QHBoxLayout()
        self.mainlayout.addLayout(self.options)

        self.content = QVBoxLayout()
        self.mainlayout.addLayout(self.content)
        self.contenttitle("Select a file to load data")

    def contenttitle(self, text):
        self.content.addWidget(QLabel(text),alignment=Qt.AlignmentFlag.AlignCenter)

    def loadfile(self):
        self.clearlayout(self.content)
        self.clearlayout(self.options)
        self.jsonfile = os.path.abspath(os.path.join(self.config['settings']['data'],self.fileselection.currentText()))
        self.jsondata = self.openjson(self.jsonfile)
        self.setWindowTitle(self.config['name'] + ": " + self.jsondata.get('title','No Title')+": "+self.jsonfile)
        self.contenttitle(self.jsondata.get('title','No Title'))
        self.optionsbtn()

    def optionsbtn(self):
        generalbtn = QPushButton("General")
        generalbtn.clicked.connect(self.generalsettings)
        self.options.addWidget(generalbtn)
        heroesbtn = QPushButton("Heroes")
        heroesbtn.clicked.connect(self.heroessettings)
        self.options.addWidget(heroesbtn)
        equipementbtn = QPushButton("Equipment")
        equipementbtn.clicked.connect(self.equipementsettings)
        self.options.addWidget(equipementbtn)
        settingsbtn = QPushButton("Settings")
        settingsbtn.clicked.connect(self.applicationsettings)
        self.options.addWidget(settingsbtn)

    def clearlayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                sublayout = child.layout()
                while sublayout.count():
                    subchild = sublayout.takeAt(0)
                    if subchild.widget():
                        subchild.widget().deleteLater()

    def generalsettings(self):
        self.clearlayout(self.content)
        self.contenttitle("General Settings")

    def heroessettings(self):
        self.clearlayout(self.content)
        self.contenttitle("Heroes Settings")

    def equipementsettings(self):
        self.clearlayout(self.content)
        self.contenttitle("Equipment Settings")

        rows = []
        attributes = [
            re.sub(r"[\(\[\{].*?[\)\]\}]", "", attr).strip() for attr in self.jsondata['attributes']
        ]
        for eq in self.jsondata['equipments']:
            row = [eq['name']+" $"+str(eq['cost'])]
            for attr in attributes:
                row.append(eq.get("attributes", {}).get(attr, ""))  # empty if missing
            rows.append(row)

        headers = ["Name"]+[a.replace(" ","\n") for a in self.jsondata['attributes']]
        equipmenttable = QTableWidget()
        equipmenttable.setRowCount(len(rows))
        equipmenttable.setColumnCount(len(headers))
        equipmenttable.setHorizontalHeaderLabels(headers)
        equipmenttable.verticalHeader().setVisible(False)
        for i,row in enumerate(rows):
            for j,value in enumerate(row):
                item = QTableWidgetItem(str(value))
                equipmenttable.setItem(i, j, item)
        equipmenttable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, equipmenttable.columnCount()):
            equipmenttable.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        equipmenttable.resizeRowsToContents()
        equipmenttable.setWordWrap(False)
        self.content.addWidget(equipmenttable)
    def applicationsettings(self):
        self.clearlayout(self.content)
        self.contenttitle("Application Settings")
        self.content.addWidget(QLabel(f"Version: {self.config.get('version','No Version')}"),alignment=Qt.AlignmentFlag.AlignCenter)

if __name__ == "__main__":
    app = QApplication([])
    window = MOBACodex()
    window.show()
    app.exec()