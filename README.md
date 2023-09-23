Dotfiles
===
This repository contains dotfiles for my vanilla _ArchLinux_/_i3wm_ setup.  

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


### Installing Dotfiles
Dotfiles are installed on a machine using the `stow` command.
To install dotfiles on a machine, run the following command:
```bash
stow home -t ~/
```
