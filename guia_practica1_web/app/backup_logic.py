import shutil
import os
from datetime import datetime
import hashlib
import threading
import time

# Controlador global para el backup automático
backup_running = False
backup_thread = None

def make_backup_file(filepath):
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.basename(filepath)
        destino = os.path.join('backup', f"{filename}_{timestamp}")
        shutil.copy2(filepath, destino)
        return destino
    return None

def restaurar_backup(nombre_original):
    backups = [f for f in os.listdir("backup") if f.startswith(nombre_original + "_")]
    if not backups:
        return False
    backups.sort(reverse=True)  # El más reciente
    archivo_respaldo = os.path.join("backup", backups[0])
    destino = os.path.join("backup", nombre_original)
    shutil.copy2(archivo_respaldo, destino)
    return True

def validar_archivos(file1, file2):
    def hash_file(path):
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    return hash1 == hash2

def backup_automatico(filepath):
    global backup_running
    while backup_running:
        make_backup_file(filepath)
        time.sleep(300)  # 5 minutos

def iniciar_backup_automatico(filepath):
    global backup_running, backup_thread
    if not backup_running:
        backup_running = True
        backup_thread = threading.Thread(target=backup_automatico, args=(filepath,))
        backup_thread.start()

def detener_backup_automatico():
    global backup_running
    backup_running = False