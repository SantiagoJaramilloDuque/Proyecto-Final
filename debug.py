from controller.doctor_controller import DoctorController
from controller.hospital_controller import HospitalController
from persistence.imp_crud_doctor import ImpCrudDoctor
from persistence.imp_crud_hospital import ImpCrudHospital

print("\n== DEBUG GENERAL: COMPOSICIÓN + HERENCIA ==")

# COMPOSICIÓN: Hospital tiene Doctores
doctor_ctrl = DoctorController()
hospital_ctrl = HospitalController()

# Crear doctores
doc1 = doctor_ctrl.crear_doctor("D1", "Ana María", "Pediatría")
doc2 = doctor_ctrl.crear_doctor("D2", "Carlos Pérez", "Cardiología")

# Crear hospital y asociar doctores
hospital_ctrl.crear_hospital("Hospital San José")
hospital_ctrl.agregar_doctor("Hospital San José", doc1)
hospital_ctrl.agregar_doctor("Hospital San José", doc2)

# Obtener hospital actualizado
hospital = hospital_ctrl.buscar_hospital("Hospital San José")

# Mostrar información
print(f"Hospital: {hospital.nombre}")
print("Doctores asociados:")
for d in hospital.doctores:
    print(f"  - {d.nombre} ({d.especialidad})")

# HERENCIA: Mostrar clases base
crud_doctor = ImpCrudDoctor()
crud_hospital = ImpCrudHospital()

print("\nClases base (herencia):")
print("ImpCrudDoctor hereda de:", ImpCrudDoctor.__bases__)
print("ImpCrudHospital hereda de:", ImpCrudHospital.__bases__)

# breakpoint
