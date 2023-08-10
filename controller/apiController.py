
from flask import jsonify
import constants.paths as paths
from util import file
from model.response import SuccessResponse,ErrorResponse
from mappers.StatusMapper import StatusMapper
from mappers.MeMapper import MeMapper

class ApiController:
    @staticmethod
    def getStatus():
            statusFile={}
            try:
                statusFile =file.FileUtil.read_file(paths.STATUS_RB) 
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
    def getMe():
            meFile={}
            try:
                path=paths.ME
                print('Path Me: '+path)
                meFile =file.FileUtil.read_file(path) 
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