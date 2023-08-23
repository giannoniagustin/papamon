from dataclasses import dataclass,field
@dataclass
class Status:
    cameraRunning :bool =field(default=None)
    lastImage : str = field(default=None) 
    

    