---
wordpress_id: 818
title: "DMVPN Single Hub Dual Cloud: Why Redundancy Does Not Always Mean Optimal Failover"
date: "2026-05-14T19:34:40"
url: "https://networkpuzzles.com/2026/05/14/dmvpn-single-hub-dual-cloud-why-redundancy-does-not-always-mean-optimal-failover/"
---

DMVPN is often designed to provide transport flexibility. A company may have an MPLS WAN as the primary transport and an Internet circuit as a backup path. At first glance, the design looks simple: build one DMVPN cloud over MPLS and another DMVPN cloud over the Internet.

This design is usually called **Single Hub, Dual Cloud**.

It provides redundancy, but it also introduces important design challenges. The most important lesson is this:

```

Two available paths do not automatically mean optimal failover.
```


In a dual-cloud design, the routing protocol, next-hop behavior, and NHRP operation must all align correctly

##### Design Goal

In this topology, The Corporation has one main site and two remote sites.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/05/image-4.png?resize=1336%2C981&ssl=1)

|  | DMVPN Tunnel | Role |
| --- | --- | --- |
| MPLS | Tunnel100 | Primary |
| Internet / ISP-1 | Tunnel200 | Backup |

The goal is:

```

Use MPLS as the primary path.Use Internet as the backup path.Maintain spoke-to-spoke reachability when possible.
```


###### Topology Concept

Each transport has its own DMVPN cloud.

On the hub:

```

Tunnel100 → MPLS cloudTunnel200 → Internet cloud
```


On the spokes:

```

Tunnel100 → MPLS-facing sourceTunnel200 → Internet-facing source
```


This means Tunnel100 and Tunnel200 are completely separate overlay networks.

For example:

```

Tunnel100: 100.1.1.0/24Tunnel200: 200.1.1.0/24
```


The hub learns spokes dynamically using NHRP:

```

ip nhrp map multicast dynamic
```


The spokes are configured with the hub as their NHS:

```

ip nhrp nhs <hub-tunnel-ip>
```


This provides redundancy, but the important question is:

How does the routing protocol behave when one transport fails?

##### DMVPN Phase 1 Behavior

Phase 1 is the simplest case.

In Phase 1, spoke-to-spoke traffic always goes through the hub:

```

Spoke → Hub → Spoke
```


Because direct spoke-to-spoke tunnels do not exist, Phase 1 works reasonably well with a dual-cloud design.

The main design task is to prefer MPLS over Internet.

###### OSPF in Phase 1

With OSPF, both DMVPN tunnels can form adjacencies with the hub.

If OSPF broadcast network type is used, the hub must become the DR and the spokes should never become DR or BDR:

```

ip ospf network broadcastip ospf priority 0
```


By default, both GRE tunnel interfaces may have the same OSPF cost. This can lead to ECMP:

```

Tunnel100 cost 1000Tunnel200 cost 1000
```


To prefer MPLS, reduce the OSPF cost on Tunnel100:

```

interface Tunnel100 ip ospf cost 500
```


A cleaner Phase 1 OSPF design is often:

```

Hub:    point-to-multipointSpokes: point-to-point
```


This avoids DR/BDR election and makes the next-hop point to the hub, which matches Phase 1 forwarding behavior.

###### EIGRP in Phase 1

With EIGRP, the hub can advertise only a default route to the spokes on both tunnels:

```

interface Tunnel100  ip summary-address eigrp 100 0.0.0.0 0.0.0.0interface Tunnel200  ip summary-address eigrp 100 0.0.0.0 0.0.0.0
```


If both tunnels have equal EIGRP metrics, the spokes may load-share across MPLS and Internet.

To prefer MPLS, tune the delay on Tunnel100:

```

interface Tunnel100 delay 500
```


In Phase 1, this is a clean design because the spokes do not need specific routes to each other.

###### BGP in Phase 1

With iBGP, the hub should act as a Route Reflector.

For dual cloud, it is better to use separate peer groups:

```

neighbor tunnel100 peer-groupneighbor tunnel200 peer-group
```


Dynamic neighbors can be accepted per cloud:

```

bgp listen range 100.1.1.0/24 peer-group tunnel100bgp listen range 200.1.1.0/24 peer-group tunnel200
```


The hub can advertise only a default route to the spokes and suppress more-specific routes.

To prefer MPLS, use a deterministic BGP attribute such as Local Preference:

```

route-map MPLS-PREFERRED permit 10  set local-preference 200
```


Do not rely on “lowest neighbor IP address” as the reason Tunnel100 is selected. That may work in the lab, but it is not a good design principle.

##### DMVPN Phase 2 Behavior

Phase 2 is more sensitive.

In Phase 2, spokes should be able to build direct spoke-to-spoke tunnels:

```

Spoke → Spoke
```


For this to work, the route on the spoke must point to the remote spoke tunnel IP.

Example on R2:

```

36.1.1.0/24 via 100.1.1.3
```


not:

```

36.1.1.0/24 via 100.1.1.1
```


This is the key requirement of Phase 2:

```

The real remote spoke next-hop must be preserved.
```


