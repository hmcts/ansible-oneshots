import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('disable-restriction')


def test_iptables_config_file(host):
    f = host.file('/etc/sysconfig/iptables-config')

    assert f.exists
    assert f.is_file


def test_iptables_is_installed(host):
    iptables = host.package("iptables")

    assert iptables.is_installed


def test_iptables_rules(host):
    access_rule = '-A INPUT -s 10.0.0.0/12 -p tcp -m tcp -j ACCEPT'
    block_rule = '-A INPUT -j LOGGING'
    r = host.iptables.rules()

    assert access_rule not in r
    assert block_rule not in r


def test_local_ping(host):
    host.check_output("ping -c1 localhost | grep packet > l")

    l = host.file("l")
    assert l.exists
    assert "0% packet loss" in l.content_string
