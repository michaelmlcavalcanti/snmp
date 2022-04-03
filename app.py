from flask import Flask, request
import logging
from service.snmp_manager import SnmpManager


app = Flask(__name__)
snmp = SnmpManager(timeout=10)
logging.basicConfig(level=logging.INFO)

@app.route('/get_request', methods=['POST'])
def get_request():
    request_body = request.json
    ip_address = request_body['ip_address']
    community = request_body['community']
    oid = request_body['oid']
    logging.info(f'Sending GET REQUEST to ({ip_address}, {community}, {oid})')
    status, oid_response = snmp.get_request(ip_address=ip_address, community=community, oid=oid)
    
    print(status, oid_response)
    return {'status': status, 'response': oid_response} 

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)