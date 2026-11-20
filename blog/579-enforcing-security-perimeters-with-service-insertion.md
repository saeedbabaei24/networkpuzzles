---
wordpress_id: 579
title: "Enforcing Security Perimeters with Service Insertion"
date: "2026-03-27T11:04:47"
url: "https://networkpuzzles.com/2026/03/27/enforcing-security-perimeters-with-service-insertion/"
---

In modern enterprise WANs, not all traffic should go directly from a branch to the internet or to internal applications without inspection. Even in an SD-WAN architecture, organizations often need to enforce **security perimeters** by steering selected traffic through centralized security services such as firewalls, IDS/IPS, secure web gateways, or traffic inspection platforms.

Cisco SD-WAN provides this capability through **Service Insertion**, which allows the network to redirect traffic toward a specific security device or service path before it reaches its final destination.

Service Insertion in Cisco SD-WAN is a method of **redirecting selected traffic** to a designated service node before forwarding it to the final destination.

That service node can be:

* a **firewall**
* an **IDS/IPS**
* a **secure web gateway**
* a **proxy**
* or another **security appliance**

On the edge device which is providing the service (here DC) we should configure the service in feature template of that vpn:

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-64.png?resize=1891%2C929&ssl=1)

We have 2 options here:

**IP = the service is reached via a next-hop IP**

**Interface = the service is directly connected to a specific interface**

We can use tracking so the SD-WAN edge knows whether the firewall is reachable. That way if the firewall dies, the service can be considered unavailable.

We can also use tracking so the SD-WAN edge knows whether the firewall is reachable.

That way if the firewall dies, the service can be considered unavailable.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-65.png?resize=1890%2C867&ssl=1)
```
viptela-policy:policy
 control-policy Fw-Service

  sequence 1
   match route
    site-list Spokes-list
    prefix-list _AnyIpv4PrefixList
   !
   action accept
    set
     service Fw
   !
  !
 !
 default-action reject
!

lists
 site-list Spokes-list
  site-id 1001-1003
 !

 prefix-list _AnyIpv4PrefixList
  ip-prefix 0.0.0.0/0 le 32
 !
!
!

apply-policy
 site-list Spokes-list
  control-policy Fw-Service out

```
