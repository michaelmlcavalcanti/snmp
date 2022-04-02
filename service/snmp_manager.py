from re import I
import socket 
import logging



class SnmpManager():
    '''Class define ....'''

    def __init__(self, timeout,  port = 161) -> None:
        self.port = port
        self.timeout = timeout
        logging.basicConfig(level=logging.INFO)
        self.is_ready = self.__create_socket()

    def __create_socket(self) -> bool:
        try:
            logging.info('Creating SNMP socket...')
            self.snmp_socket = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
            #self.snmp_socket.bind((self.address, self.port))
            self.snmp_socket.settimeout(self.timeout)
            return True
        except Exception as ex:
            logging.error(f'Error during SnmpManager initialization: {ex}') 
            return False

    def get_oid_list(self, ip_address, community):
        '''Return a list of oid'''
        oid_list = []
        status = False
        
        if(self.is_ready):
            if (community is ''):
                community = 'public'

            while True:
                try:
                    snmp_response = self.snmp_socket.recv(2000).decode()
                    logging.info('SNMP Message received!')
                    oid_list = self.__create_oid_list(snmp_response) 
                except self.snmp_socket:
                    logging.error(f'The socket timed out ({self.timeout})')


        return status, oid_list

    def get_oid_info(self, ip_address, community, oid):
        pass

    def __create_oid_list(self, oid_response):
        return [{'oid': oid[0], 'description': oid[1]} for oid in oid_response]