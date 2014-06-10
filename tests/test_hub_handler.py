#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import datetime

from iso8583translator.constants import *
from iso8583translator.hub_handler import HubHandler
from iso8583translator.tests.constants import *
from iso8583translator.tests.mocks.mock_hub_request import MOCKED_HUB_REQUEST


class HubHandlerTester(unittest.TestCase):
    def test_ensamble_xml(self):
        #expected = MOCKED_XML_STRING
        h_handler = HubHandler()
        result = h_handler._ensamble_xml(1, '1130616901', 'bla', '10.00', '3', '34')
        #ass = open('/tmp/testxml', 'wb')
        #ass.write(result)
        #ass.close()
        #self.assertEquals(result, expected)

    def test_hash_info(self):
        expected = ""
        h_handler = HubHandler()
        h_handler._hash_info('2', '1130616901', 'bla', '10.00', '3', '34')
    
    def test_construct_date_for_batch(self):
        h_handler = HubHandler()
        print h_handler._construct_date_for_batch()

    def test_send_xml_request_to_hub(self):
        xml_string = MOCKED_HUB_REQUEST
        #xml_file = open('./tests/mocks/mock_hub_request.xml', 'r')
        #xml_string = xml_file.read()
        h_handler = HubHandler()
        xml_result =  h_handler.send_xml_request_to_hub(xml_string)
 
    def test_parse_xml_hub_response(self):
        xml_string = MOCKED_HUB_REQUEST
        #xml_file = open('./tests/mocks/mock_hub_request.xml', 'r')
        #xml_string = xml_file.read()
        h_handler = HubHandler()
        xml_result =  h_handler.send_xml_request_to_hub(xml_string)

        dict_response = h_handler.parse_xml_hub_response(xml_result)
       
        print dict_response 
        
    def test_process_hub_request(self):
        h_handler = HubHandler()
        MOCK_MESSAGE_REQ
 
        xml_result =  h_handler.process_hub_request(MOCK_MESSAGE_REQ)

        dict_response = h_handler.parse_xml_hub_response(xml_result)
       
        print dict_response 

        
