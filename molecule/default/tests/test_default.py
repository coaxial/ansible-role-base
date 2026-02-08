import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall_rules(host):
    ufw_status = host.command("ufw status").stdout

    assert "Status: active" in ufw_status
    assert "22/tcp" in ufw_status  # SSH rule
    assert ("Anywhere on lo" in ufw_status or
            "127.0.0.0/8" in ufw_status)
    # Check defaults via /etc/default/ufw (not shown in 'ufw status')
    defaults_file = host.file('/etc/default/ufw')
    assert defaults_file.contains('DEFAULT_INPUT_POLICY="DROP"')
    assert defaults_file.contains('DEFAULT_OUTPUT_POLICY="ACCEPT"')
    assert defaults_file.contains('DEFAULT_FORWARD_POLICY="DROP"')


def test_firewall_rules_persist(host):
    # Reload UFW to simulate persistence (e.g., after config changes)
    host.command("ufw reload")
    ufw_status = host.command("ufw status").stdout
    assert "Status: active" in ufw_status


def test_sshd(host):
    is_debian_based = (host.system_info.distribution.lower()
                       in ['ubuntu', 'debian'])
    service_name = 'ssh' if is_debian_based else 'sshd'
    s = host.service(service_name)

    assert s.is_running
    assert s.is_enabled


def test_sshd_config(host):
    f = host.file('/etc/ssh/sshd_config')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert 'PermitRootLogin no' in f.content_string
    assert 'PasswordAuthentication no' in f.content_string
    
    # Dynamically check AllowUsers using Ansible variables
    provisioning_username = host.ansible.get_variables()['base__provisioning_username']
    operator_username = host.ansible.get_variables()['base__operator_username']
    expected_allow_users = f'AllowUsers {provisioning_username} {operator_username}'
    assert expected_allow_users in f.content_string


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
