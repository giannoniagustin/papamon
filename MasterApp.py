import os
import platform
import sys
from controllers.MasterController import MasterController
from controllers.scheduler.SchedulerController import SchedulerController

import datetime
import time as time1
import constants.Paths as Paths
from util.Sentry import Sentry
import schedule
import config.master.config as config
TIME_SLEEP= 10
def initApp():
    
    Sentry.init()
    Sentry.customMessage(Paths.ME_MASTER_FILE,Paths.ME_MASTER,f"Inicio de App Master {datetime.datetime.now()}")   
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de App Master {datetime.datetime.now()}{os.linesep} Version {config.version} "+os.linesep)
    print(f"Raspberry {config.meRaspb} "+os.linesep)
    configParameter()
    checkConfig()


def checkConfig():
    print(os.linesep+"###########################CHECK CONFIGURATION######################################"+os.linesep)

    if (MasterController.checkConfig()):
        print("Configuracion correcta")
    else:
        print("Configuracion incorrecta,chequee las ips,id,puertos y nombres de las Raspberries,deben coincidir.")

    
def callReconstruct():
    Sentry.customMessage(filename=None,path=None,eventName=f"Obteniendo Imagenes {datetime.datetime.now()} ")  
    if (MasterController.getImages()):
        print(f"Reconstruccion exitosa: {datetime.datetime.now()}")    
    else:
        print(f"Reconstruccion fallida,puede haber generado alguna imagen: {datetime.datetime.now()}")   

def processGetImages(job):
     job()
     while True:
      schedule.run_pending()
      time1.sleep(TIME_SLEEP) 

def everyOur():
    SchedulerController.buildEverOur(job=callReconstruct)

def everyMinute():
    SchedulerController.buildEveryMinute(job=callReconstruct)
def everySecond():
    SchedulerController.buildEverySecond(job=callReconstruct)
def byScheduler():
    SchedulerController.build(job=callReconstruct,pathScheduler=Paths.SCHEDULER_GET_IMAGES)

    

def configParameter():
    print(os.linesep+"#########################CONFIGURATIONS########################################"+os.linesep)

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
    print(f"Program to execute {config.programsaveCam} ")
    
    if ("-force" in sys.argv):
        print("Se esta forzando reconstruccion")
        config.forceReconstruc=True
          
if __name__ == "__main__":

    initApp()
    if (config.forceReconstruc):
        callReconstruct()
        processGetImages(everySecond)
    else:
        processGetImages(byScheduler)
    
    

