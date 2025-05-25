from icrud.icrud import ICrud
from model.doctor import Doctor

class ImpCrudDoctor(ICrud):
    def __init__(self):
        self.__doctores = []

    def crear(self, **kwargs):
        doctor = Doctor(kwargs['doctor_id'], kwargs['nombre'], kwargs['especialidad'])
        self.__doctores.append(doctor)
        return doctor

    def obtener_por_id(self, id):
        for doctor in self.__doctores:
            if doctor.doctor_id == id:
                return doctor
        return None

    def obtener_todos(self):
        return self.__doctores.copy()

    def actualizar(self, id, **kwargs):
        doctor = self.obtener_por_id(id)
        if doctor:
            if 'nombre' in kwargs:
                doctor.nombre = kwargs['nombre'] 
            if 'especialidad' in kwargs:
                doctor.especialidad = kwargs['especialidad']  
            return True
        return False

    def eliminar(self, id):
        doctor = self.obtener_por_id(id)
        if doctor:
            self.__doctores.remove(doctor)
            return True
        return False

    def relacion(self, **kwargs):
        # Implementación específica para relaciones de doctores
        pass
