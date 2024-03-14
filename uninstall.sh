#!/bin/bash

# Prompt the user for the sudo password
read -s -p "Enter your sudo password: " password
echo

# Use sudo to perform operations as root
echo "$password" | sudo -S rm -rf /usr/bin/manage_photos \
  && echo "$password" | sudo -S rm /usr/bin/mp

