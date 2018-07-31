Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-16.04"
    config.vm.box_version = "= 2.3.5"
    config.vm.synced_folder ".", "/vagrant"

    config.vm.provision "shell", inline: <<-SHELL
        apt-get -qqy update
        DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
        apt-get -qqy install postgresql
        apt-get -qqy install python-pip
        sudo pip install psycopg2-binary

        su postgres -c 'createuser -dRS vagrant'
        su vagrant -c 'createdb'
        su vagrant -c 'createdb news'

        sudo -u vagrant psql -d news -f /vagrant/newsdata.sql
        sudo -u vagrant psql -d news -f /vagrant/create-views.sql

        echo "Done installing your virtual machine!"
    SHELL
end