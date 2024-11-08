from googlesearch import search
import requests
from bs4 import BeautifulSoup

def buscar_letra(cancion):
    # Término de búsqueda solo con el nombre de la canción
    query = f"{cancion} lyrics"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    # Iterar sobre múltiples resultados de Google
    for enlace in search(query, num_results=10):
        if any(site in enlace for site in ["letras.com", "musixmatch.com", "genius.com"]):
            print(f"Intentando obtener la letra desde: {enlace}")
            letra = extraer_letra(enlace)
            if letra:
                return letra
    
    return "No se encontró la letra en los resultados de Google."

def extraer_letra(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer letra según el sitio
        if "letras.com" in url:
            letra_div = soup.find('div', {'class': 'cnt-letra'})
        elif "musixmatch.com" in url:
            letra_div = soup.find('span', {'class': 'lyrics__content__ok'})
            if letra_div is None:  # Probar con otra estructura
                letra_div = soup.find_all('p')
                letra = "\n".join(p.get_text() for p in letra_div)
                return letra if letra else None
        elif "genius.com" in url:
            letra_div = soup.find('div', {'data-lyrics-container': 'true'})
            if letra_div is None:  # En Genius, las letras pueden estar en múltiples contenedores
                letra_divs = soup.find_all('div', {'data-lyrics-container': 'true'})
                letra = "\n".join(div.get_text(separator="\n") for div in letra_divs)
                return letra if letra else None

        if letra_div:
            return letra_div.get_text(separator="\n")
    return None

# Solicitar al usuario el nombre de la canción sin el artista
cancion = input("Ingrese el nombre de la canción: ")

# Buscar la letra basándose solo en el nombre de la canción
print(f"Buscando letra para la canción '{cancion}'...")
print(buscar_letra(cancion))
