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
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

def main():
   sentry_sdk.init(
    dsn="https://907fed6f0f57920999ad05c29b8f74fa@o4505815265902592.ingest.sentry.io/4505815269113856",
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    debug=False,  # Habilita el modo de depuración (opcional)
    ) 
   sentry_sdk.capture_message("Inicio de App")
   #division_by_zero = 1 / 0

   
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
   # Api.app.run(host='0.0.0.0', port=5000)

