#!/usr/bin/env python
# -*- coding: utf-8 -*-
from iso8583translator.constants import *

class ISO8583Parser(object):
    @staticmethod
    def get_MTI(msg):
        """
        Retrieves the message identifier
        """

        try:
            mti =  msg[12:16]
            if mti == MTI_ADMIN_CONN and len(msg) < MTI_LEN_ADMIN_CONN:
                mti = MTI_ADMIN_CONN_ERROR
            elif mti == MTI_REQ and len(msg) < MTI_LEN_REQ:
                mti = MTI_REQ_ERROR
        except:
            return None
        
        return mti


    @staticmethod
    def get_NMI(msg):
        """
        Retrieves the NMI
        """
        try:
            # Get the first three chars of the last four chars of the string
            # Take into account the termination character
            # Quick and dirty
            mti = ISO8583Parser.get_MTI(msg)

            if mti == MTI_ADMIN_CONN:
                nmi = msg[64:67]
            elif mti == MTI_ADMIN_CONN_RESP or mti == MTI_ADMIN_CONN_ERROR:
                nmi = msg[66:69]

            if nmi not in NMIS_LIST:
                return None
            else:
                return nmi
        except:
            return None

    @staticmethod
    def ensamble_response_admin_conn(msg, xdata, result_transaction):
        """
   		Changes last characater of C-002 to 5,
   		Changes c-003 to 0810
   		Changes c-004 to 8220000002000000
   		Changes p-001 to 0400000000000000
   		Adds p-039 on the 64 char of the response
        Values are: 00 approved, 05 denied and 91 down
        """
        response = []
        response.append(msg[0:11])
        response.append(DICT_MIDDLE_ADMIN_CONN[result_transaction])
        response.append(msg[48:64])        
        response.append(result_transaction)        
        response.append(xdata)        
        response.append(msg[-1:])
        return ''.join(response)

    @staticmethod
    def extract_phone(msg):
        """
        Extract phone number
        phone: S-126
        client: [80:98] (Variable Data)
        """    
        return msg[229:248].strip()

    @staticmethod
    def extract_amount(msg):
        """
        Extract amount to load
        amount: P-004 with two decimal spaces [55:67]
        convert to string without decimals
        """    
        return str(int(msg[55:66])/100)

    @staticmethod
    def ensamble_response_req(msg, action, result_transaction):
        """
   		Changes last characater of C-002 to 5,
   		Changes c-003 to 0210
   		Changes c-004 to B038800008808018
   		Changes p-001 to 0000000000000004
   		Adds p-039 on the 98 char of the response
        Values are: 00 approved, 82 invalid line and 90 internal error
        """
  
        response = []
        action = str(action)
        action_1 = action.ljust(16)
        action_2 = action.ljust(30)
        response.append(msg[0:12])
        response.append(DICT_MIDDLE_REQ[result_transaction])
        response.append(msg[48:98])
        response.append(result_transaction)
        response.append(msg[98:248])        
        response.append(action_1)
        response.append(action_2)
        response.append(msg[294:382])        
        return ''.join(response)
