
#apt install -y openssh-server

sudo apt install -y chrony
sudo systemctl start chrony

sudo systemctl enable chrony

systemctl status --no-pager chrony

sudo chronyc tracking
sudo chronyc sources
sudo sed -i '/^pool /c\
server 0.fr.pool.ntp.org iburst\
\nserver 1.fr.pool.ntp.org iburst\
\nserver 2.fr.pool.net.org iburst\
\nserver 3.fr.pool.net.org iburst' /etc/chrony/chrony.conf

sudo grep '^server' /etc/chrony/chrony.conf

FILE="/etc/chrony/chrony.conf"
STRING="allow 192.168.120.0/24"
if grep -Fxq "$STRING" "$FILE"
then
        echo "already exist"
        break
else
        sudo echo "allow 192.168.120.0/24" >> /etc/chrony/chrony.conf
fi
#sudo systemctl restart chronyd
#chrony sources -v

#apt install -y postfix
#tools ? utils
exit
