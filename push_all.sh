#!/bin/bash
source base.sh

MAIN_BRANCH="main"
HOSTNAMES="Friday tulimiero1"

for branch in $HOSTNAMES; do
  Log "Force-pushing $branch ..."
  git push -f origin $branch
  CheckSuccessOrExitWith "Failed to rebase on top of $MAIN_BRANCH"
done
Log "Force-pushing $MAIN_BRANCH ..."
git push -f origin $MAIN_BRANCH
CheckSuccessOrExitWith "Failed to rebase on top of $MAIN_BRANCH"
Success "Done"
