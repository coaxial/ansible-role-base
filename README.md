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
`base__operator_password` | none, must be set | password for the operator account. cf. to generate https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module
`base__operator_shell` | `/bin/bash` | shell to use instead of `sh`
`base__provisioning_username` | `ansible` | username for the account that ansible will use
`base__ssh_pubkey_path` | `~/.ssh/id_rsa.pub` | path to the public key to be inserted into `authorized_keys` for both users
`base__timezone` | `Etc/UTC` | the timezone to be used on the machine

Dependencies
------------

Same as Ansible

Example Playbook
----------------

`playbook.yml`:
```yaml
---
- hosts: all
  become: true
  roles:
    - ansible-role-base
  vars_files:
    - myvars.yml # to override the default **insecure** operator password
```

`myvars.yml`:
```yaml
# Note that the whole dict has to be redefined, because this will overwrite the
# default one, and missing keys won't fall through
base__operator_user:
  username: 'user'
  password: 'my_$ecure_password!' # Generate with `mkpasswd --method=sha-512`, and encrypt with vault
  shell: '/bin/bash'
```

> Note: If the target system requires a password for SSH and/or sudo, run the
> playbook with both the `-k` and `-K` options.

License
-------

CC-BY

Author Information
------------------

Created by [coaxial](https://64b.it)
