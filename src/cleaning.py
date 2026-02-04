import pandas as pd


# Funciones para limpiar los datos de películas
def clean_movies_data(df, genre_dict):

    # Seleccionamos columnas y eliminamos duplicados
    cols = ['id', 'title', 'release_date', 'genre_ids']
    df_clean = df[cols].drop_duplicates(subset='id').copy()

    # Convertimos release_date a datetime y extraemos el año
    df_clean['release_date'] = pd.to_datetime(df_clean['release_date'], errors='coerce')
    df_clean['year'] = df_clean['release_date'].dt.year
    df_clean = df_clean.dropna(subset=['year'])
    df_clean['year'] = df_clean['year'].astype(int)

    # Limpieza IDs de géneros
    df_clean['genre_ids'] = df_clean['genre_ids'].astype(str).str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace(' ', '', regex=False)

    # Separamos los géneros en varias columnas
    df_columns = df_clean['genre_ids'].str.split(',', expand=True)

    # Creamos lista vacía para guardar todo
    lista_tablas = []

    for col in df_columns.columns:
        df_temp = df_clean.copy()
        df_temp['main_genre'] = df_columns[col]
        lista_tablas.append(df_temp)

    # Concatenamos todas las tablas
    df_final = pd.concat(lista_tablas)

    # Traducimos los números de géneros a nombres
    genre_dict_texto = {str(k): v for k, v in genre_dict.items()}

    df_final['main_genre'] = df_final['main_genre'].map(genre_dict_texto)

    # Borramos filas sin género
    df_final = df_final.dropna(subset=['main_genre'])

    # Añadimos décadas
    df_final['decade'] = (df_final['year'] // 10) * 10

    return df_final.reset_index(drop=True)

    
# Funciones para limpiar los datos históricos
def clean_wars_data(df_wars, min_year=1930, max_year=2024):
    df = df_wars.copy()

    # Extraemos 1 año (4 dígitos)
    df["start_year"] = (df["started_year"].astype(str).str.extract(r"(\d{4})").astype("Int64"))
    df["end_year"] = (df["ended_year"].astype(str).str.extract(r"(\d{4})").astype("Int64"))

    # Manejo de de "Ongoing" y sin fecha de finalización
    df["end_year"] = df["end_year"].fillna(max_year).astype("Int64")

    # Limpieza y nulos
    df["conflict_name"] = df["conflict_name"].astype(str).str.strip()
    df = df.dropna(subset=["start_year"])
    df = df[df["conflict_name"].str.len() > 0]

    # Filtramos por rango de años
    df = df[(df["start_year"] >= min_year) & (df["start_year"] <= max_year)]

    # Agrupamos por década
    df["decade"] = (df["start_year"] // 10) * 10

    return df.reset_index(drop=True)