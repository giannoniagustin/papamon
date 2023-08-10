import json
from dataclasses import asdict
from model.Status import Status

class Parser:
    
#Status
    def statusFromJson(self,json_str: str):
        statusJson = json.loads(json_str)
        status = Status(**statusJson) 
        print('Json to Status   --'+status.lastImage)
        return status    