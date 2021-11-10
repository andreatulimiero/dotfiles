# Env Vars {{{
set PATH ~/bin $PATH
set PATH ~/.local/bin $PATH
# }}}

# Key Bindings {{{
set fish_key_bindings fish_user_key_bindings
fzf_key_bindings
# }}}

set PATH $PATH ~/go/bin

# Utils {{{
function qrcode
  qrencode -r $argv[1] -d 192 -o - | feh -
end
function clip
  xclip -sel clip
end
# }}}

fzf_key_bindings
