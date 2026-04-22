import random
from datetime import date, timedelta
import sys
import os

# Asegurar que el script pueda importar desde la carpeta raíz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services import excel_service

CLIENTES = [
    {"rut": "76.123.456-1", "nombre": "Constructora Alfa S.A.", "equipos": 1},
    {"rut": "77.234.567-2", "nombre": "Comunidad Edificio Central", "equipos": 1},
    {"rut": "78.345.678-3", "nombre": "Agrícola del Valle", "equipos": 1},
    {"rut": "79.456.789-4", "nombre": "Industrias Plásticas Omega", "equipos": 2},
    {"rut": "80.567.890-5", "nombre": "Minera Las Condes", "equipos": 3},
]

TIPOS_SERVICIO = ["Mantenimiento Preventivo", "Reparación de Sellos", "Cambio de Rodamientos", "Alineación Láser", "Prueba Hidrostática", "Rebobinado de Motor"]
TECNICOS = ["Ingeniero Roberto", "Técnico Especialista Carlos", "Mecánico Hidráulico Ana"]

def generar_datos():
    print("Iniciando carga de datos ficticios para Hidropro Bombas...")
    total_equipos = 0
    total_servicios = 0
    
    for cliente in CLIENTES:
        rut = cliente["rut"]
        nombre = cliente["nombre"]
        num_equipos = cliente["equipos"]
        total_equipos += num_equipos
        
        # Generar nombres de equipo para simular la nueva lógica
        equipos = []
        for i in range(num_equipos):
            equipos.append({
                "equipo": f"Bomba Centrífuga {random.randint(1, 10)}HP",
                "referencia": f"Pozo {i+1}",
                "ubicacion": f"Nivel {-random.randint(1, 3)}",
                "presion_bar": round(random.uniform(2.5, 6.0), 1)
            })

        sesiones_totales = sum(random.randint(3, 6) for _ in range(num_equipos))
            
        print(f"  -> Cliente {nombre} (RUT: {rut}): Tiene {num_equipos} equipos. Generando {sesiones_totales} servicios en total...")
        
        # Generar fechas aleatorias ordenadas
        fechas = []
        for _ in range(sesiones_totales):
            dias_atras = random.randint(1, 400)
            fechas.append(date.today() - timedelta(days=dias_atras))
        fechas.sort()
        
        for i, fecha_sesion in enumerate(fechas):
            # Asignar a un equipo aleatorio de los que tiene este cliente
            eq = random.choice(equipos)
            
            sesion = {
                "rut": rut,
                "nombre_paciente": nombre,
                "fecha": fecha_sesion.isoformat(),
                "tipo_servicio": random.choice(TIPOS_SERVICIO),
                "trabajo_realizado": "Mantención de bomba realizada exitosamente según pauta del fabricante. Sistema operando con presión estable.",
                "repuestos_usados": "Sellos mecánicos O-Ring 25mm",
                "tecnico": random.choice(TECNICOS),
                "equipo": eq["equipo"],
                "referencia": eq["referencia"],
                "ubicacion": eq["ubicacion"],
                "presion_bar": eq["presion_bar"]
            }
            excel_service.guardar_sesion(sesion)
            total_servicios += 1
                
    print(f"\n¡Listo! Se crearon {len(CLIENTES)} clientes simulando {total_equipos} equipos y un total de {total_servicios} servicios hidráulicos.")

if __name__ == "__main__":
    generar_datos()
