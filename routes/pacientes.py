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
def historial_paciente(request: Request, rut: str, ref: str = None):
    """
    Recupera todas las sesiones del paciente desde Excel
    y las renderiza en formato bitácora.
    Incluye filtro opcional por referencia del equipo.
    """
    # 1. Obtener todas las sesiones para extraer referencias
    todas_sesiones = excel_service.obtener_sesiones(rut)
    
    # 2. Obtener el nombre del cliente (ahora usando la función de pacientes o de las sesiones)
    cliente = excel_service.obtener_paciente(rut)
    if cliente:
        nombre = cliente["nombre_paciente"]
    else:
        nombre = todas_sesiones[0]["nombre_paciente"] if todas_sesiones else "Cliente no encontrado"
        
    # 3. Extraer referencias únicas
    referencias = set()
    for s in todas_sesiones:
        if s.get("referencia"):
            referencias.add(s["referencia"])
    referencias = sorted(list(referencias))
    
    # 4. Filtrar si se solicita
    sesiones_mostrar = todas_sesiones
    if ref:
        sesiones_mostrar = [s for s in todas_sesiones if s.get("referencia") == ref]

    return templates.TemplateResponse(
        request=request,
        name="historial.html",
        context={
            "rut": rut,
            "nombre": nombre,
            "sesiones": sesiones_mostrar,
            "referencias": referencias,
            "ref_seleccionada": ref
        },
    )