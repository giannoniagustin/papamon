from flask import Flask,request, jsonify
from controllers.MasterApiController import MasterApiController
import uuid
import constants.Paths as Paths



app = Flask(__name__)
# Diccionario para almacenar identificadores de solicitud
request_ids = {}
@app.before_request
def set_request_id():
    request_id = str(uuid.uuid4())
    request_ids[request] = request_id    
@app.route('/', methods=['GET'])
def me():
    return MasterApiController.getMe()
    
@app.route('/status', methods=['GET']) 
def getStatus():
     return MasterApiController.getStatus()

@app.route('/status', methods=['PUT'])
def updateStatus():
       return MasterApiController.updateStatus()


@app.route('/image', methods=['POST'])
def uploadImage():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    image = request.files['image']
    image.save('received_image.jpg')  # Guardar la imagen en el servidor
    return jsonify({"message": "Image uploaded successfully"}), 200

#Invoca al programa que toma la imagen y devuelve los archivos
@app.route('/image', methods=['GET'])
def geImage(): 
    key, currentRequestId = request_ids.popitem()
    return MasterApiController.getImage()

@app.route('/raspberries', methods=['GET'])
def raspberries():
    return MasterApiController.getRaspberries()

# Endpoint para obtener el listado de carpetas
@app.route('/reconstruct', methods=['GET'])
def reconstruct_folders():
    location = Paths.IMAGES # Reemplaza con tu ubicación
    return MasterApiController.get_folder_list(location)

@app.route('/reconstruct/download', methods=['GET'])
def getReconstructForDate():
    date = request.args.get('date')
    return MasterApiController.getReconstructForDate(date)

@app.route('/reconstruct/download/rgb/<int:idCamera>', methods=['GET'])
def getRGBForDateAndCamera(idCamera):
        date = request.args.get('date')
        return MasterApiController.getRGBForDateAndCamera(date=date,idCamera=str(idCamera))
@app.route('/reconstruct/download/result', methods=['GET'])
def getReconsResultForDate():
        date = request.args.get('date')
        return MasterApiController.getReconsResultForDate(date=date)
    
@app.route('/freespace', methods=['GET'])
def getFreeSpace():
        return MasterApiController.getFreeSpace()
@app.route('/delete', methods=['GET'])
def delete():
        date = request.args.get('date')
        return MasterApiController.deleteFolder(date)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 
  
