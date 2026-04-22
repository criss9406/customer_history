# Historial Clínico — MVP

Sistema de digitalización de historial de tratamientos para clínicas dentales.
Ejecución local, sin base de datos externa.

---

## Requisitos

- Python 3.10 o superior
- pip

---

## Instalación

```bash
# 1. Clona o copia el proyecto
cd historial_clinico

# 2. Crea un entorno virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt
```

---

## Ejecución

```bash
uvicorn main:app --reload
```

Abre el navegador en: **http://localhost:8000**

---

## Estructura del proyecto

```
historial_clinico/
├── main.py                  # Punto de entrada
├── routes/
│   ├── sesiones.py          # Registrar sesión
│   ├── pacientes.py         # Buscar y ver historial
│   └── reportes.py          # Generar PDF
├── services/
│   ├── excel_service.py     # Lectura/escritura Excel
│   └── pdf_service.py       # Generación PDF
├── templates/               # HTML (Jinja2)
├── static/                  # CSS
├── data/                    # historial.xlsx (se crea automáticamente)
├── output/                  # PDFs generados
└── requirements.txt
```

---

## Uso

| Acción | URL |
|---|---|
| Buscar paciente | `http://localhost:8000/` |
| Ver historial | `http://localhost:8000/paciente/{rut}/historial` |
| Registrar sesión | `http://localhost:8000/sesiones/registrar` |
| Descargar PDF | `http://localhost:8000/reportes/pdf/{rut}` |

---

## Notas importantes

- El archivo `data/historial.xlsx` se crea automáticamente en el primer uso.
- Los PDFs se guardan en `output/historial_{rut}.pdf` y se sobreescriben en cada generación.
- No modificar el orden de columnas en el Excel manualmente.
- Esta versión no tiene autenticación. Para uso en red local, asegurarse de que solo los equipos autorizados tengan acceso.

### Notas de Desarrollo (Rama Autofix)
- **Mejora futura:** Generar una nueva base de datos (nueva hoja en el archivo `.xlsx`) para tener un registro independiente de vehículos, dado que un mismo cliente puede tener más de uno. En esta nueva base de datos, el identificador único (ID) será la patente.
- **Búsqueda Extendida:** Ampliar el rango de búsqueda en la página principal, permitiendo buscar tanto por RUT del cliente como por Patente del vehículo.
- **Filtros en el Historial:** Agregar un sistema de filtros en la pestaña del historial para permitir buscar u ordenar las atenciones por Patente u otros campos relevantes (ej. fecha o tipo de servicio).