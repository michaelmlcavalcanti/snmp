from flask import Flask, request


app = Flask(__name__)


#Definir endpoints

@app.route('/get_oid_info', methods=['POST'])
def get_oid():
    request_body = request.json
    ip_address = request_body['ip_address']
    oid_list = request_body['oid_list']
    #adicionar schema pra validar json
    print(ip_address)
    print(oid_list)
    return 'ola', 200   #json response, status_code

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)