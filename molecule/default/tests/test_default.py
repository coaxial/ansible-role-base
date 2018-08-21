import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall_rules(host):
    i = host.iptables

    assert '-P INPUT DROP' in i.rules('filter', 'INPUT')
    assert '-P FORWARD DROP' in i.rules('filter', 'FORWARD')
    assert '-P OUTPUT DROP' in i.rules('filter', 'OUTPUT')
    assert (
        '-A INPUT -p tcp -m tcp --dport 22 -m '
        'comment --comment "Allow SSH traffic" -j ACCEPT'
    ) in i.rules('filter', 'INPUT')


def test_firewall_rules_persist(host):
    r4 = host.file('/etc/iptables/rules.v4')
    r6 = host.file('/etc/iptables/rules.v6')

    assert r4.exists
    assert r6.exists
