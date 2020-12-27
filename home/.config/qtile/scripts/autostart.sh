#!/bin/sh
# Background
feh --bg-fill ~/Pictures/Iron_Man.jpg &

# Network
nm-applet &

# Bluetooth
blueman-applet &

# Compton
compton --config ~/.config/compton.config &
