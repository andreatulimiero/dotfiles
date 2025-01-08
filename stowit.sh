#!/bin/bash
source base.sh

# Prepare the config files
branch=$(GetHostname)
Log "Versioning configs by switching to ${branch} branch ..."
git checkout ${branch} &>/dev/null
CheckSuccessOrExitWith "Failed to switch to ${branch} branch"

# Stow the home folder
Log "Stowing configs ..."
stow home -t ~/

# Check out back to main
Log "Checking back out to main ..."
git checkout main

Success "Done"
