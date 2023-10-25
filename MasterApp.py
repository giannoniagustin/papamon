import os
import sys
from controllers.MasterController import MasterController
from controllers.scheduler.SchedulerController import SchedulerController

import datetime
import time as time1
import constants.Paths as Paths
from util.Sentry import Sentry
import schedule
import config.master.config as config
def initApp():
    configParameter()
    Sentry.init()
    Sentry.customMessage(Paths.ME_FILE,Paths.ME,f"Inicio de App Master {datetime.datetime.now()}")   

def callReconstruct():
    if (MasterController.getImages()):
        print(f"Reconstruccion exitosa: {datetime.datetime.now()}")    
    else:
        print(f"Reconstruccion fallida,puede haber generado alguna imagen: {datetime.datetime.now()}")   
def getImages(): 
      MasterController.getImages()
def processGetImages():
     Sentry.init()
     Sentry.customMessage(filename=None,path=None,eventName="Inicio de Sentry ProcessGetImages ")  
     SchedulerController.build(job=getImages,pathScheduler=Paths.SCHEDULER_GET_IMAGES)
     while True:
      schedule.run_pending()
      time1.sleep(1) 
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
          
if __name__ == "__main__":
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de App Master {datetime.datetime.now()}{os.linesep} Version {config.version} "+os.linesep)
    print(f"Raspberry {config.meRaspb} "+os.linesep)
    print("#################################################################")

    initApp()
    #processGetImages()
    callReconstruct()
    #Api.app.run(host='0.0.0.0', port=meRaspb.port)
    
    

