#!/bin/bash

# Validation (just in case)
echo "This is the boot script!"

# set access password for ubuntu user
echo "ubuntu:3996931" | sudo chpasswd

# make updates
sudo apt-get update
sudo unattended-upgrade
