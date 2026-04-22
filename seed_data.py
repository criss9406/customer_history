import os
import sys
from datetime import date, timedelta
import random

# Asegurar que el script pueda importar desde la carpeta raíz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services import excel_service

CLIENTES = [
    {"rut_cliente": "12.345.678-9", "nombre": "Juan Pérez", "vehiculos": 1},
    {"rut_cliente": "15.678.901-2", "nombre": "María González", "vehiculos": 1},
    {"rut_cliente": "10.111.222-3", "nombre": "Empresa Transportes Sur", "vehiculos": 3},
    {"rut_cliente": "17.444.555-4", "nombre": "Carlos Rojas", "vehiculos": 2},
    {"rut_cliente": "11.222.333-K", "nombre": "Ana Silva", "vehiculos": 1},
]

TIPOS_SERVICIO = ["Mantención Preventiva", "Cambio de Aceite", "Revisión de Frenos", "Alineación y Balanceo", "Diagnóstico Escáner"]
TECNICOS = ["Mecánico Roberto", "Técnico Especialista Carlos", "Electricista Automotriz Ana"]
MARCAS = [("Toyota", "Yaris"), ("Hyundai", "Accent"), ("Chevrolet", "Sail"), ("Ford", "Ranger"), ("Nissan", "Versa"), ("Peugeot", "208")]

def generar_datos():
    print("Iniciando carga de datos ficticios para Autofix...")
    total_vehiculos = 0
    total_servicios = 0
    
    for cliente in CLIENTES:
        rut_cliente = cliente["rut_cliente"]
        nombre = cliente["nombre"]
        num_vehiculos = cliente["vehiculos"]
        total_vehiculos += num_vehiculos
        
        vehiculos = []
        for i in range(num_vehiculos):
            marca, modelo = random.choice(MARCAS)
            # Generar patente aleatoria formato AA1111 o ABCD12
            if random.choice([True, False]):
                patente = f"{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{random.randint(1000, 9999)}"
            else:
                patente = f"{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{random.randint(10, 99)}"
                
            vehiculos.append({
                "patente": patente,
                "marca": marca,
                "modelo": modelo,
                "kilometraje": random.randint(10000, 150000)
            })

        sesiones_totales = sum(random.randint(2, 5) for _ in range(num_vehiculos))
            
        print(f"  -> Cliente {nombre} (RUT: {rut_cliente}): Tiene {num_vehiculos} vehículos. Generando {sesiones_totales} servicios en total...")
        
        fechas = []
        for _ in range(sesiones_totales):
            dias_atras = random.randint(1, 400)
            fechas.append(date.today() - timedelta(days=dias_atras))
        fechas.sort()
        
        for fecha_sesion in fechas:
            vehiculo = random.choice(vehiculos)
            
            sesion = {
                "rut_cliente": rut_cliente,
                "patente": vehiculo["patente"],
                "nombre_paciente": nombre,
                "fecha": fecha_sesion.isoformat(),
                "tipo_servicio": random.choice(TIPOS_SERVICIO),
                "kilometraje": str(vehiculo["kilometraje"] - random.randint(500, 5000)),
                "marca": vehiculo["marca"],
                "modelo": vehiculo["modelo"],
                "trabajo_realizado": "Revisión completa de fluidos y sistemas de seguridad. Sin observaciones críticas.",
                "repuestos_usados": "Filtro de aceite, Aceite 5W30",
                "mecanico": random.choice(TECNICOS),
            }
            excel_service.guardar_sesion(sesion)
            total_servicios += 1
                
    print(f"\n¡Listo! Se crearon {len(CLIENTES)} clientes simulando {total_vehiculos} vehículos y un total de {total_servicios} servicios mecánicos.")

if __name__ == "__main__":
    generar_datos()
