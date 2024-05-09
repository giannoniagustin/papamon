
from mappers.statusRaspberies.StatusRaspberiesMapper import StatusRaspberiesMapper
import constants.Paths as Paths
from model.StatusSlave import StatusSlave
from util import File
from typing import List
class StatusRaspberiesController:
    @staticmethod
    def update(newStatus:List[StatusSlave]):
        try:
            mapper = StatusRaspberiesMapper()
            content = mapper.toJson(newStatus)
            #chequeo si el archivo existe o es vacio y se crea
            print("File example read:")
            fileExample = mapper.toJson(File.FileUtil.readFile(Paths.STATUS_RASPBERIES_EXAMPLE))
            File.FileUtil.createIsFileEmptyOrNotExist(Paths.STATUS_RASPBERIES,fileExample) 
            if ( File.FileUtil.writeFile(Paths.STATUS_RASPBERIES,content=content)):
                print("Update status successfully. ")
            else:
                print("Update status error ")
        except FileNotFoundError as e:
                print("An error occurred when StatusRaspberies updating:", e)
                raise
        except IOError as e:
        # Manejar otras excepciones de I/O aquí
                print("An error occurred when StatusRaspberies updating:", e)
                raise

    @staticmethod
    def get()->List[StatusSlave]:
            fileData={}
            try:
                fileData =File.FileUtil.readFile(Paths.STATUS_RASPBERIES) 
                statusMapper = StatusRaspberiesMapper()
                instance = statusMapper.toStatusRaspberiesList(dictFile=fileData) 
                return instance
            except FileNotFoundError as e:
                print("An error occurred when get Status: "+e.strerror)
                raise
            except IOError as e:
                print("An error occurred when get Status: "+e.strerror)
                raise
            except Exception as e:
                print("An error occurred when get Status: ",e)
                raise
                      