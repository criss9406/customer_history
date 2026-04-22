"""
routes/pacientes.py
-------------------
Rutas relacionadas a la búsqueda y visualización del historial de pacientes.

Rutas:
  GET /                        → Página principal con buscador
  GET /buscar?rut=...          → Redirige al historial del paciente (recibe form GET)
  GET /paciente/{rut}/historial → Muestra la bitácora de sesiones del paciente
"""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services import excel_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(request: Request):
    """Página principal: muestra el buscador por RUT."""
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/buscar")
def buscar(rut: str):
    """
    Intermediario entre el formulario de búsqueda (que envía query params)
    y la ruta de historial (que usa path params).

    Los formularios HTML GET no pueden construir rutas dinámicas,
    por eso esta ruta actúa como puente.
    """
    return RedirectResponse(url=f"/paciente/{rut.strip()}/historial")


@router.get("/paciente/{rut}/historial")
def historial_paciente(request: Request, rut: str):
    """
    Recupera todas las sesiones del paciente desde Excel
    y las renderiza en formato bitácora.
    """
    sesiones = excel_service.obtener_sesiones(rut)

    paciente = excel_service.obtener_paciente(rut)
    nombre = paciente["nombre_paciente"] if paciente else "Paciente no encontrado"

    return templates.TemplateResponse(
        request=request,
        name="historial.html",
        context={"rut": rut, "nombre": nombre, "sesiones": sesiones},
    )