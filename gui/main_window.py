from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from controller.doctor_controller import DoctorController
from controller.hospital_controller import HospitalController
from gui.management_tab import ManagementTab
from gui.assignment_tab import AssignmentTab

class HospitalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.doctor_controller = DoctorController()
        self.hospital_controller = HospitalController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sistema Hospitalario Integrado")
        self.setGeometry(100, 100, 1000, 700)

        tabs = QTabWidget()
        tabs.setObjectName("mainTabs")
        self.management_tab = ManagementTab(self.doctor_controller, self.hospital_controller)
        self.assignment_tab = AssignmentTab(self.doctor_controller, self.hospital_controller)

        self.management_tab.data_updated.connect(self.assignment_tab.refresh)
        self.assignment_tab.data_updated.connect(self.management_tab.refresh_data)

        tabs.addTab(self.management_tab, "Gestión")
        tabs.addTab(self.assignment_tab, "Asignaciones")

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = HospitalApp()
    window.show()
    sys.exit(app.exec_())