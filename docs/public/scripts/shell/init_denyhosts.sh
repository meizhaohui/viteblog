#!/bin/bash
##################################################
#      Filename: init_denyhosts.sh
#        Author: Zhaohui Mei<mzh.whut@gmail.com>
#   Description: init the denyhosts service. 
#   Create Time: 2022-05-14 22:14:32
# Last Modified: 2022-05-14 23:38:22
##################################################


pushd /tmp || exit 1
echo "Step 1: Download install package"
wget --no-check-certificate https://udomain.dl.sourceforge.net/project/denyhosts/denyhosts/3.0/denyhosts-3.0.tar.gz
echo "Step 2: Extract the package"
tar -zxvf denyhosts-3.0.tar.gz
cd denyhosts-3.0 || exit 1
echo "Step 3: Install"
python setup.py install
echo "Step 4: Copy configuration file"
cp denyhosts.conf /etc
echo "Step 5: Change the configuration file"
sed -i 's@SECURE_LOG = /var/log/auth.log@#SECURE_LOG = /var/log/auth.log@g' /etc/denyhosts.conf
sed -i 's@#SECURE_LOG = /var/log/secure@SECURE_LOG = /var/log/secure@g' /etc/denyhosts.conf
sed -i 's@LOCK_FILE = /var/run/denyhosts.pid@#LOCK_FILE = /var/run/denyhosts.pid@g' /etc/denyhosts.conf
sed -i 's@#LOCK_FILE = /var/lock/subsys/denyhosts@LOCK_FILE = /var/lock/subsys/denyhosts@g' /etc/denyhosts.conf
sed -i 's@# from types import ListType, TupleType@from types import ListType, TupleType@g' /usr/lib/python2.7/site-packages/DenyHosts/report.py
echo "Step 6: Set the service"
cp denyhosts.service /usr/lib/systemd/system/denyhosts.service
sed -i 's@/var/run/denyhosts.pid@/var/lock/subsys/denyhosts@g' /usr/lib/systemd/system/denyhosts.service
echo "Step 7: Start the denyhosts service"
systemctl daemon-reload
systemctl enable denyhosts.service
systemctl start denyhosts.service
echo "Done!!"

