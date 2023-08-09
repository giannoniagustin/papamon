import json
from dataclasses import dataclass,asdict
@dataclass
class Status():
    cameraRunning :bool 
    lastImage : str

    def toJson(self):
        # Convert Persona instance to dictionary and then to JSON
        status_dict = asdict(self)
        status_json = json.dumps(status_dict, indent=4)
        print('Status to Json --'+status_json)
        return status_json
