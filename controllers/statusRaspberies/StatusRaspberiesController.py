
from mappers.statusRaspberies.StatusRaspberiesMapper import StatusRaspberiesMapper
import constants.Paths as Paths
from model.StatusRaspberies import StatusRaspberies
from util import File
class StatusRaspberiesController:
    @staticmethod
    def update(newStatus:list[StatusRaspberies]):
        try:
            mapper = StatusRaspberiesMapper()
            content = mapper.toJsonList(newStatus)
            File.FileUtil.writeFile(Paths.STATUS_RASPBERIES,content=content)
        except FileNotFoundError as e:
                print("An error occurred when StatusRaspberies updating:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when StatusRaspberies updating:", e)
                raise
        else:
                print("Update status successfully. ")
    @staticmethod
    def get()->list[StatusRaspberies]:
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
                      