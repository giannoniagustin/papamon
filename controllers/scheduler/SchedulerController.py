
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

    @staticmethod
    def build(job): 
        scheduler: Scheduler =  SchedulerController.get()
        #Monday
        for hour in scheduler.monday:
            print(f"{hour.hour}:{hour.minute}")
            schedule.every().monday.at(f"{hour.hour}:{hour.minute}").do(job)
        #tuesday
        for hour in scheduler.tuesday:
            schedule.every().tuesday.at(f"{hour.hour}:{hour.minute}").do(job)
        #wednesday
        for hour in scheduler.wednesday:
            schedule.every().wednesday.at(f"{hour.hour}:{hour.minute}").do(job)
        #thursday
        for hour in scheduler.thursday:
            schedule.every().thursday.at(f"{hour.hour}:{hour.minute}").do(job)
        #friday
        for hour in scheduler.friday:
            schedule.every().friday.at(f"{hour.hour}:{hour.minute}").do(job)
        #saturday
        for hour in scheduler.saturday:
            schedule.every().saturday.at(f"{hour.hour}:{hour.minute}").do(job)
        #sunday
        for hour in scheduler.sunday:
            schedule.every().sunday.at(f"{hour.hour}:{hour.minute}").do(job)
            


               
                      