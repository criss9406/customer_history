"""
main.py
-------
Punto de entrada de la aplicación.
Instancia FastAPI, monta archivos estáticos, registra las rutas
y crea las carpetas necesarias si no existen.

Ejecución: uvicorn main:app --reload
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import sesiones, pacientes, reportes

# ── Crear carpetas necesarias si no existen ──────────────────────────────────
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# ── Instancia principal ──────────────────────────────────────────────────────
app = FastAPI(title="Historial Clínico")

# ── Archivos estáticos (CSS) ─────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Rutas ────────────────────────────────────────────────────────────────────
app.include_router(pacientes.router)
app.include_router(sesiones.router)
app.include_router(reportes.router)
