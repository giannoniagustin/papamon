
from flask import request,jsonify,json
import constants.Paths as Paths
from util import File
from model.response import SuccessResponse,ErrorResponse
from mappers.StatusMapper import StatusMapper
from mappers.MeMapper import MeMapper

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