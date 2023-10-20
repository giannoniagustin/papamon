
from flask import request,jsonify,send_file
import os
import constants.Paths as Paths
from util import File
from util.TimeUtil import TimeUtil

import subprocess
from model.Response import SuccessResponse,ErrorResponse
from mappers.status.StatusMapper import StatusMapper
from mappers.raspberry.RaspberryMapper import RaspberryMapper
from controllers.status.StatusController import StatusController
from controllers.raspberry.RaspberryController import RaspberryController
from datetime import datetime
from model.Raspberry import Raspberry
from config import meRaspb
from config import programsaveCam
from config import reconstructFolder
from config import isDemo
import io
import zipfile
from flask import  make_response

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
                me_instance = meRaspb
            except FileNotFoundError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())
            except IOError as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  
            except Exception as e:
                return jsonify(ErrorResponse(data='', message="An error occurred: ").serialize())
            else:
             return jsonify( SuccessResponse(data=me_instance, message="Status Raspberry").serialize())
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
    def callTakeImage(pathDest:str,id:str ,isDemo:str,programName:str,folderPath:str):
        result=True
        # Argumentos del programa
        if (isDemo):
            demo="-demo"
        else:
            demo=""    
        args = ["-dir", f"{pathDest}", demo, "-id", id]
        try:
           # folderPath = "reconstruct"
            os.chdir(folderPath)
            print(f"Current path {os.getcwd()}")
            #programName="./rs-save-cam-status"
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
        finally:
            os.chdir("..")
            print(f"Current path {os.getcwd()}")
            return result

   
    @staticmethod
    def getImage(key, currentRequestId: str):
        #nombre_carpeta=''
        try:
            date = request.args.get('data')
            print(f"Parametro {date} " )
            '''nombre_carpeta = TimeUtil.timeToString(datetime.now(),TimeUtil.formato)
            localPathImage =Paths.BUILD_IMAGE_FOLDER.format(nombre_carpeta)
            File.FileUtil.createFolder(localPathImage)'''
            if ApiController.callTakeImage(pathDest=date, id=meRaspb.id,isDemo=isDemo,programName=programsaveCam,folderPath=reconstructFolder):
                # filename = pathImage+currentRequestId+'.jpg' #'received_image.jpg'  # Ruta de la imagen que deseas enviar
                '''filename = Paths.IMAGES+'83e56229-0dd4-4faf-9fe5-fdd510ca6af2'+os.sep+'83e56229-0dd4-4faf-9fe5-fdd510ca6af2'+'.jpg' 
                return send_file(filename, mimetype='image/jpeg')'''
                return ApiController.getResult(date,meRaspb.id)
            else:
                print("Ocurrió un error al ejecutar la llamada al programa C++")
                return jsonify(ErrorResponse(data='', message="An error occurred").serialize())

        except FileExistsError as e:
            print(f"La carpeta '{date}' ya existe.")
            return jsonify(ErrorResponse(data='', message="An error occurred: "+e.strerror).serialize())  

        except Exception as e:
            print("Ocurrió un error:", e)
            return jsonify(ErrorResponse(data='', message="An error occurred").serialize())  

        else:
             print("Ocurrió un error:", e)
             return jsonify(ErrorResponse(data='', message="An error occurred").serialize())  

    def getResult(date:str,id:str):
        imageRgb =Paths.IMAGES+date+os.sep+id+os.sep+Paths.RGB_FILE
        imageDepth =Paths.IMAGES+date+os.sep+id+os.sep+Paths.DEPTH_FILE
        datosCSV=Paths.IMAGES+date+os.sep+id+os.sep+Paths.POINT_FILE
        # Crear un archivo ZIP en memoria
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Agregar las imágenes PNG al archivo ZIP
            with open(imageRgb, 'rb') as imagen1:
                zipf.writestr(Paths.RGB_FILE, imagen1.read())
            with open(imageDepth, 'rb') as imagen2:
                zipf.writestr(Paths.DEPTH_FILE, imagen2.read())
            
            # Agregar el archivo CSV al archivo ZIP
            with open(datosCSV, 'rb') as datos_csv:
                zipf.writestr(Paths.POINT_FILE, datos_csv.read())

        # Preparar la respuesta
        buffer.seek(0)
        response = make_response(buffer.read())
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = 'attachment; filename=archivos.zip'

        return response

