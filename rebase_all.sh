#!/bin/bash
source base.sh

MAIN_BRANCH="main"
HOSTNAMES="Friday tulimiero1"

for branch in $HOSTNAMES; do
  Log "Rebasing $branch on top of $MAIN_BRANCH ..."
  git rebase -X theirs $MAIN_BRANCH $branch
  CheckSuccessOrExitWith "Failed to rebase on top of $MAIN_BRANCH"
done
Log "Checking out to $MAIN_BRANCH branch ..."
git checkout $MAIN_BRANCH
Success "Done"
