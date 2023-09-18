from model.Raspberry import Raspberry
from typing import List

class RaspberryMapper:

    def toRaspberies( self,dictFile: dict)-> List[Raspberry] :
        return [self.toRaspberry(raspberry_data) for raspberry_data in dictFile]
    
    def toRaspberry( self,dictFile: dict)->Raspberry :
        return Raspberry(**dictFile)
     