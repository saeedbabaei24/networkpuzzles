---
wordpress_id: 704
title: "DNS and HTTP GET with IP SLA"
date: "2026-04-05T17:31:25"
url: "https://networkpuzzles.com/2026/04/05/dns-and-http-get-with-ip-sla/"
---

When engineers first learn **IP SLA**, they often start with **ICMP echo**, because it is simple and useful for checking basic reachability. But in production networks, just knowing that a device is reachable is often **not enough**.

A server may still answer ping, while the actual **service** users need is already broken.

That is where **DNS** and **HTTP GET** operations become useful. They allow the router to test not only whether a host is reachable, but whether a **specific service** is actually responding.

In this post, I want to show a very simple example of both:

* **DNS IP SLA**
* **HTTP GET IP SLA**

and explain where each one is useful.

A ping only tells us: “Can I reach the remote IP?” That is helpful, but it does **not** tell us: whether the **DNS server** is answering queries, whether the **web server** is serving content, whether the **application** is usable for the user.

That is why IP SLA supports more advanced operations.

###### DNS IP SLA

DNS IP SLA is used when we want to verify that a **DNS server can answer a name resolution request**.

For example, if users say: “Internet is not working”. sometimes the real problem is **not routing** and **not connectivity**, but simply that **DNS is broken**.

In this example, router R1 sends a DNS request to **1.1.1.1** every **8 seconds**.

```
ip sla 2
 dns 1.1.1.1 name www.cisco.com
 frequency 8
ip sla schedule 2 life forever start-time now
```

Here The router behaves like a **DNS client**, it asks DNS server **1.1.1.1** to resolve **www.cisco.com**, repeats this test every **8 seconds** and it continues forever.

So instead of only checking whether **1.1.1.1** is reachable, we are checking whether it is actually **providing DNS service**

A DNS server may still respond to ping, but: UDP/53 may be blocked or DNS process may have failed or recursion may be broken or the server may be overloaded. In that case: **ICMP succeeds** but **DNS SLA fails**.

Sometimes the ISP path is technically up, but users still cannot browse because DNS resolution is failing. In that case, tracking DNS can be better than tracking only ping.

###### HTTP GET IP SLA

HTTP GET IP SLA is used when we want to verify that a **web service** is actually responding. This is different from just pinging a server or checking whether TCP port 80 is open. With HTTP GET, the router behaves like a simple web client and sends an actual **HTTP GET request**.

In this example, router sends an HTTP GET request to **192.168.34.4** every **60 seconds**.

```
ip sla 5
 http get http://192.168.34.4
 frequency 60
ip sla schedule 5 life forever start-time now
```

Here the router acts like a **web client**, it requests a webpage from **192.168.34.4**, repeats this every **60 seconds** and it continues forever.

A server may still be alive and reachable by ping, but web service may have crashed, or application may not be responding or HTTP process may be down.
