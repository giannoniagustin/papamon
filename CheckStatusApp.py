#!/usr/bin/env python3
'''Agregar al servicio para que se ejcute cada vez que se inicia el servidor'''

from util.Sentry import Sentry
from controllers.MasterController import MasterController
from controllers.scheduler.SchedulerController import SchedulerController
import time as time
import schedule
import constants.Paths as Paths


def checkStatus(): 
      MasterController.getStatus()
def processCheckStatus():
     Sentry.init()
     Sentry.customMessage(filename=None,path=None,eventName="Inicio de Sentry ProcessCheckStatus ")  
     #SchedulerController.build(job=checkStatus,pathScheduler=Paths.SCHEDULER_STATUS)
     SchedulerController.buildEveryMinute(checkStatus)

     while True:
      schedule.run_pending()
      time.sleep(1)

if __name__ == '__main__':
    Sentry.init()
    #MasterController.getStatus()
    processCheckStatus()
