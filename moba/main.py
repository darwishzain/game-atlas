import json,os
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
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtGui import QFont, QColor, QBrush
APP_DIR = os.path.dirname(os.path.abspath(__file__))
class MOBACodex(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOBA Codex")
        self.showMaximized()
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.errors = QLabel()
        self.errors.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.errors.setStyleSheet("color: red;")
        self.mainlayout.addWidget(self.errors)
        self.topui()
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainlayout.addWidget(self.title)
        self.content = QVBoxLayout()
        self.mainlayout.addLayout(self.content)

    def topui(self):
        openfile = QHBoxLayout()
        self.mainlayout.addLayout(openfile)
        self.filelist = QComboBox()
        self.filelist.addItems(os.listdir('../data/moba'))
        openfile.addWidget(self.filelist,stretch=1)
        self.loadbtn = QPushButton(">")
        self.loadbtn.clicked.connect(self.loadfile)
        openfile.addWidget(self.loadbtn,stretch=0)
        openfile.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.options = QHBoxLayout()
        self.mainlayout.addLayout(self.options)

    def loadfile(self):
        self.clearcontent(self.content)
        self.clearcontent(self.options)
        self.jsonfile = os.path.abspath(os.path.join(APP_DIR, '../data/moba', self.filelist.currentText()))
        if not os.path.isfile(self.jsonfile):
            self.errors.setText("Error: File does not exist.")
            return
        try:
            with open(self.jsonfile, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            self.errors.setText(f"Error loading JSON: {e}")
            return

        with open(self.jsonfile, 'r', encoding='utf-8') as f:
            self.rawdata = f.read()
        self.setWindowTitle("MOBA Codex: "+self.jsonfile)
        self.errors.setText("")
        self.viewbtn = QPushButton("View")
        self.viewbtn.clicked.connect(self.view)
        self.options.addWidget(self.viewbtn,stretch=0)
        self.generalbtn = QPushButton("General")
        self.generalbtn.clicked.connect(self.general)
        self.options.addWidget(self.generalbtn,stretch=0)
        self.heroesbtn = QPushButton("Heroes")
        self.heroesbtn.clicked.connect(self.addheroes)
        self.options.addWidget(self.heroesbtn,stretch=0)
        self.equipmentsbtn = QPushButton("Equipments")
        self.equipmentsbtn.clicked.connect(self.addequipments)
        self.options.addWidget(self.equipmentsbtn,stretch=0)
        self.view()

    def clearcontent(self, layout):
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

    def view(self):
        self.clearcontent(self.content)
        self.title.setText("View")
        self.content.addWidget(QLabel(self.data['title']+" ("+self.data['description']+") - "+self.data['updated']))

        equipmenttable = QTableWidget()
        equipmenttable.verticalHeader().setVisible(False)
        equipmenttable.setColumnCount(len(self.data['attributes'])+1)
        headers = ["names"]
        for attr, unit in self.data['attributes'].items():
            a = attr
            a = " ".join(word.capitalize() for word in a.split()).replace(" ", "\n")
            headers.append(a + (f"\n({unit})" if unit else ""))
        equipmenttable.setHorizontalHeaderLabels(headers)
        equipmenttable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Fill rows
        for equipment in self.data['equipments']:
            row = equipmenttable.rowCount()
            equipmenttable.insertRow(row)

            # First column: equipment name
            equipmenttable.setItem(row, 0, QTableWidgetItem(equipment['name']+" ("+str(equipment['cost'])+")"))

            # Attribute columns
            for col, attr in enumerate(self.data['attributes'], start=1):
                value = equipment.get("attributes", {}).get(attr, "")
                item = QTableWidgetItem(str(value) if value != "" else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                equipmenttable.setItem(row, col, item)
        equipmenttable.resizeRowsToContents()

        self.content.addWidget(equipmenttable)

    def addequipments(self):
        self.clearcontent(self.content)
        self.title.setText("Equipments")
        equipmentlayout = QHBoxLayout()
        self.content.addLayout(equipmentlayout)
        self.equipmentname = QLineEdit()
        self.equipmentname.setPlaceholderText("Equipment Name")
        equipmentlayout.addWidget(self.equipmentname)
        self.equipmentcost = QLineEdit()
        self.equipmentcost.setPlaceholderText("Cost")
        equipmentlayout.addWidget(self.equipmentcost)
        self.addattributebtn = QPushButton("+ Attribute")
        self.addattributebtn.clicked.connect(self.addattribute)
        equipmentlayout.addWidget(self.addattributebtn)
        savebtn = QPushButton("Save")
        savebtn.clicked.connect(self.saveequipment)
        equipmentlayout.addWidget(savebtn)
        self.attributelayout = QVBoxLayout()
        self.content.addLayout(self.attributelayout)

    def saveequipment(self):
        name = self.equipmentname.text().strip()
        cost = self.equipmentcost.text().strip()
        
    def addattribute(self):
        print("add attribute")
    def general(self):
        self.clearcontent(self.content)
        self.title.setText("General")

    def addheroes(self):
        self.clearcontent(self.content)
        self.title.setText("Heroes")
        self.heroname = QLineEdit()
        self.heroname.setPlaceholderText("Hero Name")
        self.content.addWidget(self.heroname)
if __name__ == "__main__":
    app = QApplication([])
    window = MOBACodex()
    window.show()
    app.exec()