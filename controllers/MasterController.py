
from controllers.RaspberryController import RaspberryController
import constants.Paths as Paths
from util import File,Time
import constants.EndPoints as EndPoint
import requests
from datetime import datetime


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