
from mappers.scheduler.SchedulerMapper import SchedulerMapper
import constants.Paths as Paths
from model.Scheduler import Scheduler
from util import File

class SchedulerController:
    @staticmethod
    def update(newStatus:Scheduler):
        try:
            mapper = SchedulerMapper()
            content = mapper.toJson(newStatus)
            File.FileUtil.writeFile(Paths.SCHEDULER,content=content)
        except FileNotFoundError as e:
                print("An error occurred when Scheduler updating:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when Scheduler updating:", e)
                raise
        else:
                print("Update Scheduler successfully. ")
    @staticmethod
    def get():
            myFile={}
            try:
                myFile =File.FileUtil.readFile(Paths.SCHEDULER) 
                statusMapper = SchedulerMapper()
                scheduler_instance = statusMapper.toScheduler(dictFile=myFile) 
                return scheduler_instance
            except FileNotFoundError as e:
                print("An error occurred when get Scheduler: "+e.strerror)
                raise
            except IOError as e:
                print("An error occurred when get Scheduler: "+e.strerror)
                raise
            except Exception as e:
                print("An error occurred when get Scheduler: ",e)
                raise

           
                      