import pandas as pd
import googlemaps
import logging
gmaps = googlemaps.Client(key='asd')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

input_csv = "vehiculos.csv"
output_csv = "vehiculos_actualizado.csv"

logging.info("Iniciando el proceso...")

try:
    logging.info("Intentando leer el archivo CSV con codificación UTF-8...")
    df = pd.read_csv(input_csv, encoding='utf-8')
    logging.info("Archivo leído correctamente con UTF-8.")
except UnicodeDecodeError:
    logging.warning("Error al leer con UTF-8, intentando con latin-1...")
    df = pd.read_csv(input_csv, encoding='latin-1')
    logging.info("Archivo leído correctamente con latin-1.")

logging.info("Contenido inicial del archivo CSV:")
logging.info(df.head())

def esta_en_bogota(lat, lng, fila_actual, total_filas):
    try:
        logging.info(f"Procesando fila {fila_actual} de {total_filas}: Coordenadas ({lat}, {lng})...")
        reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
        dentro_bogota = any("Bogotá" in result.get("formatted_address", "") for result in reverse_geocode_result)
        resultado = "Si" if dentro_bogota else "No"
        logging.info(f"Resultado para fila {fila_actual}: {'Si' if dentro_bogota else 'No'}")
        return resultado
    except Exception as e:
        logging.error(f"Error al consultar Google Maps API para fila {fila_actual}: {e}")
        return "Error"

logging.info("Procesando cada fila para determinar si está en Bogotá...")
total_filas = len(df)
df["estaenbogota?"] = [
    esta_en_bogota(row["lat"], row["lng"], idx + 1, total_filas)
    for idx, row in df.iterrows()
]

logging.info("Contenido del archivo después de procesar:")
logging.info(df.head())

df.to_csv(output_csv, index=False)
logging.info(f"Archivo actualizado guardado como {output_csv}")
