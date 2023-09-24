#!/bin/bash

MAIN_BRANCH=main

branches=$(git for-each-ref --format='%(refname:short)' refs/heads/)
for branch in $branches; do
  if [ "$branch" == "$MAIN_BRANCH" ]; then
    continue
  fi
  git checkout $branch
  git rebase $MAIN_BRANCH
  git checkout $MAIN_BRANCH
done
