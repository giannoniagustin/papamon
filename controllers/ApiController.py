
import time
from flask import request,jsonify,send_file
import os
import constants.Paths as Paths
from model.Status import Status
from util import File

import subprocess
from model.Response import SuccessResponse,ErrorResponse
from mappers.status.StatusMapper import StatusMapper
from mappers.raspberry.RaspberryMapper import RaspberryMapper
from controllers.status.StatusController import StatusController
from controllers.raspberry.RaspberryController import RaspberryController
from datetime import datetime
from model.Raspberry import Raspberry
import config.slave.config as config

import io
import zipfile
from flask import  make_response

from util import TimeUtil
from util.Sentry import Sentry

class ApiController:    
    @staticmethod
    def getStatus():
            try:
                status_instance= StatusController.get()
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
            StatusController.update(newInstance)
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
                me_instance =config. meRaspb
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
                return jsonify( SuccessResponse(data=instance, message="Status Raspberry").serialize())
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
                
    @staticmethod
    def callTakeImage(pathDest:str,id:str ,isDemo:str,programName:str,folderPath:str):
        result=False
        print(os.linesep+"#########################LLAMADO A PROGRAMA TOMA IMAGEN########################################"+os.linesep)
        print(f"Carpeta destino {pathDest}")
        print(f"ID de raspberry {id}")
        print(f"Ejecutando en modo demo {isDemo}")
        print(f"Programa a ejecutar {programName}")
        print(f"Carpeta de ejecucion del programa {folderPath}")
        # Argumentos del programa
        if (isDemo):
            demo="-demo"
            print("Ejecutando en modo demo")
        else:
            demo=""    
        args = ["-dir", f"{pathDest}", demo, "-id", id]
        try:
            os.chdir(folderPath)
            print(f"Cambio a path de ejecucion {os.getcwd()}")
            comando = [programName]+ args
            print(f"Comando a ejecutar {comando} ")
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if (isDemo):
                time.sleep(5)
            # Capturar la salida estándar y de error
            print(f"Salida programa:{resultado.returncode}")
            if resultado.returncode == 0:
               result = True
            else:
                result = False
        except subprocess.CalledProcessError as e:
                print("Error al ejecutar el programa C++:", e)
                Sentry.captureException(e)

        except Exception as e:
                Sentry.captureException(e)
                print("Ocurrió un error al ejecutar el programa C++::", e)
        finally:
            os.chdir("..")
            print(f"Current path {os.getcwd()}")
            if (result):
               print(f"Imagen capturada exitosamente " )
               lastImageR =TimeUtil.TimeUtil.timeToString(datetime.now(), TimeUtil.TimeUtil.format_DD_MM_YYYY_HH_MM)
            else:
                print(f"Imagen no capturada " )
                lastImageR =None
            try:      
                StatusController.updateIfChange(newStatus=Status(cameraRunning=result, lastImage=lastImageR))  
            except Exception as e:
                    print("No se pudo actualizar el archivo de estado", e)
            return result

   
    @staticmethod
    def getImage():
        try:
            date = request.args.get('data')
            print(os.linesep+f"#########################INICIO DE CAPTURA {date}########################################"+os.linesep)
            localPathImage =Paths.BUILD_IMAGE_FOLDER.format(date)
            print(f"Carpeta destino: {localPathImage} " )
            if ApiController.callTakeImage(pathDest=localPathImage, id=config.meRaspb.id,isDemo=config.isDemo,programName=config.programsaveCam,folderPath=config.reconstructFolder):
                return ApiController.buildZip(date,config.meRaspb.id)
            else:
                message="Ocurrió un error al ejecutar la llamada al programa C++"
                print(message)
                Sentry.customMessage(eventName=message)  
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

