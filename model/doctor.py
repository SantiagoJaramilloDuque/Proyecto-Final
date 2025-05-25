class Doctor:
    def __init__(self, doctor_id, nombre, especialidad):
        self.__doctor_id = doctor_id
        self.__nombre = nombre
        self.__especialidad = especialidad

    @property
    def doctor_id(self):
        return self.__doctor_id
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def especialidad(self):
        return self.__especialidad
    
    def __str__(self):
        return f"Doctor(ID: {self.doctor_id}, Nombre: {self.nombre}, Especialidad: {self.especialidad})"