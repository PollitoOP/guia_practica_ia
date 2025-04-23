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
    Los valores nulos en 'Valor' son reemplazados por el valor mínimo encontrado.
    """
    df = pd.read_csv(path)

    # Convertir a numérico y depurar valores nulos
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df['Valor'].fillna(df['Valor'].min(), inplace=True)

    # Añadir códigos a las provincias
    df['Codigo'] = df['Provincia'].map(CODIGOS)

    # Calcular promedio por provincia
    promedio = df.groupby('Provincia')['Valor'].mean().round(2)

    return promedio.to_dict()
