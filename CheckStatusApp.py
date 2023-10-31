#!/usr/bin/env python3
'''Agregar al servicio para que se ejcute cada vez que se inicia el servidor'''

import os
import platform
import sys
from util.Sentry import Sentry
from controllers.MasterController import MasterController
from controllers.scheduler.SchedulerController import SchedulerController
import time as time
import schedule
import constants.Paths as Paths
import datetime
import config.master.config as config

def initApp():
    
    Sentry.init()
    Sentry.customMessage(filename=None,eventName=f"Inicio de App CheckStatus {datetime.datetime.now()}") 
    configParameter()
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de App Check Status {datetime.datetime.now()}{os.linesep} Version {config.version} "+os.linesep)
    print(f"Raspberry {config.meRaspb} "+os.linesep)
    print("#################################################################")
    
def configParameter():
    # Imprime los parámetros
    print("Parámetros recibidos:", sys.argv)
    sistema_operativo = platform.system()
    print(f"Estás ejecutando en {sistema_operativo}.")
    if ("-force" in sys.argv):
        print("Se esta forzando el chequeo de estado")
        config.forceCheckStatus=True

def checkStatus(): 
      MasterController.getStatus()
def processCheckStatus():
     Sentry.customMessage(filename=None,path=None,eventName="Inicio de Sentry ProcessCheckStatus ")  
     SchedulerController.build(job=checkStatus,pathScheduler=Paths.SCHEDULER_STATUS)
     #SchedulerController.buildEveryMinute(checkStatus)
     while True:
      schedule.run_pending()
      time.sleep(1)

if __name__ == '__main__':
    initApp()
    if (config.forceCheckStatus):
        checkStatus()
        processCheckStatus()
    else:
        processCheckStatus()