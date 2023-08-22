from dataclasses import dataclass
@dataclass
class Status:
    cameraRunning :bool =None
    lastImage : str = None
    

    