from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import os
from . import backup_logic, poblacion_logic, mundial_logic
import subprocess

main_bp = Blueprint("main", __name__)

# Diccionario reducido solo a países sede de mundiales
CODIGO_BANDERAS = {
    "Uruguay": "uy", "Italia": "it", "Francia": "fr", "Brasil": "br", "Suiza": "ch",
    "Suecia": "se", "Chile": "cl", "Inglaterra": "gb", "México": "mx", "Alemania": "de",
    "Argentina": "ar", "España": "es", "Estados Unidos": "us", "Corea/Japón": "kr",  
    "Sudáfrica": "za", "Rusia": "ru", "Catar": "qa"
}

@main_bp.route('/')
def index():
    return render_template("backup.html")

@main_bp.route('/backup', methods=['GET', 'POST'])
def backup():
    if request.method == 'POST':
        accion = request.form.get('accion')
        file = request.files.get('file')
        filepath = None

        if file and file.filename:
            filepath = os.path.join('backup', file.filename)
            file.save(filepath)

        if accion == 'manual':
            if filepath:
                backup_logic.make_backup_file(filepath)
                flash('✅ Backup manual creado.', 'success')

        elif accion == 'iniciar_auto':
            if filepath:
                backup_logic.iniciar_backup_automatico(filepath)
                flash('🕓 Backup automático iniciado cada 5 minutos.', 'success')
            else:
                flash('❌ Selecciona un archivo para iniciar el backup automático.', 'error')

        elif accion == 'detener_auto':
            backup_logic.detener_backup_automatico()
            flash('🛑 Backup automático detenido.', 'success')

        return redirect(url_for('main.backup'))

    return render_template("backup.html")


@main_bp.route('/restaurar', methods=['POST'])
def restaurar():
    filename = request.form.get('filename')
    if filename:
        resultado = backup_logic.restaurar_backup(filename)
        flash('✅ Archivo restaurado correctamente.' if resultado else '❌ No se encontró copia de seguridad.', 'success' if resultado else 'error')
    return redirect(url_for('main.backup'))

@main_bp.route('/validar', methods=['POST'])
def validar():
    original = request.files['original']
    recuperado = request.files['recuperado']

    path_original = os.path.join('backup', 'original_temp')
    path_recuperado = os.path.join('backup', 'recuperado_temp')

    original.save(path_original)
    recuperado.save(path_recuperado)

    resultado = backup_logic.validar_archivos(path_original, path_recuperado)

    os.remove(path_original)
    os.remove(path_recuperado)

    return render_template('backup.html', resultado_validacion=resultado)
"""
@main_bp.route('/poblacion')
def poblacion():
    
    promedio = poblacion_logic.procesar_poblacion("poblacionMunicipios_recaudacion.csv")
    provincias = list(promedio.keys())
    valores = list(promedio.values())

    # Diccionario para la tabla
    codigos = {
        'Albacete': 'Alb_001', 'Alicante': 'Ali_002', 'Almería': 'Alm_003',
        'Araba': 'Ara_004', 'Ávila': 'Avi_005', 'Badajoz': 'Bad_006',
        'Balears': 'Bal_007', 'Barcelona': 'Bar_008', 'Burgos': 'Bur_009', 'Cáceres': 'Cac_010'
    }

    return render_template("poblacion.html", provincias=provincias, valores=valores, provincias_codigos=codigos)
"""
@main_bp.route('/poblacion')
def poblacion():
    pagina = int(request.args.get('pagina', 1))
    df = poblacion_logic.procesar_poblacion("poblacionMunicipios_recaudacion.csv")

    # Paginación
    tamano = 10
    total = len(df)
    total_paginas = (total + tamano - 1) // tamano
    inicio = (pagina - 1) * tamano
    fin = inicio + tamano

    df_pagina = df.iloc[inicio:fin]
    provincias = df_pagina['Provincia'].tolist()
    valores = df_pagina['Recaudación'].tolist()

    codigos = {
        'Albacete': 'Alb_001', 'Alicante': 'Ali_002', 'Almería': 'Alm_003',
        'Araba/Álava': 'Ara_004', 'Ávila': 'Avi_005', 'Badajoz': 'Bad_006',
        'Balears': 'Bal_007', 'Barcelona': 'Bar_008', 'Burgos': 'Bur_009',
        'Cáceres': 'Cac_010'
    }

    return render_template("poblacion.html",
                           provincias=provincias,
                           valores=valores,
                           provincias_codigos=codigos,
                           pagina=pagina,
                           total_paginas=total_paginas)

@main_bp.route('/mundial')
def mundial():
    pagina = int(request.args.get('pagina', 1))
    df = mundial_logic.obtener_datos_mundial()
    datos_pagina, total_paginas = mundial_logic.obtener_datos_paginados(df, pagina)

    equipos = list(datos_pagina['Selección'])
    ganados = list(datos_pagina['Ganados'])
    empatados = list(datos_pagina['Empatados'])
    perdidos = list(datos_pagina['Perdidos'])
    pendientes = list(datos_pagina['Pendientes'])

    total_equipos = len(df)
    paises_visualizados = min(pagina * 10, total_equipos)

    historial = mundial_logic.obtener_historial_mundiales()

    return render_template(
        "mundial.html",
        equipos=equipos,
        ganados=ganados,
        empatados=empatados,
        perdidos=perdidos,
        pendientes=pendientes,
        pagina=pagina,
        total_paginas=total_paginas,
        historial=historial,
        paises_visualizados=paises_visualizados,
        total_equipos=total_equipos,
        codigos=CODIGO_BANDERAS
    )
