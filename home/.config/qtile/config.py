import os
import subprocess

from libqtile import hook
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile.config import EzKey
from plasma import Plasma
from hacks.widget import *

from typing import List

mod = "mod4"

keymap = {
    'M-h': lazy.layout.left(),
    'M-j': lazy.layout.down(),
    'M-k': lazy.layout.up(),
    'M-l': lazy.layout.right(),
    'M-S-h': lazy.layout.move_left(),
    'M-S-j': lazy.layout.move_down(),
    'M-S-k': lazy.layout.move_up(),
    'M-S-l': lazy.layout.move_right(),
    'M-A-h': lazy.layout.integrate_left(),
    'M-A-j': lazy.layout.integrate_down(),
    'M-A-k': lazy.layout.integrate_up(),
    'M-A-l': lazy.layout.integrate_right(),
    'M-s': lazy.layout.mode_horizontal(),
    'M-v': lazy.layout.mode_vertical(),
    'M-C-l': lazy.layout.grow_width(50),
    'M-C-h': lazy.layout.grow_width(-50),
    'M-C-k': lazy.layout.grow_height(50),
    'M-C-j': lazy.layout.grow_height(-50),

    'M-S-<space>': lazy.window.toggle_floating(),
    'M-S-p': lazy.spawn("betterlockscreen -l blur"),
    'M-f': lazy.window.toggle_fullscreen(),
    'M-S-r': lazy.restart(),
    'M-<Return>': lazy.spawn("kitty"),
    'M-S-q': lazy.window.kill(),
    'M-d': lazy.spawn("rofi -show combi"),
    'M-e': lazy.spawn("nautilus"),
    'M-S-e': lazy.shutdown()

}
keys = [
        Key([], "XF86AudioMute", lazy.spawn("amixer -q -D pulse sset Master toggle")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 3-")),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 3+")),
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
]
keys += [EzKey(k, v) for k, v in keymap.items()]

groups = [Group(str(i)) for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    Plasma(
        border_normal='#333333',
        border_focus='#00e891',
        border_normal_fixed='#006863',
        border_focus_fixed='#00e8dc',
        border_width=3,
        border_width_single=0,
        margin=8
    )
]

widget_defaults = dict(
    font='Arial',
    fontsize=30,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            widgets=[
                widget.GroupBox(),
                widget.Prompt(),
                WindowName(),
                Player(),
                widget.Systray(icon_size=30, padding=10),
                widget.Notify(),
                Backlight(),
                VolumeIcon(theme_path=os.path.expanduser('~/.config/qtile/hacks/resources/volume-icons/')),
                widget.Volume(),
                BatteryIcon(battery_name='BAT1', theme_path=os.path.expanduser('~/.config/qtile/hacks/resources/battery-icons/')),
                Battery(battery_name='BAT1'),
                widget.Clock(format='%H:%M %b %d, %a'),
            ],
            size=50,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules: List = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass

    {'wmclass': 'Blueman-manager'},  # Blueman manager
    {'wmclass': 'Org.gnome.Nautilus'}, # Nautilus
    {'wmclass': 'Nm-connection-editor'}, # NM Edit Connections
    {'wmclass': 'Gcr-prompter'}, # Password insertion
    {'wmclass': 'Gnome-calculator'}, # Gnome calculator
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Hooks
# {{{
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.call([home])
# }}}
