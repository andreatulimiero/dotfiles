#!/bin/bash
source base.sh

branch=$(GetHostname)
Log "Versioning configs by switching to ${branch} branch ..."
git checkout ${branch} &>/dev/null
CheckSuccessOrExitWith "Failed to switch to ${branch} branch"
Success "Versioned configs"
