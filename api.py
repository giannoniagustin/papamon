from flask import Flask,request, jsonify,send_file
import json

with open('config/global.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
data = {"message": "La papamon esta online"}  # Almacenar la información que se desea intercambiar entre las Raspberry Pis

@app.route('/')
def hello_world():
    return '¡Hola, esta es mi API REST en mi Raspberry Pi!'
    
@app.route('/get', methods=['GET'])
def get_data():
    global data
    return jsonify(data), 200

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


def test(): return print('Holaaaaaa')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 