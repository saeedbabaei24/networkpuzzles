---
wordpress_id: 714
title: "Proxy ARP"
date: "2026-04-05T20:08:31"
url: "https://networkpuzzles.com/2026/04/05/proxy-arp/"
---

When we design networks, we usually expect hosts to communicate with devices in other subnets through a **default gateway**. Each subnet is a separate broadcast domain, and ARP is only used for local communication.

But what happens if hosts are **misconfigured** and don’t have a proper default gateway? This is where **Proxy ARP** comes into play.

Proxy ARP is a feature where a router answers ARP requests **on behalf of another device**, making hosts believe the destination is directly reachable on the local network.

In this lab, we have two different subnets:

* 172.16.0.0 /16 (top side)
* 172.16.1.0 /24 (bottom side)

All hosts must communicate with each other **without changing IP addresses**.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/04/grafik.png?resize=2263%2C816&ssl=1)

Let’s say **PC 1 (172.16.0.1)** wants to reach **PC 3 (172.16.1.4)**.

From PC1’s perspective: Destination is in a different subnet but if no default gateway is configured (or misconfigured), it will: Send an ARP request for **172.16.1.4**.

Problem is PC3 is not in the same broadcast domain so no one answers → communication fails.

With Proxy ARP enabled, the router does something clever:

1. PC1 sends arp for 172.16.1.4
2. Router replies using its own MAC address (It uses the **MAC address of Proxy’s f0/0 interface**)
3. PC1 now sends traffic to Proxy
4. The router routes the packet to the correct destination (PC3)

From PC1’s point of view, it thinks PC3is directly reachable.

On Router:

```
interface f0/0
 ip proxy-arp
```
