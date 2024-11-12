import essentia.standard as ess
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2

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

# Ejemplo de uso
process_audio_files('/ruta/a/tu/carpeta')
