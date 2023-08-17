
from mappers.raspberry.RaspberryMapper import RaspberryMapper
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
    @staticmethod
    def getMe()-> Raspberry:
            meFile={}
            try:
                path=Paths.ME
                print('Path Me: '+path)
                meFile =File.FileUtil.readFile(path) 
                meMapper = RaspberryMapper()
                instance = meMapper.toRaspberry(dictFile=meFile) 
                return instance
            except FileNotFoundError as e:
                print("An error occurred when get Raspberry: "+e.strerror)
                raise
            except IOError as e:
                print("An error occurred when get Raspberry: "+e.strerror)
                raise
            except Exception as e:
                print("An error occurred when get Raspberry: ",e)
                raise