#!/usr/bin/env python3
import os
import platform
import sys
import Api
from util.Sentry import Sentry
from config.slave.config import meRaspb,version
import datetime
import config.slave.config as config

def configParameter():
    # Imprime los parámetros
    print("Parámetros recibidos:", sys.argv)
    # Verifica si "-demo" está en la lista de argumentos
    if "-demo" in sys.argv:
        print("El parámetro '-demo' está presente.")
        config.isDemo=True
    else:
        print("El parámetro '-demo' no está presente.")
        config.isDemo=False
        
    sistema_operativo = platform.system()
    print(f"Estás ejecutando en {sistema_operativo}.")
    if (sistema_operativo == "Windows"):
        config.programsaveCam = config.programsaveCam_Win
    else:
        config.programsaveCam = config.programsaveCam_Linux
def initApp():
    configParameter()


if __name__ == '__main__':
    initApp()
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de App Slave {datetime.datetime.now()} Version {version} "+os.linesep)
    print(f"Raspberry {meRaspb} "+os.linesep)
    print("#################################################################")
    Sentry.init()
    Api.app.run(host='0.0.0.0', port=meRaspb.port)
