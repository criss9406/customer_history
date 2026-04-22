import os

RUTA_EXCEL = "data/historial.xlsx"
RUTA_OUTPUT = "output/"

def limpiar_datos():
    print("Iniciando limpieza de base de datos...")
    
    # 1. Eliminar base de datos Excel
    if os.path.exists(RUTA_EXCEL):
        os.remove(RUTA_EXCEL)
        print(f"✅ Archivo de base de datos eliminado: {RUTA_EXCEL}")
    else:
        print(f"ℹ️ El archivo de base de datos no existe: {RUTA_EXCEL}")
        
    # 2. Eliminar PDFs generados (opcional, pero útil para pruebas)
    if os.path.exists(RUTA_OUTPUT):
        archivos_pdf = [f for f in os.listdir(RUTA_OUTPUT) if f.endswith('.pdf')]
        for pdf in archivos_pdf:
            os.remove(os.path.join(RUTA_OUTPUT, pdf))
        if archivos_pdf:
            print(f"✅ Se eliminaron {len(archivos_pdf)} reportes PDF de prueba.")
            
    print("\n¡Limpieza completada! El entorno está como nuevo.")

if __name__ == "__main__":
    limpiar_datos()
