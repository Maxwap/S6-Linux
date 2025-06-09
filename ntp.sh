#!/bin/sh
#apt install -y openssh-server

sudo apt install -y chrony
sudo systemctl start chronyd
sudo systemctl enable chronyd
sudo systemctl status chronyd

sudo chronyc tracking
sudo chronyc sources
sudo sed -i '/^pool /c\
server 0.fr.pool.ntp.org iburst\
\nserver 1.fr.pool.ntp.org iburst\
\nserver 2.fr.pool.net.org iburst\
\nserver 3.fr.pool.net.org iburst' /etc/chrony/chrony.conf

sudo grep '^server' /etc/chrony/chrony.conf
sudo systemctl restart chrony
#chrony sources -v

