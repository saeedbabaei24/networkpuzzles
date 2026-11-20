---
wordpress_id: 563
title: "Cisco SD-WAN TLOC Extension"
date: "2026-03-25T21:41:51"
url: "https://networkpuzzles.com/2026/03/25/cisco-sd-wan-tloc-extension/"
---

In this lab, I demonstrate how **TLOC Extension** works in Cisco SD-WAN using a simple branch topology.

At **Site3**, I have two WAN Edge routers:

* **cEdge01** → connected to **Internet**
* **cEdge02** → connected to **MPLS**

By default, each WAN Edge can only use its **own transport interface**.  
However, in many real-world deployments, we want both routers to **share available transports**.

TLOC Extension allows a WAN Edge router to **use a transport (TLOC)** that is physically connected to another WAN Edge router in the same site.

The two routers are connected via a **LAN link (usually VPN 0 or transport extension interface)**.

Then:

* The router with the transport advertises its **TLOC**
* The other router uses that TLOC via the **extension link**

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-63.png?resize=1450%2C1027&ssl=1)

**WAN Edge 1**

* **Gi0/0** → **Internet (real/directly connected)**
* **Gi0/1** → **TLOC Extension of Gi0/0**
* **Gi0/2** → **Normal MPLS**

**WAN Edge 2**

* **Gi0/0** → **MPLS (real/directly connected)**
* **Gi0/1** → **TLOC Extension of Gi0/0**
* **Gi0/2** → **Normal Internet**

###### Configure TLOC Extension on interface

**WAN Edge 1 Configuration:**

Gi0/1 → Extension of Gi0/0 (Internet extension toward Edge2)

```
vpn 0
 interface GigabitEthernet0/1
  ip address 172.16.12.1/30
  no shutdown
  tunnel-interface
   encapsulation ipsec
   color biz-internet
   tloc-extension GigabitEthernet0/0
```

Gi0/2 → Normal MPLS transport:

```
vpn 0
 interface GigabitEthernet0/0
  ip address 192.168.20.2/30
  no shutdown
  tunnel-interface
   encapsulation ipsec
   color mpls
   no allow-service all
   allow-service icmp
   allow-service ssh
```

**WAN Edge 2 Configuration:**

Gi0/1 → Extension of Gi0/0 (MPLS extension toward Edge1)

```
vpn 0
 interface GigabitEthernet0/1
  ip address 172.16.12.2/30
  no shutdown
  tunnel-interface
   encapsulation ipsec
   color mpls
   tloc-extension GigabitEthernet0/0
```

Gi0/2 → Normal Internet transport:

```
vpn 0
interface GigabitEthernet0/2
ip address dhcp
no shutdown
tunnel-interface
encapsulation ipsec
color biz-internet
no allow-service all
allow-service dhcp
allow-service dns
allow-service icmp
allow-service https
allow-service ssh
```

**The router that is physically connected to the Internet must handle NAT for both itself and the neighboring WAN Edge router.**

```
vpn 0
 interface GigabitEthernet0/0
  ip nat outside

vpn 10
 interface GigabitEthernet0/2
  ip nat inside

ip nat inside source list NAT_ACL interface GigabitEthernet0/0 overload

```

The subnet used for the TLOC Extension link must be reachable via the MPLS transport, otherwise the extended TLOC cannot be properly resolved.

We must ensure that the subnet used between the two WAN Edges is: **Advertised into the MPLS network**, or **Reachable via routing (static or dynamic**).
