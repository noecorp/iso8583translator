#!/usr/bin/env python
# -*- coding: utf-8 -*-

MOCKED_HUB_REQUEST = """<?xml version = "1.0" encoding = "UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<SOAP-ENV:Body>
<ns1:pinvirtualtrans xmlns:ns1="pinvirtualService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<lote xsi:type="xsd:string">115023301220090530171337</lote>
<bill xsi:type="xsd:string">1150233012</bill>
<codtarjeta xsi:type="xsd:string">VVS010</codtarjeta>
<codoperacion xsi:type="xsd:string">S</codoperacion>
<codentidad xsi:type="xsd:string">2</codentidad>
<pos xsi:type="xsd:string">1234</pos>
<verificador xsi:type="xsd:string">4982b0fa12ce517e44a2521dc8b1a860eadbffb3</verificador>
</ns1:pinvirtualtrans>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

MOCKED_XML_STRING = """<?xml version = "1.0" encoding = "UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<SOAP-ENV:Body>
<ns1:pinvirtualtrans xmlns:ns1="pinvirtualService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<lote xsi:type="xsd:string">1</lote>
<bill xsi:type="xsd:string">1130616901</bill>
<codtarjeta xsi:type="xsd:string">10.00</codtarjeta>
<codoperacion xsi:type="xsd:string">S</codoperacion>
<codentidad xsi:type="xsd:string">bla</codentidad>
<pos xsi:type="xsd:string">3</pos>
<verificador xsi:type="xsd:string">34</verificador>
</ns1:pinvirtualtrans>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

