import pandas as pd

# Diccionario de códigos postales por provincia
CODIGOS = {
    'Albacete': 'Alb_001', 'Alicante': 'Ali_002', 'Almería': 'Alm_003',
    'Araba': 'Ara_004', 'Ávila': 'Avi_005', 'Badajoz': 'Bad_006',
    'Balears': 'Bal_007', 'Barcelona': 'Bar_008', 'Burgos': 'Bur_009', 'Cáceres': 'Cac_010'
}
def procesar_poblacion(path):
    """
    Procesa el archivo CSV de población y devuelve un diccionario con el valor promedio por provincia.
    - Convierte la columna 'Recaudación' a numérico.
    - Reemplaza valores nulos con el valor mínimo.
    - Agrega códigos por provincia.
    - Calcula el promedio por provincia.
    
    # Leer archivo CSV
    df = pd.read_csv(path, sep=';')

    # Asegurarse de que la columna Recaudación sea numérica
    df['Recaudación'] = pd.to_numeric(df['Recaudación'], errors='coerce')

    # Rellenar valores nulos con el mínimo de la columna
    df['Recaudación'].fillna(df['Recaudación'].min(), inplace=True)

    # Agregar columna de códigos de provincia
    df['Codigo'] = df['Provincia'].map(CODIGOS)

    # Agrupar por provincia y calcular promedio
    promedio = df.groupby('Provincia')['Recaudación'].mean().round(2)

    # Devolver como diccionario
    return promedio.to_dict()"""
    
    df = pd.read_csv(path, sep=";")
    df['Recaudación'] = pd.to_numeric(df['Recaudación'], errors='coerce')
    df['Recaudación'].fillna(df['Recaudación'].min(), inplace=True)
    promedio = df.groupby('Provincia')['Recaudación'].mean().round(2).reset_index()
    return promedio  # Ahora retorna un DataFrame, no un diccionario