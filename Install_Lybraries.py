import subprocess
import sys

# Lista de bibliotecas necesarias para el script
required_libraries = ['googlesearch-python', 'requests', 'beautifulsoup4']

def check_and_install_libraries():
    """Verifica si las bibliotecas están instaladas, si no, las instala y actualiza las existentes."""
    for library in required_libraries:
        try:
            __import__(library.split('-')[0])  # Intenta importar el módulo principal de la biblioteca
            print(f"{library} ya está instalada.")
        except ImportError:
            print(f"{library} no está instalada. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(f"{library} instalada correctamente.")
    
    # Actualizar todas las bibliotecas
    print("Actualizando bibliotecas instaladas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + required_libraries)

# Ejecutar la verificación e instalación
check_and_install_libraries()
