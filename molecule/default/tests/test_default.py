import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

# Good example: https://github.com/nephelaiio/ansible-role-rbenv/blob/4771cdc2ee559b78d29929ab0700e8fca15019ab/molecule/compile/tests/test_compile.py

def test_etc_dnsmasq_folders(host):
    f = host.file('/etc/dnsmasq.conf')

    assert f.exists
    assert f.user == 'dnsmasq'
    assert f.group == 'nogroup'

    f = host.file('/etc/dnsmasq.hosts')
    assert f.exists
    assert f.user == 'dnsmasq'
    assert f.group == 'nogroup'
    assert f.contains('192.168.33.100 dnsmasq1.darklabs.home dnsmasq1')
    assert f.contains('192.168.33.101 dnsmasq2.darklabs.home dnsmasq2')

def test_hosts_file(host):
    f = host.file('/etc/hosts.molecule')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

@pytest.mark.parametrize('f',
                         ['dnsmasq', 'dnsmasq-base', 'dns-root-data', 'dnsutils'])
def test_packages_installed(host, f):
    pkg = host.package(f)
    assert pkg.is_installed

def test_dnsmasq_running_and_enabled(host):
    dnsmasq = host.service("dnsmasq")
    assert dnsmasq.is_running
    assert dnsmasq.is_enabled
    assert dnsmasq.socket("tcp://53").is_listening
    assert dnsmasq.socket("tcp://127.0.0.1:53").is_listening

def test_dnsmasq_user(host):
    dnsmasq = host.user("dnsmasq")
    assert dnsmasq.name == "dnsmasq"
    # assert dnsmasq.uid == "107"
    assert dnsmasq.gid == "65534"
    assert "nogroup" in dnsmasq.groups
    assert dnsmasq.home == "/var/lib/misc"
    assert dnsmasq.shell == "/bin/false"
