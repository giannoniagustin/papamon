from dataclasses import dataclass,asdict
@dataclass
class Status:
    cameraRunning :bool =False
    lastImage : str = "Not setted"
    

    