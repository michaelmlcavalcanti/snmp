from flask import Flask, request
import logging
from service.snmp_manager import SnmpManager


app = Flask(__name__)
snmp = SnmpManager(timeout=10)
logging.basicConfig(level=logging.INFO)

@app.route('/get_oid_list', methods=['POST'])
def get_oid_list():
    request_body = request.json
    ip_address = request_body['ip_address']
    community = request_body['community']
    logging.info(f'Finding oid list from IP {ip_address} with community: {community}')
    
    status, oid_list = snmp.get_oid_list(ip_address=ip_address, community=community)

    return {'status': status, 'oid_list': oid_list}, [200 if status else 400]   #json response, status_code


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