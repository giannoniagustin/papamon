from model.Scheduler import Scheduler
from util.Parser import Parser
from datetime import time
from model.Time import Time
import json

class SchedulerMapper:

    def toScheduler( self,dictFile: dict) :
        instance = Scheduler(**dictFile)
        return instance
    
    def toJson( self,instanceObject: Scheduler) :
        # Convert  instance to dictionary and then to JSON
        monday =json.loads('{"monday": "[]"}')
        listMonday:list[Time] = []
        for hour in instanceObject.monday:
            listMonday.append(Time(hour=hour.hour,minute=hour.minute,second=hour.second))

        monday["monday"] = Parser.toJson( listMonday)
        jsonObject =Parser.toJson(instanceObject)
        print('Status to Json --'+jsonObject)
        return jsonObject
