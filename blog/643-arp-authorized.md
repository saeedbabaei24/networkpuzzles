---
wordpress_id: 643
title: "ARP authorized"
date: "2026-03-27T22:06:56"
url: "https://networkpuzzles.com/2026/03/27/arp-authorized/"
---

In this lab, I wanted to analyze the behavior of the Cisco IOS interface command `arp authorized`.

The idea behind this feature is that the router should not rely on normal dynamic ARP learning on that interface. Cisco documents this behavior by stating that `arp authorized` stops dynamic ARP on the interface.

Because of that, forwarding depends on whether the router already has a valid ARP entry in its internal ARP table.

If an ARP entry for the destination exists, the router can use it and forward the packet.

If no ARP entry exists, the router cannot just learn it dynamically in the normal way on that interface, and the packet is dropped.

That behavior becomes interesting in a DHCP scenario.

Even if the router acts as a DHCP server and knows the client from the DHCP binding, that does not automatically mean the packet can be forwarded. The router still needs a usable ARP entry in the ARP table. In other words, a DHCP binding and an ARP entry are related, but they are not the same thing. Cisco provides the `update arp` command under the DHCP pool specifically to secure or create the ARP entry corresponding to DHCP leases.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/03/grafik-82.png?resize=872%2C402&ssl=1)

At first I enabled the arp authorized on the interface of DHCP router, the client could sent packet to DHCP router but DHCP router could not answer becuse ther is no ARP for that IP, and the router can only trust on the Autorized Arp table:

Ping from clinet side and debug on DHCP router, we can see the packet is arriving at rouer:

```
DHCP-Client#ping 192.168.123.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.123.1, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)


DHCP-Router#
*Mar  1 00:04:28.923: IP: tableid=0, s=192.168.123.2 (FastEthernet0/0), d=192.168.123.1 (FastEthernet0/0), routed via RIB
*Mar  1 00:04:28.923: IP: s=192.168.123.2 (FastEthernet0/0), d=192.168.123.1 (FastEthernet0/0), len 100, rcvd 3
*Mar  1 00:04:28.927: IP: tableid=0, s=192.168.123.1 (local), d=192.168.123.2 (FastEthernet0/0), routed via RIB

```

So in this topology, there are two ways to make the destination reachable when `arp authorized` is enabled:

First, I can create the ARP entry manually:

```
arp 192.168.123.3 000c.1234.5678 arpa
```

This is useful for a statically addressed client.

Second, if the client is using DHCP, I can tell the DHCP server to update the ARP table automatically when it assigns an address:

```
ip dhcp pool CLIENTS
 network 192.168.123.0 255.255.255.0
 default-router 192.168.123.1
 update arp
```

when `update arp` is used, ARP table entries and their corresponding DHCP leases are secured automatically for new leases and bindings. Existing active leases are not updated until the client renews the lease.

That means the DHCP client can work with `arp authorized`, because the router can populate a secure ARP entry from the DHCP process. But a static client will not benefit from that automatically, so in that case I need to configure a static ARP entry myself.
