# costumer_history (historial_clinico)

Aplicación web con FastAPI para registrar sesiones, consultar la bitácora de un paciente y generar/descargar el PDF del historial clínico a partir de un archivo Excel.

> Nota de nomenclatura: en este proyecto, `costumer_history` se utiliza como nombre del módulo/proyecto, pero el dominio corresponde a `historial_clinico`.

## Requisitos

- Python 3.10 o superior (recomendado)

## Instalación

1. Copia el proyecto en tu máquina.

2. Crear y activar el entorno virtual (si aún no existe):

   - **Windows (PowerShell):**
     - `python -m venv venv`
     - `.\venv\Scripts\Activate.ps1`

   - **Windows (cmd):**
     - `python -m venv venv`
     - `venv\Scripts\activate.bat`

   - **Linux / macOS:**
     - `python3 -m venv venv`
     - `source venv/bin/activate`

3. Instalar dependencias:

   - `pip install -r requirements.txt`

4. `data/historial.xlsx` es el Excel central (se crea automáticamente cuando implementes la lógica). La carpeta `output/` almacenará los PDFs generados bajo demanda.

## Estructura del proyecto

- `main.py` — Punto de entrada, instancia FastAPI y registro de rutas.

- `routes/`
  - `sesiones.py` — Registrar nueva sesión (GET form + POST datos).
  - `pacientes.py` — Buscar paciente y mostrar bitácora en pantalla.
  - `reportes.py` — Generar y descargar PDF del historial.

- `services/`
  - `excel_service.py` — Lectura y escritura del Excel centralizado.
  - `pdf_service.py` — Construcción y generación del PDF.

- `templates/`
  - `base.html` — Layout común (header, navegación, estilos base).
  - `index.html` — Página principal con buscador por RUT.
  - `registrar.html` — Formulario para registrar sesión.
  - `historial.html` — Bitácora del paciente (vista en pantalla).

- `static/`
  - `style.css` — Estilos básicos compartidos.

- `data/`
  - `historial.xlsx` — Base de datos Excel (se crea automáticamente).

- `output/`
  - PDFs generados por paciente (bajo demanda).

