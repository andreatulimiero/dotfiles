Dotfiles
---
This repository contains dotfiles for my vanilla _ArchLinux_/_i3wm_ setup.
Dotfiles are installed using `stow` and prepared, depending on the hostname, with a `prepare.py` script.

# Pre/Post Commit Hooks
When pushing updates from different machines, some files would change just because of the different preparations of configuration files.
To avoid such modifications to get tracked, the pre-commit hook forcibly uncomments configuration files before adding them to the commit.
Conversely, the post-commit hook re-prepares files after commit has been created.
