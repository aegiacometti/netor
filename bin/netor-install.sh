#!/bin/sh -

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

read -p "This script will install Netor in the current directory (y/n): " opc

case $opc in
 y) sudo apt-get update
    sudo apt-get --assume-yes install python3-pip
    sudo pip3 install setuptools --upgrade
    sudo pip3 install tinydb
    sudo apt-get --assume-yes install git
    git clone https://github.com/aegiacometti/netor.git
    sudo pip3 install napalm
    sudo pip3 install ansible
    sudo pip3 install "pywinrm>=0.3.0"
    ansible-galaxy install ansible-network.network-engine
    wget https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg -O $HOME/.ansible.cfg
    python3 "$DIR"/netor/netor/tinydb/scripts/netorconf.py
    wget -O bootstrap-salt.sh https://bootstrap.saltstack.com
    sudo sh bootstrap-salt.sh -x python3 -M
    "$DIR"/netor/bin/netor-salt-stop
    sudo systemctl disable salt-master.service
    sudo systemctl disable salt-minion.service
    "$DIR"/netor/bin/netor-salt-start
    sudo cp "$DIR"/netor/netor/salt/config/services/salt-proxy@.service /etc/systemd/system/
    sudo mv /etc/salt/master /etc/salt/master.bkp
    sudo mv /etc/salt/minion /etc/salt/minion.bkp
    sudo mv /etc/salt/proxy /etc/salt/proxy.bkp
    sudo ln -s "$DIR"/netor/netor/salt/config/master /etc/salt/master
    sudo ln -s "$DIR"/netor/netor/salt/config/minion /etc/salt/minion
    sudo ln -s "$DIR"/netor/netor/salt/config/proxy /etc/salt/proxy
    sudo pip3 install salt-sproxy
    "$DIR"/netor/bin/netor-db-push
    "$DIR"/netor/bin/netor-salt-restart
    echo PATH="\$PATH:"$DIR"/netor/bin/" >> $HOME/.profile
    echo ""
    echo "ATTENTION: Complete this task manually"
    echo "Since there are 2 files with bugs it is necesarry to update them manually"
    echo "locate the files runners/net.py and runners/bgp.py"
    echo "replace them with the 2 files in "$DIR"/netor/netor/salt/config/updates"
    echo "and you are ready to!"
    echo ""
    echo "###############################################################################"
    echo "The installer has finished"
    echo ""
    echo "Now:"
    echo "1.- logoff and login again."
    echo "2.- create a new DB with netor-db-switch and populate it with netor-db-customer,"
    echo "netor-db-site and netor-db-devices."
    echo "3.- push it to Ansible and Salt with netor-db-push."
    echo "4.- restart Salt daemons with netor-salt-restart."
    echo "5.- Go to the Use cases section to start trying Ansible and Salt examples."
    echo ""
    ;;
n) echo "cd to the directory where you want to install Netor and execute this script again."
    echo
    ;;
  *) echo "Invalid option"
    echo;;
esac
