#!/usr/bin/env python
# -*- coding: utf-8 -*-

import amara
import datetime
import hashlib
import httplib

from iso8583translator.iso_translator import ISO8583Parser
from iso8583translator.constants import *

# Take into account the timeout between connections,
# we will maintain a thread for each connection, for a limited time
# each echo will extend that period

class HubHandler(object):
    def process_hub_request(self, msg):
        phone = ISO8583Parser.extract_phone(msg)
        batch_date = self._construct_date_for_batch()
        amount = ISO8583Parser.extract_amount(msg)
        amount = amount.rjust(3, '0')
        amount = 'VVS' + amount
        batch = phone + batch_date
        pos = DEFAULT_POS
        passw = BANELCO_PASS
        entity = BANELCO_ID
        checksum = self._hash_info(batch, phone, entity, amount, pos, passw)
        xml_string = self._ensamble_xml(batch, phone, entity, amount, pos, checksum)
        
        response_xml = self.send_xml_request_to_hub(xml_string)

        return response_xml


    def _construct_date_for_batch(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()

        return timestamp.strftime("%Y%m%d%H%M%S")


    def _hash_info(self, batch, phone, entity, amount, pos, passw):
        MIDDLE_HASH_VARIABLE = 'S'
        unhashed_string = ''.join((batch, phone, amount, MIDDLE_HASH_VARIABLE, \
                                  entity, pos, passw))

        sha_object = hashlib.sha1()
        sha_object.update(unhashed_string)
        return sha_object.hexdigest()
            
    def _ensamble_xml(self, batch, phone, entity, amount, pos, checksum):
        xml_1 = """<?xml version = "1.0" encoding = "UTF-8"?>"""
        xml_2 = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">"""
        xml_3 = """<SOAP-ENV:Body>"""
        xml_4 = """<ns1:pinvirtualtrans xmlns:ns1="pinvirtualService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">"""
        xml_5 = """<lote xsi:type="xsd:string">%s</lote>""" % batch
        xml_6 = """<bill xsi:type="xsd:string">%s</bill>""" % phone
        xml_7 = """<codtarjeta xsi:type="xsd:string">%s</codtarjeta>""" % amount
        xml_8 = """<codoperacion xsi:type="xsd:string">S</codoperacion>"""
        xml_9 = """<codentidad xsi:type="xsd:string">%s</codentidad>""" % entity
        xml_10 = """<pos xsi:type="xsd:string">%s</pos>""" % pos
        xml_11 = """<verificador xsi:type="xsd:string">%s</verificador>""" % checksum
        xml_12 = """</ns1:pinvirtualtrans>"""
        xml_13 = """</SOAP-ENV:Body>"""
        xml_14 = """</SOAP-ENV:Envelope>"""
    	xml_string = (xml_1, xml_2, xml_3,xml_4,xml_5,xml_6,xml_7,xml_8,xml_9,
                      xml_10,xml_11,xml_12,xml_13,xml_14)
    	return '\n'.join(xml_string)
    	#return '\r\n'.join(xml_string)

    def send_xml_request_to_hub(self, xml_string):
        host = '%s:%s' % (HUB_HOST, HUB_PORT)
        webservice = httplib.HTTP(host)
        webservice.putrequest("POST", HUB_APP_PATH)
        webservice.putheader("Host", host)
        webservice.putheader("Content-type", 'text/xml; charset="utf-8"')
        webservice.putheader("Content-length", str(len(xml_string)))
        webservice.endheaders()
        webservice.send(xml_string)
        statuscode, statusmessage, header = webservice.getreply()
        return webservice.getfile().read()

    def parse_xml_hub_response(self, xml_string):  
        doc = amara.parse(xml_string)
        data = doc.xml_xpath(u"//return")[0]

        try:
            dict_response = {}
            dict_response['codrespuestaOut'] = str(data.codrespuestaOut)
            dict_response['descripcionOut'] = str(data.descripcionOut)     
            dict_response['importeOut'] = str(data.importeOut)
            dict_response['importetarjOut'] = str(data.importetarjOut)
            dict_response['mensajeOut'] = str(data.mensajeOut)
        except:
            dict_response['codrespuestaOut'] = ''
            dict_response['descripcionOut'] = ''     
            dict_response['importeOut'] = '0'         
            dict_response['importetarjOut'] = '0'
            dict_response['mensajeOut'] = ''

        return dict_response

