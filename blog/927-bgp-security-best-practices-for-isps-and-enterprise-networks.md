---
wordpress_id: 927
title: "BGP Security best Practices for ISPs and Enterprise Networks"
date: "2026-08-17T09:48:20"
url: "https://networkpuzzles.com/2026/08/17/bgp-security-best-practices-for-isps-and-enterprise-networks/"
---

One of the biggest takeaways from the RIPE NCC course is that **there is no single feature that makes BGP secure**.

Even though technologies like RPKI have significantly improved routing security, they don’t solve every problem. RPKI only validates the **origin** of a route. It doesn’t verify whether the advertised AS Path is correct, nor can it prevent every type of route leak.

For example, imagine an ISP receives a perfectly valid route from one upstream provider. If that ISP accidentally advertises the same route to another provider when it shouldn’t, the route is still **RPKI Valid**. The problem isn’t who originated the prefix—it’s that the routing policy was incorrect.

That’s why route leaks continue to happen even as RPKI adoption increases across the Internet.

The course repeatedly emphasizes that routing security isn’t about relying on one technology. It’s about combining multiple layers of protection so that if one mechanism misses something, another one can still reduce the impact.

#### Building a Layered Security Strategy

The most secure networks don’t depend on a single defense. Instead, they combine several mechanisms that complement each other.

A typical security strategy might look something like this:

* Verify which prefixes customers are allowed to advertise using **Prefix Filtering**.
* Limit the number of accepted routes with **Maximum Prefix**.
* Validate expected Autonomous Systems using **AS Path Filtering**.
* Protect BGP sessions with **TTL Security** and **TCP MD5 Authentication**.
* Use **RPKI Route Origin Validation** to detect invalid route announcements.
* Continuously monitor routing changes and investigate unexpected advertisements before they become widespread.

Each of these mechanisms addresses a different part of the problem. None of them is perfect on its own, but together they make the network much more resilient.

#### Best Practices for ISPs

For Internet Service Providers, BGP security is especially important because routing mistakes can quickly propagate to customers, peers, and upstream providers.

Some of the most practical recommendations from the course include:

* Apply strict inbound and outbound prefix filters for every customer.
* Configure Maximum Prefix limits on all external BGP sessions.
* Validate Route Origins using RPKI whenever possible.
* Regularly review routing policies to prevent accidental route leaks.
* Protect BGP sessions with authentication and TTL Security.
* Monitor BGP announcements continuously and investigate unexpected routing changes.

Good operational practices often prevent incidents long before they become visible on the global Internet.

#### Best Practices for Enterprise Networks

Enterprise networks usually have fewer external BGP peers, but they still benefit from adopting good routing practices.

If an organization owns public IP address space, creating **ROAs** is a simple step that helps other networks validate its announcements.

Enterprises should also advertise only the prefixes they actually intend to announce, review routing policies carefully before deployment, and coordinate any changes with their Internet providers.

Even if an enterprise doesn’t operate a large backbone, following these practices reduces the risk of accidentally contributing to a global routing incident.

#### Final Thoughts

Before taking this course, I was already familiar with concepts like prefix hijacking and RPKI, but what I found most valuable was seeing how all the different pieces fit together.

It’s easy to think of BGP security as a single feature or protocol, but the reality is much broader. Routing security depends on a combination of good operational practices, sensible routing policies, and technologies such as RPKI working together.

One thing that also stood out to me is that many of the largest BGP incidents weren’t the result of sophisticated attacks. They started with something much simpler: a missing filter, an incorrect routing policy, or a route advertised to the wrong neighbor. In other words, many incidents were entirely preventable.

That was probably the biggest lesson I took away from the RIPE NCC Academy. BGP itself isn’t “insecure” because it’s broken—it simply reflects the trust-based Internet it was originally designed for. As network engineers, it’s our responsibility to add the validation, filtering, and operational controls that today’s Internet requires.

Overall, I found the course to be a practical introduction to BGP security. It focuses on real operational challenges rather than theory alone, and the examples make it easy to understand why routing security matters. Whether you’re working for an ISP, a cloud provider, or an enterprise network, the concepts covered in the course are directly applicable to real-world environments.
