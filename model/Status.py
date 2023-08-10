from dataclasses import dataclass,asdict
@dataclass
class Status:
    cameraRunning :bool 
    lastImage : str
    

    