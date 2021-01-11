#!/bin/bash

# set access password for ubuntu user
echo "ubuntu:3996931" | sudo chpasswd

# make updates
sudo apt upgrade -y
