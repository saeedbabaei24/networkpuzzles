---
wordpress_id: 316
title: "Ansible Gathering Facts"
date: "2026-02-23T11:29:06"
url: "https://networkpuzzles.com/2026/02/23/ansible-gathering-facts/"
---

When automating network devices with Ansible, collecting device information (facts) is usually the first step.

In this lab, we will:

* Configure Ansible
* Define an inventory file
* Use `cisco.ios.ios_facts`
* Save the output to a JSON file
* Print selected device information

Ansible Configuration (ansible.cfg)

```
[defaults]
host_key_checking = false    #Disables SSH fingerprint verification
inventory = invt.yaml  #Tells Ansible which inventory file to use by default.
gathering = explicit   #Ansible will only gather facts if we explicitly request it
```

Inventory File (invt.yaml)

```
all:
  vars:
    ansible_user: admin
    ansible_password: cisco
    ansible_network_os: ios
    ansible_connection: network_cli

  children:
    routers:
      hosts:
        R1:
          ansible_host: 192.168.199.30
        R2:
          ansible_host: 192.168.199.31
```

We created a group called `routers`.

This allows us to target:

* One device → `hosts: R1`
* All routers → `hosts: routers`

---

Playbook – Gathering Facts


```
---
- name: "Gathering Facts"
  hosts: R1
  tasks:

    - name: Gather all Facts
      cisco.ios.ios_facts:
        gather_subset: interfaces
      register: cli_result

    - name: "Saving facts into output.json file"
      copy:
        content: "{{ cli_result | to_nice_json }}"
        dest: output.json

    - name: "Printing version"
      debug:
        msg: "{{ cli_result.ansible_facts.ansible_net_hostname }} >>> {{ cli_result.ansible_facts.ansible_net_version }}"

    - name: "Printing Facts"
      debug:
        msg: "{{ cli_result }}"
```

Let see each section separately:

Task 1 – Gather Facts

```
cisco.ios.ios_facts:
  gather_subset: interfaces
```

This module:

* Connects via SSH
* Runs internal commands
* Parses structured data
* Returns device facts

`gather_subset: interfaces` means:  
We only collect interface-related information.

Other useful subsets:

* `interface`
* `config`
* `all`

The result is stored using: register: cli\_result

Task 2 – Save Output to JSON

```
content: "{{ cli_result | to_nice_json }}"
dest: output.json
```

This:

* Converts the Python dictionary into formatted JSON
* Saves it locally

This is extremely useful for:

* Troubleshooting
* Documentation
* Feeding data into other automation tools

Task 3 – Print Device Version

```
msg: "{{ cli_result.ansible_facts.ansible_net_hostname }} >>> {{ cli_result.ansible_facts.ansible_net_version }}"
```

This task will find the ansible\_net\_version which is under ansible\_facts under cli\_result.ansible and print it in front of the host name. If we want to pars some special info we can find where is it in the hierarchical out put of gather facts all then point directly to that specific data.

Also the detain info about the modules are in available ansible official documentation: for this example:  
<https://docs.ansible.com/projects/ansible/latest/collections/cisco/ios/ios_facts_module.html#ansible-collections-cisco-ios-ios-facts-module>
