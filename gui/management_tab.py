from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QGroupBox, QSplitter, QTableWidget, QTableWidgetItem, QDialog,
    QFormLayout, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

class ManagementTab(QWidget):
    data_updated = pyqtSignal()

    def __init__(self, doctor_controller, hospital_controller):
        super().__init__()
        self.doctor_controller = doctor_controller
        self.hospital_controller = hospital_controller
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # --- Hospitales ---
        hospital_group = QGroupBox("Hospitales")
        hospital_layout = QVBoxLayout()

        self.hospital_search = QLineEdit()
        self.hospital_search.setPlaceholderText("Buscar hospital...")
        self.hospital_search.textChanged.connect(self.filter_hospitals)

        self.hospital_table = QTableWidget()
        self.hospital_table.setColumnCount(2)
        self.hospital_table.setHorizontalHeaderLabels(["Nombre", "Doctores"])

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Hospital")
        delete_btn = QPushButton("Eliminar")
        add_btn.clicked.connect(self.add_hospital)
        delete_btn.clicked.connect(self.delete_hospital)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)

        hospital_layout.addWidget(self.hospital_search)
        hospital_layout.addWidget(self.hospital_table)
        hospital_layout.addLayout(btn_layout)
        hospital_group.setLayout(hospital_layout)

        # --- Doctores ---
        doctor_group = QGroupBox("Doctores")
        doctor_layout = QVBoxLayout()

        self.doctor_search = QLineEdit()
        self.doctor_search.setPlaceholderText("Buscar doctor...")
        self.doctor_search.textChanged.connect(self.filter_doctors)

        self.doctor_table = QTableWidget()
        self.doctor_table.setColumnCount(3)
        self.doctor_table.setHorizontalHeaderLabels(["ID", "Nombre", "Especialidad"])

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Doctor")
        delete_btn = QPushButton("Eliminar")
        add_btn.clicked.connect(self.add_doctor)
        delete_btn.clicked.connect(self.delete_doctor)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)

        doctor_layout.addWidget(self.doctor_search)
        doctor_layout.addWidget(self.doctor_table)
        doctor_layout.addLayout(btn_layout)
        doctor_group.setLayout(doctor_layout)

        splitter.addWidget(hospital_group)
        splitter.addWidget(doctor_group)
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.refresh_data()

    def refresh_data(self):
        hospitals = self.hospital_controller.obtener_todos()
        self.hospital_table.setRowCount(len(hospitals))
        for i, h in enumerate(hospitals):
            self.hospital_table.setItem(i, 0, QTableWidgetItem(h.nombre))
            self.hospital_table.setItem(i, 1, QTableWidgetItem(str(len(h.doctores))))

        doctors = self.doctor_controller.obtener_todos()
        self.doctor_table.setRowCount(len(doctors))
        for i, d in enumerate(doctors):
            self.doctor_table.setItem(i, 0, QTableWidgetItem(d.doctor_id))
            self.doctor_table.setItem(i, 1, QTableWidgetItem(d.nombre))
            self.doctor_table.setItem(i, 2, QTableWidgetItem(d.especialidad))

    def filter_hospitals(self):
        text = self.hospital_search.text().lower()
        for i in range(self.hospital_table.rowCount()):
            item = self.hospital_table.item(i, 0)
            self.hospital_table.setRowHidden(i, text not in item.text().lower())

    def filter_doctors(self):
        text = self.doctor_search.text().lower()
        for i in range(self.doctor_table.rowCount()):
            visible = any(text in self.doctor_table.item(i, j).text().lower() for j in range(3))
            self.doctor_table.setRowHidden(i, not visible)

    def add_hospital(self):
        from PyQt5.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Nuevo Hospital", "Nombre:")
        if ok and name:
            self.hospital_controller.crear_hospital(name)
            self.refresh_data()
            self.data_updated.emit()

    def delete_hospital(self):
        row = self.hospital_table.currentRow()
        if row == -1:
            return
        name = self.hospital_table.item(row, 0).text()
        confirm = QMessageBox.question(self, "Confirmar", f"¿Eliminar el hospital '{name}'?",
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.hospital_controller.eliminar_hospital(name)
            self.refresh_data()
            self.data_updated.emit()

    def add_doctor(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Doctor")
        layout = QFormLayout()
        id_input = QLineEdit()
        name_input = QLineEdit()
        spec_input = QLineEdit()
        layout.addRow("ID:", id_input)
        layout.addRow("Nombre:", name_input)
        layout.addRow("Especialidad:", spec_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            self.doctor_controller.crear_doctor(id_input.text(), name_input.text(), spec_input.text())
            self.refresh_data()
            self.data_updated.emit()

    def delete_doctor(self):
        row = self.doctor_table.currentRow()
        if row == -1:
            return
        doc_id = self.doctor_table.item(row, 0).text()
        confirm = QMessageBox.question(self, "Confirmar", f"¿Eliminar el doctor con ID '{doc_id}'?",
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.doctor_controller.eliminar_doctor(doc_id)
            self.refresh_data()
            self.data_updated.emit()
