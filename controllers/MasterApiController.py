

from flask import request,jsonify,send_file
import os
import constants.Paths as Paths
import psutil
import shutil


from util import File

from model.Response import SuccessResponse,ErrorResponse
from mappers.status.StatusMapper import StatusMapper
from mappers.raspberry.RaspberryMapper import RaspberryMapper
from controllers.statusRaspberies.StatusRaspberiesController import StatusRaspberiesController
from controllers.raspberry.RaspberryController import RaspberryController
from datetime import datetime
from model.Raspberry import Raspberry
import config.master.config as config

import io
import zipfile
from flask import  make_response

from util import TimeUtil
from util.Sentry import Sentry

class MasterApiController:    
    @staticmethod
    def getStatus():
            try:
                status_instance= StatusRaspberiesController.get()
                print("File read successfully.")        
                return jsonify( SuccessResponse(data=status_instance, message="Status Raspberry").serialize())
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())


   
    @staticmethod
    def updateStatus():
        try:
            # Abre el archivo JSON y actualiza los datos
            new_data = request.get_json()  # Obtén los datos JSON de la solicitud
            mapper = StatusMapper()
            newInstance = mapper.toStatus(new_data)
            StatusRaspberiesController.update(newInstance)
            print(f'Status  --'+{newInstance})
            return jsonify( SuccessResponse(data=newInstance, message="Update status success").serialize())

        except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
        except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
        except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())


    @staticmethod
    def getMe():
            try:
                me_instance =config.meRaspb
                return jsonify( SuccessResponse(data=me_instance, message="Status Raspberry").serialize())
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())

             
    @staticmethod
    def getRaspberries():
            #Lista de raspberry a pedir las imagenes
            file={}
            try:
                instance = RaspberryController.getRaspberries()
                return jsonify( SuccessResponse(data=instance, message="Listado de raspberries configuradas").serialize())
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
    # Función para obtener el listado de carpetas en una ubicación
    @staticmethod
    def get_folder_list(location):
            #Lista de carpetas en la ubicación
            try:
                instance =File.FileUtil.getFiles(location)
            #    mapper = ListFileMapper()
                return jsonify( SuccessResponse(data=instance, message="Listado de carpetas y archivos").serialize())
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())        
    
    @staticmethod
    def getReconstructForDate(date:str):
        try:
            print(os.linesep+f"#########################INICIO DE RECUPERO RECONSTRUCT {date}########################################"+os.linesep)
            localPathImage =Paths.BUILD_IMAGE_FOLDER.format(date)
            print(f"Carpeta destino: {localPathImage} " )
            if  File.FileUtil.fileExists(localPathImage):
                return MasterApiController.buildZip(date,config.meRaspb.id)
            else:
                message="Ocurrió un error al recuperar las imágenes. No existe la carpeta de destino."
                print(message)
        
                return jsonify(ErrorResponse(data='', message=message).serialize()),500

        except FileExistsError as e:
            print(f"La carpeta '{date}' ya existe.")
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize()),500  

        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message=f"An error occurred {e.strerror} ").serialize())  ,500

    @staticmethod
    def getRGBForDateAndCamera(date,idCamera:str):
        try:
            print(os.linesep+f"#########################INICIO DE RECUPERO RGB FECHA {date} CAMARA {idCamera}-########################################"+os.linesep)
            localPathImage =Paths.BUILD_PATH_FILE_RGB.format(date,idCamera,Paths.RGB_FILE)
            print(f"Carpeta destino: {localPathImage} " )
            if  File.FileUtil.fileExists(localPathImage):
                return MasterApiController.buildZipFile(localPathImage,"RGB_"+date+"_"+idCamera)
            else:
                message="Ocurrió un error al recuperar la imágen RGB. No existe la carpeta de destino."
                print(message)
        
                return jsonify(ErrorResponse(data='', message=message).serialize()),500

        except FileExistsError as e:
            print(f"La carpeta '{date}' ya existe.")
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize()),500  

        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message=f"An error occurred {e.strerror} ").serialize())  ,500
    @staticmethod
    def getReconsResultForDate(date):
        try:
            print(os.linesep+f"#########################INICIO DE RECUPERO RECONSTRUCCION FILE {date} -########################################"+os.linesep)
            localPathImage =Paths.BUILD_PATH_FILE_RECONSTRUCT.format(date,Paths.RECONSTRUCTION_FILE)

            print(f"Carpeta destino: {localPathImage} " )
            if  File.FileUtil.fileExists(localPathImage):
                return MasterApiController.buildZipFile(localPathImage,"RECONSTRUCTION_"+date)
            else:
                message="Ocurrió un error al recuperar archivo reconstruct. No existe la carpeta de destino."
                print(message)
        
                return jsonify(ErrorResponse(data='', message=message).serialize()),500

        except FileExistsError as e:
            print(f"La carpeta '{date}' ya existe.")
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize()),500  

        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message=f"An error occurred {e.strerror} ").serialize())  ,500


    def buildZip(date:str,id:str):
        print(f"Creando zip {date} " )
        folderPath =Paths.IMAGES+date+os.sep
        print(f"Folder path {folderPath} " )
        File.FileUtil.listFolders(folderPath=folderPath)
        # Crear un archivo ZIP en memoria
        buffer = File.FileUtil.zipFoler(folderPath)
        response = make_response(buffer.read())
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = f'attachment; filename={date}.zip'
        return response   
    
    def buildZipFile(filePath:str,nameZipFile:str):
        print(f"Creando zip {filePath}")
        # Verificar si el archivo existe antes de crear el ZIP
        if os.path.exists(filePath):
            # Crear un archivo ZIP en memoria
            buffer = File.FileUtil.zipFile(filePath)
            # Configurar la respuesta HTTP con el contenido del ZIP
            buffer.seek(0)
            response = make_response(buffer.read())
            response.headers['Content-Type'] = 'application/zip'
            response.headers['Content-Disposition'] = f'attachment; filename={nameZipFile}.zip'
            return response
        else:
            # Manejar el caso donde el archivo no existe
            return jsonify(ErrorResponse(data='', message="An error occurred: El archivo no existe ").serialize())   
        
    @staticmethod
    def getFreeSpace(path='/'):
        try:

            disk_usage = psutil.disk_usage(path)
            free_space_gb = disk_usage.free / (1024 ** 3)  # Espacio libre en GB
            result=f"Espacio libre en disco: {free_space_gb} GB"
            return jsonify( SuccessResponse(data=result, message="Espacio libre en disco").serialize())
        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message=f"An error occurred {e.strerror} ").serialize())  ,500
    @staticmethod
    def deleteReconstructForDate(date:str):
        try:
            print(os.linesep+f"#########################INICIO DE DELETE RECONSTRUCT {date}########################################"+os.linesep)
            localPathImage =Paths.BUILD_IMAGE_FOLDER.format(date)
            print(f"Carpeta a borrar destino: {localPathImage} " )
            if  File.FileUtil.fileExists(localPathImage):
                return MasterApiController.buildZip(date,config.meRaspb.id)
            else:
                message="Ocurrió un error al recuperar las imágenes. No existe la carpeta de destino."
                print(message)
        
                return jsonify(ErrorResponse(data='', message=message).serialize()),500

        except FileExistsError as e:
            print(f"La carpeta '{date}' ya existe.")
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize()),500  

        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message=f"An error occurred {e.strerror} ").serialize())  ,500
        
    @staticmethod    
    def deleteFolder(date:str):
        print(f"Eliminando carpeta {date} " )
        folderPath =Paths.IMAGES+date+os.sep
        print(f"Folder path {folderPath} " )
        try:
            # Verificar si la ruta es una carpeta
            if os.path.isdir(folderPath):
                # Eliminar la carpeta y su contenido de manera recursiva
                shutil.rmtree(folderPath)
                return jsonify( SuccessResponse(data=f"Carpeta {folderPath} eliminada correctamente", message="Carpeta eliminada").serialize())
            else:
                # Manejar el caso donde la ruta no es una carpeta
                return jsonify(ErrorResponse(data='', message="An error occurred: La ruta no es una carpeta ").serialize())
        except Exception as e:
            print("Ocurrió un error:", e)
            Sentry.captureException(e)
            return jsonify(ErrorResponse(data='', message=f"Error al eliminar carpeta {e.strerror} ").serialize())  ,500


    


