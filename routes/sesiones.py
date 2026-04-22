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

# Opciones disponibles para el campo tipo_servicio
TIPOS_SERVICIO = [
    "Mantenimiento Preventivo",
    "Reparación de Sellos",
    "Cambio de Rodamientos",
    "Alineación Láser",
    "Prueba Hidrostática",
    "Rebobinado de Motor",
    "Otro"
]

@router.get("/sesiones/registrar")
def form_registrar(request: Request, rut: str = "", nombre_paciente: str = ""):
    """
    Muestra el formulario para registrar un nuevo servicio.
    Si viene desde el historial de un cliente, el RUT y el nombre llegan precargados.
    """
    return templates.TemplateResponse(
        request=request,
        name="registrar.html",
        context={"rut": rut, "nombre_paciente": nombre_paciente, "fecha_hoy": date.today().isoformat(), "tipos_atencion": TIPOS_SERVICIO},
    )

@router.post("/sesiones/registrar")
def registrar_sesion(
    rut: str = Form(...),
    nombre_paciente: str = Form(...),
    fecha: str = Form(...),
    tipo_atencion: str = Form(...),
    observaciones: str = Form(default=""),
    registrado_por: str = Form(...),
    equipo: str = Form(default=""),
    referencia: str = Form(default=""),
    ubicacion: str = Form(default=""),
    presion_bar: str = Form(default=""),
    repuestos_usados: str = Form(default=""),
):
    """
    Recibe los datos del formulario, los limpia y los guarda en Excel.
    """
    sesion = {
        "rut": rut.strip(),
        "nombre_paciente": nombre_paciente.strip(),
        "fecha": fecha,
        "tipo_servicio": tipo_atencion,
        "trabajo_realizado": observaciones.strip(),
        "tecnico": registrado_por.strip(),
        "equipo": equipo.strip(),
        "referencia": referencia.strip(),
        "ubicacion": ubicacion.strip(),
        "presion_bar": presion_bar,
        "repuestos_usados": repuestos_usados.strip(),
    }
    excel_service.guardar_sesion(sesion)

    return RedirectResponse(url=f"/paciente/{sesion['rut']}/historial", status_code=303)