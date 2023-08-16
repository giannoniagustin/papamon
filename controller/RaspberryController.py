
from mappers.RaspberryMapper import RaspberryMapper
import constants.Paths as Paths
from model.Raspberry import Raspberry
from util import File
class RaspberryController:
    @staticmethod
    def getRaspberries()-> list[Raspberry]:
            #Lista de raspberry a pedir las imagenes
                file={}
                path=Paths.RASPBERRY
                print('Path Raspberry: '+path)
                file =File.FileUtil.readFile(path) 
                mapper = RaspberryMapper()
                instance = mapper.toRaspberies(dictFile=file) 
                return instance