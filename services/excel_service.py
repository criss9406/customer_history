"""
services/excel_service.py
--------------------------
Toda la lógica de lectura y escritura del archivo Excel central.

Las rutas NUNCA acceden al Excel directamente.
Cualquier cambio en la capa de datos (ej: migrar a SQLite)
solo requiere modificar este archivo, sin tocar las rutas.
"""

import os
import openpyxl

# ── Configuración ─────────────────────────────────────────────────────────────

RUTA_EXCEL = "data/historial.xlsx"
HOJA_PACIENTES = "Pacientes"
HOJA_SESIONES = "Sesiones"

COLUMNAS_PACIENTES = ["rut", "nombre_paciente"]
COLUMNAS_SESIONES = ["rut", "fecha", "tipo_atencion", "observaciones", "registrado_por"]

# ── Función interna ───────────────────────────────────────────────────────────

def _inicializar_excel():
    """
    Crea el archivo Excel con las hojas y cabeceras si no existe.
    Se llama automáticamente antes de cada operación.
    """
    if not os.path.exists(RUTA_EXCEL):
        wb = openpyxl.Workbook()
        
        # Hoja de pacientes
        ws_pacientes = wb.active
        ws_pacientes.title = HOJA_PACIENTES
        ws_pacientes.append(COLUMNAS_PACIENTES)
        
        # Hoja de sesiones
        ws_sesiones = wb.create_sheet(title=HOJA_SESIONES)
        ws_sesiones.append(COLUMNAS_SESIONES)
        
        wb.save(RUTA_EXCEL)

# ── Funciones públicas ────────────────────────────────────────────────────────

def obtener_paciente(rut: str) -> dict:
    """
    Busca un paciente por su RUT en la hoja de pacientes.
    Retorna el diccionario con sus datos o None si no existe.
    """
    _inicializar_excel()
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    ws = wb[HOJA_PACIENTES]
    
    rut_limpio = rut.strip()
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut_limpio:
            wb.close()
            return dict(zip(COLUMNAS_PACIENTES, fila))
            
    wb.close()
    return None

def guardar_sesion(sesion: dict):
    """
    Agrega una nueva sesión a la hoja de sesiones.
    Si el paciente no existe, lo crea en la hoja de pacientes.
    """
    _inicializar_excel()
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    
    rut_limpio = sesion["rut"].strip()
    
    # 1. Crear paciente si no existe
    ws_pacientes = wb[HOJA_PACIENTES]
    paciente_existe = False
    for fila in ws_pacientes.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut_limpio:
            paciente_existe = True
            break
            
    if not paciente_existe and "nombre_paciente" in sesion:
        fila_paciente = [rut_limpio, sesion.get("nombre_paciente", "").strip()]
        ws_pacientes.append(fila_paciente)
        
    # 2. Guardar sesión
    ws_sesiones = wb[HOJA_SESIONES]
    fila_sesion = [sesion.get(col, "") for col in COLUMNAS_SESIONES]
    ws_sesiones.append(fila_sesion)
    
    wb.save(RUTA_EXCEL)
    wb.close()

def obtener_sesiones(rut: str) -> list[dict]:
    """
    Retorna todas las sesiones de un paciente ordenadas por fecha descendente.
    """
    _inicializar_excel()
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    ws = wb[HOJA_SESIONES]

    sesiones = []
    rut_limpio = rut.strip()

    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut_limpio:
            sesion = dict(zip(COLUMNAS_SESIONES, fila))
            sesiones.append(sesion)

    wb.close()
    sesiones.sort(key=lambda x: str(x.get("fecha") or ""), reverse=True)
    return sesiones
