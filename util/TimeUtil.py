from datetime import datetime

class TimeUtil:
    formato = "%Y_%m_%d_%H_%M_%S"
    format_DD_MM_YYYY = "%d-%m-%Y"
    format_DD_MM_YYYY_HH_MM = "%d-%m-%Y-%H-%M"


    @staticmethod
    def timeToString(time:datetime,format:str)-> str:
          return time.strftime(format)