import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# ---------------------------------------------------------
# 1. Servidor HTTP local para simular respuestas sin internet
# ---------------------------------------------------------
class ServidorSimuladoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Manejar simulaciones de retardo para forzar un Timeout
        if "/delay" in self.path:
            time.sleep(3)
            self.send_response(200)
            self.end_headers()
            return

        # Extraer el código de estado deseado desde la URL (ej. /status/404 -> 404)
        try:
            codigo = int(self.path.split("/")[-1])
        except ValueError:
            codigo = 200

        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Retry-After", "5")
        self.end_headers()
        
        # Enviar respuesta JSON en solicitudes exitosas
        if codigo in (200, 201):
            self.wfile.write(b'{"mensaje": "Operacion simulada con exito"}')

    # Desactivar registros por defecto en consola del servidor local
    def log_message(self, format, *args):
        return


def iniciar_servidor_local():
    servidor = HTTPServer(('127.0.0.1', 8080), ServidorSimuladoHandler)
    servidor.serve_forever()


# ---------------------------------------------------------
# 2. Función principal para el manejo de respuestas HTTP
# ---------------------------------------------------------
def manejar_respuesta(respuesta):
    """
    Evalúa el código de estado HTTP de una respuesta
    y muestra mensajes informativos claros en español.
    """
    codigo = respuesta.status_code

    if codigo in (200, 201):
        print(f"  [Éxito - Código {codigo}] Operación completada satisfactoriamente.")
        try:
            datos = respuesta.json()
            print(f"  Respuesta de la API: {datos}")
        except Exception:
            print("  El servidor respondió correctamente.")

    elif codigo == 400:
        print(f"  [Error {codigo}] Solicitud incorrecta (Bad Request). Verifique la sintaxis o parámetros enviados.")

    elif codigo == 401:
        print(f"  [Error {codigo}] No autorizado (Unauthorized). Se requieren credenciales válidas o API Key.")

    elif codigo == 404:
        print(f"  [Error {codigo}] Recurso no encontrado (Not Found). La URL o identificador solicitado no existe.")

    elif codigo == 429:
        espera = respuesta.headers.get("Retry-After", "5")
        print(f"  [Error {codigo}] Demasiadas peticiones. Esperar {espera} segundos antes de reintentar.")

    elif codigo == 500:
        print(f"  [Error {codigo}] Error interno del servidor (Internal Server Error). Fallo en el servidor remoto.")

    else:
        print(f"  [Código {codigo}] Estado HTTP no contemplado en las reglas principales.")


def ejecutar_prueba(url, timeout=5):
    """
    Realiza la petición HTTP y captura excepciones de red.
    """
    print(f"Consultando: {url}")
    try:
        respuesta = requests.get(url, timeout=timeout)
        manejar_respuesta(respuesta)

    except requests.exceptions.Timeout:
        print("  [Excepción de Red] Tiempo de espera agotado (Timeout). El servidor tardó demasiado en responder.")

    except requests.exceptions.ConnectionError:
        print("  [Excepción de Red] Error de conexión (ConnectionError). No se pudo conectar con el servidor.")

    except requests.exceptions.RequestException as e:
        print(f"  [Excepción de Petición]: {e}")

    print("-" * 65)


# ---------------------------------------------------------
# 3. Flujo de pruebas
# ---------------------------------------------------------
if __name__ == "__main__":
    # Iniciar servidor simulado en segundo plano
    hilo_servidor = threading.Thread(target=iniciar_servidor_local, daemon=True)
    hilo_servidor.start()
    time.sleep(0.5)  # Breve pausa para asegurar el arranque del servidor

    print("=== INICIANDO PRUEBAS DE MANEJO DE ERRORES HTTP ===\n")

    # 1. Pruebas de Códigos de Estado exigidos por la práctica (7 códigos)
    codigos_a_probar = [200, 201, 400, 401, 404, 429, 500]

    for cdg in codigos_a_probar:
        url_prueba = f"http://127.0.0.1:8080/status/{cdg}"
        ejecutar_prueba(url_prueba)

    # 2. Pruebas de Excepciones de Red
    print("=== PRUEBAS DE EXCEPCIONES DE RED ===\n")

    # Forzar un Timeout (petición que tarda 3 segundos con límite de 1 segundo)
    ejecutar_prueba("http://127.0.0.1:8080/delay", timeout=1)

    # Forzar un ConnectionError (puerto local cerrado donde no hay servicio)
    ejecutar_prueba("http://127.0.0.1:9999/test")