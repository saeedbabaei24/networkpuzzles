---
wordpress_id: 162
title: "Network Device Automation with Jinja2 Template"
date: "2026-02-01T09:22:57"
url: "https://networkpuzzles.com/2026/02/01/network-device-automation-with-jinja2-template/"
---

If we want to automate a network with many devices we have normally 4 files a python code, host files, config file and data file.

In this example I want to automate BGP configuration of routers. So I prepare these 4 files. The first file is Host file which contains the IP of the devices, the second file is BGP template file that is a jinja2 and as you can see I am using for loop in this file. In bgp.yaml file we have the data which will be rendered into the jinja2 template and then pushes to the devices, and this is the python script job.

```
The sample config on one router:
Router bgp 100
 neighbor 192.168.10.1
 neighbor 192.168.20.1
 neighbor 192.168.30.1

#hosts.yaml host file

hosts:
  - 10.10.10.1
  - 10.10.11.1
  - 10.10.12.1
  - 10.10.13.1
  - 10.10.14.1


#BGP_Template.j2 file

router bgp {{ bgp.asn }}
{% for n in bgp.neighbors %}
 neighbor {{ n.ip }}
{% endfor %}


#bgp.yaml file:

bgp:
  asn: 100
  neighbors:
    - ip: 192.168.10.1
    - ip: 192.168.20.1
    - ip: 192.168.30.1

```

Lets look at the python code. It loads the Host and bgp yaml file and also the jinja2 template file. Then it renders the template with the data. so we have the config file now. With help of the netmiko library we can push the prepared config to the routers.

```
import yaml
import getpass
from jinja2 import Template
from netmiko import ConnectHandler

# files
HOSTS_FILE = "hosts.yaml"
DATA_FILE = "bgp.yaml"
TEMPLATE_FILE = "BGP_Template.j2"

DEVICE_TYPE = "cisco_ios"   # change if needed


# read hosts
with open(HOSTS_FILE, "r") as f:
    hosts = yaml.safe_load(f)["hosts"]

# read data
with open(DATA_FILE, "r") as f:
    data = yaml.safe_load(f)

# read template
with open(TEMPLATE_FILE, "r") as f:
    template_text = f.read()

# render config
config_text = Template(template_text).render(**data)

print("\n=== Rendered Config ===")
print(config_text)

# credentials
username = input("Username: ").strip()
password = getpass.getpass("Password: ")

# push to routers
for ip in hosts:
    try:
        conn = ConnectHandler(
            device_type=DEVICE_TYPE,
            host=ip,
            username=username,
            password=password
        )

        commands = [line for line in config_text.splitlines() if line.strip()]
        conn.send_config_set(commands)
        conn.save_config()
        conn.disconnect()

        print(f" Done: {ip}")

```
