
import os
import subprocess
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

from config.master.config import meRaspb
from config.master.config import programsaveCam
from config.master.config import reconstructFolder
from config.master.config import isDemo


from model.StatusSlave import StatusSlave
from model.Status import Status
from model.StatusSystem import StatusSystem
from util.Sentry import Sentry
from typing import List

class MasterController:
    @staticmethod
    def getImages():
        request_id = TimeUtil.TimeUtil.timeToString(datetime.now(), TimeUtil.TimeUtil.format_DD_MM_YYYY)
        # Crear la carpeta con el ID de solicitud actual
        localPathImage =Paths.BUILD_IMAGE_FOLDER.format(request_id)
        File.FileUtil.createFolder(localPathImage)
        listRasperr = RaspberryController.getRaspberries()
        for rB in listRasperr:
            url= EndPoint.url_template.format(rB.ip,rB.port,EndPoint.IMAGE)
            print("Url RB ",url)
            params = {f"data": {request_id}}
            try:
                response = requests.get(url,params=params)
                if response.status_code == 200:
                    imageFile=Paths.BUILD_IMAGE_FILE.format(request_id,rB.id,request_id,Paths.ZIP)
                    ImageController.save(imageFile,response.content)
                    ImageController.extract(File.FileUtil.filePath(imageFile), response.content)
                    print(f"Imagen descargada y almacenada con éxito de RB {rB.name} ")
                else:
                    print(f"Error al descargar la imagen de RB {rB.name}")
            except requests.exceptions.ConnectionError as e:
                    print("Error de conexión:", e)
            except requests.exceptions.RequestException as e:
                    print("Error en la solicitud:", e) 
        MasterController.callReconstructImage( localPathImage,isDemo,programsaveCam,reconstructFolder)           
                    
    @staticmethod
    def callReconstructImage(pathDest:str,isDemo:str,programName:str,folderPath:str):
        result=True
        args = ["-dir", f"{pathDest}"]
        try:
            os.chdir(folderPath)
            print(f"Current path {os.getcwd()}")
            comando = [programName]+ args
            print(f"comando a ejecutar {comando} ")
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capturar la salida estándar y de error
            salida_estandar =resultado.stdout
            salida_error = resultado.stderr
            print(f"Salida estándar:{salida_estandar}")
            print(f"Salida Error:{salida_error}")
            if salida_estandar:
               result = True
            if salida_error:
                result = False
        except subprocess.CalledProcessError as e:
            print("Error al ejecutar el programa C++:", e)
        except Exception as e:
            print("Ocurrió un error:", e)
            return result 
        finally:
            os.chdir("..")
            print(f"Current path {os.getcwd()}")
            return result
                    
    def getStatus()->List[StatusSlave]:
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
        Sentry.customMessage(Paths.STATUS_RASPBERIES_FILE,Paths.STATUS_RASPBERIES,f"Estado del sistema {datetime.datetime.now()}")      

        
        # Buscar si todas estan Ok
        has_error = all(statusSlave.state for statusSlave in listStatusRaspberies)
        systemStatus =  StatusSystem(slaves=listRasperr,slaveStatus=listStatusRaspberies,status=has_error,message="Error")
        print(f"System status {systemStatus}")
        return listStatusRaspberies
