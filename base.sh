#!/bin/bash

set -euo pipefail

Log() { echo -e "[\x1b[90m*\x1b[0m] $1"; }

Success() { echo -e "[\x1b[32m✓\x1b[0m] $1"; }

Error() { echo -e "[\x1b[31mx\x1b[0m] $1"; }

CheckSuccessOrExitWith() {
  if [ $? -ne 0 ]; then
    error "$1"
    exit 1
  fi
}

GetHostname() {
  cat /proc/sys/kernel/hostname
}

