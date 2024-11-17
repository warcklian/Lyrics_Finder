import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs de páginas con listas de canciones populares
URLS = [
    "https://www.billboard.com/charts/hot-100",  # Billboard Hot 100
    "https://www.last.fm/charts"  # Last.fm Trending Tracks
]

# Función para obtener y procesar las canciones en Billboard
def obtener_canciones_billboard():
    url = "https://www.billboard.com/charts/hot-100"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("No se pudo acceder a Billboard")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    canciones = []

    # Selector específico para Billboard (ajusta si la estructura cambia)
    for idx, item in enumerate(soup.select("li.o-chart-results-list__item h3"), start=1):
        nombre = item.text.strip()
        artista = item.find_next_sibling("span").text.strip()  # El artista está en un <span> siguiente
        canciones.append({
            "Número": idx,
            "Nombre Canción": nombre,
            "Artistas": artista,
            "Fuente": "Billboard Hot 100"
        })

    return canciones

# Función para obtener y procesar las canciones en Last.fm
def obtener_canciones_lastfm():
    url = "https://www.last.fm/charts"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("No se pudo acceder a Last.fm")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    canciones = []

    # Selector específico para Last.fm (ajusta si la estructura cambia)
    for idx, item in enumerate(soup.select("div.chartlist-name"), start=1):
        nombre = item.a.text.strip()
        artista = item.find_next("span", {"class": "chartlist-artist"}).text.strip()
        canciones.append({
            "Número": idx,
            "Nombre Canción": nombre,
            "Artistas": artista,
            "Fuente": "Last.fm Trending Tracks"
        })

    return canciones

# Función principal para unificar las canciones de todas las fuentes
def obtener_todas_canciones():
    canciones_totales = []
    # Billboard
    canciones_totales.extend(obtener_canciones_billboard())
    # Last.fm
    canciones_totales.extend(obtener_canciones_lastfm())
    return canciones_totales

# Función para exportar los datos a Excel
def exportar_a_excel(canciones):
    df = pd.DataFrame(canciones)
    df.to_excel("canciones_populares.xlsx", index=False)
    print("Archivo exportado exitosamente como 'canciones_populares.xlsx'")

# Ejecutar scraping y exportar
canciones = obtener_todas_canciones()
if canciones:
    exportar_a_excel(canciones)
else:
    print("No se encontraron datos de canciones.")
