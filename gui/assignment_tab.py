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
        self._setup_ui() 
        self._apply_styles() 
    def _setup_ui(self):
        main_layout = QVBoxLayout(self) 

        assign_group = QGroupBox("Asignar Doctor a Hospital")
        assign_group.setObjectName("assignGroupBox")
        assign_layout = QHBoxLayout(assign_group) 

        self.hospital_combo = QComboBox()
        self.hospital_combo.setPlaceholderText("Seleccionar Hospital")
        self.hospital_combo.setObjectName("hospitalCombo")

        self.doctor_combo = QComboBox()
        self.doctor_combo.setPlaceholderText("Seleccionar Doctor")
        self.doctor_combo.setObjectName("doctorCombo")

        assign_btn = QPushButton("Asignar")
        assign_btn.setObjectName("assignButton")
        assign_btn.clicked.connect(self.assign_doctor)

        assign_layout.addWidget(self.hospital_combo)
        assign_layout.addWidget(self.doctor_combo)
        assign_layout.addWidget(assign_btn)
        
        self.assignment_table = QTableWidget()
        self.assignment_table.setColumnCount(3)
        self.assignment_table.setHorizontalHeaderLabels(["Hospital", "Doctor", "Especialidad"])
        self.assignment_table.setObjectName("dataTable")

        main_layout.addWidget(assign_group)
        main_layout.addWidget(self.assignment_table)

        self.refresh()

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: "Segoe UI", sans-serif;
                color: #333333;
            }

            QGroupBox#assignGroupBox {
                border: 2px solid #007BFF;
                border-radius: 10px;
                margin-top: 10px;
                background-color: #ffffff;
                padding: 15px;
            }

            QGroupBox#assignGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 15px;
                background-color: #007BFF;
                color: white;
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 16px;
                font-weight: bold;
            }

            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 8px 10px;
                min-width: 150px;
                background-color: #ffffff;
                font-size: 14px;
                color: #555555;
            }
            QComboBox:hover {
                border-color: #007BFF;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 30px;
                background-color: transparent;
            }
            QComboBox::down-arrow {
                image: url(./icons/arrow_down.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
                selection-background-color: #ADD8E6;
                selection-color: #333333;
                padding: 5px;
                font-size: 14px;
            }

            QPushButton#assignButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 10px 25px;
                font-size: 15px;
                font-weight: bold;
                margin-left: 10px;
            }
            QPushButton#assignButton:hover {
                background-color: #218838;
            }
            QPushButton#assignButton:pressed {
                background-color: #196f2e;
            }

            QTableWidget#dataTable {
                border: 1px solid #dddddd;
                border-radius: 8px;
                font-size: 13px;
                background-color: #fefefe;
                gridline-color: #eeeeee;
                margin-top: 20px;
            }
            QTableWidget#dataTable QHeaderView::section {
                background-color: #607D8B;
                color: white;
                padding: 8px;
                border: 1px solid #78909C;
                font-weight: bold;
            }
            QTableWidget#dataTable QHeaderView::section:hover {
                background-color: #78909C;
            }
            QTableWidget#dataTable::item {
                padding: 5px;
            }
            QTableWidget#dataTable::item:selected {
                background-color: #9FA8DA;
                color: #333333;
            }
            QTableWidget#dataTable::item:hover {
                background-color: #E8EAF6;
            }
            QTableWidget#dataTable {
                alternate-background-color: #f9f9f9;
            }
        """)

    def refresh(self):
        self.hospital_combo.clear()
        self.doctor_combo.clear()

        hospitals = self.hospital_controller.obtener_todos()
        doctors = self.doctor_controller.obtener_todos()

        if not hospitals:
            self.hospital_combo.addItem("No hay hospitales disponibles", None)
        else:
            self.hospital_combo.addItem("Seleccionar Hospital", None)
            for h in hospitals:
                self.hospital_combo.addItem(h.nombre, h.nombre)

        if not doctors:
            self.doctor_combo.addItem("No hay doctores disponibles", None)
        else:
            self.doctor_combo.addItem("Seleccionar Doctor", None)
            for d in doctors:
                self.doctor_combo.addItem(f"{d.nombre} (ID: {d.doctor_id})", d.doctor_id)

        self.assignment_table.setRowCount(0) 
        for h in hospitals:
            for d in h.doctores:
                row_pos = self.assignment_table.rowCount()
                self.assignment_table.insertRow(row_pos)
                self.assignment_table.setItem(row_pos, 0, QTableWidgetItem(h.nombre))
                self.assignment_table.setItem(row_pos, 1, QTableWidgetItem(d.nombre))
                self.assignment_table.setItem(row_pos, 2, QTableWidgetItem(d.especialidad))
        self.assignment_table.horizontalHeader().setStretchLastSection(True)
        self.assignment_table.resizeColumnsToContents()


    def assign_doctor(self):
        hospital_name = self.hospital_combo.currentData()
        doctor_id = self.doctor_combo.currentData()

        if hospital_name is None or doctor_id is None:
            QMessageBox.warning(self, "Error de Asignación", "Por favor, selecciona un hospital y un doctor válidos.",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

        doctor = self.doctor_controller.buscar_doctor(doctor_id)
        hospital_a_asignar = self.hospital_controller.buscar_hospital(hospital_name)

        if not doctor or not hospital_a_asignar:
            QMessageBox.critical(self, "Error Interno", "No se pudo encontrar el doctor o el hospital seleccionado. Por favor, recarga la aplicación.",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

        hospital_actual_del_doctor = None
        todos_los_hospitales = self.hospital_controller.obtener_todos()
        for h in todos_los_hospitales:
            if doctor in h.doctores:
                hospital_actual_del_doctor = h
                break 

        if hospital_actual_del_doctor is not None:
            QMessageBox.warning(self, "Doctor Ya Asignado",
                                f"El doctor '{doctor.nombre}' (ID: {doctor.doctor_id}) ya está asignado a '{hospital_actual_del_doctor.nombre}'. "
                                "Un doctor solo puede estar asignado a un hospital a la vez.",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

        if doctor in hospital_a_asignar.doctores:
            QMessageBox.information(self, "Información", f"El doctor '{doctor.nombre}' ya está asignado a '{hospital_a_asignar.nombre}'.",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.hospital_controller.agregar_doctor(hospital_a_asignar.nombre, doctor)
            QMessageBox.information(self, "Asignación Exitosa", f"Doctor '{doctor.nombre}' asignado a '{hospital_a_asignar.nombre}'.",
                                    QMessageBox.Ok, QMessageBox.Ok)
            self.refresh()
            self.data_updated.emit()
