---
wordpress_id: 797
title: "DMVPN Single Hub Single Cloud: Design Behavior Across Phase 1, 2 and 3"
date: "2026-05-14T12:27:51"
url: "https://networkpuzzles.com/2026/05/14/dmvpn-single-hub-single-cloud-design-behavior-across-phase-1-2-and-3/"
---

DMVPN is often introduced as a configuration topic, but in real networks the more important question is design behavior. The same DMVPN topology can behave very differently depending on the phase and the overlay routing protocol.

In this post, we look at the simplest DMVPN topology: **Single Hub, Single Cloud**.

This design contains one hub router, multiple spokes, and one DMVPN cloud. It is simple, easy to understand, and a good starting point before moving to dual-cloud and dual-hub designs

##### Topology Overview

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/05/image.png?resize=1024%2C904&ssl=1)

In a Single Hub, Single Cloud design, all spokes register to one hub/NHS. The hub acts as the central point for control-plane communication, routing adjacency, and in some phases also forwarding.

This model is commonly used in labs, small WAN environments, or as the foundation for understanding larger DMVPN architectures.

The main limitation is obvious: the hub is a single point of failure. However, from a learning and design perspective, this topology is very useful because it clearly shows the difference between DMVPN Phase 1, Phase 2, and Phase 3.

##### DMVPN Phase 1

In Phase 1, the design is purely hub-and-spoke.

Spoke-to-spoke traffic always follows this path:

```

Spoke → Hub → Spoke
```



![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/05/image-2.png?resize=657%2C757&ssl=1)

There is no direct spoke-to-spoke tunnel.

From a design perspective, Phase 1 is simple and predictable. The spoke routers do not need to know detailed routes for every other spoke. A default route from the hub to the spokes is often enough.

###### EIGRP in Phase 1

With EIGRP, the hub learns spoke routes through the tunnel interface. Because of split horizon, the hub does not advertise routes learned from one spoke back out of the same tunnel interface to another spoke.

There are two possible design choices:

```

no ip split-horizon eigrp 100
```


or a better Phase 1 design:

```

ip summary-address eigrp 100 0.0.0.0 0.0.0.0
```


For Phase 1, sending only a default route from the hub to the spokes is often cleaner. The spokes do not need a full routing table because all traffic goes through the hub anyway

###### OSPF in Phase 1

OSPF over DMVPN requires special attention because OSPF network types influence:

```

Neighbor formationDR/BDR electionNext-hop behaviorSummarization options
```


In Phase 1, next-hop preservation is not a major problem because direct spoke-to-spoke forwarding does not exist.

With OSPF broadcast network type, the hub must become the DR. Spokes should be prevented from becoming DR or BDR:

```

ip ospf priority 0
```


The reason is simple: spokes only form full adjacency with the hub. If a spoke becomes DR, the OSPF topology can break.

For a cleaner Phase 1 design, point-to-multipoint on the hub and point-to-point on the spokes can also be used:

Hub:

```

ip ospf network point-to-multipointip ospf hello-interval 10
```


Spokes:

```

ip ospf network point-to-point
```


This avoids DR/BDR election and changes the next-hop to the hub.

###### BGP in Phase 1

With iBGP, the hub should act as a Route Reflector. Otherwise, routes learned from one iBGP spoke will not be advertised to another iBGP spoke.

Hub:

```

neighbor spokes peer-groupneighbor spokes remote-as 100bgp listen range 100.1.1.0/24 peer-group spokesneighbor spokes route-reflector-client
```


For Phase 1, the best design is usually to advertise only a default route from the hub to the spokes and suppress more-specific spoke routes.

This keeps the spoke routing table small and matches the forwarding behavior of Phase 1.

##### DMVPN Phase 2

Phase 2 introduces direct spoke-to-spoke tunnels.

The important requirement is:

```

Spokes must have specific routes with the real remote spoke as the next-hop.
```


For example, on R2:

```

36.1.1.0/24 via 100.1.1.3
```


not:

```

36.1.1.0/24 via 100.1.1.1
```


If the next-hop is the hub, traffic will continue to go through the hub. If the next-hop is the remote spoke, NHRP resolution can happen and a direct spoke-to-spoke tunnel can be built.

###### EIGRP in Phase 2

On the hub, two commands are important:

```

no ip split-horizon eigrp 100no ip next-hop-self eigrp 100
```


The first command allows the hub to advertise routes learned from one spoke to another spoke.

The second command preserves the real spoke next-hop.

This is what makes EIGRP work correctly with Phase 2.

###### OSPF in Phase 2

For OSPF Phase 2, broadcast network type is usually required because it preserves the next-hop.

The hub must be DR:

```

ip ospf network broadcast
```


On the spokes:

```

ip ospf network broadcastip ospf priority 0
```


This allows spoke routes to point to the real remote spoke tunnel IP, which triggers NHRP resolution.

###### BGP in Phase 2

BGP works well in Phase 2 when the next-hop is preserved.

With iBGP, the hub as Route Reflector naturally preserves the next-hop. This means a spoke can learn another spoke’s prefix with the remote spoke as the next-hop.

With eBGP, third-party next-hop behavior may also preserve the spoke next-hop when all tunnel addresses are in the same subnet.

That behavior is useful in Phase 2 because direct spoke-to-spoke tunnels require the real spoke next-hop.

##### DMVPN Phase 3

hase 3 is the most scalable DMVPN model.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/05/image-3.png?resize=648%2C714&ssl=1)

The design goal changes:

```

Phase 2: Spokes know all routes and go direct.Phase 3: Spokes know minimal routes and NHRP optimizes forwarding.
```


In Phase 3, spokes can receive only a default route from the hub:

```

0.0.0.0/0 via Hub
```


When a spoke sends traffic to another spoke, the first packet goes through the hub. The hub detects that traffic enters and exits the same DMVPN cloud and sends an NHRP redirect.

Then the spoke installs an NHRP shortcut route and builds a direct tunnel.

Hub:

```

ip nhrp redirect
```


Spokes:

```

ip nhrp shortcut
```


This is the key idea of Phase 3:

```

Routing points to the hub.Forwarding becomes direct after NHRP optimization.
```


###### OSPF Limitation in Phase 3

OSPF is not ideal for a fully optimized Phase 3 design.

The reason is OSPF summarization behavior. Inside a single OSPF area, routers need a consistent LSDB. The hub cannot simply advertise only a default route and suppress all specific spoke routes in the same way EIGRP or BGP can.

OSPF broadcast network type can build direct spoke-to-spoke tunnels, but that behavior is closer to Phase 2 because the spoke already has the real remote spoke as next-hop.

True Phase 3 behavior should be triggered by NHRP redirect from the hub, not by the spoke resolving a remote next-hop from the routing table.

This is why OSPF can work, but it is not the best protocol for an optimized Phase 3 design.
