import sys
from PyQt5.QtWidgets import (
    QInputDialog, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox, QComboBox, QGroupBox, QSplitter, QDialog, QInputDialog,
    QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt
from controller.doctor_controller import DoctorController
from controller.hospital_controller import HospitalController

class HospitalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.doctor_controller = DoctorController()
        self.hospital_controller = HospitalController()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Sistema Hospitalario Integrado')
        self.setGeometry(100, 100, 1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        tabs = QTabWidget()
        
        # Pestaña unificada de Gestión
        management_tab = QWidget()
        self.setup_management_tab(management_tab)
        
        # Pestaña de Asignación con búsqueda
        assignment_tab = QWidget()
        self.setup_assignment_tab(assignment_tab)
        
        tabs.addTab(management_tab, "Gestión")
        tabs.addTab(assignment_tab, "Asignaciones")
        
        main_layout.addWidget(tabs)
    
    def setup_management_tab(self, tab):
        layout = QHBoxLayout()
        
        # Splitter para dividir el espacio
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel de Hospitales
        hospital_group = QGroupBox("Hospitales")
        hospital_layout = QVBoxLayout()
        
        self.hospital_search = QLineEdit()
        self.hospital_search.setPlaceholderText("Buscar hospital...")
        self.hospital_search.textChanged.connect(self.filter_hospitals)
        
        self.hospital_table = QTableWidget()
        self.hospital_table.setColumnCount(2)
        self.hospital_table.setHorizontalHeaderLabels(["Nombre", "Doctores"])
        self.hospital_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        hospital_btn_layout = QHBoxLayout()
        self.add_hospital_btn = QPushButton("+ Hospital")
        self.add_hospital_btn.clicked.connect(self.show_add_hospital_dialog)
        self.delete_hospital_btn = QPushButton("Eliminar")
        self.delete_hospital_btn.clicked.connect(self.delete_hospital)
        
        hospital_btn_layout.addWidget(self.add_hospital_btn)
        hospital_btn_layout.addWidget(self.delete_hospital_btn)
        
        hospital_layout.addWidget(self.hospital_search)
        hospital_layout.addWidget(self.hospital_table)
        hospital_layout.addLayout(hospital_btn_layout)
        hospital_group.setLayout(hospital_layout)
        
        # Panel de Doctores
        doctor_group = QGroupBox("Doctores")
        doctor_layout = QVBoxLayout()
        
        self.doctor_search = QLineEdit()
        self.doctor_search.setPlaceholderText("Buscar doctor...")
        self.doctor_search.textChanged.connect(self.filter_doctors)
        
        self.doctor_table = QTableWidget()
        self.doctor_table.setColumnCount(3)
        self.doctor_table.setHorizontalHeaderLabels(["ID", "Nombre", "Especialidad"])
        self.doctor_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        doctor_btn_layout = QHBoxLayout()
        self.add_doctor_btn = QPushButton("+ Doctor")
        self.add_doctor_btn.clicked.connect(self.show_add_doctor_dialog)
        self.delete_doctor_btn = QPushButton("Eliminar")
        self.delete_doctor_btn.clicked.connect(self.delete_doctor)
        
        doctor_btn_layout.addWidget(self.add_doctor_btn)
        doctor_btn_layout.addWidget(self.delete_doctor_btn)
        
        doctor_layout.addWidget(self.doctor_search)
        doctor_layout.addWidget(self.doctor_table)
        doctor_layout.addLayout(doctor_btn_layout)
        doctor_group.setLayout(doctor_layout)
        
        splitter.addWidget(hospital_group)
        splitter.addWidget(doctor_group)
        splitter.setSizes([400, 400])
        
        layout.addWidget(splitter)
        tab.setLayout(layout)
        self.refresh_management_data()
    
    def setup_assignment_tab(self, tab):
        layout = QVBoxLayout()
        
        # Panel de Asignación
        assign_group = QGroupBox("Asignar Doctor a Hospital")
        assign_layout = QHBoxLayout()
        
        self.assign_hospital_combo = QComboBox()
        self.assign_doctor_combo = QComboBox()
        
        assign_btn = QPushButton("Asignar")
        assign_btn.clicked.connect(self.assign_doctor)
        
        assign_layout.addWidget(self.assign_hospital_combo)
        assign_layout.addWidget(self.assign_doctor_combo)
        assign_layout.addWidget(assign_btn)
        assign_group.setLayout(assign_layout)
        
        # Tabla de Resultados
        self.assignment_table = QTableWidget()
        self.assignment_table.setColumnCount(3)
        self.assignment_table.setHorizontalHeaderLabels(["Hospital", "Doctor", "Especialidad"])
        
        layout.addWidget(assign_group)
        layout.addWidget(self.assignment_table)
        
        tab.setLayout(layout)
        self.refresh_assignment_data()
    
    # Métodos de actualización de datos
    def refresh_management_data(self):
        # Actualizar tabla de hospitales
        hospitals = self.hospital_controller.obtener_todos()
        self.hospital_table.setRowCount(len(hospitals))
        
        for i, hospital in enumerate(hospitals):
            self.hospital_table.setItem(i, 0, QTableWidgetItem(hospital.nombre))
            self.hospital_table.setItem(i, 1, QTableWidgetItem(str(len(hospital.doctores))))
        
        # Actualizar tabla de doctores
        doctors = self.doctor_controller.obtener_todos()
        self.doctor_table.setRowCount(len(doctors))
        
        for i, doctor in enumerate(doctors):
            self.doctor_table.setItem(i, 0, QTableWidgetItem(doctor.doctor_id))
            self.doctor_table.setItem(i, 1, QTableWidgetItem(doctor.nombre))
            self.doctor_table.setItem(i, 2, QTableWidgetItem(doctor.especialidad))
    
    def refresh_assignment_data(self):
        # Actualizar comboboxes
        self.assign_hospital_combo.clear()
        self.assign_doctor_combo.clear()
        
        hospitals = self.hospital_controller.obtener_todos()
        doctors = self.doctor_controller.obtener_todos()
        
        for hospital in hospitals:
            self.assign_hospital_combo.addItem(hospital.nombre, hospital.nombre)
            
        for doctor in doctors:
            self.assign_doctor_combo.addItem(f"{doctor.nombre} ({doctor.doctor_id})", doctor.doctor_id)
        
        # Actualizar tabla de asignaciones
        self.update_assignment_table()
    
    # Métodos de filtrado y búsqueda
    def filter_hospitals(self):
        text = self.hospital_search.text().lower()
        for i in range(self.hospital_table.rowCount()):
            item = self.hospital_table.item(i, 0)
            self.hospital_table.setRowHidden(i, text not in item.text().lower())
    
    def filter_doctors(self):
        text = self.doctor_search.text().lower()
        for i in range(self.doctor_table.rowCount()):
            match = False
            for j in range(self.doctor_table.columnCount()):
                item = self.doctor_table.item(i, j)
                if text in item.text().lower():
                    match = True
                    break
            self.doctor_table.setRowHidden(i, not match)
    
    def search_assignments(self):
        hospital_text = self.search_hospital_input.text().lower()
        doctor_text = self.search_doctor_input.text().lower()
        
        all_hospitals = self.hospital_controller.obtener_todos()
        results = []
        
        for hospital in all_hospitals:
            if hospital_text and hospital_text not in hospital.nombre.lower():
                continue
                
            for doctor in hospital.doctores:
                if (not doctor_text or 
                    doctor_text in doctor.nombre.lower() or 
                    doctor_text in doctor.doctor_id.lower() or
                    doctor_text in doctor.especialidad.lower()):
                    results.append((hospital, doctor))
        
        self.assignment_table.setRowCount(len(results))
        for i, (hospital, doctor) in enumerate(results):
            self.assignment_table.setItem(i, 0, QTableWidgetItem(hospital.nombre))
            self.assignment_table.setItem(i, 1, QTableWidgetItem(doctor.nombre))
            self.assignment_table.setItem(i, 2, QTableWidgetItem(doctor.especialidad))
    
    # Métodos de diálogo
    def show_add_hospital_dialog(self):
        name, ok = QInputDialog.getText(self, 'Nuevo Hospital', 'Nombre del hospital:')
        if ok and name:
            self.hospital_controller.crear_hospital(name)
            self.refresh_management_data()
            self.refresh_assignment_data()
    
    def show_add_doctor_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Doctor")
        
        layout = QFormLayout()
        
        id_input = QLineEdit()
        name_input = QLineEdit()
        specialty_input = QLineEdit()
        
        layout.addRow("ID:", id_input)
        layout.addRow("Nombre:", name_input)
        layout.addRow("Especialidad:", specialty_input)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        
        layout.addRow(btn_box)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            self.doctor_controller.crear_doctor(
                id_input.text(),
                name_input.text(),
                specialty_input.text()
            )
            self.refresh_management_data()
            self.refresh_assignment_data()
    
    # Métodos de acciones
    def delete_hospital(self):
        selected = self.hospital_table.currentRow()
        if selected == -1:
            return
            
        hospital_name = self.hospital_table.item(selected, 0).text()
        reply = QMessageBox.question(
            self, 'Confirmar',
            f'¿Eliminar el hospital "{hospital_name}" y todas sus asignaciones?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.hospital_controller.eliminar_hospital(hospital_name)
            self.refresh_management_data()
            self.refresh_assignment_data()
    
    def delete_doctor(self):
        selected = self.doctor_table.currentRow()
        if selected == -1:
            return
            
        doctor_id = self.doctor_table.item(selected, 0).text()
        reply = QMessageBox.question(
            self, 'Confirmar',
            f'¿Eliminar al doctor con ID "{doctor_id}" y todas sus asignaciones?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.doctor_controller.eliminar_doctor(doctor_id)
            self.refresh_management_data()
            self.refresh_assignment_data()
    
    def assign_doctor(self):
        hospital_name = self.assign_hospital_combo.currentData()
        doctor_id = self.assign_doctor_combo.currentData()
        
        if not hospital_name or not doctor_id:
            return
            
        doctor = self.doctor_controller.buscar_doctor(doctor_id)
        if doctor:
            self.hospital_controller.agregar_doctor(hospital_name, doctor)
            self.update_assignment_table()
            self.refresh_management_data()
    
    def update_assignment_table(self):
        hospitals = self.hospital_controller.obtener_todos()
        self.assignment_table.setRowCount(0)
        
        for hospital in hospitals:
            for doctor in hospital.doctores:
                row = self.assignment_table.rowCount()
                self.assignment_table.insertRow(row)
                self.assignment_table.setItem(row, 0, QTableWidgetItem(hospital.nombre))
                self.assignment_table.setItem(row, 1, QTableWidgetItem(doctor.nombre))
                self.assignment_table.setItem(row, 2, QTableWidgetItem(doctor.especialidad))

def main():
    app = QApplication(sys.argv)
    window = HospitalApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()