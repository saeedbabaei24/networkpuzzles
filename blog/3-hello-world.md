---
wordpress_id: 3
title: "JSON Data format"
date: "2025-10-19T21:02:52"
url: "https://networkpuzzles.com/2025/10/19/hello-world/"
---

JSON (JavaScript Object Notation) is one of the most important data formats in modern networking.  
It is widely used in **REST APIs, SD-WAN controllers, automation tools, and network management systems**.

In lists, we can have multiple entries that are indexed starting from 0 up to *n*.  
Access to list elements is based on their index number.

Another data type is the **dictionary**, which uses a **key–value** structure instead of indexes.

JSON follows the same key–value concept as dictionaries. We can access values using their keys, but we cannot directly access a key if we only know the value.

###### JSON Syntax

JSON uses **key–value pairs**.

###### Rules:

* Keys must be in **double quotes**
* Values can be:
  + String
  + Number
  + Boolean
  + Object
  + Array
* Objects use `{ }`
* Arrays use `[ ]`

###### 

###### JSON Object

A JSON object represents a **single entity**.

Similar to a **Python dictionary**  
Commonly used to describe a device or configuration block.

```
{
  "device": "SW1",
  "model": "Cisco Catalyst 9300",
  "mgmt_ip": "192.168.10.10",
  "location": "DataCenter-1"
}
```
###### JSON Array

A JSON array is a **list of values**.

```
[
  "GigabitEthernet0/0",
  "GigabitEthernet0/1",
  "GigabitEthernet0/2"
]
or
[
  "10.0.0.1",
  "10.0.0.2",
  "10.0.0.3"
]
```
###### JSON Array of Objects

This is one of the **most important structures** in networking automation.

It represents **multiple devices or interfaces**.

```
[
  {
    "hostname": "R1",
    "ip": "10.1.1.1",
    "role": "core"
  },
  {
    "hostname": "R2",
    "ip": "10.1.1.2",
    "role": "distribution"
  }
]
```
###### Nested JSON Structures

Nested JSON means:

* Objects inside objects
* Arrays inside objects
* Objects inside arrays

```
Example:
{
  "device": {
    "hostname": "SW1",
    "interfaces": [
      {
        "name": "GigabitEthernet0/1",
        "ip": "192.168.1.1",
        "vlan": 10
      },
      {
        "name": "GigabitEthernet0/2",
        "ip": "192.168.2.1",
        "vlan": 20
      }
    ],
    "routing": {
      "ospf": {
        "process_id": 1,
        "area": 0
      }
    }
  }
}
```
```
device
 ├── hostname
 ├── interfaces (array)
 │         ├── interface 1
 │         └── interface 2
 └── routing
            └── ospf
```
###### Converting Json into dict in Python

here is an example of Json which I want to converting to dict in python. We should use Json library for that.

```
{
  "interfaces": {
    "interface": [
      {
        "name": "GigabitEthernet2",
        "description": "Wide Area Network",
        "enabled": true,
        "ipv4": {
          "address": {
            "ip": "172.16.0.2",
            "netmask": "255.255.255.0"
          }
        }
      },
      {
        "name": "GigabitEthernet3",
        "description": "LAN Users",
        "enabled": true,
        "ipv4": {
          "address": {
            "ip": "10.10.10.1",
            "netmask": "255.255.255.0"
          }
        }
      },
      {
        "name": "Loopback0",
        "description": "Router-ID",
        "enabled": true,
        "ipv4": {
          "address": {
            "ip": "192.0.2.1",
            "netmask": "255.255.255.255"
          }
        }
      }
    ]
  }
}

```
```
#Python code:

import json

from pprint import pprint

jason_example = open("Json_example.json").read()

jason_dict = json.loads(jason_example)

pprint (jason_dict)
```
```
Output:
{'interfaces': {'interface': [{'description': 'Wide Area Network',
                               'enabled': True,
                               'ipv4': {'address': {'ip': '172.16.0.2',
                                                    'netmask': '255.255.255.0'}},
                               'name': 'GigabitEthernet2'},
                              {'description': 'LAN Users',
                               'enabled': True,
                               'ipv4': {'address': {'ip': '10.10.10.1',
                                                    'netmask': '255.255.255.0'}},
                               'name': 'GigabitEthernet3'},
                              {'description': 'Router-ID',
                               'enabled': True,
                               'ipv4': {'address': {'ip': '192.0.2.1',
                                                    'netmask': '255.255.255.255'}},
                               'name': 'Loopback0'}]}}
```
