class Doctor:
    def __init__(self, doctor_id, nombre, especialidad):
        self.__doctor_id = doctor_id
        self.__nombre = nombre
        self.__especialidad = especialidad

    @property
    def doctor_id(self):
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = value

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, value):
        self.__especialidad = value

    def __str__(self):
        return f"Doctor(ID: {self.doctor_id}, Nombre: {self.nombre}, Especialidad: {self.especialidad})"
