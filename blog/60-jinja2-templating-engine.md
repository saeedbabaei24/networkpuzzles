---
wordpress_id: 60
title: "Jinja2 templating engine"
date: "2026-01-28T09:18:40"
url: "https://networkpuzzles.com/2026/01/28/jinja2-templating-engine/"
---

Jinja2 is a template processing toolkit which allows us to create and render text templates.  
It is a text based templating system. It renders a template using variable replacement, tags (conditional, lopping, inheritance, macros) and filters.

In this example, I will use **Jinja2** to automatically generate a network switch configuration file.

###### Folder and file Structure

```
project/
│
├── render_config.py
├── templates/
│   └── switch_interfaces.j2
└── output/

```
###### Jinja2 Template

```
hostname {{ hostname }}

{% for intf in interfaces %}
interface {{ intf.name }}
 description {{ intf.desc }}
 switchport mode {{ intf.mode }}
{% if intf.vlan is defined %}
 switchport access vlan {{ intf.vlan }}
spanning-tree portfast
{% endif %}
!
{% endfor %}

```

`{{ hostname }}` is replaced with a value from Python. for example if `hostname = "SW-BR-01"`, the output becomes:

```
hostname SW-BR-01
```
###### For Loop (`{% for %}`)

```
{% for intf in interfaces %}
...
{% endfor %}

```

This loop Iterates over a **list of interfaces** and replace the block once for each interface. we can also have loops in Python code. but I think the loops and Conditions in jibja2 templates are better because they are simple and also we can use the same template with Ansible too.

###### Conditional Logic (`{% if %}`)

```
{% if intf.vlan is defined %}
 switchport access vlan {{ intf.vlan }}
{% endif %}

```

This means only add the VLAN line **if the VLAN exists** and prevents invalid configs for trunk ports.

###### Python Script

```
# you should install Jinja2 module firs: ~ python -m pip install jinja2 

from jinja2 import Environment, FileSystemLoader

data = {
    "hostname": "SW-BR-01",
    "interfaces": [
        {"name": "GigabitEthernet1/0/1", "desc": "POS terminal", "mode": "access", "vlan": 10},
        {"name": "GigabitEthernet1/0/2", "desc": "Printer", "mode": "access", "vlan": 20},
        {"name": "GigabitEthernet1/0/48", "desc": "Uplink to core", "mode": "trunk"},
    ],
}

env = Environment(
    loader=FileSystemLoader("templates"),  # tells Jinja where templates are
    trim_blocks=True,  #removes empty lines
    lstrip_blocks=True  #cleans indentation
)

template = env.get_template("switch_interfaces.j2")

rendered = template.render(data)  #Replaces variables, executes loops+conditions & Produces result

with open("output/SW-BR-01.cfg", "w") as f:
    f.write(rendered)

print("Configuration generated successfully.")

```
###### Output

```
hostname SW-BR-01

interface GigabitEthernet1/0/1
 description POS terminal
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface GigabitEthernet1/0/2
 description Printer
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
!
interface GigabitEthernet1/0/48
 description Uplink to core
 switchport mode trunk
!

```
