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
from config.master.config import meRaspb  # Importa meRaspb desde config.py

def initApp():
   Sentry.init()
   Sentry.customMessage(Paths.ME_FILE,Paths.ME,f"Inicio de App Master {datetime.datetime.now()}")   

def checkStatus(): 
      MasterController.getStatus()
      

    
def main():
   initApp()
   checkStatus()
   sentry_sdk.capture_message(f"Fin de App Master {datetime.datetime.now()}") 
def scheduler():
        # Crear objetos time
    hora1 = Time(10, 30, 00)
    hora2 = Time(15, 45, 00)
    hora3 = Time(23, 15, 00)
    # Crear una lista de objetos time
    lista_horas = [hora1, hora2, hora3]
    scheduler = Scheduler(monday=lista_horas,tuesday=lista_horas,wednesday=lista_horas,thursday=lista_horas,friday=lista_horas,saturday=lista_horas,sunday=lista_horas)
    SchedulerMapper().toJson(scheduler)
    schedulerController = SchedulerController()
    schedulerController.update(scheduler)
    
    #print(schedulerController.get())
def job():
    print(f"I'm working... {datetime.datetime.now()}")

      
def processCheckStatus():
     Sentry.init()
     Sentry.customMessage(filename=None,path=None,eventName="Inicio de Sentry en proceso ")  
     SchedulerController.build(job=checkStatus)
     while True:
      schedule.run_pending()
      time1.sleep(1)
def checkCallTakeImage():
    ApiController.callTakeImage("")
          
if __name__ == "__main__":
    
    initApp()
    MasterController.getImages()    
    #Api.app.run(host='0.0.0.0', port=meRaspb.port)
    
    

