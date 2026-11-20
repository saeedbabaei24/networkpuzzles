---
wordpress_id: 85
title: "YANG Data Structure"
date: "2026-01-28T13:32:21"
url: "https://networkpuzzles.com/2026/01/28/yang-data-structure/"
---

**YANG** (Yet Another Next Generation) is a **data modeling language** used to describe the **structure and configuration of network devices**. A data model is a well understood and agreed upon method to describe **something**.

Data models may describe some aspect of a **network device**, or a **network service**. Network servies like Interface, vlan,OSPF.. and Network services like VRF, ACL..

It does **not configure devices directly**, but defines **how configuration and state data are structured**, so tools like **NETCONF / RESTCONF /grpc** can read or modify them in a standardized way.

###### Simple YANG Example

```
module simple-interface {
  namespace "urn:example:interface";
  prefix if;

  container interfaces {
    list interface {
      key "name";

      leaf name {
        type string;
      }

      leaf description {
        type string;
      }

      leaf enabled {
        type boolean;
        default true;
      }

      leaf ip-address {
        type string;
      }
    }
  }
}

```

This means: A device has **interfaces**, Each interface has: name, description, enabled / disabled and IP address.

You can find the Yang data model here: <https://github.com/YangModels/yang>

There are standard and also vendor base Yang data models.

###### Core YANG Concepts

A **module** is the top-level file in YANG. Everything lives inside a module. Think of it as: A project folder that contains everything related to this model.

```
module router-config {
  namespace "urn:example:router";
  prefix rt;

```

A **container** groups related configuration items. For example here this container holds all interface-related data.

```
container interfaces {
```

A **list** is used when something can appear multiple times(e.g., multiple interfaces). GigabitEthernet0/0, GigabitEthernet0/1, Loopback0, Each one is an entry in this list.

```
list interface {
  key "name";

```

A **leaf** holds one value only. for example `name = "GigabitEthernet0/0"`, `ip-address = "192.168.1.1"` ,`enabled = true`

```
leaf name {
  type string;
}

leaf ip-address {
  type string;
}

leaf enabled {
  type boolean;
}

```

A **leaf-list** holds multiple values of the same type. Unlike `list`, it has **no keys**, only values.

```
leaf-list dns-servers {
  type string;
}

```

**typedef** is used to define reusable data types.

```
typedef ipv4-address {
  type string {
    pattern "([0-9]{1,3}\\.){3}[0-9]{1,3}";
  }
}

```

**rpc** Remote Procedure Call is for **actions**, not configuration. For example Reset interface, clear counters..

```
rpc restart-interface {
  input {
    leaf name {
      type string;
    }
  }
}

```
```
Full Example:
module router-config {
  namespace "urn:example:router";
  prefix rt;

  typedef ipv4-address {
    type string;
  }

  container interfaces {
    list interface {
      key "name";

      leaf name {
        type string;
      }

      leaf ip-address {
        type ipv4-address;
      }

      leaf enabled {
        type boolean;
      }
    }
  }

  rpc restart-interface {
    input {
      leaf name {
        type string;
      }
    }
  }

  notification interface-down {
    leaf name {
      type string;
    }
  }
}

```

We can also open a yang file with **pyang** in linux, so we can have a better look:

```
$pyang -f tree router-config.yang
module: router-config
  +--rw interfaces
     +--rw interface* [name]
        +--rw name          string
        +--rw ip-address   ipv4-address
        +--rw enabled      boolean
  +---x restart-interface
     +--rw input
        +--rw name   string
  +---n interface-down
     +--rw name   string

```
