#!/bin/bash

log() { echo -e "[\x1b[90m*\x1b[0m] $1"; }
success() { echo -e "[\x1b[32m✓\x1b[0m] $1"; }
error() { echo -e "[\x1b[31mx\x1b[0m] $1"; }
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
