from dataclasses import asdict
import dataclasses
import json
from model.CameraStatus import CameraStatus
from model.SystemStatus import SystemStatus
from util.Parser import Parser

class SystemStatusMapper:

    def toStatus( self,dictFile: dict) :
        instance = SystemStatus(**dictFile)
        return instance
    
    def toJson( self,instanceObject: SystemStatus) :
        system_status_json = json.dumps(dataclasses.asdict(instanceObject), indent=4)
        print(system_status_json)
        return system_status_json

