Base role
=========

This is the Ansible role I use to configure any machine. All these settings are
opinionated. You might do things differently, so read through the role to see
if it suits your needs.

Requirements
------------

The role is written for Ubuntu 16.04 only at the moment. I'm planning on
expanding to other Ubuntus and other distros eventually, once I ramp up with
Ansible.

Role Variables
--------------

TBD

Dependencies
------------

TBD

Example Playbook
----------------

```yaml
---
- hosts: all
  become: true
  roles:
    - ansible-role-base
```

License
-------

CC-BY

Author Information
------------------

Created by [coaxial](https://64b.it)
