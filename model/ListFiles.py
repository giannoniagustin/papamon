from dataclasses import dataclass,field
from typing import List

@dataclass
class ListFiles:
    files :List[str] = field(default_factory=list)
    folders :List[str] = field(default_factory=list)


   


    