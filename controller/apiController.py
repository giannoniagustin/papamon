
from flask import request,jsonify,json,send_file
import constants.Paths as Paths
from util import File
import subprocess
from model.Response import SuccessResponse,ErrorResponse
from mappers.StatusMapper import StatusMapper
from mappers.MeMapper import MeMapper
from mappers.RaspberryMapper import RaspberryMapper

import os

class ApiController:
    @staticmethod
    def getStatus():
            statusFile={}
            try:
                statusFile =File.FileUtil.read_file(Paths.STATUS_RB) 
                statusMapper = StatusMapper()
                status_instance = statusMapper.toStatus(dictFile=statusFile) 
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
            fileUpdate =File.FileUtil.read_file(Paths.STATUS_RB) 
            #Ver que no agregue el campo si no existe ya,solo que actualice si existe
            for key, value in new_data.items():
                if key in fileUpdate:
                    fileUpdate[key] = value
            mapper = StatusMapper()
            # Lo convierte a nueva instancia
            status_instance = mapper.toStatus(dictFile=fileUpdate) 
            print('File path write: '+Paths.STATUS_RB)
            content = mapper.toJson(status_instance)
            File.FileUtil.write_file(Paths.STATUS_RB,content=content)
        except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
        except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
        except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
        else:
                print("File read successfully.")        
                return jsonify( SuccessResponse(data=status_instance, message="Update status success").serialize())

    @staticmethod
    def getMe():
            meFile={}
            try:
                path=Paths.ME
                print('Path Me: '+path)
                meFile =File.FileUtil.read_file(path) 
                meMapper = MeMapper()
                status_instance = meMapper.toMe(dictFile=meFile) 
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
    def getRaspberry():
            #Lista de raspberry a pedir las imagenes
            file={}
            try:
                path=Paths.RASPBERRY
                print('Path Raspberry: '+path)
                file =File.FileUtil.read_file(path) 
                mapper = RaspberryMapper()
                instance = mapper.toRaspberry(dictFile=file) 
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
            else:
             print("File read successfully.")        
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
            # Crear la carpeta con el ID de solicitud actual
            nombre_carpeta = currentRequestId
            localPathImage = Paths.IMAGES+nombre_carpeta
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
    

