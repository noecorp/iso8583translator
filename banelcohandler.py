#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from iso8583translator.constants import *
from iso8583translator.hub_handler import HubHandler
from iso8583translator.iso_translator import ISO8583Parser

# Take into account the timeout between connections,
# we will maintain a thread for each connection, for a limited time
# each echo will extend that period

class BanelcoHandler(object):
    _ttl = datetime.timedelta(seconds=DEFAULT_TIME_TO_LIVE_SECONDS)

    def __init__(self, logged, opened_since):
        # Flag to check if it is already logged in
        self._logged = logged
        # time to live when it reachs 0 it terminates conneection
        # it can be renewed by the echo test
        self._opened_since = opened_since
        # Registering handlers for mti's
        self._handlers_mti = {}
        self._handlers_mti[MTI_ADMIN_CONN] = self.process_mti_admin_conn
        self._handlers_mti[MTI_REQ] = self.process_mti_req
        self._handlers_mti[MTI_ADMIN_CONN_ERROR] = self.create_err_msg
        self._handlers_mti[MTI_REQ_ERROR] = self.create_err_msg
        self._handlers_mti[MTI_REQ_REVERSAL] = self.create_err_msg
        self._handlers_mti[MTI_REQ_REVERSAL_REATTEMPT] = self.create_err_msg

        # Registering handlers for nmi's
        self._handlers_nmi = {}
        self._handlers_nmi[NMI_LOGIN] = self.process_nmi_login
        self._handlers_nmi[NMI_LOGOUT] = self.process_nmi_logout
        self._handlers_nmi[NMI_ECHO_TEST] = self.process_nmi_echo_test

    def process_request(self, msg):

        mti = ISO8583Parser.get_MTI(msg)

        try:

            handler = self._handlers_mti[mti]
        except:
            return "BAD LINE" #The errors should be handled according to doc
    
        try:        
            return handler(msg)
        except AssertionError:
            return "No esta Logueado"
        except:
            return "Error interno"
   
        
    def process_mti_admin_conn(self, msg):
        nmi = ISO8583Parser.get_NMI(msg)
        if nmi is not None:
            return self._handlers_nmi[nmi](msg)
        else:
            raise ValueError

    def process_mti_req(self, msg):
        # Check time to live against opened since
        now = datetime.datetime.now()
       
        try: 
            assert self._logged, True
            assert now - self._opened_since < self._ttl
        except:
            raise

        hub_handler = HubHandler()
        response_unproc = hub_handler.process_hub_request(msg)
        response_hub = hub_handler.parse_xml_hub_response(response_unproc)

        result_transaction, importeOut = self.translate_to_ISO8583(response_hub)
        
        # Send message parameters based on result_transaction

        return ISO8583Parser.ensamble_response_req(msg, importeOut, result_transaction)

    def create_err_msg(self, msg):
        """
        Simply replace bit 12 with a 9
        """
        tmp_msg = list(msg)
        tmp_msg[12] = MTI_BIT_ERROR
        err_msg = ''.join(tmp_msg)
        return  err_msg
        
    def process_nmi_login(self, msg):
        return ISO8583Parser.ensamble_response_admin_conn(msg, NMI_LOGIN, OK_TRANSACTION)

    def process_nmi_logout(self, msg):
        # After this this particular thread should expire
        return ISO8583Parser.ensamble_response_admin_conn(msg, NMI_LOGOUT, OK_TRANSACTION)

    def process_nmi_echo_test(self, msg):
        # Renew time to live
        return ISO8583Parser.ensamble_response_admin_conn(msg, NMI_ECHO_TEST, OK_TRANSACTION)

    def translate_to_ISO8583(self, response_hub):
        try:
            if response_hub['codrespuestaOut'] != 'O':
                response_hub['importeOut'] = '0'
    
                if response_hub['codrespuestaOut'] == 'E' and \
                   response_hub['descripcionOut'] == '009':
                    # Bad Line: 82
                    result_transaction = ERROR_TRANSACTION_BAD_LINE
                else:
                    result_transaction = ERROR_TRANSACTION_INTERNAL_ERROR
            else:
                    result_transaction = OK_TRANSACTION
            return result_transaction, str(response_hub['importeOut'])
        except:
            return ERROR_TRANSACTION_INTERNAL_ERROR,  '0'
