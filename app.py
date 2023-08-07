from flask import Flask,request, jsonify

app = Flask(__name__)
data = {"message": "La papamon esta online"}  # Almacenar la información que se desea intercambiar entre las Raspberry Pis

@app.route('/')
def hello_world():
    return '¡Hola, esta es mi API REST en mi Raspberry Pi!'
    
@app.route('/get', methods=['GET'])
def get_data():
    global data
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
