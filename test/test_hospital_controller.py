import unittest
from controller.hospital_controller import HospitalController
from controller.doctor_controller import DoctorController

class TestHospitalController(unittest.TestCase):
    def setUp(self):
        self.hospital_ctrl = HospitalController()
        self.doctor_ctrl = DoctorController()

    def test_crear_hospital(self):
        hospital = self.hospital_ctrl.crear_hospital("San José")
        self.assertEqual(hospital.nombre, "San José")

    def test_buscar_hospital(self):
        self.hospital_ctrl.crear_hospital("San Pedro")
        hospital = self.hospital_ctrl.buscar_hospital("San Pedro")
        self.assertIsNotNone(hospital)

    def test_obtener_todos(self):
        self.hospital_ctrl.crear_hospital("San Juan")
        hospitales = self.hospital_ctrl.obtener_todos()
        self.assertTrue(any(h.nombre == "San Juan" for h in hospitales))

    def test_actualizar_hospital(self):
        self.hospital_ctrl.crear_hospital("Clínica Sur")
        actualizado = self.hospital_ctrl.actualizar_hospital("Clínica Sur", "Clínica Norte")
        self.assertTrue(actualizado)
        self.assertIsNotNone(self.hospital_ctrl.buscar_hospital("Clínica Norte"))

    def test_eliminar_hospital(self):
        self.hospital_ctrl.crear_hospital("El Rosario")
        eliminado = self.hospital_ctrl.eliminar_hospital("El Rosario")
        self.assertTrue(eliminado)
        self.assertIsNone(self.hospital_ctrl.buscar_hospital("El Rosario"))

    def test_agregar_doctor_a_hospital(self):
        self.hospital_ctrl.crear_hospital("San Rafael")
        doctor = self.doctor_ctrl.crear_doctor("D10", "Juliana", "Dermatología")
        resultado = self.hospital_ctrl.agregar_doctor("San Rafael", doctor)
        self.assertTrue(resultado)
        hospital_actualizado = self.hospital_ctrl.buscar_hospital("San Rafael")
        self.assertIn(doctor, hospital_actualizado.doctores)

if __name__ == '__main__':
    unittest.main()
