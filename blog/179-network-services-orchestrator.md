---
wordpress_id: 179
title: "Network Services Orchestrator"
date: "2026-02-01T11:12:07"
url: "https://networkpuzzles.com/2026/02/01/network-services-orchestrator/"
---

Cisco Network Services Orchestrator is a Linux application which orchestrates the configuration life cycle of network devices. NSO uses software packages called Network Element Drivers (NEDs) to facilitate telnet, SSH, or API interactions with the devices that it manages. The NED provides an abstraction layer that reads in the device’s running configuration and parses it into a data-model-validated snapshot in the CDB.

NSO is maybe the best tool for automating the controller-less networks.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik.png?resize=842%2C430&ssl=1)

If we want to configure other vendors we need to install the driver of them in NSO.

Here is a GUI of NSO which I reseved it from cisco sandbox. At first I select all the devices and sync config from the devices so that NSO has the config of them.

All the configuration can be made through the CLI too.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-1.png?resize=2520%2C1255&ssl=1)

In order to see the the config of the device we can just select the device from the the menu.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-4.png?resize=2052%2C1017&ssl=1)

As an example I choose dist-rtr1 and I changed description and add secondary ip on one of the interfaces.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-3.png?resize=1956%2C950&ssl=1)

In tools section there is a Commit manager which we can see our changes ,commit or revert them.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-5.png?resize=1891%2C702&ssl=1)![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-6.png?resize=1946%2C882&ssl=1)![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-7.png?resize=1207%2C563&ssl=1)

We can load committed configuration and then edit or delete it. This can be selective that means only for some devices not all of them.

![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/grafik-8.png?resize=1873%2C1013&ssl=1)
