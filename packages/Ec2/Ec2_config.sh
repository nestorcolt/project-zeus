#!/bin/bash

# Validation (just in case)
echo "This is the boot script!"

# set access password for ubuntu user
echo "ubuntu:3996931" | sudo chpasswd

# Set the hostname as env var to query in code
export MY_IP="hostname -I"

#make updates
sudo apt-get update
sudo unattended-upgrade
