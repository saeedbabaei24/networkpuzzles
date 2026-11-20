---
wordpress_id: 589
title: "Creating Extranets and Access to Shared Services"
date: "2026-03-27T14:24:12"
url: "https://networkpuzzles.com/2026/03/27/creating-extranets-and-access-to-shared-services/"
---

In enterprise WAN environments, not every network segment should have unrestricted access to every other segment. However, many isolated segments still need access to a small set of **shared services**, such as DNS, Active Directory, RADIUS, monitoring systems, or internal application platforms.

our Senario:

* **VPN 10**
* **VPN 20**
* **VPN 30 = Shared Services**

your goal is:

* VPN 10 can reach services in VPN 30
* VPN 20 can reach services in VPN 30
* VPN 10 and VPN 20 cannot reach each other

For a **shared services VPN**:

* the **consumer VPNs** import the **shared service routes**
* the **shared services VPN** imports the **consumer routes** only if services need to initiate or reply to them
* the **consumer VPNs should not import each other’s routes**

We should make a Topology policy and export the routes to other vpns:

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-66.png?resize=1896%2C602&ssl=1)

**BUT** if we export **all routes of VPN 30** back to both VPN 10 and VPN 20 **without filtering**, and VPN 30 learns routes from both, then we can accidentally create **transit behavior**.

Meaning:

* VPN 10 routes go into VPN 30
* VPN 20 routes go into VPN 30
* then VPN 30 may export learned routes back out

And suddenly:

VPN 10 may learn VPN 20 or VPN 20 may learn VPN 10

And that is exactly what we **do not want**.

We can solve this problem with adding an atribute from Shared service vpn during exporting, so that only shared service network be exported to other vpns.

Here I use Prefix-list for that:

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-67.png?resize=1870%2C592&ssl=1)

And the policy should be applied in inbound direction of vsmart:

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-68.png?resize=1898%2C652&ssl=1)
```
viptela-policy:policy
 control-policy Shared-Services
    sequence 1
     match route
      vpn-list vpn-stores
      prefix-list _AnyIpv4PrefixList
     !
     action accept
      export-to vpn-list vpn30
     !
    !
    sequence 11
     match route
      vpn-list vpn30
      prefix-list Shared-Services-Prefix
     !
     action accept
      export-to vpn-list vpn-stores
     !
    !
    sequence 21
     match tloc
     !
     action accept
     !
    !
  default-action accept
 !
 lists
  prefix-list Shared-Services-Prefix
   ip-prefix 172.21.21.0/24 
  !
  site-list Hub-list
   site-id 100 
  !
  vpn-list vpn-stores
   vpn 10 
   vpn 20 
  !
  vpn-list vpn30
   vpn 30 
  !
  prefix-list _AnyIpv4PrefixList
   ip-prefix 0.0.0.0/0 le 32 
  !
 !
!
apply-policy
 site-list Hub-list
  control-policy Shared-Services in
```
