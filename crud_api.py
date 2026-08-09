import requests

# URL base de la API de prueba (JSONPlaceholder)
BASE_URL = "https://jsonplaceholder.typicode.com/posts"
TIMEOUT_SECONDS = 5

def ejecutar_crud():
    # ---------------------------------------------------------
    # 1. Operación GET: Obtener posts y mostrar los primeros 2
    # ---------------------------------------------------------
    print("=== 1. OPERACIÓN GET ===")
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()  # Genera excepción si el status no es 2xx
        
        posts = response.json()
        print(f"Código de estado: {response.status_code}")
        print("Primeros 2 posts obtenidos:")
        for post in posts[:2]:
            print(f"  [ID: {post['id']}] Título: {post['title']}")
            
    except requests.exceptions.Timeout:
        print("Error en GET: Tiempo de espera agotado (Timeout).")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión/petición en GET: {e}")

    print("\n" + "-"*40 + "\n")

    # ---------------------------------------------------------
    # 2. Operación POST: Crear un nuevo post
    # ---------------------------------------------------------
    print("=== 2. OPERACIÓN POST ===")
    nuevo_post = {
        "title": "Automatización de Infraestructura",
        "body": "Práctica de peticiones HTTP con Python requests.",
        "userId": 1
    }
    try:
        response = requests.post(BASE_URL, json=nuevo_post, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        
        data = response.json()
        print(f"Código de estado: {response.status_code}")
        print(f"Éxito: Post creado con el ID generado -> {data.get('id')}")
        print(f"Respuesta de la API: {data}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error en POST: {e}")

    print("\n" + "-"*40 + "\n")

    # ---------------------------------------------------------
    # 3. Operación PUT: Actualizar el post con ID 1
    # ---------------------------------------------------------
    print("=== 3. OPERACIÓN PUT ===")
    post_actualizado = {
        "id": 1,
        "title": "Título actualizado mediante script Python",
        "body": "Contenido modificado correctamente.",
        "userId": 1
    }
    try:
        url_put = f"{BASE_URL}/1"
        response = requests.put(url_put, json=post_actualizado, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        
        data = response.json()
        print(f"Código de estado: {response.status_code}")
        print("Éxito: El post ID 1 ha sido actualizado correctamente.")
        print(f"Respuesta de la API: {data}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error en PUT: {e}")

    print("\n" + "-"*40 + "\n")

    # ---------------------------------------------------------
    # 4. Operación DELETE: Eliminar el post con ID 1
    # ---------------------------------------------------------
    print("=== 4. OPERACIÓN DELETE ===")
    try:
        url_delete = f"{BASE_URL}/1"
        response = requests.delete(url_delete, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        
        print(f"Código de estado: {response.status_code}")
        print("Éxito: El post ID 1 ha sido eliminado satisfactoriamente.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error en DELETE: {e}")

if __name__ == "__main__":
    ejecutar_crud()