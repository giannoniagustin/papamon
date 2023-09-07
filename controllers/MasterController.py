
from controllers.raspberry.RaspberryController import RaspberryController
import constants.Paths as Paths
from util import File,TimeUtil
import constants.EndPoints as EndPoint
import requests
from datetime import datetime
from mappers.status.StatusMapper import StatusMapper
from mappers.statusRaspberies.StatusRaspberiesMapper import StatusRaspberiesMapper
from controllers.statusRaspberies.StatusRaspberiesController import StatusRaspberiesController
from controllers.image.ImageController import ImageController


from model.StatusSlave import StatusSlave
from model.Status import Status
from model.StatusSystem import StatusSystem
from util.Sentry import Sentry



class MasterController:
    @staticmethod
    def getImages():
        request_id = TimeUtil.TimeUtil.timeToString(datetime.now(),TimeUtil.TimeUtil.formato)
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
                    ImageController.save(imageFile,response.content)
                    print(f"Imagen descargada y almacenada con éxito de RB {rB.name} ")
                else:
                    print(f"Error al descargar la imagen de RB {rB.name}")
            except requests.exceptions.ConnectionError as e:
                    print("Error de conexión:", e)
            except requests.exceptions.RequestException as e:
                    print("Error en la solicitud:", e)
    def getStatus()->list[StatusSlave]:
        statusMapper= StatusMapper()
        listStatusRaspberies: list=[]
        listRasperr = RaspberryController.getRaspberries()
        for rB in listRasperr:
            status= Status()
            message ="Error de Conexion"
            state = False
            statusRb=StatusSlave(raspberry=rB,status=status)
            url= EndPoint.url_template.format(rB.ip,rB.port,EndPoint.STATUS)
            print("Url RB ",url)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    responseJson= response.json()
                    status= statusMapper.toStatus(responseJson["data"])   
                    message= "Se logro conexion"
                    state= True                
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
                    statusRb.state = state
                    statusRb.message=message
                    listStatusRaspberies.append(statusRb)
        StatusRaspberiesController().update(listStatusRaspberies)
        Sentry.customMessage(Paths.STATUS_RASPBERIES_FILE,Paths.STATUS_RASPBERIES,"Estado del sistema")      

        
        # Buscar si todas estan Ok
        has_error = all(statusSlave.state for statusSlave in listStatusRaspberies)
        systemStatus =  StatusSystem(slaves=listRasperr,slaveStatus=listStatusRaspberies,status=has_error,message="Error")
        print(f"System status {systemStatus}")
        return listStatusRaspberies
