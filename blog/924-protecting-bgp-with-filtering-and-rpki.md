---
wordpress_id: 924
title: "Protecting BGP with Filtering and RPKI"
date: "2026-07-23T21:30:57"
url: "https://networkpuzzles.com/2026/07/23/protecting-bgp-with-filtering-and-rpki/"
---

One thing I really liked about the RIPE NCC course is that it doesn’t present a single “magic solution.” Instead, it explains that BGP security is built from multiple layers. Every mechanism addresses a different type of problem, and together they significantly reduce the chances of routing incidents.

#### Prefix Filtering

The first and probably most important defense is **Prefix Filtering**.

The basic idea is simple: only accept prefixes that a customer or peer is actually allowed to advertise.

Without prefix filtering, one simple configuration mistake on the customer side could quickly become a problem for every upstream provider connected to that network.

This sounds straightforward, but many famous BGP incidents happened because filtering wasn’t configured properly or wasn’t configured at all.

#### Maximum Prefix Limits

Another useful protection is **Maximum Prefix**.

Every BGP session can be configured with a maximum number of routes that a neighbor is expected to advertise.

For example, if a customer normally sends five prefixes, there’s no reason to accept fifty thousand.

If that limit is exceeded, the router can automatically terminate the BGP session before thousands of unexpected routes enter the network.

This feature doesn’t stop hijacking, but it’s extremely effective against configuration mistakes and accidental route leaks.

#### AS Path Filtering

Another common security mechanism is **AS Path Filtering**.

Besides checking the advertised prefix itself, operators can also verify whether the route originated from the expected Autonomous System.

For example, suppose a customer owns prefix **203.0.113.0/24** and operates **AS65010**.

If the same prefix suddenly appears with an AS Path beginning with **AS65099**, something is clearly wrong.

By filtering unexpected AS Paths, operators can prevent many routing policy violations before they spread.

Although AS Path filtering requires maintenance, it’s still an important part of BGP security in many ISP environments.

#### Protecting the BGP Session

Not every attack targets routing information itself. Sometimes the goal is simply to disrupt the BGP session.

Two older—but still useful—mechanisms covered in the course are **TTL Security (GTSM)** and **TCP MD5 Authentication**.

###### TTL Security

Normally, directly connected BGP neighbors exchange packets with a TTL value close to 255.

TTL Security takes advantage of this behavior. The router only accepts BGP packets whose TTL indicates they came from a directly connected neighbor.

If someone on another network tries to spoof BGP packets, the TTL value will usually be lower, and the packets will be discarded before they ever reach the BGP process.

It’s a simple feature, but it helps reduce certain remote attacks against BGP sessions.

###### TCP MD5 Authentication

Another classic security mechanism is **TCP MD5 Authentication**.

Both BGP neighbors are configured with the same shared password.

Every BGP packet includes an MD5 hash calculated using that secret. If the receiving router calculates a different hash, the packet is rejected immediately.

This prevents unauthorized devices from establishing a BGP session simply by pretending to be a legitimate neighbor.

It’s important to remember that MD5 authentication does **not** validate routing information. It only verifies that the packets are coming from a trusted peer.

#### RPKI

Traditional filtering works well, but it depends on operators creating and maintaining filters manually.

That becomes increasingly difficult when thousands of Autonomous Systems exchange millions of routes every day.

This is where **RPKI (Resource Public Key Infrastructure)** comes in.

RPKI introduces cryptographic validation into Internet routing.

Instead of relying only on trust or manually maintained filters, resource holders can digitally state which Autonomous System is authorized to originate a particular IP prefix.

#### What Is a ROA?

The key building block of RPKI is the **Route Origin Authorization**, or **ROA**.

A ROA is essentially a signed statement saying:

> “This IP prefix may be originated by this Autonomous System.”

For example:

```

Prefix:203.0.113.0/24Origin AS:AS65001Maximum Length:/24
```


This tells the rest of the Internet that AS65001 is authorized to announce that prefix.

If another AS advertises the same network, routers performing validation can immediately detect that something is wrong.

#### Route Origin Validation

Routers that support RPKI can validate incoming routes against existing ROAs.

Every received route falls into one of three categories.

**Valid**

The prefix matches an existing ROA, and the originating Autonomous System is exactly the one specified in the authorization.

Example:

```

ROA203.0.113.0/24Origin: AS65001Announcement203.0.113.0/24Origin: AS65001Result:Valid
```


**Invalid**

A matching ROA exists, but the route is being originated by a different Autonomous System.

Example:

```

ROA203.0.113.0/24Origin: AS65001Announcement203.0.113.0/24Origin: AS65099Result:Invalid
```


In many networks, these routes are rejected automatically.

**Not Found**

No ROA exists for the advertised prefix.

Example:

```

Announcement198.51.100.0/24No ROA exists.Result:Not Found
```


This doesn’t necessarily mean the route is malicious. It simply means there’s no RPKI information available to validate it.

#### Hosted vs Delegated RPKI

With **Hosted RPKI**, the Regional Internet Registry (such as RIPE NCC) manages the Certificate Authority and the underlying infrastructure. Resource holders simply create their ROAs through a web portal.

For most organizations, this is by far the easiest option.

With **Delegated RPKI**, the organization manages its own Certificate Authority and publishes its own repository.

This offers greater flexibility but also introduces additional operational responsibility.

Unless there’s a specific requirement for full control, the hosted model is usually the simpler and more practical choice.
