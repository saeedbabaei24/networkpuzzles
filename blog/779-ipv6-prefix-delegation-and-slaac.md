---
wordpress_id: 779
title: "IPv6 Prefix Delegation and SLAAC"
date: "2026-05-11T09:31:45"
url: "https://networkpuzzles.com/2026/05/11/ipv6-prefix-delegation-and-slaac/"
---

One of the most elegant features of IPv6 is the ability to dynamically allocate entire prefixes to downstream routers using **DHCPv6 Prefix Delegation (PD)**.

Instead of manually assigning IPv6 subnets to every remote site, an ISP can delegate a larger block to a customer edge router, which can then automatically create internal LAN subnets for its downstream networks.

In this lab, I built a simple topology to demonstrate how DHCPv6-PD works together with SLAAC.

###### Topology

```
        R1 (ISP / DHCPv6-PD Server)
                    |
                    |
            Delegated Prefix
                    |
                R2 (CE Router)
                 /          \
               R3            R4
```

* **R1** acts as the ISP router and DHCPv6-PD server.
* **R2** is the customer edge router receiving a delegated prefix.
* **R3** and **R4** are internal downstream routers using SLAAC.

###### The Design Requirement

The company connected behind R2 plans to have up to 16 internal LANs in the future.

Since SLAAC requires every LAN to use a `/64` subnet, R2 needs enough address space to create at least sixteen `/64` networks.

This is where prefix delegation becomes useful.

###### Prefix Size Calculation

To create 16 subnets, we need 4 additional bits:

```

2^4 = 16
```


Because each LAN must remain a `/64`:

```

/64 - 4 bits = /60
```


So the ISP should delegate a `/60` prefix to R2.

A `/60` contains exactly sixteen `/64` subnets.

###### DHCPv6 Prefix Delegation on R1

R1 creates a local delegation pool:

```

ipv6 local pool DELEGATE 2001:db8:500:100::/56 60
```


This means:

* The ISP owns the `/56`
* Each customer receives a `/60`

Then the DHCPv6 pool is configured:

```

ipv6 dhcp pool ISP prefix-delegation pool DELEGATE lifetime infinite infinite
```


And applied toward the CE router:

```

interface g0/0 ipv6 dhcp server ISP
```


###### Prefix Delegation on R2

R2 requests a delegated prefix dynamically from R1:

```

interface g0/0 ipv6 enable ipv6 address autoconfig default ipv6 dhcp client pd CUSTOMER-PD
```


After the DHCPv6 exchange, R2 may receive something like:

```

2001:db8:500:100::/60
```


At this point, R2 owns sixteen separate `/64` networks.

###### Internal Subnet Allocation

Inside the delegated `/60`, R2 can now create multiple LAN subnets:

```

2001:db8:500:100::/642001:db8:500:101::/642001:db8:500:102::/64...2001:db8:500:10F::/64
```


For this lab:

* R4 uses the first non-zero subnet
* R3 uses the second non-zero subnet

###### R4 Configuration

R4 should use subnet:

```

2001:db8:500:101::/64
```


R2 configuration:

```

interface g0/2 ipv6 address CUSTOMER-PD ::1:0:0:0:88/64
```


Resulting address:

```

2001:db8:500:101::88/64
```


###### R3 Configuration

R3 should use subnet:

```

2001:db8:500:102::/64
```


R2 configuration:

```

interface g0/1 ipv6 address CUSTOMER-PD ::2:0:0:0:77/64
```


Resulting address:

```

2001:db8:500:102::77/64
```


###### SLAAC on R3 and R4

Both downstream routers are configured using SLAAC only:

```

interface g0/0 ipv6 address autoconfig default
```


Using Router Advertisements (RA), both routers automatically learn:

* Their IPv6 address
* Prefix information
* Default gateway

No static addressing is required.

###### Final Result

R4 automatically receives an address from:

```

2001:db8:500:101::/64
```


R3 automatically receives an address from:

```

2001:db8:500:102::/64
```


And both install their default route dynamically using the link-local address of R2.

###### Why This Design Matters

This is exactly how many ISPs deliver IPv6 connectivity today.

Instead of assigning a single subnet to customers, providers delegate an entire prefix, allowing customers to build scalable internal IPv6 networks without manual subnet assignment.

The combination of:

* DHCPv6 Prefix Delegation
* Router Advertisements
* SLAAC

creates a fully dynamic and highly scalable IPv6 deployment model.

###### Interesting IPv6 Detail: Link-Local Addresses

One interesting IPv6 behavior is that the same link-local address can exist on multiple interfaces of the same router.

Example:

```

interface g0/1 ipv6 address FE80::1 link-localinterface g0/2 ipv6 address FE80::1 link-local
```


This is completely valid because link-local addresses only have local-link scope and are never routed.

That is also why IPv6 often requires specifying the outgoing interface when using link-local addresses:

```

ping FE80::1 source g0/1
```


or:

```

ipv6 route ::/0 FE80::1 g0/1
```


Without the interface, the router cannot determine which local link should be used.

IPv6 Prefix Delegation is one of the cleanest examples of how IPv6 was designed for automation and scalability from the beginning.

Instead of manually managing subnet assignments, routers can dynamically receive large address blocks and automatically distribute them internally using SLAAC and Router Advertisements.

For enterprise networks, ISPs, and large-scale deployments, DHCPv6-PD is an essential technology to understand.
