# Git Cheatsheet

## Basics

```bash
# Check where are what you are doing
git status

# Check what branch you are on
git branch
```

## Configuring your Git

```bash
# Set VS Code to be your git editor
git config --global core.editor "'C:\Program Files (x86)\Microsoft VS Code\code.exe' -w"
```

## Creating a new branch

```bash
# confirm you are on the right branch to branch from
git branch

# If not git checkout the right branch, usually develop
git checkout develop
git branch

# create your branch
git checkout -b {insert branch name here}
# set the upstream branch from github to the same name
git push -u origin {insert branch name here}
```

## Stashing Changes

If you have changes on your local and need to pull down the latest changes from github, or you need to move your changes from one branch to another, you can git stash those changes to get your working directory clean.

```bash
# List current stashes
git stash list

# Stash changes will save the unstaged changes to the first stash slot: stash@{0}
git stash save
# Confirm your changes are stashed
git stash list
git status

# When you have moved branches to where you want to apply your changes you can pop the stash
git stash pop
```

## Commiting Changes

```bash
# check the status of your working directory
git status

# add a single file
git add {path to file here}
# OR add all uncommitted files
git add .

# Check your status again. Make sure you have staged what you thought you were staging
git status

# If you are happy with the state of your staged files:
git commit -m "Here's a commit message"
git push
# You should now see your changes available on github
```


