# Env Vars {{{
fish_add_path ~/bin
fish_add_path ~/.local/bin
fish_add_path ~/go/bin
# }}}

# Key Bindings {{{
set fish_key_bindings fish_user_key_bindings
fzf_key_bindings
# }}}

# Utils {{{
function qrcode
  qrencode -r $argv[1] -d 192 -o - | feh -
end
function clip
  xclip -sel clip
end
function i3tmuxgo
  set host $argv[1]
  set session (i3tmux -host $host -list | grep '-' | fzf | cut -d' ' -f2)
  i3tmux -host $argv[1] -resume $session
end
# }}}

fzf_key_bindings
