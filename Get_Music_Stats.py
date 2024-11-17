import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página con las canciones más populares (reemplaza con una página real si es posible)
URL = "https://www.example.com/top-songs"  # Asegúrate de reemplazar esta URL por una real

# Función para obtener y procesar la página web
def obtener_datos_canciones():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    
    # Intentar acceder a la página
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")
        return []

    # Revisar contenido de la página (descomenta para depurar)
    # print(response.text[:500])

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Listado para almacenar las canciones
    canciones = []
    
    # Ejemplo de estructura HTML (debes ajustar los selectores CSS a la página que uses)
    for item in soup.select(".song-item"):
        try:
            # Verificar y obtener cada dato, con validación para evitar errores si el elemento no se encuentra
            numero = item.select_one(".song-rank")
            numero = numero.text.strip() if numero else "N/A"

            nombre = item.select_one(".song-title")
            nombre = nombre.text.strip() if nombre else "N/A"

            artistas = item.select_one(".song-artist")
            artistas = artistas.text.strip() if artistas else "N/A"

            genero = item.select_one(".song-genre")
            genero = genero.text.strip() if genero else "N/A"
            
            # Extraer vistas por país y plataforma, con validación de existencia de elementos
            vistas_por_pais = {}
            for vista in item.select(".song-views .view-item"):
                pais = vista.select_one(".view-country")
                pais = pais.text.strip() if pais else "Desconocido"

                reproducciones = vista.select_one(".view-count")
                reproducciones = reproducciones.text.strip() if reproducciones else "0"

                plataforma = vista.select_one(".view-platform")
                plataforma = plataforma.text.strip() if plataforma else "Desconocida"

                vistas_por_pais[f"{pais}, {plataforma}"] = reproducciones
            
            # Añadir la canción a la lista con todos los detalles extraídos
            canciones.append({
                "Número": numero,
                "Nombre Canción": nombre,
                "Artistas": artistas,
                "Género Musical": genero,
                "Vistas por País y Plataforma": "; ".join([f"{pais}: {vistas}" for pais, vistas in vistas_por_pais.items()])
            })
        
        except AttributeError:
            # Si falta algún dato o hay un error, continúa con la siguiente canción
            continue

    return canciones

# Función para exportar los datos a Excel
def exportar_a_excel(canciones):
    # Crear DataFrame y exportar a Excel
    df = pd.DataFrame(canciones)
    df.to_excel("canciones_mas_reproducidas.xlsx", index=False)
    print("Archivo exportado exitosamente como 'canciones_mas_reproducidas.xlsx'")

# Ejecutar scraping y exportar
canciones = obtener_datos_canciones()
if canciones:
    exportar_a_excel(canciones)
else:
    print("No se encontraron datos de canciones.")
