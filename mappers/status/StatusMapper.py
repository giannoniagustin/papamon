from dataclasses import make_dataclass,asdict
from model.Status import Status
import json

class StatusMapper:

    def toStatus( self,dictFile: dict) :
        instance = Status(**dictFile)
        return instance
    
    def toJson( self,dictFile: Status) :
        # Convert Persona instance to dictionary and then to JSON
        status_dict = asdict(dictFile)
        status_json = json.dumps(status_dict, indent=4)
        print('Status to Json --'+status_json)
        return status_json
