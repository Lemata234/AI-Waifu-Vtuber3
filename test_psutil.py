import psutil

# Uso de CPU
print(f"CPU: {psutil.cpu_percent(interval=1)}%")

# Memoria RAM
mem = psutil.virtual_memory()
print(f"RAM Total: {mem.total / (1024**3):.2f} GB")
print(f"RAM Usada: {mem.percent}%")
print(f"RAM Disponible: {mem.available / (1024**3):.2f} GB")

# Discos (opcional)
print("\n--- Particiones de disco ---")
for part in psutil.disk_partitions():
    try:
        uso = psutil.disk_usage(part.mountpoint)
        print(f"Unidad {part.device}: {uso.percent}% usado")
    except:
        pass