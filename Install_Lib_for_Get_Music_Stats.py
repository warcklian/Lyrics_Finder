import subprocess
import sys
import importlib

# Lista de librerías necesarias para el proyecto
required_libraries = [
    "requests",
    "beautifulsoup4",
    "pandas"
]

def install_or_update_library(library):
    """
    Verifica si una biblioteca está instalada. Si no lo está, la instala.
    Si ya está instalada, intenta actualizarla.
    """
    try:
        # Intentar importar la biblioteca para verificar si está instalada
        importlib.import_module(library)
        print(f"{library} ya está instalada. Intentando actualizar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", library])
        print(f"{library} se ha actualizado correctamente.")
    except ImportError:
        # Si no está instalada, se procede a la instalación
        print(f"{library} no está instalada. Procediendo con la instalación...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])
        print(f"{library} se ha instalado correctamente.")

def check_and_install_libraries():
    """
    Verifica todas las bibliotecas de la lista y las instala o actualiza según sea necesario.
    """
    for library in required_libraries:
        install_or_update_library(library)

if __name__ == "__main__":
    print("Verificando e instalando dependencias necesarias...")
    check_and_install_libraries()
    print("Todas las dependencias están instaladas y actualizadas.")
