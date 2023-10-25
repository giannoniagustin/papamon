
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
        result=isDemo
        # Argumentos del programa
        if (isDemo):
            demo="-demo"
        else:
            demo=""    
        args = ["-dir", f"{pathDest}", demo, "-id", id]
        try:
            os.chdir(folderPath)
            print(f"Cambio a path de ejecucion {os.getcwd()}")
            comando = [programName]+ args
            print(f"Comando a ejecutar {comando} ")
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
            print("Ocurrió un error al ejecutar el programa C++::", e)
        finally:
            os.chdir("..")
            print(f"Current path {os.getcwd()}")
            if (result):
               print(f"Imagen capturada exitosamente " )
               lastImageR =TimeUtil.TimeUtil.timeToString(datetime.now(), TimeUtil.TimeUtil.format_DD_MM_YYYY)
            else:
                print(f"Imagen no capturada " )
                lastImageR =None  
            StatusController.updateIfChange(newStatus=Status(cameraRunning=result, lastImage=lastImageR))    
            return result

   
    @staticmethod
    def getImage():
        try:
            date = request.args.get('data')
            print(f"Inicio toma imagen fecha {date} " )
            localPathImage =Paths.BUILD_IMAGE_FOLDER.format(date)
            if ApiController.callTakeImage(pathDest=localPathImage, id=config.meRaspb.id,isDemo=config.isDemo,programName=config.programsaveCam,folderPath=config.reconstructFolder):
                return ApiController.getResult(date,config.meRaspb.id)
            else:
                print("Ocurrió un error al ejecutar la llamada al programa C++")
                return jsonify(ErrorResponse(data='', message="An error occurred").serialize())

        except FileExistsError as e:
            print(f"La carpeta '{date}' ya existe.")
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  

        except Exception as e:
            print("Ocurrió un error:", e)
            return jsonify(ErrorResponse(data='', message=f"An error occurred {e.strerror} ").serialize())  

    def getResult(date:str,id:str):
        folderPath =Paths.IMAGES+date+os.sep
        # Crear un archivo ZIP en memoria
        buffer = File.FileUtil.zipFoler(folderPath)
        response = make_response(buffer.read())
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = f'attachment; filename={date}.zip'
        return response

