from dataclasses import asdict
from model.Status import Status
from util.Parser import Parser

class StatusMapper:

    def toStatus( self,dictFile: dict) :
        instance = Status(**dictFile)
        return instance
    
    def toJson( self,instanceObject: Status) :
        # Convert  instance to dictionary and then to JSON
        jsonObject =Parser.toJson(instanceObject)
        print('Status to Json --'+jsonObject)
        return jsonObject
