"""
routes/reportes.py
------------------
Rutas para generación y descarga de reportes en PDF.

Rutas:
  GET /reportes/pdf/{rut} → Genera el PDF del historial y lo descarga
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from services import excel_service, pdf_service

router = APIRouter()


@router.get("/reportes/pdf/{rut}")
def descargar_pdf(rut: str):
    """
    Obtiene las sesiones del paciente, genera el PDF y lo retorna
    como descarga directa en el navegador.

    Si no hay sesiones, retorna un mensaje en lugar de un PDF vacío.
    """
    sesiones = excel_service.obtener_sesiones(rut)

    if not sesiones:
        return HTMLResponse(
            content="<p>No hay sesiones registradas para este RUT.</p>",
            status_code=404,
        )

    nombre = sesiones[0]["nombre_paciente"]
    ruta_pdf = pdf_service.generar_pdf(rut, nombre, sesiones)

    return FileResponse(
        path=ruta_pdf,
        filename=f"historial_{rut}.pdf",
        media_type="application/pdf",
    )