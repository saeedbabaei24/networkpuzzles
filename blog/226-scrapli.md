---
wordpress_id: 226
title: "Scrapli"
date: "2026-02-03T10:47:46"
url: "https://networkpuzzles.com/2026/02/03/scrapli/"
---

**Scrapli** is a modern Python library for network automation that provides fast, flexible, and reliable communication with network devices. It is designed with a clean API, supports both synchronous and asynchronous workflows, and offers built-in parsing, logging, and interactive command handling.

```
# Basic connection
from scrapli import Scrapli

device = {
    "host": "10.10.20.48",
    "auth_username": "developer",
    "auth_password": "Cisco12345",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
}

conn = Scrapli(**device)
conn.open()
print(conn.get_prompt())


with Scrapli(**device) as conn:
    print(conn.get_prompt())


```

Scrapli allows us to send **single commands** or **multiple commands** to a network device and collect the output in a structured way. For multiple command we should use list.

```
Single Command:

sh_ver = conn.send_command("show version")
print(sh_ver.result)


output:
Cisco IOS XE Software, Version 17.9.3
...


Multiple commands:

result = conn.send_commands(["show version", "show run"])
print(result.result)

output:
Cisco IOS XE Software, Version 17.9.3
...
!
Current configuration : 4567 bytes
...


this is other way with using context manager:
with Scrapli(**device) as conn:
    result = conn.send_command("show run")
    print(result.result)

```

Parsing converts **raw CLI text** into **structured Python data** (dicts / lists) that automation scripts can easily work with.

Scrapli supports **Genie** and **TextFSM** parsing.

```
response = conn.send_command("show version")
print(response.genie_parse_output())


Output:
Returns a nested dictionary with detailed information
{
    "version": {
        "version": "17.9.3",
        "hostname": "Router",
        "uptime": "2 weeks, 3 days"
    },
    "platform": {
        "chassis": "C9300-48P",
        "os": "IOS-XE"
    }
}



response = conn.send_command("show version")
print(response.textfsm_parse_output())


Output:
Returns a list of dictionaries

[
    {
        "hostname": "Router",
        "version": "17.9.3",
        "uptime": "2 weeks, 3 days"
    }
]

```

`send_interactive()` allows Scrapli to automate CLI commands that require user interaction by matching prompts and responding automatically. It takes a **list of interaction steps**, where each step is a tuple:

```
with IOSXEDriver(**device) as conn:
    interactive = conn.send_interactive(
        [
            ("copy run start", "Destination filename [startup-config]?", "\n"),
        ]
    )

print(interactive.result)

```

Logging helps you **see what Scrapli is doing internally**, which is critical for debugging SSH connections, authentication issues, and command execution problems.

```
import logging
from scrapli.driver.core import IOSXEDriver

logging.basicConfig(
    filename="scrapli.log",
    level=logging.DEBUG
)

device = {
    "host": "10.10.20.47",
    "auth_username": "developer",
    "auth_password": "Cisco12345",
    "auth_strict_key": False,
}

conn = IOSXEDriver(**device)
conn.open()
print(conn.get_prompt())
print(conn.send_command("show run | i hostname").result)



or using Scrapli logging:

from scrapli import Scrapli
from scrapli.logging import enable_basic_logging

enable_basic_logging(file=True, level="debug")

device = {
    "host": "10.10.20.48",
    "auth_username": "developer",
    "auth_password": "Cisco12345",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
}

with Scrapli(**device) as conn:
    print(conn.get_prompt())
    print(conn.send_command("show run | i hostname").result)

```

We can send the config from a configuration file to the device instead of the commands:

In Send command from file it does it in Exec mode but in Send config from file it does it from **configuration mode**.

```
config.txt >

interface loopback50
 ip address 50.50.50.50 255.255.255.255
 description CONFIG_FROM_FILE

Code>

from scrapli import Scrapli

with open("config.txt") as f:
    config_lines = [line.strip() for line in f if line.strip()]

with Scrapli(**device) as conn:
    response = conn.send_configs(config_lines)
    print(response.result)


```
###### Asynchronous Programming

Asynchronous programming is a **programming style that allows code to run without waiting for long tasks to finish**.

Instead of blocking execution (waiting for one task to complete), the program can **start other tasks while waiting**, making it much faster and more efficient.

```
import asyncio

async def first_function():
    print("Start of first function")
    await asyncio.sleep(2)  # Simulating a 2-second delay
    print("End of first function")

async def second_function():
    print("Start of second function")
    await asyncio.sleep(1)  # Simulating a 1-second delay
    print("End of second function")

async def main():
    task1 = asyncio.create_task(first_function())
    task2 = asyncio.create_task(second_function())
    await asyncio.gather(task1, task2)

asyncio.run(main())

Output:
Start of first function
Start of second function
End of second function
End of first function


```

Multithreading is another way to run tasks **concurrently**, but it works very differently from asynchronous programming. In multithreading Each task runs in its **own thread**, The operating system switches between threads and also it is more resource like CPU and memory consuming.
