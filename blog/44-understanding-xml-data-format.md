---
wordpress_id: 44
title: "XML Data format"
date: "2026-01-27T10:21:57"
url: "https://networkpuzzles.com/2026/01/27/understanding-xml-data-format/"
---

XML (**eXtensible Markup Language**) is a **data format** used to store and exchange structured data. Unlike JSON and YAML, XML uses **tags** to define data. It also works with YANG models.

###### XML Syntax

XML uses **opening and closing tags** to describe data.

###### Basic Rules:

Data is stored between tags

Every tag must have a closing tag

Tags are case-sensitive

Elements must be properly nested

Attributes are optional

###### XML Element

An **XML element** is the basic building block of XML.

```
<hostname>R1</hostname>
```

`<hostname>` → opening tag

`R1` → value

`</hostname>` → closing tag

###### XML Attributes

Attributes provide **additional information** inside a tag. Attributes are optional and Values must be in quotes.

```
<interface name="GigabitEthernet0/1" status="up">
  <ip>192.168.1.1</ip>
</interface>

```
###### XML Nested Structures

Like JSON and YAML, XML supports **nested structures**.

```
<device>
  <hostname>SW1</hostname>
  <interfaces>
    <interface>
      <name>GigabitEthernet0/1</name>
      <ip>192.168.1.1</ip>
      <vlan>10</vlan>
    </interface>
    <interface>
      <name>GigabitEthernetnet0/2</name>
      <ip>192.168.2.1</ip>
      <vlan>20</vlan>
    </interface>
  </interfaces>
</device>

```
###### XML List (Array of Objects)

XML does not have arrays explicitly, but **repeated tags act like lists**.

```
<interfaces>
  <interface>
    <name>GigabitEthernet0/1</name>
  </interface>
  <interface>
    <name>GigabitEthernet0/2</name>
  </interface>
</interfaces>

```
###### Converting XML into Python dictionary

If we want to convert the XML code into Python dict. we can use xmltodict library. Here is a sample XML file:

```
<?xml version="1.0" encoding="UTF-8"?>
<interfaces xmlns="ietf-interfaces">
  <interface>
    <name>GigabitEthernet2</name>
    <description>Wide Area Network</description>
    <enabled>true</enabled>
    <ipv4>
      <address>
        <ip>172.16.0.2</ip>
        <netmask>255.255.255.0</netmask>
      </address>
    </ipv4>
  </interface>

  <interface>
    <name>GigabitEthernet3</name>
    <description>LAN Users</description>
    <enabled>true</enabled>
    <ipv4>
      <address>
        <ip>10.10.10.1</ip>
        <netmask>255.255.255.0</netmask>
      </address>
    </ipv4>
  </interface>

  <interface>
    <name>Loopback0</name>
    <description>Router-ID</description>
    <enabled>true</enabled>
    <ipv4>
      <address>
        <ip>192.0.2.1</ip>
        <netmask>255.255.255.255</netmask>
      </address>
    </ipv4>
  </interface>
</interfaces>

```
```
#Install xmltodict with pip

import xmltodict
from pprint import pprint

xml_example = open ("xml_example.xml").read()

xml_dict = xmltodict.parse(xml_example)

pprint(xml_dict)
```
```
Output:

{'interfaces': {'@xmlns': 'ietf-interfaces',
'interface': [{'description': 'Wide Area Network',
'enabled': 'true',
'ipv4': {'address': {'ip': '172.16.0.2',
'netmask': '255.255.255.0'}},
'name': 'GigabitEthernet2'},
{'description': 'LAN Users',
'enabled': 'true',
'ipv4': {'address': {'ip': '10.10.10.1',
'netmask': '255.255.255.0'}},
'name': 'GigabitEthernet3'},
{'description': 'Router-ID',
'enabled': 'true',
'ipv4': {'address': {'ip': '192.0.2.1',
'netmask': '255.255.255.255'}},
'name': 'Loopback0'}]}}
```
