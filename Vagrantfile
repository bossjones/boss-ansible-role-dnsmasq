# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # set auto_update to false, if you do NOT want to check the correct
  # additions version when booting this machine
  config.vbguest.auto_update = true

  # do NOT download the iso file from a webserver
  config.vbguest.no_remote = false

  config.vm.define "dnsmasq" do |master|
    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://atlas.hashicorp.com/search.
    #master.vm.box = "ubuntu/trusty64"
    # For Xenial
    master.vm.box = "ubuntu/xenial64"
    # On Centos the interfaces are not eth0 ... change the playbooks!
    # master.vm.box = "bento/centos-7.5"

    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    # master.vm.box_check_update = false

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    master.vm.network "forwarded_port", guest: 53, host: 5300
    master.vm.network "forwarded_port", guest: 6543, host: 65430

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    master.vm.network "private_network", ip: "10.0.0.10"

    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # master.vm.network "public_network"

    # source: http://stackoverflow.com/questions/17845637/how-to-change-vagrant-default-machine-name
    config.vm.provider :virtualbox do |vb|
      vb.gui = false
      vb.name = 'dnsmasq'

      # user modifiable memory/cpu settings
      vb.memory = 1024
      vb.cpus = 2
      vb.customize ['modifyvm', :id, '--cpuexecutioncap', '50']
      vb.customize ['modifyvm', :id, '--chipset', 'ich9']

      # SOURCE: https://github.com/mitre/unfetter-mediawiki-vagrant/blob/master/Vagrantfile
      # SOURCE: https://serverfault.com/questions/74672/why-should-i-enable-io-apic-in-virtualbox?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
      vb.customize ['modifyvm', :id, '--ioapic', 'on'] # Bug 51473
      # Speed up dns resolution in some cases
      vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
      vb.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
      # Prevent clock drift, see http://stackoverflow.com/a/19492466/323407
      vb.customize ['guestproperty', 'set', :id, '/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold', 10_000]

      vb.customize ['modifyvm', :id, '--usb', 'on']
      vb.customize ['modifyvm', :id, '--audio', 'coreaudio', '--audiocontroller', 'ac97' ]
    end

    if Vagrant.has_plugin?('vagrant-hostmanager')
      config.hostmanager.enabled = true
      config.hostmanager.manage_host = true
    end

    # Vagrant can share the source directory using rsync, NFS, or SSHFS (with the vagrant-sshfs
    # plugin). Consult the Vagrant documentation if you do not want to use SSHFS.
    config.vm.synced_folder '.', '/vagrant', disabled: true
    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # master.vm.synced_folder "../data", "/vagrant_data"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    #
    #master.vm.provider "virtualbox" do |vb|
    #  # Customize the amount of memory on the VM:
    #  vb.memory = "2048"
    #end

    # Enable provisioning with a shell script. Additional provisioners such as
    # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
    # documentation for more information about their specific syntax and use.
#    master.vm.provision "shell", inline: <<-SHELL
#        sudo apt-get update
#    SHELL
    master.vm.provision "ansible" do |ansible|
        ansible.playbook = "site.yml"
        ansible.verbose = "vvvv"
        #ansible.raw_arguments = "--list-task"
    end
  end

end
