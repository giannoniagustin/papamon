from dataclasses import asdict
from model.Status import Status
import json

class StatusMapper:

    def toStatus( self,dictFile: dict) :
        instance = Status(**dictFile)
        return instance
    
    def toJson( self,dictFile: Status) :
        # Convert Persona instance to dictionary and then to JSON
        dict = asdict(dictFile)
        jsonObject = json.dumps(dict, indent=4)
        print('Status to Json --'+jsonObject)
        return jsonObject
