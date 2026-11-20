---
wordpress_id: 34
title: "YAML Data format"
date: "2026-01-27T10:04:54"
url: "https://networkpuzzles.com/2026/01/27/understanding-yaml-data-format/"
---

YAML (**YAML Ain’t Markup Language**) is a human-readable data format widely used in **network automation**. Compared to JSON, YAML is **easier to read and write**, especially for large configurations.

###### YAML Syntax

YAML uses **indentation instead of brackets** to define structure.

###### Key Rules:

Case-sensitive

Indentation is **very important**

No `{ }` or `[ ]`

Uses `:` for key–value pairs

Spaces are required (tabs are not allowed)

###### YAML Mapping (Key–Value Structure)

A **mapping** in YAML is similar to:

An object in JSON

A dictionary in Python

```
device:
  hostname: SW1
  model: Cisco Catalyst 9300
  location: DataCenter-1

```
###### YAML Sequence (List)

A **sequence** is a list of values.  
Each item starts with a dash (`-`).

```
interfaces:
  - GigabitEthernet0/0
  - GigabitEthernet0/1
  - GigabitEthernet0/2

```
###### YAML Array of Objects

This is one of the **most important YAML structures** for automation.

Each list item is a full object.

```
devices:
  - hostname: R1
    ip: 10.1.1.1
    role: core
  - hostname: R2
    ip: 10.1.1.2
    role: access

```
###### YAML Nested Structures (Very Important)

Nested YAML is used in **real network configurations**.

```
device:
  hostname: SW1
  interfaces:
    - name: GigabitEthernet0/1
      ip: 192.168.1.1
      vlan: 10
    - name: GigabitEthernet0/2
      ip: 192.168.2.1
      vlan: 20
  routing:
    ospf:
      process_id: 1
      area: 0

```
```
device
 ├── hostname
 ├── interfaces (list)
 │    ├── interface 1
 │    └── interface 2
 └── routing
      └── ospf

```
###### Converting Yaml into Python dict.

```
interfaces:
  interface:
    - name: GigabitEthernet2
      description: Wide Area Network
      enabled: true
      ipv4:
        address:
          ip: 172.16.0.2
          netmask: 255.255.255.0

    - name: GigabitEthernet3
      description: LAN Users
      enabled: true
      ipv4:
        address:
          ip: 10.10.10.1
          netmask: 255.255.255.0

    - name: Loopback0
      description: Router-ID
      enabled: true
      ipv4:
        address:
          ip: 192.0.2.1
          netmask: 255.255.255.255

```
```
#pip install pyyaml
import yaml
from pprint import pprint

with open("yaml_example.yaml", "r") as f:
    yaml_dict = yaml.safe_load(f)


pprint(yaml_dict)


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
