#!/bin/bash
source base.sh

# Prepare the config files
./prepare.py

# Stow the home folder
stow home -t ~/
