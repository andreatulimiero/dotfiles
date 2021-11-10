Dotfiles
===
This repository contains dotfiles for my vanilla _ArchLinux_/_i3wm_ setup.  
Dotfiles are first **prepared**, for per-host preferences, and then installed using `stow`.

### Preparing
While the majority of my dotfiles are fine across my machines, I have the need for some specific tweaks.
To tackle this need, I have a custom script (`prepare.py`) that automatically prepares the dotfiles based on the hostname of the machine.
### Why a custom solution?
I have heard there are some solutions that combine different per-host files into a single configuration.
While this is a sensible approach, I believe it makes sense only when the number of changes between hosts is significant enough to justify the additional fragmentation of the files.  
Since I found myself changing only a tiny part of my dotfiles, I opted for a solution that kept the structure of my dotfiles the same as in a single machine use case.
### How does it work?
Currently, the solution works on a line-by-line basis (e.g., no per-host blocks of configurations).  
The idea is simple: by default, a configuration line is valid of all machines; if one wants a line to be active only on a specific host, they append a rule that specifies on which machines it should be valid.  

Here is an example of how to specify a different background image for hosts `A` and `B`:
```
exec --no-startup-id feh --bg-tile ~/Pictures/Squares.jpg #> [#@_A]
exec --no-startup-id feh --bg-fill ~/Pictures/Mountain.jpg #> [#@_B]
```
