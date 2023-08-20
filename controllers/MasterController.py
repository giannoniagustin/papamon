
from controllers.RaspberryController import RaspberryController
import constants.Paths as Paths
from util import File,Time
import constants.EndPoints as EndPoint
import requests
from datetime import datetime
from mappers.status.StatusMapper import StatusMapper
from model.StatusRaspberies import StatusRaspberies
from model.Status import Status



class MasterController:
    @staticmethod
    def getImages():
        request_id = Time.TimeUtil.timeToString(datetime.now(),Time.TimeUtil.formato)
        # Crear la carpeta con el ID de solicitud actual
        localPathImage =Paths.BUILD_IMAGE_FOLDER.format(request_id)
        File.FileUtil.createFolder(localPathImage)
        listRasperr = RaspberryController.getRaspberries()
        for rB in listRasperr:
            url= EndPoint.url_template.format(rB.ip,rB.port,EndPoint.IMAGE) #EndPoint.buildUrl(rB.ip,EndPoint.IMAGE,rB.port)
            print("Url RB ",url)
            params = {f"data": {request_id}}
            try:
                response = requests.get(url,params=params)
                if response.status_code == 200:
                    imageFile=Paths.BUILD_IMAGE_FILE.format(request_id,request_id,rB.id,".jpg")
                    File.FileUtil.writeImage(imageFile,response.content)
                    print(f"Imagen descargada y almacenada con éxito de RB {rB.name} ")
                else:
                    print(f"Error al descargar la imagen de RB {rB.name}")
            except requests.exceptions.ConnectionError as e:
                    print("Error de conexión:", e)
            except requests.exceptions.RequestException as e:
                    print("Error en la solicitud:", e)
    def getStatus():
        statusMapper= StatusMapper()
        listStatusRaspberies: list=[]
        listRasperr = RaspberryController.getRaspberries()
        for rB in listRasperr:
            status= Status()
            statusRb=StatusRaspberies(raspberry=rB,status=status)
            url= EndPoint.url_template.format(rB.ip,rB.port,EndPoint.STATUS)
            print("Url RB ",url)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    responseJson= response.json()
                    status= statusMapper.toStatus(responseJson["data"])                   
                    print(f"Estado  de RB {rB.name} {status} ")
                else:
                
                    print(f"Error al pedir estado RB {rB.name}")
            except requests.exceptions.ConnectionError as e:
                    print("Error de conexión:", e)
            except requests.exceptions.RequestException as e:
                    print("Error en la solicitud:", e)
            finally:
                    statusRb.status=status
                    statusRb.raspberry=rB
                    listStatusRaspberies.append(statusRb)
        print(listStatusRaspberies)