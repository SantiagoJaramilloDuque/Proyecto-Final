import unittest
from controller.doctor_controller import DoctorController

class TestDoctorController(unittest.TestCase):
    def setUp(self):
        self.controller = DoctorController()

    def test_crear_doctor(self):
        doctor = self.controller.crear_doctor("D1", "Ana", "Cardiología")
        self.assertEqual(doctor.nombre, "Ana")
        self.assertEqual(doctor.especialidad, "Cardiología")

    def test_buscar_doctor(self):
        self.controller.crear_doctor("D2", "Luis", "Pediatría")
        doctor = self.controller.buscar_doctor("D2")
        self.assertIsNotNone(doctor)
        self.assertEqual(doctor.nombre, "Luis")

    def test_obtener_todos(self):
        self.controller.crear_doctor("D3", "Carlos", "Neurología")
        doctores = self.controller.obtener_todos()
        self.assertTrue(any(d.doctor_id == "D3" for d in doctores))

    def test_actualizar_doctor(self):
        self.controller.crear_doctor("D4", "Mario", "Urología")
        actualizado = self.controller.actualizar_doctor("D4", nombre="Mariano")
        self.assertTrue(actualizado)
        doctor = self.controller.buscar_doctor("D4")
        self.assertEqual(doctor.nombre, "Mariano")

    def test_eliminar_doctor(self):
        self.controller.crear_doctor("D5", "Laura", "Oncología")
        eliminado = self.controller.eliminar_doctor("D5")
        self.assertTrue(eliminado)
        self.assertIsNone(self.controller.buscar_doctor("D5"))

if __name__ == '__main__':
    unittest.main()
