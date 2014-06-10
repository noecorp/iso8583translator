#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from iso8583translator.iso_translator import ISO8583Parser
from iso8583translator.constants import *
from iso8583translator.tests.constants import *


class ISO8583Tester(unittest.TestCase):
    def test_get_mti(self):
        expected = MTI_ADMIN_CONN
        result = ISO8583Parser.get_MTI(MOCK_MESSAGE_ADMIN_CONN)
        self.assertEquals(result, expected)
        
    def test_get_nmi_0800(self):
        expected = NMI_LOGIN
        result = ISO8583Parser.get_NMI(MOCK_MESSAGE_ADMIN_CONN)
        self.assertEquals(result, expected)

    def test_get_nmi_0810(self):
        expected = NMI_LOGIN
        result = ISO8583Parser.get_NMI(MOCK_MESSAGE_RESPONSE_ADMIN_CONN)
        self.assertEquals(result, expected)
 
    def test_get_mti_admin_conn_error_len(self):
        expected = MTI_ADMIN_CONN_ERROR
        result = ISO8583Parser.get_MTI(MOCK_MESSAGE_ADMIN_CONN_BL)
        self.assertEquals(result, expected)
 
    def test_get_mti_req_error_len(self):
        expected = MTI_REQ_ERROR
        result = ISO8583Parser.get_MTI(MOCK_MESSAGE_REQ_BL)
        self.assertEquals(result, expected)

    def test_ensamble_response_admin(self):
        expected = MOCK_MESSAGE_RESPONSE_ADMIN_CONN
        result = ISO8583Parser.ensamble_response_admin_conn(MOCK_MESSAGE_ADMIN_CONN, NMI_LOGIN, \
                                                             OK_TRANSACTION)
        self.assertEquals(result, expected)

    def test_ensamble_response_req(self):
        expected = MOCK_MESSAGE_RESPONSE_REQ
        result = ISO8583Parser.ensamble_response_req(MOCK_MESSAGE_REQ, '0', 
                                                    OK_TRANSACTION)

        self.assertEquals(result, expected)

    def test_extract_phone(self):
        expected = '1144558899' 
        result = ISO8583Parser.extract_phone(MOCK_MESSAGE_REQ)
        self.assertEquals(result, expected)

    def test_extract_amount(self):
        expected = '10' 
        result = ISO8583Parser.extract_amount(MOCK_MESSAGE_REQ)
        self.assertEquals(result, expected)
