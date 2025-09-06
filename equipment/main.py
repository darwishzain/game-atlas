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

jsonfile = os.path.join(os.path.dirname(__file__), 'honorofkings.json')
with open(jsonfile) as f:
    data = json.load(f)
    print(data['title'])
    print(data['credits'])

types = data['types']
attributes = data['attributes']
equipment = data['equipments']
class EquipmentEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equipment Editor")
        self.showMaximized()

        newequipment_layout = QHBoxLayout()
        newequipment_layout.addWidget(QLabel("New Equipment:"))
        #* Input for equipment name
        self.layout = QVBoxLayout()
        self.name = QLineEdit(self)
        self.name.setPlaceholderText("Enter equipment name")
        newequipment_layout.addWidget(self.name)
        #* Input for equipment cost
        self.cost = QLineEdit(self)
        self.cost.setPlaceholderText("Enter equipment cost")
        newequipment_layout.addWidget(self.cost)
        #* Dropdown for equipment type
        self.type_dropdown = QComboBox(self)
        self.type_dropdown.addItems(types)
        self.type_dropdown.setPlaceholderText("Select equipment type")
        newequipment_layout.addWidget(self.type_dropdown)
        #* Save button
        self.save_button = QPushButton("Save Equipment", self)
        self.save_button.clicked.connect(self.save_equipment)
        newequipment_layout.addWidget(self.save_button)

        #Attribute Layout
        self.attributelayout = QVBoxLayout()
        self.attribute_fields = []
        #*Attribute Add Button
        self.attribute_btn = QPushButton("+ Attribute", self)
        self.attribute_btn.clicked.connect(self.add_attribute)
        self.attributelayout.addWidget(self.attribute_btn)

        self.layout.addLayout(newequipment_layout)
        self.layout.addLayout(self.attributelayout)
        self.setLayout(self.layout)

        #! Display existing equipment in a table
        self.content = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(14)
        # Set header labels with line breaks for overflow
        headers = ["Name"] + [
            f"{attr}{f' ({attributes[attr]})' if attributes[attr] else ''}".replace(" ", "\n")
            for attr in attributes.keys()
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setRowCount(len(equipment))
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for row, item in enumerate(equipment):
            self.table.setItem(row, 0, QTableWidgetItem(f"{item['name']} ({item['cost']})"))
            for col, attr in enumerate(attributes.keys(), start=1):
                value = item['attributes'].get(attr, "")
                item_widget = QTableWidgetItem(str(value))
                item_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item_widget)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.content.addWidget(self.table)

        self.layout.addLayout(self.content)

    def add_attribute(self):
        attrlayout = QHBoxLayout()
        attribute = QComboBox(self)
        for key, unit in attributes.items():
            attribute.addItem(key)  # store key as hidden data
        attrlayout.addWidget(attribute)
        value_input = QLineEdit(self)
        value_input.setPlaceholderText("Value")
        attrlayout.addWidget(value_input)
        self.attributelayout.addLayout(attrlayout)
        self.attribute_fields.append((attribute, value_input))

    def refresh_table(self):
        self.table.setRowCount(len(equipment))
        for row, item in enumerate(equipment):
            self.table.setItem(row, 0, QTableWidgetItem(f"{item['name']} ({item['cost']})"))
            for col, attr in enumerate(attributes.keys(), start=1):
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
    editor = EquipmentEditor()
    editor.show()
    app.exec()