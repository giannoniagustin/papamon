from dataclasses import dataclass
@dataclass
class Status:
    cameraRunning :bool =False
    lastImage : str = "Not setted"
    

    