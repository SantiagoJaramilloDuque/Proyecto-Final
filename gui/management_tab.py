from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QGroupBox, QSplitter, QDialog, QFormLayout, QDialogButtonBox,
    QMessageBox, QLabel # Importa QLabel para los mensajes de error inline
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
        self.hospital_search.setObjectName("searchLineEdit")
        self.hospital_search.textChanged.connect(self.filter_hospitals)

        self.hospital_table = QTableWidget()
        self.hospital_table.setColumnCount(2)
        self.hospital_table.setHorizontalHeaderLabels(["Nombre", "Doctores"])
        self.hospital_table.setObjectName("dataTable")

        btn_layout = QHBoxLayout()
        add_hospital_btn = QPushButton("+ Hospital")
        delete_hospital_btn = QPushButton("Eliminar")
        add_hospital_btn.setObjectName("addButton")
        delete_hospital_btn.setObjectName("deleteButton")
        add_hospital_btn.clicked.connect(self.add_hospital)
        delete_hospital_btn.clicked.connect(self.delete_hospital)
        btn_layout.addWidget(add_hospital_btn)
        btn_layout.addWidget(delete_hospital_btn)

        hospital_layout.addWidget(self.hospital_search)
        hospital_layout.addWidget(self.hospital_table)
        hospital_layout.addLayout(btn_layout)
        hospital_group.setLayout(hospital_layout)

        # --- Doctores ---
        doctor_group = QGroupBox("Doctores")
        doctor_layout = QVBoxLayout()

        self.doctor_search = QLineEdit()
        self.doctor_search.setPlaceholderText("Buscar doctor...")
        self.doctor_search.setObjectName("searchLineEdit")
        self.doctor_search.textChanged.connect(self.filter_doctors)

        self.doctor_table = QTableWidget()
        self.doctor_table.setColumnCount(3)
        self.doctor_table.setHorizontalHeaderLabels(["ID", "Nombre", "Especialidad"])
        self.doctor_table.setObjectName("dataTable")

        btn_layout = QHBoxLayout()
        add_doctor_btn = QPushButton("+ Doctor")
        delete_doctor_btn = QPushButton("Eliminar")
        add_doctor_btn.setObjectName("addButton")
        delete_doctor_btn.setObjectName("deleteButton")
        add_doctor_btn.clicked.connect(self.add_doctor)
        delete_doctor_btn.clicked.connect(self.delete_doctor)
        btn_layout.addWidget(add_doctor_btn)
        btn_layout.addWidget(delete_doctor_btn)

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
        self.hospital_table.horizontalHeader().setStretchLastSection(True)
        self.hospital_table.resizeColumnsToContents()

        doctors = self.doctor_controller.obtener_todos()
        self.doctor_table.setRowCount(len(doctors))
        for i, d in enumerate(doctors):
            self.doctor_table.setItem(i, 0, QTableWidgetItem(d.doctor_id))
            self.doctor_table.setItem(i, 1, QTableWidgetItem(d.nombre))
            self.doctor_table.setItem(i, 2, QTableWidgetItem(d.especialidad))
        self.doctor_table.horizontalHeader().setStretchLastSection(True)
        self.doctor_table.resizeColumnsToContents()


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
        name, ok = QInputDialog.getText(self, "Nuevo Hospital", "Nombre del Hospital:")
        if ok:
            cleaned_name = name.strip()
            if not cleaned_name:
                QMessageBox.warning(self, "Error de Entrada", "El nombre del hospital no puede estar vacío.",
                                    QMessageBox.Ok, QMessageBox.Ok)
                return

            # Verificar si el hospital ya existe
            if self.hospital_controller.buscar_hospital(cleaned_name):
                QMessageBox.warning(self, "Error de Duplicidad", f"Ya existe un hospital con el nombre '{cleaned_name}'.",
                                    QMessageBox.Ok, QMessageBox.Ok)
                return

            self.hospital_controller.crear_hospital(cleaned_name)
            self.refresh_data()
            self.data_updated.emit()

    def delete_hospital(self):
        row = self.hospital_table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Advertencia", "Selecciona un hospital para eliminar.",
                                    QMessageBox.Ok, QMessageBox.Ok)
            return
        name = self.hospital_table.item(row, 0).text()
        confirm = QMessageBox.question(self, "Confirmar Eliminación",
                                        f"¿Estás seguro de eliminar el hospital '{name}' y todos los doctores asociados a él? Esta acción es irreversible.",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.hospital_controller.eliminar_hospital(name)
            self.refresh_data()
            self.data_updated.emit()

    def add_doctor(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Doctor")
        layout = QFormLayout()

        id_input = QLineEdit()
        id_input.setPlaceholderText("ID del doctor (ej: D001)")
        id_error_label = QLabel("¡ID no puede estar vacío!")
        id_error_label.setProperty("class", "error") # Aplica la "clase" CSS
        id_error_label.hide()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Nombre completo del doctor")
        name_error_label = QLabel("¡Nombre no puede estar vacío!")
        name_error_label.setProperty("class", "error")
        name_error_label.hide()

        spec_input = QLineEdit()
        spec_input.setPlaceholderText("Especialidad (ej: Cardiología)")
        spec_error_label = QLabel("¡Especialidad no puede estar vacía!")
        spec_error_label.setProperty("class", "error")
        spec_error_label.hide()

        layout.addRow("ID:", id_input)
        layout.addRow(id_error_label)
        layout.addRow("Nombre:", name_input)
        layout.addRow(name_error_label)
        layout.addRow("Especialidad:", spec_input)
        layout.addRow(spec_error_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        dialog.setLayout(layout)

        # Validación personalizada antes de aceptar
        def validate_inputs():
            is_valid = True
            cleaned_id = id_input.text().strip()
            cleaned_name = name_input.text().strip()
            cleaned_spec = spec_input.text().strip()

            # Validación de campos vacíos
            if not cleaned_id:
                id_error_label.show()
                is_valid = False
            else:
                id_error_label.hide()

            if not cleaned_name:
                name_error_label.show()
                is_valid = False
            else:
                name_error_label.hide()

            if not cleaned_spec:
                spec_error_label.show()
                is_valid = False
            else:
                spec_error_label.hide()

            if not is_valid: # Si hay campos vacíos, mostramos el mensaje general y no continuamos
                QMessageBox.warning(dialog, "Campos Incompletos", "Por favor, completa todos los campos requeridos.",
                                    QMessageBox.Ok, QMessageBox.Ok)
                return


            # Validación de duplicidad para el ID del doctor
            if self.doctor_controller.buscar_doctor(cleaned_id):
                QMessageBox.warning(dialog, "Error de Duplicidad", f"Ya existe un doctor con el ID '{cleaned_id}'.",
                                    QMessageBox.Ok, QMessageBox.Ok)
                id_error_label.setText("¡Este ID ya existe!")
                id_error_label.show()
                is_valid = False
            else:
                id_error_label.hide() # Ocultar si ya no hay duplicidad

            if is_valid:
                dialog.accept() # Si todo es válido, acepta el diálogo

        # Conectar el botón OK a nuestra función de validación
        buttons.accepted.disconnect(dialog.accept) # Desconecta la conexión original
        buttons.accepted.connect(validate_inputs) # Conecta a la función de validación

        if dialog.exec_() == QDialog.Accepted:
            self.doctor_controller.crear_doctor(id_input.text().strip(), name_input.text().strip(), spec_input.text().strip())
            self.refresh_data()
            self.data_updated.emit()

    def delete_doctor(self):
        row = self.doctor_table.currentRow()
        if row == -1:
            QMessageBox.information(self, "Advertencia", "Selecciona un doctor para eliminar.",
                                    QMessageBox.Ok, QMessageBox.Ok)
            return
        doc_id = self.doctor_table.item(row, 0).text()
        confirm = QMessageBox.question(self, "Confirmar Eliminación",
                                        f"¿Estás seguro de eliminar el doctor con ID '{doc_id}'? Esta acción es irreversible.",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.doctor_controller.eliminar_doctor(doc_id)
            self.refresh_data()
            self.data_updated.emit()