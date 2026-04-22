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
    Busca por RUT o Patente.
    Si encuentra la patente, redirige al historial del dueño con el filtro aplicado.
    Si no, asume que se ingresó un RUT.
    """
    termino = rut.strip().upper()
    rut_encontrado = excel_service.buscar_cliente_por_patente(termino)
    
    if rut_encontrado:
        # Se ingresó una patente, redirigir al historial del dueño filtrando por esa patente
        return RedirectResponse(url=f"/paciente/{rut_encontrado}/historial?filtro_pat={termino}")
    else:
        # Se asume que es un RUT
        return RedirectResponse(url=f"/paciente/{termino}/historial")


@router.get("/paciente/{rut}/historial")
def historial_paciente(request: Request, rut: str, filtro_pat: str = None):
    """
    Recupera todas las sesiones del paciente desde Excel.
    Incluye filtro opcional por patente.
    """
    rut = rut.strip()
    todas_sesiones = excel_service.obtener_sesiones(rut)

    paciente = excel_service.obtener_paciente(rut)
    nombre = paciente["nombre_paciente"] if paciente else "Cliente no encontrado"

    # Extraer patentes únicas de las sesiones
    patentes = set()
    for s in todas_sesiones:
        if s.get("patente"):
            patentes.add(s["patente"])
    patentes = sorted(list(patentes))
    
    # Filtrar sesiones si hay filtro_pat
    sesiones_mostrar = todas_sesiones
    if filtro_pat:
        sesiones_mostrar = [s for s in todas_sesiones if s.get("patente") == filtro_pat]

    return templates.TemplateResponse(
        request=request,
        name="historial.html",
        context={
            "rut": rut, 
            "nombre": nombre, 
            "sesiones": sesiones_mostrar,
            "patentes": patentes,
            "pat_seleccionada": filtro_pat
        },
    )