import unittest
from model.hospital import Hospital
from model.doctor import Doctor

class TestHospitalModel(unittest.TestCase):
    def setUp(self):
        self.hospital = Hospital("San Rafael")
        self.doctor1 = Doctor("D1", "Laura", "Dermatología")
        self.doctor2 = Doctor("D2", "José", "Neurología")

    def test_nombre(self):
        self.assertEqual(self.hospital.nombre, "San Rafael")
        self.hospital.nombre = "San Juan"
        self.assertEqual(self.hospital.nombre, "San Juan")

    def test_lista_doctores_vacia(self):
        self.assertEqual(len(self.hospital.doctores), 0)

    def test_agregar_doctor(self):
        self.hospital.agregar_doctor(self.doctor1)
        self.assertIn(self.doctor1, self.hospital.doctores)

    def test_setter_lista_valida(self):
        self.hospital.doctores = [self.doctor1, self.doctor2]
        self.assertEqual(len(self.hospital.doctores), 2)

    def test_setter_lista_invalida(self):
        with self.assertRaises(ValueError):
            self.hospital.doctores = ["no es un doctor"]

    def test_str(self):
        self.hospital.agregar_doctor(self.doctor1)
        texto = str(self.hospital)
        self.assertIn("Hospital(Nombre: San Rafael", texto)
        self.assertIn("Doctores: 1", texto)

if __name__ == '__main__':
    unittest.main()
