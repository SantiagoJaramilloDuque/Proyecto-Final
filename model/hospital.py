from model.doctor import Doctor

class Hospital:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__doctores = []

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def doctores(self):
        return self.__doctores

    @doctores.setter
    def doctores(self, lista_doctores):
        if isinstance(lista_doctores, list) and all(isinstance(d, Doctor) for d in lista_doctores):
            self.__doctores = lista_doctores
        else:
            raise ValueError("La lista de doctores debe contener solo objetos de tipo Doctor.")

    def agregar_doctor(self, doctor: Doctor):
        self.__doctores.append(doctor)

    def __str__(self):
        return f"Hospital(Nombre: {self.nombre}, Doctores: {len(self.doctores)})"
