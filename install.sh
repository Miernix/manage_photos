#!/bin/bash

# Prompt the user for the sudo password
read -s -p "Enter your sudo password: " password
echo

# Use sudo to perform operations as root
echo "$password" | sudo -S python -m venv /usr/bin/manage_photos/venv \
  && echo "$password" | sudo -S /usr/bin/manage_photos/venv/bin/python -m pip install --upgrade pip \
  && echo "$password" | sudo -S /usr/bin/manage_photos/venv/bin/pip install -r requirements.txt \
  && echo "$password" | sudo -S cp mp.py /usr/bin/mp