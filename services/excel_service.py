"""
services/excel_service.py
--------------------------
Toda la lógica de lectura y escritura del archivo Excel central.

Las rutas NUNCA acceden al Excel directamente.
Cualquier cambio en la capa de datos (ej: migrar a SQLite)
solo requiere modificar este archivo, sin tocar las rutas.

Funciones:
  guardar_sesion(sesion: dict)         → Agrega una fila nueva al Excel
  obtener_sesiones(rut: str) -> list   → Retorna sesiones filtradas por RUT
"""

import os
import openpyxl

# ── Configuración ─────────────────────────────────────────────────────────────

RUTA_EXCEL = "data/historial.xlsx"
NOMBRE_HOJA = "Historial"

# Orden de columnas: debe mantenerse siempre igual.
# Si se agrega un campo nuevo en el futuro, agregarlo AL FINAL de esta lista.
COLUMNAS = [
    "rut",
    "nombre_paciente",
    "fecha",
    "tipo_atencion",
    "observaciones",
    "registrado_por",
]


# ── Función interna ───────────────────────────────────────────────────────────

def _inicializar_excel():
    """
    Crea el archivo Excel con la hoja y cabeceras si no existe.
    Se llama automáticamente antes de cada operación.
    """
    if not os.path.exists(RUTA_EXCEL):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = NOMBRE_HOJA
        ws.append(COLUMNAS)
        wb.save(RUTA_EXCEL)


# ── Funciones públicas ────────────────────────────────────────────────────────

def guardar_sesion(sesion: dict):
    """
    Agrega una nueva fila al Excel con los datos de la sesión.

    Input:  dict con keys: rut, nombre_paciente, fecha,
                           tipo_atencion, observaciones, registrado_por
    Output: ninguno (escribe en disco)
    """
    _inicializar_excel()

    wb = openpyxl.load_workbook(RUTA_EXCEL)
    ws = wb[NOMBRE_HOJA]

    # Construye la fila respetando el orden de columnas definido arriba
    fila = [sesion.get(col, "") for col in COLUMNAS]
    ws.append(fila)

    wb.save(RUTA_EXCEL)
    wb.close()


def obtener_sesiones(rut: str) -> list[dict]:
    """
    Retorna todas las sesiones de un paciente ordenadas por fecha descendente.

    Input:  rut (str) — RUT del paciente a buscar
    Output: lista de dicts, cada uno representa una sesión.
            Retorna lista vacía si no hay registros.
    """
    _inicializar_excel()

    wb = openpyxl.load_workbook(RUTA_EXCEL)
    ws = wb[NOMBRE_HOJA]

    sesiones = []
    rut_limpio = rut.strip()

    # Recorre desde la fila 2 (fila 1 son las cabeceras)
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut_limpio:
            sesion = dict(zip(COLUMNAS, fila))
            sesiones.append(sesion)

    wb.close()

    # Ordena por fecha descendente (más reciente primero)
    sesiones.sort(key=lambda x: str(x.get("fecha") or ""), reverse=True)

    return sesiones
