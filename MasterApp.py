import os
from controllers.MasterController import MasterController
from controllers.status.StatusController import StatusController
from controllers.scheduler.SchedulerController import SchedulerController
from controllers.ApiController import ApiController



from model.Scheduler import Scheduler
from mappers.scheduler.SchedulerMapper import SchedulerMapper

import datetime
import time as time1
from model.Time import Time
import constants.Paths as Paths
from util.Sentry import Sentry
from sentry_sdk import configure_scope
import sentry_sdk
import Api
import schedule
from config.master.config import version, meRaspb  # Importa meRaspb desde config.py

def initApp():
   Sentry.init()
   Sentry.customMessage(Paths.ME_FILE,Paths.ME,f"Inicio de App Master {datetime.datetime.now()}")   

    
def main():
   initApp()
   sentry_sdk.capture_message(f"Fin de App Master {datetime.datetime.now()}") 
   
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
          
if __name__ == "__main__":
    
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de App Master {datetime.datetime.now()} Version {version} "+os.linesep)
    print(f"Raspberry {meRaspb} "+os.linesep)
    print("#################################################################")
    
    initApp()
    processGetImages()
    #callReconstruct()
    
    #Api.app.run(host='0.0.0.0', port=meRaspb.port)
    
    

