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

# Opciones disponibles para el campo tipo_atencion
TIPOS_ATENCION = [
    "Limpieza",
    "Extracción",
    "Endodoncia",
    "Ortodoncia",
    "Revisión",
    "Otro",
]


@router.get("/sesiones/registrar")
def form_registrar(request: Request, rut: str = ""):
    """
    Muestra el formulario para registrar una nueva sesión.
    Si viene desde el historial de un paciente, el RUT llega precargado.
    """
    return templates.TemplateResponse(
        request=request,
        name="registrar.html",
        context={"rut": rut, "fecha_hoy": date.today().isoformat(), "tipos_atencion": TIPOS_ATENCION},
    )


@router.post("/sesiones/registrar")
def registrar_sesion(
    rut: str = Form(...),
    nombre_paciente: str = Form(...),
    fecha: str = Form(...),
    tipo_atencion: str = Form(...),
    observaciones: str = Form(default=""),
    registrado_por: str = Form(...),
):
    """
    Recibe los datos del formulario, los limpia y los guarda en Excel.
    Al finalizar redirige al historial del paciente.
    """
    sesion = {
        "rut": rut.strip(),
        "nombre_paciente": nombre_paciente.strip(),
        "fecha": fecha,
        "tipo_atencion": tipo_atencion,
        "observaciones": observaciones.strip(),
        "registrado_por": registrado_por.strip(),
    }
    excel_service.guardar_sesion(sesion)

    # Redirige al historial del paciente recién registrado
    # 303 See Other es el código correcto para redirect post POST
    return RedirectResponse(url=f"/paciente/{sesion['rut']}/historial", status_code=303)