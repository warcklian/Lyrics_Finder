import subprocess
import sys
import os

# Lista de dependencias requeridas
DEPENDENCIAS = [
    ("essentia", "essentia"),
    ("mutagen", "mutagen"),
    ("googlesearch-python", "googlesearch"),
    ("requests", "requests"),
    ("beautifulsoup4", "bs4")
]

def instalar_o_actualizar(paquete, modulo):
    """
    Verifica si el módulo está instalado. Si no está, lo instala.
    Si está instalado, intenta actualizarlo.
    """
    try:
        # Intenta importar el módulo para verificar si está instalado
        __import__(modulo)
        print(f"{modulo} ya está instalado. Intentando actualizar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", paquete])
        print(f"{modulo} se ha actualizado correctamente.")
    except ImportError:
        # Si el módulo no está instalado, procede a instalarlo
        print(f"{modulo} no está instalado. Procediendo con la instalación...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"{modulo} se ha instalado correctamente.")

def verificar_dependencias():
    """
    Verifica todas las dependencias requeridas e instala o actualiza según sea necesario.
    """
    print("Verificando dependencias...")
    for paquete, modulo in DEPENDENCIAS:
        instalar_o_actualizar(paquete, modulo)
    print("Todas las dependencias están instaladas y actualizadas.")

# Verificar dependencias antes de las importaciones específicas
verificar_dependencias()

# Importaciones después de verificar e instalar las dependencias
import essentia.standard as ess
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2

# Función para obtener el BPM, el tono, el género y la estructura de la canción
def get_bpm_key_genre_structure(file_path):
    # Cargar el archivo de audio independientemente de su tipo
    audio = ess.MonoLoader(filename=file_path)()

    # Extracción de BPM
    rhythm_extractor = ess.RhythmExtractor2013(method="multifeature")
    bpm, _, _, _, _ = rhythm_extractor(audio)
    
    # Extracción del tono
    key_extractor = ess.KeyExtractor()
    key, scale, strength = key_extractor(audio)
    
    # Estimación del género (esto es solo un ejemplo, puede no ser preciso)
    genre_extractor = ess.MusicExtractor(lowlevelSilentFrames='drop')  # Extrae varias características
    features, genre_data = genre_extractor(file_path), None
    if 'genre' in features:  # Verifica si el género está presente en los datos extraídos
        genre_data = features['genre']
    
    # Detección de estructura básica (segmentos de la canción)
    segmenter = ess.BeatTrackerMultiFeature()  # Detecta segmentos en la pista
    beats = segmenter(audio)  # Lista de tiempos de los beats detectados
    
    # Crear una descripción simple de estructura
    structure_description = "Estructura estimada: "
    if beats:
        structure_description += "Intro - Verso - Coro - Outro"  # Esto es solo una estimación de ejemplo

    return bpm, f"{key}-{scale}", genre_data, structure_description

# Función para procesar una carpeta con archivos MP3 y WAV
def process_audio_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            bpm, key, genre, structure = get_bpm_key_genre_structure(file_path)
            print(f"Archivo: {filename}")
            print(f"  BPM: {bpm}")
            print(f"  Key: {key}")
            print(f"  Género: {genre}")
            print(f"  Estructura: {structure}")
            print()

# Función principal para ejecutar el script
def main():
    print("Dependencias verificadas. Procesando archivos de audio...")
    directory = input("Introduce la ruta de la carpeta que contiene los archivos MP3 y WAV: ")
    if os.path.isdir(directory):
        process_audio_files(directory)
    else:
        print("La ruta especificada no es válida.")

if __name__ == "__main__":
    main()
