"""
services/pdf_service.py
-----------------------
Genera el PDF del historial clínico de un paciente usando ReportLab.

El PDF sobreescribe el anterior si ya existe (nombre = historial_{rut}.pdf).
Esto evita acumulación innecesaria de archivos en /output.

Funciones:
  generar_pdf(rut, nombre, sesiones) → str (ruta del PDF generado)
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ── Configuración ─────────────────────────────────────────────────────────────

RUTA_OUTPUT = "output"
COLOR_PRIMARIO = colors.HexColor("#2c7be5")
COLOR_FILA_PAR = colors.HexColor("#f0f6ff")


# ── Función pública ───────────────────────────────────────────────────────────

def generar_pdf(rut: str, nombre: str, sesiones: list) -> str:
    """
    Genera el PDF del historial del paciente.

    Input:
      rut      (str)  — RUT del paciente (usado para el nombre del archivo)
      nombre   (str)  — Nombre completo del paciente
      sesiones (list) — Lista de dicts con las sesiones ordenadas

    Output:
      str — Ruta completa del archivo PDF generado
    """
    os.makedirs(RUTA_OUTPUT, exist_ok=True)
    ruta_pdf = os.path.join(RUTA_OUTPUT, f"historial_{rut}.pdf")

    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    # Estilo de texto para celdas del cuerpo de la tabla
    # Paragraph respeta los anchos de columna y hace wrap automático
    celda_style = ParagraphStyle(
        "celda",
        fontName="Helvetica",
        fontSize=9,
        leading=13,       # Espaciado entre líneas
        spaceAfter=0,
    )

    # Estilo para cabeceras (texto blanco, negrita)
    cabecera_style = ParagraphStyle(
        "cabecera",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=colors.white,
    )

    elementos = []

    # ── Encabezado ────────────────────────────────────────────────────────────
    elementos.append(Paragraph("Historial Clínico", styles["Title"]))
    elementos.append(Spacer(1, 0.4 * cm))
    elementos.append(Paragraph(f"<b>Paciente:</b> {nombre}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>RUT:</b> {rut}", styles["Normal"]))
    elementos.append(Spacer(1, 0.8 * cm))

    # ── Tabla de sesiones ─────────────────────────────────────────────────────
    if sesiones:
        # Cabecera con Paragraph para consistencia de estilo
        datos_tabla = [[
            Paragraph("Fecha", cabecera_style),
            Paragraph("Tipo de Atención", cabecera_style),
            Paragraph("Observaciones", cabecera_style),
            Paragraph("Registrado por", cabecera_style),
        ]]

        for s in sesiones:
            # Usar Paragraph en cada celda permite wrap automático del texto
            datos_tabla.append([
                Paragraph(str(s.get("fecha", "")), celda_style),
                Paragraph(str(s.get("tipo_atencion", "")), celda_style),
                Paragraph(str(s.get("observaciones", "")), celda_style),
                Paragraph(str(s.get("registrado_por", "")), celda_style),
            ])

        # Anchos de columna — total 17cm (A4 21cm - 2cm margen x2)
        # Fecha: fija, Tipo: fija, Observaciones: la mayor parte, Registrado: resto
        tabla = Table(
            datos_tabla,
            colWidths=[2.5 * cm, 3.5 * cm, 8.0 * cm, 3.0 * cm],
            repeatRows=1,
        )

        # Estilo base — tipografía la maneja Paragraph, aquí solo layout y color
        estilo_base = [
            # Cabecera
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARIO),
            # Cuerpo y cabecera
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]

        # Filas alternas (color de fondo intercalado para facilitar lectura)
        for i in range(1, len(datos_tabla)):
            if i % 2 == 0:
                estilo_base.append(
                    ("BACKGROUND", (0, i), (-1, i), COLOR_FILA_PAR)
                )

        tabla.setStyle(TableStyle(estilo_base))
        elementos.append(tabla)

    else:
        elementos.append(
            Paragraph("No se encontraron sesiones registradas.", styles["Normal"])
        )

    doc.build(elementos)
    return ruta_pdf