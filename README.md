Análisis de la Industria del Cine Bélico: ¿Reflejo o Reacción a los Conflictos Globales?

## Objetivo del proyecto
Analizar la correlación histórica entre la intensidad de los conflictos armados globales y la producción cinematográfica del género bélico para identificar patrones en la industria cultural ante crisis internacionales.

## Datasets
-Cine: Datos extraídos mediante la API de TMDB (The Movie Database). Se consultó el catálogo histórico filtrando por el identificador de géneros para filtrar luego por "War".

- Conflictos: Datos extraídos de Wikipedia (vía web scraping) sobre conflictos armados mundiales, procesados para cuantificar la duración y simultaneidad.

Variables principales: 
- decade: Periodo de 10 años.
- num_war_movies: Conteo de títulos únicos identificados bajo el género "War".
- intensity: Suma de años de duración de todos los conflictos de la década.
- intensity_prev_decade: Métrica de intensidad de la década anterior.

# Calidad del dato
- Procesamiento de géneros: Los datos originales de la API contenían códigos numéricos para los géneros. Se implementó un mapeo mediante un diccionario de géneros para transformar estos códigos en etiquetas legibles y asegurar que solo las películas estrictamente categorizadas como "War" formaran parte del análisis.

- Consistencia: Se limpiaron registros con fechas incompletas para garantizar la precisión de las agrupaciones por décadas.

# Preguntas clave
1. ¿Existe relación directa entre el número de guerras activas y las películas producidas en el mismo periodo?

2. ¿Es más fuerte el efecto en la década siguiente que la reacción inmediata?

# Proceso de análisis
1. Extracción de datos.
2. Limpieza y transformación: Normalización de géneros y cálculo de la métrica "Años-Guerra".
3. Análisis: Identificación de valores atípicos o que sobresalgan.
4. Creación de variables (retraso temporal) para testear la Hipótesis 2.
5. Visualización.

# Resultados / Insights
- No se observa una correlación directa entre la intensidad de los conflictos armados en una década y la cantidad de películas bélicas producidas en ese mismo periodo. A pesar del aumento sostenido del volumen de conflictos a lo largo del tiempo, la producción cinematográfica del género no sigue un patrón proporcional inmediato.

- El mayor pico de producción de cine bélico se concentra en los años posteriores a grandes conflictos históricos, especialmente tras la Segunda Guerra Mundial, lo que sugiere que el cine tiende a reaccionar con cierta distancia temporal.

- Al incorporar la variable de intensidad de la década anterior, se aprecia una relación más coherente entre conflictos pasados y producción cinematográfica, reforzando la hipótesis de que el cine bélico actúa como una forma de reinterpretación histórica más que como un reflejo inmediato de la realidad contemporánea.

- En décadas recientes, a pesar de una alta intensidad bélica global, la producción de cine bélico disminuye, lo que puede estar relacionado con cambios en los intereses del público, la diversificación de géneros o una transformación en la manera de representar los conflictos en la industria audiovisual.

# Limitaciones
- La categorización de las películas depende de la clasificación por géneros de TMDB, lo que puede excluir títulos con contenido bélico no etiquetados explícitamente como "War".

- La métrica de intensidad bélica se basa en la duración y solapamiento de conflictos, pero no distingue entre tipos de guerra, escalas de violencia o impacto geopolítico.

- El análisis se realiza a nivel de década, lo que suaviza variaciones anuales y puede ocultar respuestas más inmediatas de la industria cinematográfica.

# Próximos pasos 
- Ampliar el análisis incorporando subgéneros (drama bélico, documental, ciencia ficción bélica) para estudiar posibles desplazamientos narrativos.

- Explorar modelos estadísticos que permitan cuantificar la fuerza de la relación entre conflictos y producción cinematográfica.

# Como replicar el proyecto
1. Clonar el repositorio.
2. Configurar las variables de entorno necesarias para el acceso a la API de TMDB. (extraction.py)
3. Ejecutar extraction.py y cleaning.py.
4. Ejecutar main_notebook.ipynb

Este proyecto requiere una clave de acceso a la API de TMDB.
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
TMDB_READ_TOKEN=tu_token o TMDB_API_KEY=tu_api_key
