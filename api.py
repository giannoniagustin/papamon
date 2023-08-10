from flask import Flask,request, jsonify,send_file
from controller.ApiController import ApiController

app = Flask(__name__)

@app.route('/', methods=['GET'])
def me():
    return ApiController.getMe()
    
@app.route('/status', methods=['GET']) 
def getStatus():
     return ApiController.getStatus()

@app.route('/status', methods=['PUT'])
def updateStatus():
       return ApiController.updateStatus()


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
 