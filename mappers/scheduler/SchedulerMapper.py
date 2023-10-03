from model.Scheduler import Scheduler
from util.Parser import Parser
from datetime import time
from model.Time import Time
import json

class SchedulerMapper:
    
    def toScheduler( self,dictFile: dict) :
        scheduler = Scheduler()
        for day in scheduler.__annotations__.keys():
            if day in dictFile:
                scheduler.__setattr__(day, [Time(**time_data) for time_data in dictFile[day]])
        return scheduler    
    def toJson( self,instanceObject: Scheduler) :
        jsonObject =json.dumps(instanceObject, default=lambda o: o.__dict__, indent=4)
        return  jsonObject

