from src.extraction import cargar_pestaña_excel

def ejecutar_pipeline():
    print("=== PIPELINE CALL CENTER: FASE 1 (EXTRACCION) ===")
    
    # Definicion de rutas de los archivos fuentes
    ruta_interacciones = 'data/raw/Data_Robust_Call_Center_Log_Interacciones.xlsx'
    ruta_maestro = 'data/raw/Data_Robust_Call_Center_Maestro_Clientes.xlsx'
    
    try:
        # Extraccion del Log de Interacciones
        df_interacciones = cargar_pestaña_excel(ruta_interacciones, 'Log_Interacciones')
        
        # Extraccion del Maestro de Clientes
        df_clientes = cargar_pestaña_excel(ruta_maestro, 'Maestro_Clientes')
        
        print("\n--- Control de Calidad en la Extraccion ---")
        print(f"Campos de Interacciones: {list(df_interacciones.columns)}")
        print(f"Campos de Clientes:      {list(df_clientes.columns)}")
        print("==================================================")
        
        return df_interacciones, df_clientes
        
    except Exception as e:
        print(f"Error critico en la Fase 1: {e}")
        return None, None

if __name__ == "__main__":
    ejecutar_pipeline()