---
wordpress_id: 370
title: "Ansible Playbook"
date: "2026-02-24T11:15:50"
url: "https://networkpuzzles.com/2026/02/24/ansible-playbook/"
---

In this post, I’ll walk through several small but powerful Ansible playbook examples.  
Each example focuses on a specific concept such as variables, loops, conditions, filters, lookups, and facts.

These are small puzzle pieces — but together they form the foundation of automation.

###### Variables in a Playbook + Filters

It defines a variable directly inside the playbook and prints it using the `debug` module.  
It also demonstrates how to use a filter (`type_debug`) to see the variable type.

* `vars:` → define variables in the playbook
* `{{ variable }}` → reference variables
* `| filter` → apply Jinja2 filters

```
msg: "The IP is: {{ IP_Addr | type_debug }}"
```

This helps when troubleshooting type mismatches in complex automation workflows.

###### Using `shell` + `register` + Parsing Output

It executes a shell command (`ping`), Saves the output using `register` and Parses and manipulates the output.

* `shell:` → run local shell command
* `register:` → store task output
* `output.stdout` → access dictionary key
* `.split('\n')` → convert output to list

```
msg: "{{ output.stdout.split('\n') }}"
```

This converts command output into a list, making it easier to loop over lines later.

In network automation, this is often used before parsing CLI output into structured data.

Using `vars_prompt` (Interactive Input)

It prompts the user for input during playbook execution.

* `vars_prompt`
* `private: no` → show input
* `encrypt: sha512_crypt`
* `confirm: yes`

###### Working with Lists

It defines a list and accesses its elements.

* Lists in YAML
* Indexing like Python (`IP_Addr[1]`)

Without specifying an index → entire list is printed  
With index → specific element is printed

###### Working with Dictionaries

It defines key-value pairs and retrieves values using keys.

```
IP_Addr['R1']

devices:
  R1: 192.168.199.30
  R2: 192.168.199.31
```
###### Using `when` Conditions

It executes a task only if a condition is met.

```
when: ansible_facts['os_family'] == "Debian"

when:
  - ansible_facts['os_family'] == "Debian"
  - ansible_facts['distribution_version'] | int >= 20
```

This prevents breaking configurations on unsupported systems.

###### Loop + Filter (IPv4 Validation)

It loops through a list and runs task only if item is a valid IPv4 address.

```
when: item | ipv4
```

This prevents invalid configuration lines from being pushed to devices.

###### Looping Over Dictionaries (`with_dict` / `dict2items`)

It converts a dictionary into a list of key-value pairs.

```
Dict | dict2items
```

This is especially powerful in Jinja2 templates.

###### Using `lookup('file')`

It reads a file from disk and loads its content.

```
lookup('file', 'R1_config.txt')

lookup('file', 'R1_config.txt').splitlines()
```

This converts file content into a list for looping or parsing.

###### Working with JSON + `from_json` + `json_query`

It loads JSON file, Parses it into structured data and Extracts specific values using `json_query`.

```
file_d | json_query('devices.*.partitions')
```

This allows extracting deeply nested data easily.

###### Saving Facts to JSON

It Stores `ansible_facts` into a file.

```
content: "{{ ansible_facts | to_nice_json }}"
```
