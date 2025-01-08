Dotfiles
===
This repository contains dotfiles for my vanilla _ArchLinux_/_Sway_ setup.  

### Versioning Files For Different Machines
Although the vast majority of configurations are machine-agnostic, some minor tweaks are required.  
The versioning of machine-specific configurations is based on`git` branches,
making it easy to switch between different versions while keeping a common
base.

Branch-based-versioning works as follows:
```ascii
              - [Branch A] → Host A Tweaks
            /
0xv1 → 0xv2
            \
              - [Branch B] → Host B Tweaks
```

The idea is that the common configuration are in the `main` branch and
machine-specific configurations are added on top of it.  

Versioning the configuration for a specific machine is then a matter of `git
checkout <hostname>`.

#### Making Changes
Depending on the type of changes (machine-agnostic or machine-dependent), you
follow one of the following approaches.
##### Machine Independent
1. Checkout the `main` branch (which is machine-agnostic)
1. Make changes and create a new commit
1. Run the `./rebase_all.sh` script to rebase all machine-specific branches on
   top of the latest `main` commit.
1. Push the changes with `git push --all --force` (you need to `--force` since
   machine-specific branches were rebased -- IIUC)

N.B.: Squashing changes in the `main` branch will make the `./rebase_all.sh`
script fail since the base commit of the machine-specific branches is going to
be different.

##### Mahine Specific
1. Checkout the machine-specific branch
1. Make changes and create a new commit
1. Push the changes with `git push <machine-specific-branch>`

### Installing Dotfiles
Dotfiles are installed on a machine using the `stow` command.
To install dotfiles on a machine, run the following command:
```bash
stow home -t ~/
```
