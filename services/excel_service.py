"""
services/excel_service.py
--------------------------
Lógica de lectura y escritura del archivo Excel, simulando una base de datos relacional.
Hojas:
  - Clientes (rut, nombre_cliente)
  - Equipos (id_equipo, rut_cliente, equipo, referencia, ubicacion, presion_bar)
  - Servicios (id_equipo, fecha, tipo_servicio, trabajo_realizado, repuestos_usados, tecnico)
"""

import os
import openpyxl

# ── Configuración ─────────────────────────────────────────────────────────────

RUTA_EXCEL = "data/historial.xlsx"

COL_CLIENTES = ["rut", "nombre_cliente"]
COL_EQUIPOS = ["id_equipo", "rut_cliente", "equipo", "referencia", "ubicacion", "presion_bar"]
COL_SERVICIOS = ["id_equipo", "fecha", "tipo_servicio", "trabajo_realizado", "repuestos_usados", "tecnico"]


# ── Funciones internas ───────────────────────────────────────────────────────────

def _inicializar_excel():
    """
    Crea el archivo Excel con las hojas y cabeceras si no existe.
    Si el archivo ya existe pero tiene la hoja antigua 'Historial', la elimina.
    """
    if not os.path.exists(RUTA_EXCEL):
        wb = openpyxl.Workbook()
        # Eliminar la hoja por defecto y crear las nuevas
        if 'Sheet' in wb.sheetnames:
            del wb['Sheet']
        
        ws_clientes = wb.create_sheet("Clientes")
        ws_clientes.append(COL_CLIENTES)
        
        ws_equipos = wb.create_sheet("Equipos")
        ws_equipos.append(COL_EQUIPOS)
        
        ws_servicios = wb.create_sheet("Servicios")
        ws_servicios.append(COL_SERVICIOS)
        
        wb.save(RUTA_EXCEL)
        wb.close()


def _obtener_o_crear_cliente(wb, rut, nombre):
    """Verifica si el cliente existe, si no, lo crea."""
    ws = wb["Clientes"]
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut:
            return
    ws.append([rut, nombre])


def _obtener_o_crear_equipo(wb, rut, datos):
    """
    Verifica si el equipo (mismo rut y referencia) existe.
    Si no existe, genera un id_equipo correlativo y lo guarda.
    Retorna el id_equipo.
    """
    ws = wb["Equipos"]
    referencia = str(datos.get("referencia", "")).strip()
    
    max_id = 0
    for fila in ws.iter_rows(min_row=2, values_only=True):
        id_eq = fila[0]
        rut_cl = str(fila[1]).strip()
        ref = str(fila[3]).strip()
        
        if isinstance(id_eq, int) and id_eq > max_id:
            max_id = id_eq
            
        if rut_cl == rut and ref == referencia and referencia != "":
            return id_eq
            
    # Si no existe o no tiene referencia, creamos uno nuevo
    nuevo_id = max_id + 1
    fila_equipo = [
        nuevo_id,
        rut,
        datos.get("equipo", ""),
        referencia,
        datos.get("ubicacion", ""),
        datos.get("presion_bar", "")
    ]
    ws.append(fila_equipo)
    return nuevo_id


# ── Funciones públicas ────────────────────────────────────────────────────────

def guardar_sesion(datos: dict):
    """
    Inserta Cliente, Equipo y Servicio en el Excel.
    """
    _inicializar_excel()
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    
    rut = datos.get("rut", "").strip()
    nombre = datos.get("nombre_paciente", "").strip()
    
    # 1. Gestionar Cliente
    _obtener_o_crear_cliente(wb, rut, nombre)
    
    # 2. Gestionar Equipo
    id_equipo = _obtener_o_crear_equipo(wb, rut, datos)
    
    # 3. Guardar Servicio
    ws_servicios = wb["Servicios"]
    fila_servicio = [
        id_equipo,
        datos.get("fecha", ""),
        datos.get("tipo_servicio", ""),
        datos.get("trabajo_realizado", ""),
        datos.get("repuestos_usados", ""),
        datos.get("tecnico", "")
    ]
    ws_servicios.append(fila_servicio)
    
    wb.save(RUTA_EXCEL)
    wb.close()


def obtener_paciente(rut: str) -> dict:
    """Busca y retorna un cliente por RUT."""
    if not os.path.exists(RUTA_EXCEL):
        return None
        
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    if "Clientes" not in wb.sheetnames:
        return None
        
    ws = wb["Clientes"]
    rut_limpio = rut.strip()
    
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut_limpio:
            return {"rut": fila[0], "nombre_paciente": fila[1]}
            
    wb.close()
    return None


def obtener_sesiones(rut: str, filtro_ref: str = None) -> list[dict]:
    """
    Retorna todos los servicios asociados a un cliente, cruzando
    los datos de Equipos y Servicios (JOIN).
    Filtra opcionalmente por la referencia del equipo.
    """
    if not os.path.exists(RUTA_EXCEL):
        return []
        
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    
    # Manejar caso donde el archivo es antiguo
    if "Equipos" not in wb.sheetnames or "Servicios" not in wb.sheetnames:
        return []
        
    ws_equipos = wb["Equipos"]
    ws_servicios = wb["Servicios"]
    rut_limpio = rut.strip()
    
    # 1. Obtener equipos del cliente
    equipos_del_cliente = {} # id_equipo -> dict(datos_equipo)
    for fila in ws_equipos.iter_rows(min_row=2, values_only=True):
        if str(fila[1]).strip() == rut_limpio:
            id_eq = fila[0]
            ref = str(fila[3]).strip()
            
            # Si hay filtro_ref, omitimos los que no coinciden
            if filtro_ref and ref != filtro_ref:
                continue
                
            equipos_del_cliente[id_eq] = {
                "id_equipo": id_eq,
                "equipo": fila[2],
                "referencia": fila[3],
                "ubicacion": fila[4],
                "presion_bar": fila[5]
            }
            
    # 2. Buscar los servicios que coincidan con esos equipos
    sesiones = []
    for fila in ws_servicios.iter_rows(min_row=2, values_only=True):
        id_eq = fila[0]
        if id_eq in equipos_del_cliente:
            datos_eq = equipos_del_cliente[id_eq]
            
            # Combinamos los datos
            sesion = {
                "fecha": fila[1],
                "tipo_servicio": fila[2],
                "trabajo_realizado": fila[3],
                "repuestos_usados": fila[4],
                "tecnico": fila[5],
                # Agregamos datos del equipo para visualización
                "equipo": datos_eq["equipo"],
                "referencia": datos_eq["referencia"],
                "ubicacion": datos_eq["ubicacion"],
                "presion_bar": datos_eq["presion_bar"]
            }
            sesiones.append(sesion)
            
    wb.close()
    
    # Ordenar por fecha descendente
    sesiones.sort(key=lambda x: str(x.get("fecha") or ""), reverse=True)
    return sesiones
