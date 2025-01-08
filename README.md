Dotfiles
===
This repository contains dotfiles for my vanilla _ArchLinux_/_Sway_ setup.  

### Versioning Files For Different Machines
Although the vast majority of configurations are machine-agnostic, some minor tweaks are required.  
The versioning of machine-specific configurations is based on`git` branches: this makes it easy to switch between different versions while keeping a common basis between them.  
Branch-based-versioning works as follows:
```ascii
              - [Branch A] → Host A Tweaks
            /
0xv1 → 0xv2
            \
              - [Branch B] → Host B Tweaks
```

The idea is that the common configuration are in the `main` branch and machine 
specific configurations are added on top of it in specific branches.  
Then, to version the configuration for a specific machine, all it takes is switching
to the dedicated branch with `git checkout <hostname>`.

#### Making Changes
##### Machine Independent
To make changes that apply to all machines:
1. Check out to the `main` branch (which is machine-independent)
1. Make changes and create a new commit
1. Run the `./rebase_all.sh` script to rebase all machine-dependent branches on
   top of the latest `main` commit.

N.b.: Squashing changes in the `main` branch will make the `./rebase_all.sh`
script fail since the base commit of the machine-dependent branches is going to
be different.

##### Mahine Specific
In this case, simply check out the machine-specific branch, make changes and
create a new commit. Squashing commits is not an issue in this case.

### Installing Dotfiles
Dotfiles are installed on a machine using the `stow` command.
To install dotfiles on a machine, run the following command:
```bash
stow home -t ~/
```
