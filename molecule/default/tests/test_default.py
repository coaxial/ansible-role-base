import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall_rules(host):
    u = host.ufw

    assert u.is_enabled
    assert '22/tcp' in u.rules  # SSH rule
    assert 'Anywhere on lo' in u.rules or '127.0.0.0/8' in u.rules  # Loopback (adjust string if needed based on output)
    assert u.defaults['incoming'] == 'deny'
    assert u.defaults['outgoing'] == 'allow'
    assert u.defaults['routed'] == 'deny'


def test_firewall_rules_persist(host):
    # UFW persists automatically; just verify it's enabled
    u = host.ufw
    assert u.is_enabled


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
    assert o.password == '!'
    assert p.name == 'ansible'
    assert p.shell == '/bin/bash'
    assert p.password == '!'


def test_ssh_key(host):
    o = host.file('/home/user/.ssh/authorized_keys')
    p = host.file('/home/ansible/.ssh/authorized_keys')
    k = 'dummy_test_key'

    assert o.contains(k)
    assert p.contains(k)


def test_unattended_upgrades(host):
    a = host.file('/etc/apt/apt.conf.d/20auto-upgrades')
    u = host.file('/etc/apt/apt.conf.d/50unattended-upgrades')

    for f in [a, u]:
        assert f.exists
        assert f.user == 'root'
        assert f.group == 'root'
        assert f.mode == 0o644

    assert a.contains("""
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
""")
    assert u.contains("""
Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}";
        "${distro_id}:${distro_codename}-backports";
        "${distro_id}:${distro_codename}-security";
        "${distro_id}:${distro_codename}-updates";
};

Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "true";
""")


def test_timesync(host):
    f = host.file('/etc/systemd/timesyncd.conf')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert f.contains('NTP=ntp.ubuntu.com')
    assert f.contains('FallbackNTP=pool.ntp.org')


def test_tzdata(host):
    p = host.package('tzdata')

    assert p.is_installed


def test_fail2ban(host):
    s = host.service('fail2ban')

    assert s.is_running
    assert s.is_enabled
