"""
routes/sesiones.py
------------------
Rutas relacionadas al registro de sesiones de tratamiento.

Rutas:
  GET  /sesiones/registrar  → Muestra el formulario de registro
  POST /sesiones/registrar  → Recibe y guarda los datos del formulario
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services import excel_service
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

TIPOS_SERVICIO = [
    "Mantención Preventiva",
    "Cambio de Aceite",
    "Revisión de Frenos",
    "Alineación y Balanceo",
    "Cambio de Batería",
    "Diagnóstico Escáner",
    "Reparación de Motor",
    "Otro"
]

@router.get("/sesiones/registrar")
def form_registrar(request: Request, rut_cliente: str = "", patente: str = "", nombre_paciente: str = ""):
    """
    Muestra el formulario para registrar un nuevo servicio.
    Si viene desde el historial, el RUT y posiblemente la patente llegan precargados.
    """
    # Si viene con patente pero sin rut, buscar el rut
    if patente and not rut_cliente:
        rut_encontrado = excel_service.buscar_cliente_por_patente(patente)
        if rut_encontrado:
            rut_cliente = rut_encontrado
            
    # Si viene con rut, intentar buscar su nombre
    if rut_cliente and not nombre_paciente:
        cliente = excel_service.obtener_paciente(rut_cliente)
        if cliente:
            nombre_paciente = cliente.get("nombre_paciente", "")

    return templates.TemplateResponse(
        request=request,
        name="registrar.html",
        context={
            "rut_cliente": rut_cliente,
            "patente": patente,
            "nombre_paciente": nombre_paciente,
            "fecha_hoy": date.today().isoformat(),
            "tipos_atencion": TIPOS_SERVICIO
        },
    )

@router.post("/sesiones/registrar")
def registrar_sesion(
    rut_cliente: str = Form(...),
    patente: str = Form(...),
    nombre_paciente: str = Form(...),
    fecha: str = Form(...),
    tipo_atencion: str = Form(...),
    kilometraje: str = Form(default=""),
    marca: str = Form(default=""),
    modelo: str = Form(default=""),
    observaciones: str = Form(default=""),
    repuestos_usados: str = Form(default=""),
    registrado_por: str = Form(...)
):
    """
    Recibe los datos del formulario, los limpia y los guarda en Excel.
    """
    
    sesion = {
        "rut_cliente": rut_cliente.strip(),
        "patente": patente.strip().upper(),
        "nombre_paciente": nombre_paciente.strip(),
        "fecha": fecha,
        "tipo_servicio": tipo_atencion,
        "kilometraje": kilometraje.strip(),
        "marca": marca.strip(),
        "modelo": modelo.strip(),
        "trabajo_realizado": observaciones.strip(),
        "repuestos_usados": repuestos_usados.strip(),
        "mecanico": registrado_por.strip()
    }
    
    excel_service.guardar_sesion(sesion)
    return RedirectResponse(url=f"/paciente/{sesion['rut_cliente']}/historial", status_code=303)