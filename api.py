from flask import Flask,request, jsonify,send_file
import json
import os
import constants.paths as paths
from util import file

from model.response import SuccessResponse,ErrorResponse

globalConfig={}
with open('config'+os.sep+'global.json') as config_file:
    globalConfig = json.load(config_file)
    meConfig={}
with open('config'+os.sep+'me.json') as me_file:
    meConfig = json.load(me_file)

app = Flask(__name__)
data = {"message": "La papamon esta online"}  # Almacenar la información que se desea intercambiar entre las Raspberry Pis

@app.route('/', methods=['GET'])
def me():
   return jsonify( SuccessResponse(data=meConfig, message="Data config Raspberry").serialize())
    
@app.route('/status', methods=['GET']) 
def get_status():
    statusFile={}
    try:
            statusFile =file.FileUtil.read_file(paths.STATUS_RB) 
    except FileNotFoundError as e:
        print(f"Error: File '{statusFile}' not found.")
        return jsonify(ErrorResponse(data=statusFile, message="An error occurred: "+e.strerror).serialize())
    except IOError as e:
                return jsonify(ErrorResponse(data=statusFile, message="An error occurred: "+e.strerror).serialize())  
    except Exception as e:
                print("An error occurred:", e)
                return jsonify(ErrorResponse(data=statusFile, message="An error occurred: ").serialize())
    else:
        print("File read successfully.")        
        return jsonify( SuccessResponse(data=statusFile, message="Status Raspberry").serialize())


@app.route('/send', methods=['POST'])
def send_data():
    global data
    new_data = request.json
    data.update(new_data)
    return jsonify({"message": "Data received successfully"}), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    data1 = request.form['data']
    print(data1)
    image = request.files['image']
    image.save('received_image_'+image.filename+'.jpg')  # Guardar la imagen en el servidor

    return jsonify({"message": "Image uploaded successfully"}), 200

@app.route('/get_image', methods=['GET'])
def get_image():
    filename = 'received_image.jpg'  # Ruta de la imagen que deseas enviar
    return send_file(filename, mimetype='image/jpeg')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 