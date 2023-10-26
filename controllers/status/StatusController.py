
from mappers.status.StatusMapper import StatusMapper
import constants.Paths as Paths
from model.Status import Status
from util import File
import random
class StatusController:
    @staticmethod
    def update(newStatus:Status):
        try:
            mapper = StatusMapper()
            content = mapper.toJson(newStatus)
            File.FileUtil.writeFile(Paths.STATUS_RB,content=content)
            print("Update status successfully. ")
        except FileNotFoundError as e:
                print("An error occurred when status updating:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when status updating:", e)
                raise
    @staticmethod
    def updateIfChange(newStatus:Status):
        try:
            lastUpdate = StatusController.get()
            if (newStatus.cameraRunning is not None):
                lastUpdate.cameraRunning = newStatus.cameraRunning
            if (newStatus.lastImage is not None):
                lastUpdate.lastImage = newStatus.lastImage 
            StatusController.update(lastUpdate)        
            print(f"Status  --'{lastUpdate}")
        except FileNotFoundError as e:
                print("An error occurred when status updating:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when status updating:", e)
                raise
    @staticmethod
    def get()-> Status:
            statusFile={}
            try:
                statusMapper = StatusMapper()
                #chequeo si el archivo existe o es vacio y se crea
                fileExample = statusMapper.toJson(File.FileUtil.readFile(Paths.STATUS_RB_EXAMPLE))
                File.FileUtil.createIsFileEmptyOrNotExist(Paths.STATUS_RB,fileExample) 
                statusFile =File.FileUtil.readFile(Paths.STATUS_RB) 
                status_instance = statusMapper.toStatus(dictFile=statusFile) 
                return status_instance
            except FileNotFoundError as e:
                print("An error occurred when get Status: "+e.strerror)
                raise
            except IOError as e:
                print("An error occurred when get Status: "+e.strerror)
                raise
            except Exception as e:
                print("An error occurred when get Status: ",e)
                raise

    @staticmethod
    def isCameraRunning()-> bool:
            try:
                isCameraRunning:bool =random.choice([True, False]) # Ver como controlar si la camara esta encendida
                print("isCameraRunning: ",isCameraRunning)
                return isCameraRunning 
            except Exception as e:
                print("An error occurred when get isCameraRunning: ",e)
                raise
            
           
                      