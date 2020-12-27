#!/bin/bash

set -euo pipefail

source ./logs.sh

get_hostname() {
  cat /proc/sys/kernel/hostname
}

branch=$(get_hostname)
log "Versioning configs by switching to ${branch} branch ..."
git checkout ${branch} &>/dev/null
if [ $? -ne 0 ]; then
  error "Failed to switch to ${branch} branch"
  exit 1
else
  success "Versioned configs"
fi
