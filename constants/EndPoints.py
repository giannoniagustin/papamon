url_template = "http://{}:{}/{}"

#STATUS
STATUS='status'
#GET
GET='get'
#IMAGE
IMAGE='image'
#RASPBERRY
RASPBERRY='raspberry'

@staticmethod
def buildUrl(ip,endPoint,port:str):
   return url_template.format(ip,port,endPoint)      
   
