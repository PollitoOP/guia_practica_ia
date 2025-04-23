import shutil
import os
from datetime import datetime
import hashlib

def make_backup_file(filepath):
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.basename(filepath)
        backup_name = f"{filename}_{timestamp}"
        destino = os.path.join('backup', backup_name)
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
