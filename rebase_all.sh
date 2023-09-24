#!/bin/bash
source ./logs.sh

MAIN_BRANCH=main

checkSuccessOrExitWith() {
  if [ $? -ne 0 ]; then
    error "$1"
    exit 1
  fi
}

branches=$(git for-each-ref --format='%(refname:short)' refs/heads/)
for branch in $branches; do
  if [ "$branch" == "$MAIN_BRANCH" ]; then
    continue
  fi
  log "Checking out $branch branch"
  git checkout $branch
  checkSuccessOrExitWith "Failed to checkout $branch branch"
  log "Rebasing on top of $MAIN_BRANCH"
  git rebase $MAIN_BRANCH
  checkSuccessOrExitWith "Failed to rebase on top of $MAIN_BRANCH"
  log "Switching back to $MAIN_BRANCH"
  git checkout $MAIN_BRANCH
  checkSuccessOrExitWith "Failed to switch back to $MAIN_BRANCH"
  success "Successfully rebased $branch on top of $MAIN_BRANCH"
done
success "Done"
