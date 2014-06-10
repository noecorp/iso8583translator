#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

from twisted.internet.protocol import Protocol, ServerFactory

from iso8583translator.banelcohandler import BanelcoHandler
from iso8583translator.constants import *
from iso8583translator.iso_translator import ISO8583Parser
from twisted.python import log

class BanelcoListener(Protocol):
    def __init__(self):
        self.logged = False
        self.opened_since = datetime.datetime.now()

    def dataReceived(self, data):
        # Strip garbage data
        data = 'ISO' + data.rpartition('ISO')[2]
        banelco_handler = BanelcoHandler(self.logged, self.opened_since)
        response = banelco_handler.process_request(data)
        # Parse response and only put logged in true if it is an 810
        # + 001, logged False on 002 and renew login on 301
        mti = ISO8583Parser.get_MTI(response)
        if mti == MTI_ADMIN_CONN_RESP:
            nmi = ISO8583Parser.get_NMI(response)
            if nmi == NMI_LOGIN:
                self.logged = True
                self.opened_since = datetime.datetime.now()
            elif nmi == NMI_LOGOUT:
                self.logged = False
            elif nmi == NMI_ECHO_TEST:
                self.opened_since = datetime.datetime.now()
        elif mti == MTI_REQ_RESP:
                self.opened_since = datetime.datetime.now()
        response_len = len(response)

        formatted_response = '%X%s' % (response_len, response)

        self.transport.write(response)

factory = ServerFactory()
factory.protocol = BanelcoListener


from twisted.application import service, internet

application = service.Application("BanelcoServer")
internet.TCPServer(APP_PORT, factory).setServiceParent(application)