If the next-hop becomes the hub, NHRP resolution for the remote spoke does not happen and the traffic falls back to hub-and-spoke forwarding.

###### OSPF in Phase 2

OSPF broadcast network type works well in Phase 2 because it preserves the next-hop.

The hub should be the DR:

```

interface Tunnel100  ip ospf network broadcast interface Tunnel200  ip ospf network broadcast
```


On the spokes:

```

ip ospf priority 0
```


To prefer MPLS:

```

interface Tunnel100  ip ospf cost 500
```


OSPF handles the dual-cloud topology relatively well because it is a link-state protocol. It builds an LSDB and understands the topology through router and network LSAs.

If Tunnel100 fails on one spoke, OSPF can recalculate and use Tunnel200 with the correct next-hop on that cloud.

###### EIGRP in Phase 2

For EIGRP Phase 2, the hub needs two important commands on both tunnels:

```

no ip split-horizon eigrp 100no ip next-hop-self eigrp 100
```


This allows the hub to advertise spoke routes between spokes while preserving the original spoke next-hop.

In normal operation, this works:

```

36.1.1.0/24 via 100.1.1.3
```


However, dual-cloud failure scenarios can be problematic.

If Tunnel100 fails on R2 but R3 still uses Tunnel100, the hub may advertise routes between different tunnel subnets:

```

Tunnel100: 100.1.1.0/24Tunnel200: 200.1.1.0/24
```


In that case, the hub may set itself as the next-hop:

```

36.1.1.0/24 via 200.1.1.1
```


Connectivity may still work, but spoke-to-spoke optimization is lost.

In a dual-cloud failure scenario, the hub may still prefer routes learned through the primary cloud, even when a spoke has already failed over to the backup cloud.

###### BGP in Phase 2

With iBGP, the hub acts as a Route Reflector. In normal operation, next-hop preservation is useful:

```

36.1.1.0/24 via 100.1.1.3
```


This allows NHRP to build a direct spoke-to-spoke tunnel.

But during a failure, a spoke may receive a route over Tunnel200 with a next-hop that still belongs to Tunnel100:

```

Next-hop: 100.1.1.3
```


If that next-hop is no longer reachable, the BGP route becomes unusable.

With eBGP, behavior depends on next-hop processing. In normal operation, third-party next-hop behavior may help preserve the remote spoke next-hop when all tunnel addresses are in the same subnet.

But in a dual-cloud failure scenario, the hub may change the next-hop to itself when advertising between different tunnel subnets.

The result is:

```

Connectivity may survive,but Phase 2 spoke-to-spoke optimization may fail.
```


##### DMVPN Phase 3 Behavior

Phase 3 is designed for scale.

The goal is different from Phase 2:

```

Phase 2: Spokes know specific routes and go direct.Phase 3: Spokes know minimal routes, and NHRP optimizes forwarding.
```


The hub can advertise only a default route to the spokes.

The Phase 3 commands are:

On the hub:

```

ip nhrp redirect
```


On the spokes:

```

ip nhrp shortcut
```


The first packet goes through the hub:

```

Spoke → Hub → Spoke
```


Then the hub sends an NHRP redirect, and the spoke builds a shortcut route.

###### The Phase 3 Dual-Cloud Problem

In a dual-cloud design, Phase 3 has an important limitation.

NHRP redirect is triggered when the hub receives traffic on a tunnel and forwards it back out the same tunnel.

But during failure, traffic may enter the hub on one cloud and leave on another:

```

Input:  Tunnel200Output: Tunnel100
```


In that case, NHRP redirect may not be triggered.

The result is:

```

No redirectNo shortcutTraffic stays through the hub
```


This is one of the most important design lessons in Single Hub Dual Cloud DMVPN.

##### Design Recommendation

Single Hub Dual Cloud is a valid redundancy design, especially for Phase 1.

However, for Phase 2 and Phase 3, it can become operationally complex because each transport is a separate overlay cloud.

A cleaner design is often:

```

Single HubSingle DMVPN CloudTunnel source = LoopbackLoopbacks reachable over both MPLS and Internet
```


In this model, the underlay provides transport redundancy, while the overlay remains simple.

Instead of building two DMVPN clouds:

```

Tunnel100 over MPLSTunnel200 over Internet
```


you build one DMVPN cloud:

```

Tunnel100 sourced from Loopback
```


The loopback is reachable through both MPLS and Internet.

If MPLS fails, the underlay changes the path to the loopback. The DMVPN overlay stays up, and the routing protocol sees a more stable topology.

Single Hub Dual Cloud DMVPN provides transport redundancy, but it does not automatically provide clean failover or optimal spoke-to-spoke forwarding.

The key design lesson is:

```

Redundancy in the physical or transport layer does not always translate into optimal overlay behavior.
```


For Phase 1, dual cloud is usually simple and predictable.

For Phase 2, next-hop preservation becomes critical.

For Phase 3, NHRP redirect behavior becomes critical.

In larger environments, it is often better to solve transport redundancy in the underlay and keep the DMVPN overlay simple.

```

Solve redundancy in the underlay.Keep the overlay stable.
```


This separation usually leads to a cleaner, more scalable, and more predictable DMVPN design.
