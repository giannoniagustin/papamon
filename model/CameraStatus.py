from dataclasses import dataclass,field
@dataclass
class CameraStatus:
    cameraRunning :bool =field(default=None)
    lastImage : str = field(default=None) 
    

    