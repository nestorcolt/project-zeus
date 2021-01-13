#!/bin/bash

# Validation (just in case)
echo "This is the boot script!"

# set access password for ubuntu user
echo "ubuntu:3996931" | sudo chpasswd
systemctl enable my_start.service


#make updates
sudo apt-get update
sudo unattended-upgrade


# code commit new versions pull
pushd deploy
git --git-dir=/home/ubuntu/deploy/.git pull origin master
echo "git pull origin master"
