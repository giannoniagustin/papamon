#!/usr/bin/env python3
'''Acordarse de ejecutar la app desde el path del file app.py , primero hacer CD path y lugo ejecutar python3 ....Otra opcion
 es cambiar el directorio de trabajo desde el script


 Cambiar el directorio de trabajo al directorio donde se encuentra el archivo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Construir la ruta relativa desde el directorio actual
ruta_archivo = os.path.join('data', 'rb', 'status.json')'''

from controllers.ApiController import ApiController
from config.slave.config import meRaspb
from config.slave.config import programsaveCam
from config.slave.config import reconstructFolder
from config.slave.config import isDemo

def checkCallTakeImage():
    ApiController.callTakeImage("20-18-1825",meRaspb.id ,isDemo,programsaveCam,reconstructFolder)

if __name__ == '__main__':
    checkCallTakeImage()
    