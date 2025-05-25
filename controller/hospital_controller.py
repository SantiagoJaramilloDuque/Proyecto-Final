from persistence.imp_crud_hospital import ImpCrudHospital

class HospitalController:
    def __init__(self):
        self.__crud = ImpCrudHospital()

    def crear_hospital(self, nombre):
        return self.__crud.crear(nombre=nombre)

    def buscar_hospital(self, nombre):
        return self.__crud.obtener_por_id(nombre)

    def obtener_todos(self):
        return self.__crud.obtener_todos()

    def actualizar_hospital(self, old_nombre, nuevo_nombre):
        return self.__crud.actualizar(old_nombre, nuevo_nombre=nuevo_nombre)

    def eliminar_hospital(self, nombre):
        return self.__crud.eliminar(nombre)

    def agregar_doctor(self, hospital_nombre, doctor):
        return self.__crud.relacion(hospital_nombre=hospital_nombre, doctor=doctor)