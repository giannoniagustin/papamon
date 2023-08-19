'''Acordarse de ejecutar la app desde el path del file app.py , primero hacer CD path y lugo ejecutar python3 ....Otra opcion
 es cambiar el directorio de trabajo desde el script


 Cambiar el directorio de trabajo al directorio donde se encuentra el archivo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Construir la ruta relativa desde el directorio actual
ruta_archivo = os.path.join('data', 'rb', 'status.json')'''

import Api

if __name__ == '__main__':
    Api.app.run(host='0.0.0.0', port=5000)
