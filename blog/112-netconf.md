---
wordpress_id: 112
title: "NETCONF"
date: "2026-01-31T12:39:08"
url: "https://networkpuzzles.com/2026/01/31/netconf/"
---

In this example I want to connect to a router in cisco sandbox and get the interface gig1 data.

If we want to use the Python we should install ncclient library at first with pip install ncclient. on the router netconf ans ssh in enabled. I would also use xmltodict library in order to be able to convert the xml data format to python dictionary. and in order to convert the xml string into xml object I use etree module from lxml library so that we can make an xml object to sent to the device. xml.dom.minidom is for have a pretty view of the xml output.

```
from ncclient import manager
import xmltodict
from lxml import etree
import xml.dom.minidom
```

I am goning to use a dictionary for user credentials here for our test.

```
IOS_XE_LAB = {
    "HOST" : "10.10.20.48",
    "PORT" : 830,
    "USER" : "developer",
    "PASS" : "C1sco12345"

}
```

On order to get, edit, delete or.. we need to specify that. The way to do this is using filter in NETCONF. So for example here we want to get the interface Gig1 of the router. In netconf filter we should specify the Data model (YANG), container and also Module name and .

```
filter_str = """
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface>
    <name>GigabitEthernet1</name>
  </interface>
</interfaces>
"""
```

Now with this code we are connecting to the device using ncclient Manager module. We are sending the User Credentials to make a Netconf session which is a SSH connection on port 830. Then we are saving the get method output in result. Filter is used as a input in get method.

```
with manager.connect(host=IOS_XE_LAB["HOST"], port=IOS_XE_LAB["PORT"], username=IOS_XE_LAB["USER"],
                     password=IOS_XE_LAB["PASS"], hostkey_verify=False) as m:
    # Retrieve the operational data
    result = m.get(filter=('subtree', etree.fromstring(filter_str)))


    Pretty_xml = xml.dom.minidom.parseString(result.xml).toprettyxml()

print(Pretty_xml)
```
```
Output:

<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:ad59644e-b1fb-4b8f-97ca-28847aef11af">
        <data>
                <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet1</name>
                                <description>MANAGEMENT INTERFACE - DON'T TOUCH ME</description>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>10.10.20.48</ip>
                                                <netmask>255.255.255.0</netmask>
                                        </address>
                                </ipv4>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                </interfaces>
        </data>
</rpc-reply>
```

  


Now if we want to add an ip address on interface Gig 2 and also turn the interface on we can use the same filter but instead of the GET request we should use edit.

```
Current Status:
cat8000v#sh ip int brie
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       10.10.20.48     YES NVRAM  up                    up
GigabitEthernet2       unassigned      YES NVRAM  administratively down down
GigabitEthernet3       unassigned      YES NVRAM  administratively down down
Loopback0              10.0.0.1        YES NVRAM  up                    up
Loopback10             unassigned      YES unset  up                    up
Loopback109            10.255.255.9    YES NVRAM  up                    up
VirtualPortGroup0      192.168.1.1     YES NVRAM  up                    up

```
```
config_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet2</name>
      <enabled>true</enabled>
      <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
        <address>
          <ip>1.1.1.1</ip>
          <netmask>255.255.255.0</netmask>
        </address>
      </ipv4>
    </interface>
  </interfaces>
</config>
"""

with manager.connect(host=IOS_XE_LAB["HOST"], port=IOS_XE_LAB["PORT"], username=IOS_XE_LAB["USER"],
                     password=IOS_XE_LAB["PASS"], hostkey_verify=False) as m:
    # Retrieve the operational data
    result = m.edit_config(target="running", config=config_payload)
```

As you can see this time we are using edit\_config method to edit the running configuration based on the config payload. hostkey\_verify=False is for not asking the ssh key verification when it wants to do ssh.

```
Output:

<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:7e3b35f5-21d7-4a19-9310-22a6b6023aa5">
        <ok/>
</rpc-reply>

On the router:

*Jan 31 11:22:58.393: %SYS-5-CONFIG_P: Configured programmatically by process io                               sp_dmiauthd_conn_100001_vty_100001 from console as developer on vty4294966926
*Jan 31 11:22:58.379: %DMI-5-CONFIG_I: R0/0: dmiauthd: Configured from NETCONF/R                               ESTCONF by developer, transaction-id 25
cat8000v#

cat8000v#sh ip int brie
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       10.10.20.48     YES NVRAM  up                    up
GigabitEthernet2       1.1.1.1         YES other  down                  down
GigabitEthernet3       unassigned      YES NVRAM  administratively down down
Loopback0              10.0.0.1        YES NVRAM  up                    up
Loopback10             unassigned      YES unset  up                    up
Loopback109            10.255.255.9    YES NVRAM  up                    up
VirtualPortGroup0      192.168.1.1     YES NVRAM  up                    up
cat8000v#

```

With the same code and the config below we can set the secondary IP address on the interface:

