from datetime import datetime

class TimeUtil:
    formato = "%Y_%m_%d_%H_%M_%S"

    @staticmethod
    def timeToString(time:datetime,format:str)-> str:
          return time.strftime(format)