"""
seed_data.py
------------
Script de carga de datos de prueba.
Simula el historial de sesiones de una consultora ficticia de software
llamada "StackSur Consultoría" que asesora a pymes en automatización.

Uso:
    python seed_data.py

Ubicación: raíz del proyecto (mismo nivel que main.py)
Ejecutar ANTES de levantar el servidor, o con el servidor detenido.
"""

from services.excel_service import guardar_sesion

SESIONES = [
    # ─── Cliente 1: Clínica DentPro ───────────────────────────────────────────
    {
        "rut": "76.234.111-5",
        "nombre_paciente": "Clínica DentPro SpA",
        "fecha": "2025-01-14",
        "tipo_atencion": "Revisión",
        "observaciones": (
            "Reunión inicial de diagnóstico. El cliente gestiona historial de "
            "pacientes en papel. Se identificaron 3 procesos automatizables: "
            "registro de sesiones, generación de PDF y envío de recordatorios."
        ),
        "registrado_por": "Andrea Muñoz",
    },
    {
        "rut": "76.234.111-5",
        "nombre_paciente": "Clínica DentPro SpA",
        "fecha": "2025-01-28",
        "tipo_atencion": "Limpieza",
        "observaciones": (
            "Entrega de propuesta técnica MVP. Se acordó stack: FastAPI + "
            "OpenPyXL + ReportLab. Plazo de entrega estimado: 3 semanas. "
            "Cliente aprobó arquitectura sin observaciones."
        ),
        "registrado_por": "Andrea Muñoz",
    },
    {
        "rut": "76.234.111-5",
        "nombre_paciente": "Clínica DentPro SpA",
        "fecha": "2025-02-18",
        "tipo_atencion": "Endodoncia",
        "observaciones": (
            "Entrega MVP v1.0. Se realizó capacitación presencial de 1 hora "
            "con la recepcionista. Se detectó necesidad de validación de RUT "
            "en el formulario. Queda como ticket para V2."
        ),
        "registrado_por": "Cristopher Vega",
    },

    # ─── Cliente 2: Ferretería Los Andes ──────────────────────────────────────
    {
        "rut": "78.901.456-2",
        "nombre_paciente": "Ferretería Los Andes Ltda.",
        "fecha": "2025-02-03",
        "tipo_atencion": "Revisión",
        "observaciones": (
            "Diagnóstico inicial. El cliente lleva inventario en cuaderno "
            "físico. Solicita sistema simple para registrar entradas y salidas "
            "de stock. Volumen estimado: 200 productos, 2 usuarios."
        ),
        "registrado_por": "Cristopher Vega",
    },
    {
        "rut": "78.901.456-2",
        "nombre_paciente": "Ferretería Los Andes Ltda.",
        "fecha": "2025-02-20",
        "tipo_atencion": "Extracción",
        "observaciones": (
            "Se descartó sistema de inventario complejo. Se propuso solución "
            "con Excel + formulario web local, mismo stack del proyecto clínica. "
            "Cliente valoró la reutilización de componentes y el menor costo."
        ),
        "registrado_por": "Andrea Muñoz",
    },
    {
        "rut": "78.901.456-2",
        "nombre_paciente": "Ferretería Los Andes Ltda.",
        "fecha": "2025-03-10",
        "tipo_atencion": "Ortodoncia",
        "observaciones": (
            "Entrega de prototipo funcional. Problema detectado: el dueño "
            "quiere exportar reportes de stock mensual en PDF. Se agenda "
            "sesión adicional para integrar módulo de reportes."
        ),
        "registrado_por": "Cristopher Vega",
    },
    {
        "rut": "78.901.456-2",
        "nombre_paciente": "Ferretería Los Andes Ltda.",
        "fecha": "2025-03-28",
        "tipo_atencion": "Revisión",
        "observaciones": (
            "Módulo de reportes PDF integrado y entregado. Sistema en producción. "
            "Cliente solicita cotización para automatizar envío de órdenes de "
            "compra a proveedores vía WhatsApp. Se deja como proyecto futuro."
        ),
        "registrado_por": "Andrea Muñoz",
    },

    # ─── Cliente 3: Consultora HR Estratégica ─────────────────────────────────
    {
        "rut": "77.543.890-K",
        "nombre_paciente": "HR Estratégica Consultores",
        "fecha": "2025-03-05",
        "tipo_atencion": "Revisión",
        "observaciones": (
            "Primera reunión. La empresa gestiona contratos de clientes en "
            "Word y carpetas locales. Necesitan trazabilidad de interacciones "
            "por cliente. Se propone sistema de historial similar al de DentPro."
        ),
        "registrado_por": "Cristopher Vega",
    },
    {
        "rut": "77.543.890-K",
        "nombre_paciente": "HR Estratégica Consultores",
        "fecha": "2025-03-19",
        "tipo_atencion": "Limpieza",
        "observaciones": (
            "Taller de levantamiento de requerimientos. Se mapearon 6 tipos "
            "de atención propios del rubro: Diagnóstico, Propuesta, Seguimiento, "
            "Cierre, Soporte, Renovación. Se adapta formulario base al contexto."
        ),
        "registrado_por": "Andrea Muñoz",
    },
    {
        "rut": "77.543.890-K",
        "nombre_paciente": "HR Estratégica Consultores",
        "fecha": "2025-04-02",
        "tipo_atencion": "Otro",
        "observaciones": (
            "Entrega de MVP adaptado. Se reemplazaron los tipos de atención "
            "de la clínica por los del rubro HR. El cliente solicitó agregar "
            "campo 'próxima acción' al formulario. Se implementa en V2."
        ),
        "registrado_por": "Cristopher Vega",
    },
]


def main():
    print(f"Cargando {len(SESIONES)} sesiones de prueba...\n")

    for s in SESIONES:
        guardar_sesion(s)
        print(f"  ✔ {s['nombre_paciente']} — {s['fecha']} — {s['tipo_atencion']}")

    print(f"\n{len(SESIONES)} sesiones cargadas correctamente en data/historial.xlsx")
    print("Puedes levantar el servidor y buscar cualquiera de estos RUTs:")
    print("  → 76.234.111-5  (Clínica DentPro SpA)")
    print("  → 78.901.456-2  (Ferretería Los Andes Ltda.)")
    print("  → 77.543.890-K  (HR Estratégica Consultores)")


if __name__ == "__main__":
    main()