from flask import Flask,request, jsonify
from controllers.ApiController import ApiController
import uuid


app = Flask(__name__)
# Diccionario para almacenar identificadores de solicitud
request_ids = {}
@app.before_request
def set_request_id():
    request_id = str(uuid.uuid4())
    request_ids[request] = request_id    
@app.route('/', methods=['GET'])
def me():
    return ApiController.getMe()
    
@app.route('/status', methods=['GET']) 
def getStatus():
     return ApiController.getStatus()

@app.route('/status', methods=['PUT'])
def updateStatus():
       return ApiController.updateStatus()


@app.route('/image', methods=['POST'])
def uploadImage():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    image = request.files['image']
    image.save('received_image.jpg')  # Guardar la imagen en el servidor
    return jsonify({"message": "Image uploaded successfully"}), 200

@app.route('/image', methods=['GET'])
def geImage(): 
    key, currentRequestId = request_ids.popitem()
    
    return ApiController.getImage(key,currentRequestId)

@app.route('/raspberry', methods=['GET'])
def raspberry():
    return ApiController.getRaspberry()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
 
  
