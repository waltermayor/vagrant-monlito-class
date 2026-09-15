Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/jammy64"

  config.vm.hostname = "monolith"

  config.vm.network "private_network",
                    ip: "192.168.56.10"

  # FastAPI
  config.vm.network "forwarded_port",
                    guest: 8000,
                    host: 8000

  config.vm.provider "virtualbox" do |vb|
    vb.name = "monolith-vm"
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/site.yml"
  end

end