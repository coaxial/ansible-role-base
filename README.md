base
=========

[![.github/workflows/ci.yml](https://github.com/coaxial/ansible-role-base/actions/workflows/ci.yml/badge.svg)](https://github.com/coaxial/ansible-role-base/actions/workflows/ci.yml)

Opinionated base config for servers.

Role Variables
--------------

Name | Default | Possible values | Description
---|---|---|---
`base__operator_username` | `user` | Any valid username | Administrative account username.
`base__operator_password` | `'!'` (i.e. no password) | Operator account password, see [instructions to generate](https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module) or use `mkpasswd --method=sha-512`.
`base__operator_shell` | `/bin/bash` | Defines the default shell for the operator.
`base__provisioning_username` | `ansible` | User for Ansible to use.
`base__ssh_pubkey_path` | `~/.ssh/id_pub.rsa` | Public key to add to `authorized_keys` for both users.
`base__timezone` | `Etc/UTC` | Timezone for that machine. See [why is UTC the one true TZ for your servers](http://yellerapp.com/posts/2015-01-12-the-worst-server-setup-you-can-make.html)
`base__ntp_server` | `ntp.ubuntu.com` | NTP server to get time from.
`base__ntp_server_fallback` | `pool.ntp.org` | Alternative NTP server should the one set above fail.


Example Playbook
----------------

```yaml
- hosts: all
  become: true
  tasks:
    - name: Apply base configuration
      include_role:
        name: coaxial.base
```

License
-------

MIT

Author Information
------------------

Coaxial ([64b.it](https://64b.it))
