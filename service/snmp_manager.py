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

    def get_request(self, ip_address, community, oid):
        status = False
        snmp_response = None
        self.__create_socket()
        if(self.is_ready):
            if (community == ''):
                logging.info('Using default community: public')
                community = 'public'

            snmp_message = self.__build_snmp_message(oid = oid, community= community)
            print(snmp_message)
            self.snmp_socket.sendto(snmp_message, (ip_address, 161))
            logging.info('Frame sent! Waiting response...')
            while True:
                try:
                    snmp_response = self.snmp_socket.recv(2000).decode()
                    logging.info('SNMP Message received!')
                    print(snmp_response)
                    #snmp_response = self.__handle_snmp_response(snmp_response) 
                    break
                except Exception as ex:
                    if(self.snmp_socket.timeout):
                        logging.info(f'The socket timed out ({self.timeout})')
                    else: 
                        logging.info(f'Unhandled exception: {ex}')
                    break

            self.snmp_socket.close()

        return status, snmp_response

    def __build_snmp_message(self, community, oid = 'public'):
        # MONTANDO VARBIND
        ####montando Value
        TypeVal= b'\x05'
        lenVal_b = b'\x00'
        SVal = TypeVal + lenVal_b
        lenSVal_i = 2

        ####montando Object Identifier
        b = oid.split(".")
        b = b[2:]
        oid = chr(0x2b)

        for i in range(len(b)):
            oid = oid + chr(int(b[i]))
        oid = oid.encode()

        lenOID_b = chr(len(oid)).encode()
        lenOID_i = len(oid)
        TypeOid = b'\x06'
        SOid = TypeOid + lenOID_b + oid
        lenSOid_i = 2 + lenOID_i

        TypeVarbind = b'\x30'
        lenVar_i = lenSOid_i + lenSVal_i
        lenVar_b = lenVar_i.to_bytes(1,'little')
        SVarbind = TypeVarbind + lenVar_b + SOid + SVal

        # MONTANDO VARBINDLIST
        TypeVarbindList = b'\x30'
        lenVarList_i = 2 + lenVar_i
        lenVarList_b = lenVarList_i.to_bytes(1,'little')
        SVarbindList = TypeVarbindList + lenVarList_b+ SVarbind

        # MONTANDO REQUEST ID
        lenRqID_i = 3
        SRqID = b'\x02'+ b'\x01' + b'\x01'

        # MONTANDO ERROR
        lenErr_i = 3
        SErr = b'\x02' + b'\x01' + b'\x00'

        # MONTANDO ERROR INDEX
        lenErrIndex_i = 3
        SErrIndex = b'\x02' + b'\x01' + b'\x00'

        # MONTANDO SNMP PDU
        TypeSPDU = b'\xa0' 
        lenPDU_i = lenRqID_i + lenErr_i + lenErrIndex_i + (2 + lenVarList_i)
        lenPDU_b = lenPDU_i.to_bytes(1,'little')
        SPDU = TypeSPDU + lenPDU_b + SRqID + SErr + SErrIndex + SVarbindList

        # MONTANDO COMMUNITY STRING
        TypeComm = b'\x04'
        Comm = b'public' #todo alterar dps
        CommChr = Comm.decode()
        lenComm_b = chr(len(CommChr)).encode()
        lenComm_i = len(Comm)
        SComm = TypeComm + lenComm_b + Comm

        # MONTANDO VERSION
        TypeVersao = b'\x02'
        lenVersao_b = b'\x01'
        lenVersao_i = 3
        Versao = b'\x00'
        SVersao = TypeVersao + lenVersao_b + Versao

        # MONTANDO SNMP MESSAGE (GETREQUEST)
        MsgType = b'\x30'
        lenSSnmpMsg_i = lenVersao_i + (2 + lenComm_i)+ (2 + lenPDU_i)
        lenSSnmpMsg_b = lenSSnmpMsg_i.to_bytes(1,'little')
        SSnmpMsg =  MsgType + lenSSnmpMsg_b + SVersao + SComm + SPDU
        return SSnmpMsg

    def __handle_snmp_response(self, snmp_response):

        pass

    def __create_oid_list(self, oid_response):
        return [{'oid': oid[0], 'description': oid[1]} for oid in oid_response]

    def __handle_oid_sequence(oid):
        return oid.replace('.', '')