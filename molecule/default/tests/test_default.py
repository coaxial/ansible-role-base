import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall_rules(host):
    i = host.iptables

    assert '-P INPUT DROP' in i.rules('filter', 'INPUT')
    assert '-P FORWARD DROP' in i.rules('filter', 'FORWARD')
    assert '-P OUTPUT ACCEPT' in i.rules('filter', 'OUTPUT')
    assert (
        '-A INPUT -i lo -m '
        'comment --comment "Allow loopback traffic" -j ACCEPT'
    ) in i.rules('filter', 'INPUT')
    assert (
        '-A INPUT -p tcp -m tcp --dport 22 -m '
        'comment --comment "Allow SSH traffic" -j ACCEPT'
    ) in i.rules('filter', 'INPUT')


def test_firewall_rules_persist(host):
    r4 = host.file('/etc/iptables/rules.v4')
    r6 = host.file('/etc/iptables/rules.v6')

    assert r4.exists
    assert r6.exists


def test_sshd(host):
    s = host.service('sshd')

    assert s.is_running
    assert s.is_enabled


def test_sshd_config(host):
    f = host.file('/etc/ssh/sshd_config')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert 'PermitRootLogin no' in f.content_string
    assert 'PasswordAuthentication no' in f.content_string
    assert 'AllowUsers ansible user' in f.content_string


def test_sudo(host):
    f = host.file('/etc/sudoers')

    assert f.contains('ansible ALL=(ALL) NOPASSWD:ALL')
    assert f.contains('user ALL=(ALL) NOPASSWD:ALL')


def test_users(host):
    o = host.user('user')
    p = host.user('ansible')

    assert o.name == 'user'
    assert o.shell == '/bin/bash'
    assert o.password == '!!'
    assert p.name == 'ansible'
    assert p.shell == '/bin/bash'
    assert p.password == '!!'


def test_ssh_key(host):
    o = host.file('/home/user/.ssh/authorized_keys')
    p = host.file('/home/ansible/.ssh/authorized_keys')
    k = 'dummy_test_key'

    assert o.contains(k)
    assert p.contains(k)
