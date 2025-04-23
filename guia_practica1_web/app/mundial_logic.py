import pandas as pd

def obtener_datos_mundial():
    return pd.read_excel("Resumen_Mundial_80_Equipos.xlsx")

def obtener_datos_paginados(df, pagina, tamano=10):
    total = len(df)
    inicio = (pagina - 1) * tamano
    fin = inicio + tamano
    paginados = df.iloc[inicio:fin]
    total_paginas = (total + tamano - 1) // tamano
    return paginados, total_paginas

def obtener_historial_mundiales():
    return [
        (1930, 'Uruguay'), (1934, 'Italia'), (1938, 'Francia'), (1950, 'Brasil'),
        (1954, 'Suiza'), (1958, 'Suecia'), (1962, 'Chile'), (1966, 'Inglaterra'),
        (1970, 'México'), (1974, 'Alemania'), (1978, 'Argentina'), (1982, 'España'),
        (1986, 'México'), (1990, 'Italia'), (1994, 'Estados Unidos'), (1998, 'Francia'),
        (2002, 'Corea/Japón'), (2006, 'Alemania'), (2010, 'Sudáfrica'),
        (2014, 'Brasil'), (2018, 'Rusia'), (2022, 'Catar')
    ]
