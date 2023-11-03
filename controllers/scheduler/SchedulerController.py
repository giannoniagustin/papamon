
from mappers.scheduler.SchedulerMapper import SchedulerMapper
import constants.Paths as Paths
from model.Scheduler import Scheduler
from util import File
import schedule
from  model.Time import Time


class SchedulerController:
    @staticmethod
    def update(newStatus:Scheduler):
        try:
            mapper = SchedulerMapper()
            content = mapper.toJson(newStatus)
            File.FileUtil.writeFile(Paths.SCHEDULER_STATUS,content=content)
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
    def get(pathScheduler:str):
            myFile={}
            try:
                schedulerMapper = SchedulerMapper()
                #chequeo si el archivo existe o es vacio y se crea
                fileExample = schedulerMapper.toJson(File.FileUtil.readFile(Paths.SCHEDULER_GET_IMAGES_EXAMPLE))
                File.FileUtil.createIsFileEmptyOrNotExist(pathScheduler,fileExample) 
              
                myFile =File.FileUtil.readFile(pathScheduler) 
                scheduler_instance = schedulerMapper.toScheduler(dictFile=myFile) 
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

    @staticmethod
    def build(job,pathScheduler:str): 
        scheduler: Scheduler =  SchedulerController.get(pathScheduler)
        print(f"Job {pathScheduler} is execute on days  : ")
        #Monday
        for hour in scheduler.monday:
            print(f"Monday :{hour.hour}:{hour.minute}")
            schedule.every().monday.at(f"{hour.hour}:{hour.minute}").do(job)
        #tuesday
        for hour in scheduler.tuesday:
            print(f"Tuesday :{hour.hour}:{hour.minute}")
            schedule.every().tuesday.at(f"{hour.hour}:{hour.minute}").do(job)
        #wednesday
        for hour in scheduler.wednesday:
            print(f"Wednesday :{hour.hour}:{hour.minute}")
            schedule.every().wednesday.at(f"{hour.hour}:{hour.minute}").do(job)
        #thursday
        for hour in scheduler.thursday:
            print(f"Thursday :{hour.hour}:{hour.minute}")
            schedule.every().thursday.at(f"{hour.hour}:{hour.minute}").do(job)
        #friday
        for hour in scheduler.friday:
            print(f"Friday :{hour.hour}:{hour.minute}")
            schedule.every().friday.at(f"{hour.hour}:{hour.minute}").do(job)
        #saturday
        for hour in scheduler.saturday:
            print(f"Saturday :{hour.hour}:{hour.minute}")
            schedule.every().saturday.at(f"{hour.hour}:{hour.minute}").do(job)
        #sunday
        for hour in scheduler.sunday:
            print(f"Sunday :{hour.hour}:{hour.minute}")
            schedule.every().sunday.at(f"{hour.hour}:{hour.minute}").do(job)
            
    @staticmethod
    def buildEverOur(job):
     schedule.every(1).hour.do(job)

     
    @staticmethod
    def buildEveryMinute(job):
     schedule.every(1).minute.do(job)

         
    @staticmethod
    def buildEverySecond(job):
     schedule.every(1).second.do(job)

     
            


               
                      