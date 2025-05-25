from icrud.icrud import ICrud
from model.hospital import Hospital

class ImpCrudHospital(ICrud):
    def __init__(self):
        self.__hospitales = []

    def crear(self, **kwargs):
        hospital = Hospital(kwargs['nombre'])
        self.__hospitales.append(hospital)
        return hospital

    def obtener_por_id(self, nombre):
        for hospital in self.__hospitales:
            if hospital.nombre == nombre:  
                return hospital
        return None

    def obtener_todos(self):
        return self.__hospitales.copy()

    def actualizar(self, old_nombre, **kwargs):
        hospital = self.obtener_por_id(old_nombre)
        if hospital and 'nuevo_nombre' in kwargs:
            hospital.nombre = kwargs['nuevo_nombre'] 
            return True
        return False

    def eliminar(self, nombre):
        hospital = self.obtener_por_id(nombre)
        if hospital:
            self.__hospitales.remove(hospital)
            return True
        return False

    def relacion(self, **kwargs):
        hospital = self.obtener_por_id(kwargs['hospital_nombre'])
        if hospital:
            hospital.agregar_doctor(kwargs['doctor'])
            return True
        return False
