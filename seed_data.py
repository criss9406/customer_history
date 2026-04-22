import random
from datetime import date, timedelta
import sys
import os

# Asegurar que el script pueda importar desde la carpeta raíz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services import excel_service

CLIENTES = [
    {"nombre": "Carlos Rojas", "vehiculos": 1},
    {"nombre": "María Silva", "vehiculos": 1},
    {"nombre": "Luis Pérez", "vehiculos": 1},
    {"nombre": "Ana Torres", "vehiculos": 2},
    {"nombre": "Jorge Gómez", "vehiculos": 3},
]

TIPOS_SERVICIO = ["Revisión de 10.000km", "Cambio de Aceite", "Frenos", "Alineación y Balanceo", "Suspensión", "Scanner"]
TECNICOS = ["Mario Técnico", "Juan Mecánico", "Pedro Especialista"]

def generar_patente():
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Formato común en Chile: AB-CD-12 o XX-YY-99
    return f"{random.choice(letras)}{random.choice(letras)}-{random.choice(letras)}{random.choice(letras)}-{random.randint(10, 99)}"

def generar_datos():
    print("Iniciando carga de datos ficticios para Autofix...")
    total_vehiculos = 0
    total_servicios = 0
    
    for cliente in CLIENTES:
        for _ in range(cliente["vehiculos"]):
            patente = generar_patente()
            num_sesiones = random.randint(3, 6)
            total_vehiculos += 1
            
            print(f"  -> Vehículo {patente} ({cliente['nombre']}): Generando {num_sesiones} servicios...")
            
            # Generar fechas aleatorias ordenadas
            fechas = []
            for _ in range(num_sesiones):
                dias_atras = random.randint(1, 400)
                fechas.append(date.today() - timedelta(days=dias_atras))
            fechas.sort() # Para que tengan un orden cronológico lógico
            
            for fecha_sesion in fechas:
                sesion = {
                    "rut": patente, # El sistema base usa 'rut', pero en Autofix es la Patente
                    "nombre_paciente": cliente["nombre"],
                    "fecha": fecha_sesion.isoformat(),
                    "tipo_atencion": random.choice(TIPOS_SERVICIO),
                    "observaciones": "Trabajo de mantenimiento rutinario completado. Cliente conforme.",
                    "registrado_por": random.choice(TECNICOS),
                }
                # Esto automáticamente insertará al cliente en la hoja Pacientes si no existe,
                # y luego agregará el servicio a la hoja Sesiones.
                excel_service.guardar_sesion(sesion)
                total_servicios += 1
                
    print(f"\n¡Listo! Se crearon {len(CLIENTES)} clientes con {total_vehiculos} vehículos y un total de {total_servicios} servicios.")

if __name__ == "__main__":
    generar_datos()
