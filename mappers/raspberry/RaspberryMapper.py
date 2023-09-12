from model.Raspberry import Raspberry

class RaspberryMapper:

    def toRaspberies( self,dictFile: dict)-> list[Raspberry] :
        return [self.toRaspberry(raspberry_data) for raspberry_data in dictFile]
    
    def toRaspberry( self,dictFile: dict)->Raspberry :
        return Raspberry(**dictFile)
     