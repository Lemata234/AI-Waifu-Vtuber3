import subprocess
import psutil

def ejecutar_diagnostico():
    informe = []
    # Disco con wmic
    try:
        resultado = subprocess.run(['wmic', 'diskdrive', 'get', 'status'], capture_output=True, text=True)
        informe.append("=== Disco (WMIC) ===\n" + resultado.stdout)
    except Exception as e:
        informe.append(f"Error en disco: {e}")
    # CPU y RAM con psutil
    informe.append(f"=== CPU ===\nUso: {psutil.cpu_percent(interval=1)}%")
    mem = psutil.virtual_memory()
    informe.append(f"=== RAM ===\nTotal: {mem.total // 1024**3} GB, Usada: {mem.percent}%")
    return "\n".join(informe)