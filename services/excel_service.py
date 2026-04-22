"""
services/excel_service.py
--------------------------
Lógica de lectura y escritura del archivo Excel, simulando una base de datos relacional para Autofix.
Hojas:
  - Clientes (rut, nombre_cliente)
  - Vehiculos (patente, rut_cliente, marca, modelo, kilometraje)
  - Servicios (patente, fecha, tipo_servicio, trabajo_realizado, repuestos_usados, mecanico)
"""

import os
import openpyxl

# ── Configuración ─────────────────────────────────────────────────────────────

RUTA_EXCEL = "data/historial.xlsx"

COL_CLIENTES = ["rut", "nombre_cliente"]
COL_VEHICULOS = ["patente", "rut_cliente", "marca", "modelo", "kilometraje"]
COL_SERVICIOS = ["patente", "fecha", "tipo_servicio", "trabajo_realizado", "repuestos_usados", "mecanico"]

# ── Funciones internas ───────────────────────────────────────────────────────────

def _inicializar_excel():
    """
    Crea el archivo Excel con las hojas y cabeceras si no existe.
    Si el archivo ya existe pero tiene las hojas antiguas, las elimina.
    """
    if not os.path.exists(RUTA_EXCEL):
        wb = openpyxl.Workbook()
        
        # Eliminar la hoja por defecto si existe y crear las nuevas
        if 'Sheet' in wb.sheetnames:
            del wb['Sheet']
        if 'Pacientes' in wb.sheetnames:
            del wb['Pacientes']
        if 'Sesiones' in wb.sheetnames:
            del wb['Sesiones']
        
        ws_clientes = wb.create_sheet("Clientes")
        ws_clientes.append(COL_CLIENTES)
        
        ws_vehiculos = wb.create_sheet("Vehiculos")
        ws_vehiculos.append(COL_VEHICULOS)
        
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

def _obtener_o_crear_vehiculo(wb, patente, rut_cliente, datos):
    """Verifica si el vehículo existe, si no, lo crea."""
    ws = wb["Vehiculos"]
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == patente:
            return
    
    fila_vehiculo = [
        patente,
        rut_cliente,
        datos.get("marca", ""),
        datos.get("modelo", ""),
        datos.get("kilometraje", "")
    ]
    ws.append(fila_vehiculo)

# ── Funciones públicas ────────────────────────────────────────────────────────

def guardar_sesion(datos: dict):
    """
    Inserta Cliente, Vehículo y Servicio en el Excel.
    """
    _inicializar_excel()
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    
    rut_cliente = datos.get("rut_cliente", "").strip()
    nombre_cliente = datos.get("nombre_paciente", "").strip()
    patente = datos.get("patente", "").strip()
    
    # 1. Gestionar Cliente
    _obtener_o_crear_cliente(wb, rut_cliente, nombre_cliente)
    
    # 2. Gestionar Vehículo
    _obtener_o_crear_vehiculo(wb, patente, rut_cliente, datos)
    
    # 3. Guardar Servicio
    ws_servicios = wb["Servicios"]
    fila_servicio = [
        patente,
        datos.get("fecha", ""),
        datos.get("tipo_servicio", ""),
        datos.get("trabajo_realizado", ""),
        datos.get("repuestos_usados", ""),
        datos.get("mecanico", "")
    ]
    ws_servicios.append(fila_servicio)
    
    wb.save(RUTA_EXCEL)
    wb.close()

def obtener_paciente(rut_cliente: str) -> dict:
    """Busca y retorna un cliente por RUT."""
    if not os.path.exists(RUTA_EXCEL):
        return None
        
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    if "Clientes" not in wb.sheetnames:
        return None
        
    ws = wb["Clientes"]
    rut_limpio = rut_cliente.strip()
    
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == rut_limpio:
            return {"rut": fila[0], "nombre_paciente": fila[1]}
            
    wb.close()
    return None

def obtener_sesiones(rut_cliente: str, filtro_patente: str = None) -> list[dict]:
    """
    Retorna todos los servicios asociados a un cliente, cruzando
    los datos de Vehículos y Servicios (JOIN).
    Filtra opcionalmente por la patente del vehículo.
    """
    if not os.path.exists(RUTA_EXCEL):
        return []
        
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    
    if "Vehiculos" not in wb.sheetnames or "Servicios" not in wb.sheetnames:
        return []
        
    ws_vehiculos = wb["Vehiculos"]
    ws_servicios = wb["Servicios"]
    rut_limpio = rut_cliente.strip()
    
    # 1. Obtener vehículos del cliente
    vehiculos_del_cliente = {} # patente -> dict(datos_vehiculo)
    for fila in ws_vehiculos.iter_rows(min_row=2, values_only=True):
        if str(fila[1]).strip() == rut_limpio:
            patente = str(fila[0]).strip()
            
            if filtro_patente and patente != filtro_patente:
                continue
                
            vehiculos_del_cliente[patente] = {
                "patente": patente,
                "marca": fila[2],
                "modelo": fila[3],
                "kilometraje": fila[4]
            }
            
    # 2. Buscar los servicios que coincidan con esas patentes
    sesiones = []
    for fila in ws_servicios.iter_rows(min_row=2, values_only=True):
        patente = str(fila[0]).strip()
        if patente in vehiculos_del_cliente:
            datos_vehiculo = vehiculos_del_cliente[patente]
            
            sesion = {
                "fecha": fila[1],
                "tipo_servicio": fila[2],
                "trabajo_realizado": fila[3],
                "repuestos_usados": fila[4],
                "mecanico": fila[5],
                # Datos del vehículo para visualización
                "patente": datos_vehiculo["patente"],
                "marca": datos_vehiculo["marca"],
                "modelo": datos_vehiculo["modelo"],
                "kilometraje": datos_vehiculo["kilometraje"]
            }
            sesiones.append(sesion)
            
    wb.close()
    
    # Ordenar por fecha descendente
    sesiones.sort(key=lambda x: str(x.get("fecha") or ""), reverse=True)
    return sesiones

def buscar_cliente_por_patente(patente: str) -> str:
    """Retorna el RUT del cliente dueño de una patente, o None si no se encuentra."""
    if not os.path.exists(RUTA_EXCEL):
        return None
    wb = openpyxl.load_workbook(RUTA_EXCEL)
    if "Vehiculos" not in wb.sheetnames:
        return None
    ws = wb["Vehiculos"]
    pat_limpia = patente.strip()
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == pat_limpia:
            rut = str(fila[1]).strip()
            wb.close()
            return rut
    wb.close()
    return None
