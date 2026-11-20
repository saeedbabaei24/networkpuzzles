---
wordpress_id: 849
title: "DMVPN Dual Hub Dual Cloud – Full Redundancy Design"
date: "2026-05-15T11:00:00"
url: "https://networkpuzzles.com/2026/05/15/dmvpn-dual-hub-dual-cloud-full-redundancy-design/"
---

When enterprises start scaling DMVPN deployments, a single hub or a single transport quickly becomes a limitation.

The Dual Hub + Dual cloud design provides:

* Hub redundancy
* Transport redundancy
* MPLS primary path
* Internet backup path
* Direct spoke-to-spoke tunnels
* Automatic failover

while still keeping the overlay scalable with DMVPN Phase 3.

##### Topology Overview

We have two independent DMVPN clouds:

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/05/image-8.png?resize=976%2C1119&ssl=1)
###### MPLS Cloud

```

Hub: R1Tunnel: Tunnel100Subnet: 100.1.1.0/24Transport: MPLS
```


###### Internet Cloud

```

Hub: R8Tunnel: Tunnel200Subnet: 200.1.1.0/24Transport: Internet
```


Each spoke connects to both hubs:

```

R2 → R1 over MPLSR2 → R8 over InternetR3 → R1 over MPLSR3 → R8 over Internet
```


This creates:

```

Dual-homed spokes
```


The goal is simple:

```

MPLS = PrimaryInternet = Backup
```


But we also want:

* Hub redundancy
* Direct spoke-to-spoke communication
* Fast failover
* Scalable routing behavior

This is where DMVPN Phase 3 becomes extremely useful.

###### Main Site Routing Challenge

At the main site we have:

```

R1, R8, SW1
```


connected through VLAN 118.

A major issue in redundant WAN designs is:

```

Asymmetric routing
```


Example:

```

Traffic arrives through R1 but returns through R8
```


This may cause problems with:

* Stateful firewalls
* QoS policies
* Monitoring systems
* Traffic engineering

The design must keep traffic symmetric whenever possible.

The solution is surprisingly clean.

**R1 (Primary MPLS Hub)**

R1 advertises:

```

Specific remote-site routes
```


Example:

```

24.1.1.0/2436.1.1.0/24
```


**R8 (Backup Internet Hub)**

R8 advertises only:

```

0.0.0.0/0
```


If R1 fails:

Only R8’s default route remains

Specific routes disappear

##### Why DMVPN Phase 3 Matters Here

At larger scale, another problem appears, and that is Routing table growth.

If every spoke must learn every remote prefix, scalability suffers.

Phase 3 changes the model completely.

Instead of permanently maintaining spoke-to-spoke routing knowledge:

* spokes mainly use summarized/default routes
* direct tunnels are created dynamically only when needed

Many engineers think Phase 3 is mainly about Spoke-to-Spoke Tunnels, but the more important idea is actually is Control-plane simplification.

##### The Design Tradeoff

Dual Hub Dual Cloud gives enormous flexibility:

* Hub redundancy
* Transport redundancy
* Dynamic shortcuts
* Multiple failover paths

But it also increases:

* routing complexity
* convergence complexity
* troubleshooting complexity
* forwarding ambiguity

This is the classic WAN engineering tradeoff: more resiliency usually means more control-plane complexity.

Architectures like SD-WAN became popular partly because they abstracted many of these problems.

Traditional DMVPN requires the engineer to think carefully about:

* route preference
* next-hop behavior
* overlay/underlay interaction
* asymmetry
* shortcut creation
* convergence behavior

In SD-WAN, much of that logic becomes centralized policy.

But understanding DMVPN designs is still extremely valuable.

Because these designs teach something deeper and that is how routing behavior actully shapes WAN architecture.

The most interesting part of Dual Hub Dual Cloud is not the tunnels. It is the realization that, Redundancy is easy, but predictable forwarding during failure is the hard part.
