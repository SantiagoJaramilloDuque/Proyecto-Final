import unittest
from model.doctor import Doctor

class TestDoctorModel(unittest.TestCase):
    def setUp(self):
        self.doctor = Doctor("D1", "Carlos Pérez", "Pediatría")

    def test_atributos_iniciales(self):
        self.assertEqual(self.doctor.doctor_id, "D1")
        self.assertEqual(self.doctor.nombre, "Carlos Pérez")
        self.assertEqual(self.doctor.especialidad, "Pediatría")

    def test_setters(self):
        self.doctor.nombre = "Ana Gómez"
        self.doctor.especialidad = "Cardiología"
        self.assertEqual(self.doctor.nombre, "Ana Gómez")
        self.assertEqual(self.doctor.especialidad, "Cardiología")

    def test_str(self):
        esperado = "Doctor(ID: D1, Nombre: Carlos Pérez, Especialidad: Pediatría)"
        self.assertEqual(str(self.doctor), esperado)

if __name__ == '__main__':
    unittest.main()
