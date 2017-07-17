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

Variable name | Default value | Purpose
--- | --- | ---
`base__operator_username` | `user` | username for the account that will be used to log into the server etc.
`base__provisioning_username` | `ansible` | username for the account that ansible will use
`base__ssh_pubkey_path` | `~/.ssh/id_rsa.pub` | path to the public key to be inserted into `authorized_keys` for both users
`base__timezone` | `America/Toronto` | the timezone to be used on the machine

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
