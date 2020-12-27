#!/bin/bash

# Prepare the config files
./prepare.py

# Stow the home folder
stow home -t ~/
