from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import pyqtSignal 

class AssignmentTab(QWidget):
    data_updated = pyqtSignal() 

    def __init__(self, doctor_controller, hospital_controller):
        super().__init__()
        self.doctor_controller = doctor_controller
        self.hospital_controller = hospital_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        assign_group = QGroupBox("Asignar Doctor a Hospital")
        assign_layout = QHBoxLayout()

        self.hospital_combo = QComboBox()
        self.hospital_combo.setObjectName("hospitalCombo")
        self.doctor_combo = QComboBox()
        self.doctor_combo.setObjectName("doctorCombo")

        assign_btn = QPushButton("Asignar")
        assign_btn.setObjectName("assignButton")
        assign_btn.clicked.connect(self.assign_doctor)

        assign_layout.addWidget(self.hospital_combo)
        assign_layout.addWidget(self.doctor_combo)
        assign_layout.addWidget(assign_btn)
        assign_group.setLayout(assign_layout)

        self.assignment_table = QTableWidget()
        self.assignment_table.setColumnCount(3)
        self.assignment_table.setHorizontalHeaderLabels(["Hospital", "Doctor", "Especialidad"])
        self.assignment_table.setObjectName("dataTable")

        layout.addWidget(assign_group)
        layout.addWidget(self.assignment_table)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        self.hospital_combo.clear()
        self.doctor_combo.clear()

        hospitals = self.hospital_controller.obtener_todos()
        doctors = self.doctor_controller.obtener_todos()

        if not hospitals:
            self.hospital_combo.addItem("No hay hospitales", None)
        else:
            for h in hospitals:
                self.hospital_combo.addItem(h.nombre, h.nombre)

        if not doctors:
            self.doctor_combo.addItem("No hay doctores", None)
        else:
            for d in doctors:
                self.doctor_combo.addItem(f"{d.nombre} ({d.doctor_id})", d.doctor_id)

        self.assignment_table.setRowCount(0)
        for h in hospitals:
            for d in h.doctores:
                row = self.assignment_table.rowCount()
                self.assignment_table.insertRow(row)
                self.assignment_table.setItem(row, 0, QTableWidgetItem(h.nombre))
                self.assignment_table.setItem(row, 1, QTableWidgetItem(d.nombre))
                self.assignment_table.setItem(row, 2, QTableWidgetItem(d.especialidad))
        self.assignment_table.horizontalHeader().setStretchLastSection(True)
        self.assignment_table.resizeColumnsToContents()

    def assign_doctor(self):
        hospital_name = self.hospital_combo.currentData()
        doctor_id = self.doctor_combo.currentData()

        if hospital_name is None:
            QMessageBox.warning(self, "Error de Asignación", "Por favor, selecciona un hospital.",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

        if doctor_id is None:
            QMessageBox.warning(self, "Error de Asignación", "Por favor, selecciona un doctor.",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

        doctor = self.doctor_controller.buscar_doctor(doctor_id)
        if doctor:
            hospital = self.hospital_controller.buscar_hospital(hospital_name)
            if hospital and doctor in hospital.doctores:
                QMessageBox.information(self, "Información", f"El doctor '{doctor.nombre}' ya está asignado a '{hospital_name}'.",
                                    QMessageBox.Ok, QMessageBox.Ok)
                return
            else:
                self.hospital_controller.agregar_doctor(hospital_name, doctor)
                QMessageBox.information(self, "Asignación Exitosa", f"Doctor '{doctor.nombre}' asignado a '{hospital_name}'.",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.refresh()
                self.data_updated.emit() 