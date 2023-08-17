
from mappers.status.StatusMapper import StatusMapper
import constants.Paths as Paths
from model.Status import Status
from util import File
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
      
                      