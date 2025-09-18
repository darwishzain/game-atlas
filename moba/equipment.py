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
APPS_DIR = os.path.dirname(os.path.abspath(__file__))

class EquipmentEditor(QWidget):
    def top(self):
        self.ui = QVBoxLayout()

        file = QHBoxLayout()
        newbtn = QPushButton("+")
        file.addWidget(newbtn)
        self.urlinput = QLineEdit()
        file.addWidget(self.urlinput)
        fileopen = QPushButton("Open")
        fileopen.clicked.connect(self.openfile)
        file.addWidget(fileopen)
        self.ui.addLayout(file)

        self.layout.addLayout(self.ui)

    def openfile(self):
        self.jsonfile = os.path.abspath(os.path.join(APPS_DIR, self.urlinput.text().strip()))
        if not os.path.isfile(self.jsonfile):
            self.errors.setText("Error: File does not exist.")
            return(False)
        if not self.jsonfile.lower().endswith(".json"):
            self.errors.setText("Error: File is not a JSON.")
            return(False)
        with open(self.jsonfile) as f:
            self.data = json.load(f)
        self.errors.setText("")
        self.types = self.data['types']
        self.attributes = self.data['attributes']
        self.equipments = self.data['equipments']
        self.heroes = self.data['heroes']
        self.setWindowTitle("Equipment Codex ["+self.jsonfile+"]")
        #* Options
        options = QHBoxLayout()
        if self.jsonfile:
            generalbtn = QPushButton("General")
            generalbtn.clicked.connect(self.general)
            options.addWidget(generalbtn)
            equipmentbtn = QPushButton("Equipments")
            options.addWidget(equipmentbtn)
            equipmentbtn.clicked.connect(self.equipment)
            heroesbtn = QPushButton("Heroes")
            options.addWidget(heroesbtn)
        self.ui.addLayout(options)
        self.equipment()

    def clearcontent(self):
        while self.content.count():
            child = self.content.takeAt(0)   # grab the first item
            if child.widget():                       # if it’s a widget, delete it
                child.widget().deleteLater()
            elif child.layout():                     # if it’s a sub-layout, clear it recursively
                sublayout = child.layout()
                while sublayout.count():
                    subchild = sublayout.takeAt(0)
                    if subchild.widget():
                        subchild.widget().deleteLater()
    def general(self):
        self.title.setText("General Settings")
        self.clearcontent()
        self.titleinput = QLineEdit()
        self.titleinput.setText(self.data['title'])
        self.content.addWidget(self.titleinput)
        self.content.addWidget(QLabel("Types (comma separated):"))
        self.typesinput = QLineEdit()
        self.content.addWidget(self.typesinput)
        self.typesinput.setText(",".join(self.data['types']))
        #TODO: Attributes Editor
        self.content.addWidget(QLabel("Attributes: "))
        self.attributesinput = QTextEdit()
        self.attributesinput.setText(json.dumps(self.data['attributes'], ensure_ascii=False, indent=4))
        self.content.addWidget(self.attributesinput)
        self.content.addWidget(QLabel("Description:"))
        self.descriptioninput = QTextEdit()
        self.content.addWidget(self.descriptioninput)
        self.descriptioninput.setText(self.data['description'])
        self.creditsinput = QLineEdit()
        self.creditsinput.setText(self.data['credits'])
        self.content.addWidget(self.creditsinput)
        savebtn = QPushButton("Save General Settings")
        savebtn.clicked.connect(self.savegeneral)
        self.content.addWidget(savebtn)

    def savegeneral(self):
        self.data['title'] = self.titleinput.text().strip()
        self.data['types'] = [t.strip() for t in self.typesinput.text().split(",") if t.strip()]
        self.data['attributes'] = json.loads(self.attributesinput.toPlainText())
        self.data['description'] = self.descriptioninput.toPlainText().strip()
        self.data['credits'] = self.creditsinput.text().strip()
        self.updatejson()

    def updatejson(self):
        with open(self.jsonfile, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
#    def input(self):
#        equipmentlayout = QHBoxLayout()
#        equipmentlayout.addWidget(QLabel("New Equipment:"))
#        #* Input for equipment name
#        self.name = QLineEdit(self)
#        self.name.setPlaceholderText("Enter equipment name")
#        equipmentlayout.addWidget(self.name)
#        #* Input for equipment cost
#        self.cost = QLineEdit(self)
#        self.cost.setPlaceholderText("Enter equipment cost")
#        equipmentlayout.addWidget(self.cost)
#        #* Dropdown for equipment type
#        self.type_dropdown = QComboBox(self)
#        self.type_dropdown.addItems(types)
#        self.type_dropdown.setPlaceholderText("Select equipment type")
#        equipmentlayout.addWidget(self.type_dropdown)
#        #* Save button
#        self.save_button = QPushButton("Save Equipment", self)
#        self.save_button.clicked.connect(self.save_equipment)
#        equipmentlayout.addWidget(self.save_button)
#
#        #Attribute Layout
#        self.attributelayout = QVBoxLayout()
#        self.attribute_fields = []
#        #*Attribute Add Button
#        self.attribute_btn = QPushButton("+ Attribute", self)
#        self.attribute_btn.clicked.connect(self.add_attribute)
#        self.attributelayout.addWidget(self.attribute_btn)
#
#        self.editor.addLayout(equipmentlayout)
#        self.editor.addLayout(self.attributelayout)
    def equipment(self):
        self.title.setText("Equipments")
        types = self.data['types']
        self.clearcontent()
        inputlayout = QVBoxLayout()
        basicinput = QHBoxLayout()
        inputlayout.addLayout(basicinput)
        attributelayout = QVBoxLayout()

        basicinput.addWidget(QLabel("New Equipment:"))
        self.content.addLayout(inputlayout)
        self.name = QLineEdit(self)
        basicinput.addWidget(self.name)
        self.name.setPlaceholderText("Enter equipment name")
        self.cost = QLineEdit(self)
        basicinput.addWidget(self.cost)
        self.cost.setPlaceholderText("Enter equipment cost")
        if types:
            self.type_dropdown = QComboBox(self)
            self.type_dropdown.addItems(types)
            basicinput.addWidget(self.type_dropdown)
        else:
            self.errors.setText("Error: Types is empty. Please add types first.")
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equipment Codex")

        self.showMaximized()
        self.layout = QVBoxLayout()
        self.jsonfile = ''
        self.types = ''
        self.attributes = ''
        self.equipments = ''
        self.errors = QLabel()
        self.errors.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errors.setStyleSheet("color: red;")
        self.layout.addWidget(self.errors)
        self.top()
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        self.content = QVBoxLayout()
        self.layout.addLayout(self.content)
        self.setLayout(self.layout)


    def add_attribute(self):
        attrlayout = QHBoxLayout()
        attribute = QComboBox(self)
        for key, unit in self.attributes.items():
            attribute.addItem(key)  # store key as hidden data
        attrlayout.addWidget(attribute)
        value_input = QLineEdit(self)
        value_input.setPlaceholderText("Value")
        attrlayout.addWidget(value_input)
        self.attributelayout.addLayout(attrlayout)
        self.attribute_fields.append((attribute, value_input))

    def refresh_table(self):
        self.table.setRowCount(len(self.equipment))
        for row, item in enumerate(self.equipment):
            self.table.setItem(row, 0, QTableWidgetItem(f"{item['name']} ({item['cost']})"))
            for col, attr in enumerate(self.attributes.keys(), start=1):
                value = item['attributes'].get(attr, "")
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def save_equipment(self):
        name = self.name.text().strip()
        cost = self.cost.text().strip()
        eqtype = self.type_dropdown.currentText()
        if name and cost.isdigit():
            # Collect attribute values from the table
            attr_values = {}
            for combo, line in self.attribute_fields:
                key = combo.currentText()
                try:
                    value = int(line.text())  # convert to int if possible
                except ValueError:
                    value = line.text()  # fallback if not a number
                attr_values[key] = value
            equipment.append({
                'name': name,
                'cost': int(cost),
                'type': eqtype,
                'attributes': attr_values
            })
            self.name.clear()
            self.cost.clear()# remove all rows from attributelayout
            while self.attributelayout.count():
                child = self.attributelayout.takeAt(0)   # grab the first item
                if child.widget():                       # if it’s a widget, delete it
                    child.widget().deleteLater()
                elif child.layout():                     # if it’s a sub-layout, clear it recursively
                    sublayout = child.layout()
                    while sublayout.count():
                        subchild = sublayout.takeAt(0)
                        if subchild.widget():
                            subchild.widget().deleteLater()
            self.attribute_fields.clear()
            self.attribute_btn = QPushButton("+ Attribute", self)
            self.attribute_btn.clicked.connect(self.add_attribute)
            self.attributelayout.addWidget(self.attribute_btn)
            # Update the equipment part of the JSON file with proper indentation
            data['equipments'] = equipment
            data["updated"] = datetime.now().strftime("%d-%m-%Y")
            with open(jsonfile, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.refresh_table()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("""
        QWidget {
            font-size: 14px;
        }
        QLineEdit, QTextEdit, QComboBox {
            font-size: 14px;
            padding: 5px;
            background-color: #0f0f0f;
        }
        QPushButton {
            font-size: 14px;
            padding: 5px 10px;
    """)
    editor = EquipmentEditor()
    editor.show()
    app.exec()