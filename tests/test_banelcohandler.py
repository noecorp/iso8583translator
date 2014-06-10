#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import datetime

from iso8583translator.banelcohandler import BanelcoHandler
from iso8583translator.constants import *
from iso8583translator.tests.constants import *

class MockResponseHub(object):
    @staticmethod
    def mock_ok(*args):
        return MOCK_HUB_OK

    @staticmethod
    def mock_E_009(*args):
        return MOCK_HUB_BADLINE

    @staticmethod
    def mock_NOT_0(*args):
        return MOCK_HUB_INTERNAL_ERROR

#class MockTranslateTOISO(object):
# TODO: Class to mock the translateiso


class BanelcoTester(unittest.TestCase):
    def _now(self):
        return datetime.datetime.now()

    def test_process_request_admin_conn_bl(self):
        """
        Teting the process of an admin_conn
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_ADMIN_CONN_BL
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_request(MOCK_MESSAGE_ADMIN_CONN_BL)
        self.assertEquals(result, expected)

    def test_process_request_req_bl(self):
        """
        Teting the process of an admin_conn
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_REQ_BL
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_request(MOCK_MESSAGE_REQ_BL)
        self.assertEquals(result, expected)

    def test_process_request_rev(self):
        """
        Teting the process of an admin_conn
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_REQ_REV_BL
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_request(MOCK_MESSAGE_REQ_REV)
        self.assertEquals(result, expected)

    def test_process_request_rev_reat(self):
        """
        Teting the process of an admin_conn
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_REQ_REV_REA_BL
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_request(MOCK_MESSAGE_REQ_REV_REA)
        self.assertEquals(result, expected)

    def test_process_request_admin_conn(self):
        """
        Teting the process of an admin_conn
        """
        # I should be asserting that the fuction that was called was admin_conn
        # not the result of the method being called!
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_LOGIN
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_request(MESSAGE_ADMIN_CONN_LOGIN)
        self.assertEquals(result, expected)
        
    def test_process_mti_admin_conn_login(self):
        """
        Testing the admin conn login handler
        """
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_LOGIN
        # Probar el time to live
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_mti_admin_conn(MESSAGE_ADMIN_CONN_LOGIN)
        self.assertEquals(result, expected)

    def test_process_mti_admin_conn_logout(self):
        """
        Testing the admin conn logout handler
        """
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_LOGOUT
        # Probar que no puedo mandar a procesar nada nuevamente si n hago
        # relogin
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_mti_admin_conn(MESSAGE_ADMIN_CONN_LOGOUT)
        self.assertEquals(result, expected)

    def test_process_mti_admin_conn_echo(self):
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_ECHO
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_mti_admin_conn(MESSAGE_ADMIN_CONN_ECHO)
        self.assertEquals(result, expected)

    def test_proces_nmi_login(self):
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_LOGIN
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_nmi_login(MESSAGE_ADMIN_CONN_LOGIN)
        self.assertEquals(result, expected)

    def test_proces_nmi_logout(self):
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_LOGOUT
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_nmi_logout(MESSAGE_ADMIN_CONN_LOGOUT)
        self.assertEquals(result, expected)

    def test_proces_nmi_echo(self):
        o_since = self._now()
        expected = MESSAGE_RESPONSE_ADMIN_CONN_ECHO
        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_nmi_echo_test(MESSAGE_ADMIN_CONN_ECHO)
        self.assertEquals(result, expected)

    def test_translate_to_IS0(self):
        # This test is missing, instead I Use th three test below
        # But they are wrong becasue they test 2 functions at the same time
        # TODO
        pass


    def test_process_mti_request_ok(self):
        """
        Testing the request (0200) with ok data 00
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_REQ
        from iso8583translator.hub_handler import HubHandler
        HubHandler.parse_xml_hub_response = MockResponseHub.mock_ok
        banelco_handler = BanelcoHandler(True, o_since)
        banelco_handler
        result = banelco_handler.process_mti_req(MOCK_MESSAGE_REQ)
        self.assertEquals(result, expected)
        del HubHandler

    def test_process_mti_request_failed_82(self):
        """
        Testing the request (0200) whit failure 82
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_REQ_82
        from iso8583translator.hub_handler import HubHandler
        HubHandler.parse_xml_hub_response = MockResponseHub.mock_E_009

        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_mti_req(MOCK_MESSAGE_REQ)
        self.assertEquals(result, expected)
        del HubHandler

    def test_process_mti_request_failed_90(self):
        """
        Testing the request (0200) whit failure 90 
        """
        o_since = self._now()
        expected = MOCK_MESSAGE_RESPONSE_REQ_INTERNAL_ERROR
        from iso8583translator.hub_handler import HubHandler
        HubHandler.parse_xml_hub_response = MockResponseHub.mock_NOT_0

        banelco_handler = BanelcoHandler(True, o_since)
        result = banelco_handler.process_mti_req(MOCK_MESSAGE_REQ)
        self.assertEquals(result, expected)
        del HubHandler

    def test_process_mti_request_expired(self):
        """
        Testing the request (0200) expired
        """
        o_since = self._now()
        banelco_handler = BanelcoHandler(True, o_since)
        #Change timetolive to 0 seconds forcing expiration
        banelco_handler._ttl = datetime.timedelta(0,0,0)
        try:
            result = banelco_handler.process_mti_req(MOCK_MESSAGE_REQ)
        except AssertionError:
            return True
