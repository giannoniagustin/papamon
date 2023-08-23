
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
        except FileNotFoundError as e:
                print("An error occurred when status updating:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when status updating:", e)
                raise
        else:
                print("Update status successfully. ")
    @staticmethod
    def get():
            statusFile={}
            try:
                statusFile =File.FileUtil.readFile(Paths.STATUS_RB) 
                statusMapper = StatusMapper()
                status_instance = statusMapper.toStatus(dictFile=statusFile) 
                isCameraRunning=   StatusController.isCameraRunning()
                status_instance.cameraRunning=isCameraRunning
                StatusController.update(status_instance)
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
           
                      