import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API Key de forma segura desde las variables de entorno
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def consultar_clima():
    if not API_KEY or API_KEY == "tu_clave_de_openweather_aqui":
        print("Error: No se ha configurado una API_KEY válida en el archivo .env")
        return

    ciudad = input("Ingrese el nombre de la ciudad: ").strip()
    
    if not ciudad:
        print("Error: Debe ingresar el nombre de una ciudad.")
        return

    # Parámetros exigidos por la API de OpenWeatherMap
    params = {
        "q": ciudad,
        "appid": API_KEY,
        "units": "metric",  # Para obtener la temperatura en grados Celsius
        "lang": "es"        # Para obtener la descripción del clima en español
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        
        # Validación explícita de respuestas HTTP
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            sensacion = data["main"]["feels_like"]
            descripcion = data["weather"][0]["description"]
            nombre_ciudad = data["name"]
            pais = data["sys"]["country"]

            print("\n=== CONSULTA METEOROLÓGICA EXITOSA ===")
            print(f"Ciudad: {nombre_ciudad}, {pais}")
            print(f"Temperatura actual: {temp}°C (Sensación térmica: {sensacion}°C)")
            print(f"Estado del clima: {descripcion.capitalize()}")
            
        elif response.status_code == 401:
            print("\nError (401): API Key inválida o aún no activada por OpenWeatherMap. Verifique su archivo .env.")
        elif response.status_code == 404:
            print(f"\nError (404): La ciudad '{ciudad}' no fue encontrada. Verifique el nombre ingresado.")
        else:
            print(f"\nError ({response.status_code}): Ocurrió un inconveniente al consultar el servicio.")

    except requests.exceptions.Timeout:
        print("\nError: Tiempo de espera agotado al conectar con OpenWeatherMap.")
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}")

if __name__ == "__main__":
    consultar_clima()