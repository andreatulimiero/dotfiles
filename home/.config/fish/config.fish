set fish_key_bindings fish_user_key_bindings
fzf_key_bindings

# Utils {{{
function qrcode
  qrencode $argv[1] -d 192 -o - | feh -
end
# }}}
