from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem
)

class AssignmentTab(QWidget):
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
        self.doctor_combo = QComboBox()
        assign_btn = QPushButton("Asignar")
        assign_btn.clicked.connect(self.assign_doctor)

        assign_layout.addWidget(self.hospital_combo)
        assign_layout.addWidget(self.doctor_combo)
        assign_layout.addWidget(assign_btn)
        assign_group.setLayout(assign_layout)

        self.assignment_table = QTableWidget()
        self.assignment_table.setColumnCount(3)
        self.assignment_table.setHorizontalHeaderLabels(["Hospital", "Doctor", "Especialidad"])

        layout.addWidget(assign_group)
        layout.addWidget(self.assignment_table)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        self.hospital_combo.clear()
        self.doctor_combo.clear()

        hospitals = self.hospital_controller.obtener_todos()
        doctors = self.doctor_controller.obtener_todos()

        for h in hospitals:
            self.hospital_combo.addItem(h.nombre, h.nombre)
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

    def assign_doctor(self):
        hospital_name = self.hospital_combo.currentData()
        doctor_id = self.doctor_combo.currentData()

        doctor = self.doctor_controller.buscar_doctor(doctor_id)
        if doctor:
            self.hospital_controller.agregar_doctor(hospital_name, doctor)
            self.refresh()
