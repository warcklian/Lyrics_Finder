import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página con las canciones más populares (reemplaza con una página real si es posible)
URL = "https://www.example.com/top-songs"

# Función para obtener y procesar la página web
def obtener_datos_canciones():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    
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
            numero = item.select_one(".song-rank").text.strip()
            nombre = item.select_one(".song-title").text.strip()
            artistas = item.select_one(".song-artist").text.strip()
            genero = item.select_one(".song-genre").text.strip()
            
            # Extraer vistas por país y plataforma (ajusta según la estructura HTML)
            vistas_por_pais = {}
            for vista in item.select(".song-views .view-item"):
                pais = vista.select_one(".view-country").text.strip()
                reproducciones = vista.select_one(".view-count").text.strip()
                plataforma = vista.select_one(".view-platform").text.strip()
                vistas_por_pais[f"{pais}, {plataforma}"] = reprodu
