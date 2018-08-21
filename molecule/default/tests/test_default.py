import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall_rules(host):
    i = host.iptables

    assert '-P INPUT DROP' in i.rules('filter', 'INPUT')
    assert '-P FORWARD DROP' in i.rules('filter', 'FORWARD')
    assert '-P OUTPUT DROP' in i.rules('filter', 'OUTPUT')
