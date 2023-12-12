
import sys
import time
from flask import request,jsonify,send_file
import os
import constants.Paths as Paths
from mappers.listFile.ListFileMapper import ListFileMapper
from model.ListFiles import ListFiles
from model.Status import Status

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
    def getReconstructForDate():
        try:
            date = request.args.get('data')
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

