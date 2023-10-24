
from mappers.status.StatusMapper import StatusMapper
import constants.Paths as Paths
from mappers.statusSystem.SystemStatusMapper import SystemStatusMapper
from model.CameraStatus import CameraStatus
from model.SystemStatus import SystemStatus
from util import File
import random
class SystemStatusController:
    @staticmethod
    def update(newStatus:SystemStatus):
        try:
            mapper = SystemStatusMapper()
            content = mapper.toJson(newStatus)
            File.FileUtil.writeFile(Paths.SYSTEM_STATUS,content=content)
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
    def updateIfChange(newStatus:CameraStatus):
        try:
            
            lastUpdate = SystemStatusController.get()
            if (newStatus.cameraRunning is not None):
                lastUpdate.cameraRunning = newStatus.cameraRunning
            if (newStatus.lastImage is not None):
                lastUpdate.lastImage = newStatus.lastImage 
            SystemStatusController.update(lastUpdate)
            print("updateIfChange status successfully. ")
        except FileNotFoundError as e:
                print("An error occurred when status updating:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when status updating:", e)
                raise
    @staticmethod
    def get()-> SystemStatus:
            statusFile={}
            try:
                statusMapper = SystemStatusMapper()
                #chequeo si el archivo existe o es vacio y se crea
                fileExample = statusMapper.toJson(File.FileUtil.readFile(Paths.SYSTEM_STATUS_FILE_EXAMPLE))
                File.FileUtil.createIsFileEmptyOrNotExist(Paths.SYSTEM_STATUS,fileExample) 
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

   
            
           
                      