```
config_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet2</name>
      <enabled>true</enabled>

      <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
        <!-- Primary IP -->
        <address>
          <ip>1.1.1.1</ip>
          <netmask>255.255.255.0</netmask>
        </address>

        <!-- Secondary IP (2nd address on same interface) -->
        <address>
          <ip>2.2.2.2</ip>
          <netmask>255.255.255.0</netmask>
        </address>
      </ipv4>

    </interface>
  </interfaces>
</config>
"""

Output:
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:847272bd-10da-4b73-8cf0-a5183300f27b">
        <ok/>
</rpc-reply>

and on the router:
cat8000v#
*Jan 31 11:31:35.734: %DMI-5-AUTH_PASSED: R0/0: dmiauthd: User 'developer' authenticated successfully from 192.168.254.11:52608  for netconf over ssh. External groups: PRIV15
*Jan 31 11:31:37.484: %SYS-5-CONFIG_P: Configured programmatically by process iosp_dmiauthd_conn_100001_vty_100001 from console as developer on vty4294966926
*Jan 31 11:31:37.476: %DMI-5-CONFIG_I: R0/0: dmiauthd: Configured from NETCONF/RESTCONF by developer, transaction-id 37
cat8000v#
cat8000v#sh run int GigabitEthernet2
Building configuration...

Current configuration : 161 bytes
!
interface GigabitEthernet2
 description Network Interface
 ip address 2.2.2.2 255.255.255.0 secondary
 ip address 1.1.1.1 255.255.255.0
 negotiation auto
end

cat8000v#

```

If we want to delete the secodary IP address we can use the operation in xml code:

```
config_payload = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet2</name>
      <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
        <address nc:operation="delete"
                 xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
          <ip>2.2.2.2</ip>
          <netmask>255.255.255.0</netmask>
        </address>
      </ipv4>
    </interface>
  </interfaces>
</config>
"""


```

We can also get the Data from the user, for example to creating a new loop back, we can use input function and save the Data then with format method insert them in the xml string.

```

# ---- Ask user for values ----
loop_num = input("Which Loopback number to add? (e.g. 10): ").strip()
desc = input("Description (optional): ").strip()
ip_addr = input("IPv4 address (e.g. 10.10.10.10): ").strip()
mask = input("Netmask (e.g. 255.255.255.255): ").strip()


# XML template with placeholders (similar to your screenshot)
netconf_interface_template = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>{name}</name>

      <!-- REQUIRED for new interfaces -->
      <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
        ianaift:softwareLoopback
      </type>

      <description>{desc}</description>
      <enabled>true</enabled>

      <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
        <address>
          <ip>{ip}</ip>
          <netmask>{mask}</netmask>
        </address>
      </ipv4>
    </interface>
  </interfaces>
</config>
"""

# Build the final XML payload
payload = netconf_interface_template.format(
    name=f"Loopback{loop_num}",
    desc=desc,
    enabled="true",
    ip=ip_addr,
    mask=mask
)

```
```
Output:

Which Loopback number to add? (e.g. 10): 11
Description (optional): 11
IPv4 address (e.g. 10.10.10.10): 11.11.11.11
Netmask (e.g. 255.255.255.255): 255.255.255.0
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:0d1140cd-3456-4ad7-b2f4-59dfcb96dd72">
        <ok/>
</rpc-reply>


*Jan 31 12:00:05.129: %DMI-5-AUTH_PASSED: R0/0: dmiauthd: User 'developer' authenticated successfully from 192.168.254.11:53103  for netconf over ssh. External groups: PRIV15
*Jan 31 12:00:07.465: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback11, changed state to up
*Jan 31 12:00:07.497: %SYS-5-CONFIG_P: Configured programmatically by process iosp_dmiauthd_conn_100001_vty_100001 from console as developer on vty4294966926
*Jan 31 12:00:07.484: %DMI-5-CONFIG_I: R0/0: dmiauthd: Configured from NETCONF/RESTCONF by developer, transaction-id 45
cat8000v#
cat8000v#
cat8000v#sh ip int brie
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       10.10.20.48     YES NVRAM  up                    up
GigabitEthernet2       1.1.1.1         YES other  up                    up
GigabitEthernet3       unassigned      YES NVRAM  administratively down down
Loopback0              10.0.0.1        YES NVRAM  up                    up
Loopback10             unassigned      YES unset  up                    up
Loopback11             11.11.11.11     YES other  up                    up
Loopback109            10.255.255.9    YES NVRAM  up                    up



```

With shh on port 830 we can sent/receive the xml config file to the device.

```
ssh -s developer@10.10.20.48 -p 830 netconf
after 
]]>]]> 
we can paste the xml string.

<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <edit-config>
    <target>
      <running/>
    </target>
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback11</name>

          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            ianaift:softwareLoopback
          </type>

          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>22.22.22.22</ip>
              <netmask>255.255.255.255</netmask>
            </address>
          </ipv4>

        </interface>
      </interfaces>
    </config>
  </edit-config>
</rpc>
]]>]]>

```
