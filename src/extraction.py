import os
import pandas as pd

def cargar_pestaña_excel(ruta_archivo: str, nombre_pestaña: str) -> pd.DataFrame:
    """
    Valida la existencia de un archivo Excel, extrae una pestaña especifica
    y normaliza las cabeceras reemplazando los espacios por guiones bajos.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontro el archivo en la ruta: {ruta_archivo}")
    
    # Lectura del archivo utilizando el motor openpyxl
    df = pd.read_excel(ruta_archivo, sheet_name=nombre_pestaña, engine='openpyxl')
    
    # Normalizacion de los nombres de las columnas
    df.columns = [str(c).strip().replace(' ', '_') for c in df.columns]
    
    print(f"Extraccion exitosa: '{nombre_pestaña}' | Filas: {len(df)} | Columnas: {len(df.columns)}")
    return df