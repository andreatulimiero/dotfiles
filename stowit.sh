#!/bin/bash

# Version the config files
./version.py

# Stow the home folder
stow home -t ~/
