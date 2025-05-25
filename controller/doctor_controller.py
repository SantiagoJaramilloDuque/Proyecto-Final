from persistence.imp_crud_doctor import ImpCrudDoctor

class DoctorController:
    def __init__(self):
        self.__crud = ImpCrudDoctor()

    def crear_doctor(self, doctor_id, nombre, especialidad):
        return self.__crud.crear(
            doctor_id=doctor_id,
            nombre=nombre,
            especialidad=especialidad
        )

    def buscar_doctor(self, doctor_id):
        return self.__crud.obtener_por_id(doctor_id)

    def obtener_todos(self):
        return self.__crud.obtener_todos()

    def actualizar_doctor(self, doctor_id, **kwargs):
        return self.__crud.actualizar(doctor_id, **kwargs)

    def eliminar_doctor(self, doctor_id):
        return self.__crud.eliminar(doctor_id)