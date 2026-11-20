---
wordpress_id: 678
title: "GLBP Weighting"
date: "2026-03-29T22:53:08"
url: "https://networkpuzzles.com/2026/03/29/glbp-weighting/"
---

When we talk about First Hop Redundancy Protocols, many engineers immediately think about **HSRP** or **VRRP**. These protocols provide gateway redundancy, but they do not natively offer load balancing across multiple active gateways in the same way as **GLBP**. **GLBP** is a Cisco proprietary protocol that allows multiple routers to share the role of forwarding traffic for hosts in the same subnet while still presenting a single virtual IP address as the default gateway.

The **AVG** is responsible for answering ARP requests for the virtual IP address.  
It assigns different virtual MAC addresses to different hosts, which allows load balancing.

The **AVF** is the router that actually forwards packets for one of the virtual MAC addresses.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-86.png?resize=1000%2C677&ssl=1)

On router **R1**, we want to configure GLBP so that:

* **Serial1/0** is tracked using **line-protocol**
* The router starts with a **GLBP weight of 120**
* If **Loopback0** goes down, the weight is reduced by **50**
* If the weight falls **below 80**, R1 must stop acting as an **AVF**
* R1 can become AVF again only when the weight rises back to at least **90**

A router may still be reachable on the local VLAN, so from the hosts’ point of view it looks available. But if an important path or service has failed, continuing to use that router as a forwarder can black-hole traffic.

With **GLBP weighting**, the router can dynamically decide whether it should still participate in forwarding.

This is better than only relying on interface up/down state of the LAN-facing interface.

GLBP Weighting Logic:

We start with **Initial weight = 120**, If Loopback0 fails: decrement = **50** so new weight is = **70**. then compare that with the thresholds:

**Lower threshold = 80**, **Upper threshold = 90** So:

* **120** → normal participation
* **70** → below lower threshold, Dalton gives up AVF role
* when Loopback0 comes back, weight returns to **120**
* because **120 is above 90**, R1 is allowed to become AVF again

on R1:

```
track 1 interface Loopback1 line-protocol
interface FastEthernet0/0
ip address 192.168.123.1 255.255.255.0
glbp 1 ip 192.168.123.100
glbp 1 weighting 120 lower 80 upper 90
glbp 1 weighting track 1 decrement 50
```

on R2:

```
interface FastEthernet0/0
ip address 192.168.123.2 255.255.255.0
glbp 1 ip 192.168.123.100
```

On R1 I shut down the loopback1:

```
R1(config)#int loopback 1
R1(config-if)#sh
*Mar  1 00:08:44.427: %TRACKING-5-STATE: 1 interface Lo1 line-protocol Up->Down
*Mar  1 00:08:44.427: GLBP: Fa0/0 1 Track 1 object changed, state Up -> Down
*Mar  1 00:08:44.431: GLBP: Fa0/0 1 Weighting 120 -> 70
*Mar  1 00:08:46.427: %LINK-5-CHANGED: Interface Loopback1, changed state to administratively down
*Mar  1 00:08:47.427: %LINEPROTO-5-UPDOWN: Line protocol on Interface Loopback1, changed state to down
*Mar  1 00:09:15.667: GLBP: Fa0/0 1.1 Active: i/Hello rcvd from higher pri Active router (135/192.168.123.2)
*Mar  1 00:09:15.667: GLBP: Fa0/0 1.1 Active -> Listen
*Mar  1 00:09:15.667: %GLBP-6-FWDSTATECHANGE: FastEthernet0/0 Grp 1 Fwd 1 state Active -> Listen
*Mar  1 00:09:15.671: GLBP: Fa0/0 API MAC address update

```

In this test, **R1** starts with a GLBP weighting of **120**.  
A tracked object is associated with **Loopback1**. When the loopback goes down, GLBP decreases the weighting by **50**, which results in a new weighting of **70**.

Because the configured **lower threshold is 80**, R1 is no longer allowed to stay **AVF** and gives up its forwarder role. When the weighting later rises above the **upper threshold of 90**, it can become AVF again. This is how GLBP uses weighting and tracking to make forwarding decisions.

Here, **R1 is still the AVG**, which is why the group state says **Active**.  
But R1 is **no longer an AVF**, which is why its forwarder state changed from **Active** to **Listen**.

on R2:  


```
R2#sh glbp
FastEthernet0/0 - Group 1
  State is Standby
    1 state change, last state change 00:05:56
  Virtual IP address is 192.168.123.100
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 0.688 secs
  Redirect time 600 sec, forwarder time-out 14400 sec
  Preemption disabled
  Active is 192.168.123.1, priority 100 (expires in 8.504 sec)
  Standby is local
  Priority 100 (default)
  Weighting 100 (default 100), thresholds: lower 1, upper 100
  Load balancing: round-robin
  Group members:
    c401.3928.0000 (192.168.123.1)
    c402.819c.0000 (192.168.123.2) local
  There are 2 forwarders (2 active)
  Forwarder 1
    State is Active
      1 state change, last state change 00:01:18
    MAC address is 0007.b400.0101 (learnt)
    Owner ID is c401.3928.0000
    Time to live: 14398.492 sec (maximum 14400 sec)
    Preemption enabled, min delay 30 sec
    Active is local, weighting 100
  Forwarder 2
    State is Active
      1 state change, last state change 00:06:02
    MAC address is 0007.b400.0102 (default)
    Owner ID is c402.819c.0000
    Preemption enabled, min delay 30 sec
    Active is local, weighting 100

```

There are 2 forwarders (2 active), It means that **R2 is currently forwarding for both GLBP virtual MAC addresses**. In other word, **R1 is still alive and still AVG**, but **R1 is no longer forwarding traffic** and **R2 has taken over all forwarding duties**.

So the gateway remains stable for the hosts, but the actual forwarding function has moved to the healthy router.

GLBP Load Balancing Methods:

```
R1(config-if)#glbp 1 load-balancing ?
  host-dependent  Load balance equally, source MAC determines forwarder choice
  round-robin     Load balance equally using each forwarder in turn
  weighted        Load balance in proportion to forwarder weighting
```

Each one changes **how the AVG answers ARP requests** for the virtual gateway IP. Hosts all use the **same virtual IP**, But GLBP can answer ARP with **different virtual MAC addresses** and Each virtual MAC belongs to a **different AVF**.

GLBP does **not** load-balance every packet individually like ECMP hashing on a router. Instead, it usually balances **hosts** by giving different hosts different virtual MACs. So each host generally sticks to the same AVF until its ARP entry changes.

Weighted load balancing allows GLBP to distribute hosts proportionally based on AVF weights. This is different from GLBP weighting thresholds, which determine whether a router is allowed to act as a forwarder at all. In other words, weighting thresholds control participation, while weighted load balancing controls traffic share.

GLBP supports three different host distribution methods:

* **round-robin** → assigns hosts equally by rotating between forwarders
* **host-dependent** → keeps the same host mapped to the same forwarder based on source MAC
* **weighted** → distributes hosts based on forwarder weighting

These options define how the **AVG replies to ARP requests** for the virtual IP. They do **not** change the virtual IP itself, but they determine **which virtual MAC address** a host receives and therefore **which AVF forwards its traffic**.
