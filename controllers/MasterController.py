
import io
import os
import subprocess
from controllers.raspberry.RaspberryController import RaspberryController
import constants.Paths as Paths
from controllers.status.StatusController import StatusController
from model.Raspberry import Raspberry
from util import File,TimeUtil
import constants.EndPoints as EndPoint
import requests
import datetime
from mappers.status.StatusMapper import StatusMapper
from controllers.statusRaspberies.StatusRaspberiesController import StatusRaspberiesController
from controllers.image.ImageController import ImageController

import config.master.config as config



from model.StatusSlave import StatusSlave
from model.Status import Status
from model.StatusSystem import StatusSystem
from util.Sentry import Sentry
from typing import List

class MasterController:
    @staticmethod
    def getImages():
        reconstructSuccess = False
        rbFailList:List[Raspberry] = []
        request_id = TimeUtil.TimeUtil.timeToString(datetime.datetime.now(), TimeUtil.TimeUtil.format_DD_MM_YYYY_HH_MM)
        # Crear la carpeta con el ID de solicitud actual
        localPathImage =Paths.BUILD_IMAGE_FOLDER.format(request_id)
        outResult= localPathImage+Paths.RECONSTRUCTION_OUT_FILE
        print(f"Carpeta de salida de reconstrucción {outResult}")
        File.FileUtil.createFolder(localPathImage)
        listRasperr = RaspberryController.getRaspberries()
        for rB in listRasperr:
            try:
                rbSucces = False
                url= EndPoint.url_template.format(rB.ip,rB.port,EndPoint.IMAGE)
                print("Url grt images ",url)
                params = {f"data": {request_id}}
                response = requests.get(url,params=params)
                if response.status_code == 200:
                    zip_data = io.BytesIO(response.content)
                    ImageController.extractMemory(localPathImage,zip_data)
                    print(f"Imagen descargada y almacenada con éxito de RB {rB.name} ")
                    rbSucces = True
                else:
                    print(f"Error al descargar la imagen de RB {rB.name}")
            except requests.exceptions.ConnectionError as e:
                    print("Error de conexión:", e)
                    Sentry.captureException(e)
            except requests.exceptions.RequestException as e:
                    print("Error en la solicitud:", e)
                    Sentry.captureException(e)

            except Exception as e:
                    print("Error en obteenr imagen:", e)
                    Sentry.captureException(e)
            finally:
                    if not rbSucces:
                        rbFailList.append(rB)
        print(f"Listado de Raspberry con error: {rbFailList}")                
        result=MasterController.callReconstructImage(localPathImage,config.isDemo,config.programsaveCam,config.reconstructFolder)
        reconstructSuccess = result   and rbFailList.__len__()  < listRasperr.__len__()
        if (reconstructSuccess):
            if (File.FileUtil.fileExists(outResult)):
             Sentry.customMessage(filename=request_id+Paths.JSON,path=outResult,eventName="Reconstrucción de imagen")  
             StatusController.updateIfChange(Status(cameraRunning=True,lastImage=request_id,))
            else:
                Sentry.customMessage(eventName="El archivo de reconstruccion no existe ")  
                print("El archivo de reconstruccion no existe ")  
                StatusController.updateIfChange(Status(cameraRunning=False,lastImage=None)) 
        else:
            Sentry.customMessage(eventName="Ocurrio un error en la reconstrucción de la imagen")  
            StatusController.updateIfChange(Status(cameraRunning=False,lastImage=None))
            
        return  reconstructSuccess
                    
    @staticmethod
    def callReconstructImage(pathDest:str,isDemo:str,programName:str,folderPath:str):
        try:
            resultSucces=isDemo
            args = ["-dir", f"{pathDest}"]
            os.chdir(folderPath)
            print(f"Current path {os.getcwd()}")
            comando = [programName]+ args
            print(f"Comando a ejecutar {comando} ")
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capturar la salida estándar y de error
            salida_estandar =resultado.stdout
            salida_error = resultado.stderr
            print(f"Salida estándar:{salida_estandar}")
            print(f"Salida Error:{salida_error}")
            if salida_estandar:
               resultSucces = True
            if salida_error:
                resultSucces = False
        except subprocess.CalledProcessError as e:
            print("Error al ejecutar el programa C++:", e)
            Sentry.captureException(e)
        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)

        finally:
            os.chdir("..")
            print(f"Current path {os.getcwd()}")
            return resultSucces
                    
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
                    
        # Buscar si todas estan Ok
        has_error =  all(statusSlave.state for statusSlave in listStatusRaspberies)
        statusMaster =StatusController.get()
        if (not has_error):
            statusMaster.cameraRunning=False
            message= "Error de Conexion con algunas de las camaras"
        else:
            statusMaster.cameraRunning=True    
            message= "Se conecto con todas las camaras"
                             
        listStatusRaspberies.append(StatusSlave(raspberry=config.meRaspb,status=statusMaster,message=message,state=has_error))            
        StatusRaspberiesController().update(listStatusRaspberies)
        Sentry.customMessage(Paths.STATUS_RASPBERIES_FILE,Paths.STATUS_RASPBERIES,f"Estado del sistema {datetime.datetime.now()}")      
        return listStatusRaspberies
