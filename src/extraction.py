import os
from dotenv import load_dotenv  
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup


# CTMDB setup
load_dotenv()
token = os.getenv("TMDB_READ_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"}

# Wikipedia setup
WIKI_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}



# Función para obtener los géneros de películas ya que los vemos en IDs
def get_genres():
    endpoint = f"{BASE_URL}/genre/movie/list"
    params = {"language": "en-US"}
    response = requests.get(endpoint, headers=HEADERS, params=params)
    #Verificación de la respuesta
    if response.status_code == 200:
        data = response.json()
        return data.get("genres", [])
    else:
        print(f"Error al obtener géneros: {response.status_code}")
        return []
    
# Función para extraer películas de un año específico
def get_movies_by_year(year, max_pages=5):
    endpoint = f"{BASE_URL}/discover/movie"
    all_movies = []
    #parámetros de la consulta
    for page in range(1, max_pages + 1):
        query_params = {"primary_release_year": year, "page": page, "sort_by": "popularity.desc", "language": "en-US"}

        try:
            response = requests.get(endpoint, headers=HEADERS, params=query_params, timeout=30)
            
            if response.status_code == 200:
                page_data = response.json()
                movies = page_data.get("results", [])
                all_movies.extend(movies)

            else:
                print(f"Error al obtener películas para el año {year}, página {page}: {response.status_code}")
                break

            time.sleep(0.2) 

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            break
    return all_movies
                        
# Función para descragar todo el rango de años elegido
def fetch_full_history(start_year:1930, end_year=2024):
    full_data = []

    for year in range(start_year, end_year + 1):
        year_movies = get_movies_by_year(year, max_pages=5)
        full_data.extend(year_movies)
    
    return full_data



# Web scraping wikipedia ("Timeline of wars")
def get_df(url):
    response = requests.get(url, headers=WIKI_HEADERS, timeout=30)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        return extract_wars_info(soup, source_page=url)
    else:
        print(f"Error al acceder a la página: {response.status_code}")
        return pd.DataFrame()
    
def extract_wars_info(soup, source_page):
    started_years = []
    ended_years = []
    conflict_names = []
    source_pages = []

    tables = soup.find_all('table', class_='wikitable')
    for table in tables: 
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            
            if len(cells) >= 3:
                started = cells[0].get_text(" ", strip=True)
                ended = cells[1].get_text(" ", strip=True)
                name = cells[2].get_text(" ", strip=True)

                started_years.append(started)
                ended_years.append(ended)
                conflict_names.append(name)
                source_pages.append(source_page)

    df = pd.DataFrame({"started_year": started_years, "ended_year": ended_years, "conflict_name": conflict_names, "source_page": source_pages})
    return df

def fetch_wars_data():
    urls = [
        "https://en.wikipedia.org/wiki/List_of_wars:_1900%E2%80%931944",
        "https://en.wikipedia.org/wiki/List_of_wars:_1945%E2%80%931989",
        "https://en.wikipedia.org/wiki/List_of_wars:_1990%E2%80%932002",
        "https://en.wikipedia.org/wiki/List_of_wars:_2003%E2%80%932019",
        "https://en.wikipedia.org/wiki/List_of_wars:_2020%E2%80%93present"]
    
    all_wars_df = []

    for url in urls:
        df_url = get_df(url)
        all_wars_df.append(df_url)

    return pd.concat(all_wars_df, ignore_index=True)