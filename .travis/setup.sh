#!/bin/sh
sudo apt-get update

sudo lxd --version
# Wait for the socket to be ready
sudo lxd waitready
sudo lxd init --auto

# Enable nesting without privileged containers,
# cf. https://stgraber.org/2017/06/15/custom-user-mappings-in-lxd-containers/
sudo sed -i 's/^\(lxd:[0-9]\{1,\}\):.*/\1:1000000000/' /etc/subuid
sudo sed -i 's/^\(root:[0-9]\{1,\}\):.*/\1:1000000000/' /etc/subuid
sudo sed -i 's/^\(lxd:[0-9]\{1,\}\):.*/\1:1000000000/' /etc/subgid
sudo sed -i 's/^\(root:[0-9]\{1,\}\):.*/\1:1000000000/' /etc/subgid
sudo systemctl restart lxd

ansible --version
molecule --version
