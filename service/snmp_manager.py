from re import I
import socket 
import logging



class SnmpManager(BaseException):
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

    def get_request(self, ip_address, community, oid):
        status = False
        snmp_response = None
        
        if(self.is_ready):
            if (community == ''):
                logging.info('Using default community: public')
                community = 'public'

            OID = oid.replace('.', '')
            lenOID = len(OID)
            lenComm = len(community)
            #montar msg
            SVal = '50'
            #Objeto Field
            TypeOId = chr(0x06)
            SOid = TypeOId + chr(lenOID) + OID

            #Sequence / Varbind Type Field
            TypeVarbind = chr(0x30) # tipo varbind
            SVarbind = TypeVarbind + chr(lenOID + 2 + 2) + SOid + SVal

            #Sequence / Varbind List Field
            TypeVarbindList = chr(0x30) # tipo varbind list
            SVarbindList = TypeVarbindList + chr(len(SVarbind)) + SVarbind

            #campos Request ID, Error, ErrorIndex
            RqID = chr(2) + chr(1) + chr(1)
            Err = chr(2) + chr(1) + chr(0)
            ErrIndex = chr(2) + chr(1) + chr(0)

            SPDU = chr(0xa0) + chr(3 + 3 + 3 + len(SVarbindList)) + RqID + Err + ErrIndex + SVarbindList

            #Community
            SComm = chr(4) + chr(lenComm) + community

            #Versao
            SVersao = chr(2) + chr(1) + chr(0)

            #SNMP MESSAGE
            MsgType = chr(0x30)
            SSnmp = MsgType + chr(3 + 2 + lenComm + len(SPDU)) + SVersao + SComm + SPDU

            str2byte = SSnmp.encode()
            print(str2byte)
            self.snmp_socket.sendto(str2byte, (ip_address, 161))

            while True:
                try:
                    snmp_response = self.snmp_socket.recv(2000).decode()
                    logging.info('SNMP Message received!')
                    snmp_response = self.__handle_snmp_response(snmp_response) 
                    break
                except Exception as ex:
                    if(self.snmp_socket.timeout):
                        logging.info(f'The socket timed out ({self.timeout})')
                    else: 
                        logging.info(f'Unhandled exception: {ex}')
                    break

        return status, snmp_response

    def __handle_snmp_response(self, snmp_response):
        pass

    def __create_oid_list(self, oid_response):
        return [{'oid': oid[0], 'description': oid[1]} for oid in oid_response]

    def __handle_oid_sequence(oid):
        return oid.replace('.', '')