from model.doctor import Doctor

class Hospital:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__doctores = []

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def doctores(self):
        return self.__doctores
    
    def agregar_doctor(self, doctor: Doctor):
        self.__doctores.append(doctor)
    
    def __str__(self):
        return f"Hospital(Nombre: {self.nombre}, Doctores: {len(self.doctores)})"