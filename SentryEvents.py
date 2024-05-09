import requests

SENTRY_API_KEY = 'c692657e3a473fde57471a12e48ed5387c433e27acdf3366143ffdd2d38de8bf'
SENTRY_ORG_SLUG = 'papamon-d70418825'
SENTRY_PROJECT_SLUG = 'TU_PROYECTO'

# URL base de la API de Sentry
base_url = f"https://sentry.io/api/0/projects/{SENTRY_ORG_SLUG}/{SENTRY_PROJECT_SLUG}/events/"

# Parámetros de la solicitud (pueden variar según lo que quieras obtener)
params = {
    'query': 'is:unresolved',  # Filtrar por eventos no resueltos
    'limit': 10  # Limitar a 10 eventos, puedes ajustar esto según tus necesidades
}

# Encabezados con la API key de Sentry
headers = {
    'Authorization': f'Bearer {SENTRY_API_KEY}',
    'Content-Type': 'application/json'
}

# Realizar la solicitud GET a la API de Sentry
response = requests.get(base_url, headers=headers, params=params)

# Verificar el código de estado de la respuesta
if response.status_code == 200:
    eventos = response.json()  # Obtener los eventos en formato JSON
    # Haz lo que necesites con los eventos obtenidos
    print("Eventos obtenidos:")
    print(eventos)
else:
    print(f"Error al obtener eventos: {response.status_code} - {response.text}")
