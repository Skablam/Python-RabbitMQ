#!/bin/bash
echo "export PATH=$PATH:/usr/local/bin" > /etc/profile.d/local_bin.sh

source /etc/profile.d/local_bin.sh

gem install --no-ri --no-rdoc puppet

puppet module install garethr-erlang

puppet apply /vagrant/erlang.pp

puppet module install puppetlabs-rabbitmq

puppet apply /vagrant/rabbit.pp
