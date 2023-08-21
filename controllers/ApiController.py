
from flask import request,jsonify,send_file
import os
import constants.Paths as Paths
from util import File
from util.Time import TimeUtil

import subprocess
from model.Response import SuccessResponse,ErrorResponse
from mappers.status.StatusMapper import StatusMapper
from mappers.raspberry.RaspberryMapper import RaspberryMapper
from controllers.status.StatusController import StatusController
from controllers.raspberry.RaspberryController import RaspberryController
from datetime import datetime


class ApiController:
    @staticmethod
    def getStatus():
            try:
                status_instance= StatusController.get()
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
            else:
                print("File read successfully.")        
                return jsonify( SuccessResponse(data=status_instance, message="Status Raspberry").serialize())
   
    @staticmethod
    def updateStatus():
        try:
            # Abre el archivo JSON y actualiza los datos
            new_data = request.get_json()  # Obtén los datos JSON de la solicitud
            mapper = StatusMapper()
            newInstance = mapper.toStatus(new_data)
            StatusController.update(newInstance)
        except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
        except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
        except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
        else:
                return jsonify( SuccessResponse(data=newInstance, message="Update status success").serialize())

    @staticmethod
    def getMe():
            try:
                status_instance = RaspberryController.getMe()
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
            else:
             return jsonify( SuccessResponse(data=status_instance, message="Status Raspberry").serialize())
    @staticmethod
    def getRaspberry():
            #Lista de raspberry a pedir las imagenes
            file={}
            try:
                instance = RaspberryController.getRaspberries()
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
            else:
                return jsonify( SuccessResponse(data=instance, message="Status Raspberry").serialize())
    @staticmethod
    def callTakeImage(pathImge:str):
        # Comando y argumentos
        comando = ["./programa",'{pathImge}']
        try:
            #resultado = subprocess.run("./programa", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capturar la salida estándar y de error
            salida_estandar =True# resultado.stdout
            salida_error = True #resultado.stderr
            print("Salida estándar:")
            print(salida_estandar)
            if salida_estandar:
               return salida_estandar
            if salida_error:
                print("Salida de error:")
                print(salida_error)
        except subprocess.CalledProcessError as e:
            print("Error al ejecutar el programa C++:", e)
        except Exception as e:
            print("Ocurrió un error:", e) 
   
    @staticmethod
    def getImage(key, currentRequestId: str):
        nombre_carpeta=''
        try:
            parametro1 = request.args.get('data')
            print(f"Parametro {parametro1} " )
            nombre_carpeta = TimeUtil.timeToString(datetime.now(),TimeUtil.formato)
            localPathImage =Paths.BUILD_IMAGE_FOLDER.format(nombre_carpeta)
            File.FileUtil.createFolder(localPathImage)

        except FileExistsError as e:
            print(f"La carpeta '{nombre_carpeta}' ya existe.")
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  

        except Exception as e:
            print("Ocurrió un error:", e)
            return jsonify(ErrorResponse(data='', message="An error occurred").serialize())  

        else:
           if ApiController.callTakeImage(pathImge=localPathImage):
           # filename = pathImage+currentRequestId+'.jpg' #'received_image.jpg'  # Ruta de la imagen que deseas enviar
            filename = Paths.IMAGES+'83e56229-0dd4-4faf-9fe5-fdd510ca6af2'+os.sep+'83e56229-0dd4-4faf-9fe5-fdd510ca6af2'+'.jpg' 
            return send_file(filename, mimetype='image/jpeg')
           else:
                print("Ocurrió un error al ejecutar la llamada al programa C++")
                return jsonify(ErrorResponse(data='', message="An error occurred").serialize())
    

