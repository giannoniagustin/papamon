from controllers.MasterController import MasterController
from controllers.status.StatusController import StatusController
from controllers.scheduler.SchedulerController import SchedulerController

from model.Status import Status
from model.StatusSystem import StatusSystem
from model.StatusSlave import StatusSlave
from model.Raspberry import Raspberry
from util.Parser import Parser
from model.Scheduler import Scheduler
from mappers.scheduler.SchedulerMapper import SchedulerMapper

from datetime import time
from model.Time import Time
import constants.Paths as Paths
from util.Sentry import Sentry
from sentry_sdk import configure_scope
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
import Api

def initApp():
   Sentry.init()
   Sentry.customMessage(Paths.ME_FILE,Paths.ME,"Inicio de App Master")   

def checkStatus(): 
      MasterController.getStatus()
    
def main():
   initApp()
   checkStatus()
   sentry_sdk.capture_message("Fin de App Master") 
   
   '''  # Crear objetos time
    hora1 = time(10, 30, 0)
    hora2 = time(15, 45, 0)
    hora3 = time(20, 15, 0)

    # Crear una lista de objetos time
    lista_horas = [hora1, hora2, hora3]
    scheduler = Scheduler(monday=lista_horas,tuesday=lista_horas,wednesday=lista_horas,thursday=lista_horas,friday=lista_horas,saturday=lista_horas,sunday=lista_horas)
    SchedulerMapper().toJson(scheduler)
    schedulerController = SchedulerController()
    #schedulerController.update(scheduler)
    #print(schedulerController.get())'''
    
 #MasterController.getStatus()
 # MasterController.getImages()
 #StatusController.update(Status(True,'2023-12-2525'))

if __name__ == "__main__":
    main()
    #Api.app.run(host='0.0.0.0', port=5000)

