#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 

# Icons: https://fontawesome.com/search?o=r&m=free

import os
import subprocess
from libqtile import hook, qtile, bar
from libqtile.lazy import lazy
from libqtile.config import Screen, Drag, Click

# code for debugging
# from libqtile.log_utils import logger

# --------------------------------------------------------
# Setting environment variables
# --------------------------------------------------------
if qtile.core.name == "wayland":
    os.environ["XDG_SESSION_DESKTOP"] = "qtile:wlroots"
    os.environ["XDG_CURRENT_DESKTOP"] = "qtile:wlroots"

# --------------------------------------------------------
# Check for Desktop/Laptop
# --------------------------------------------------------

# 3 = Desktop
platform = int(os.popen("cat /sys/class/dmi/id/chassis_type").read())

# --------------------------------------------------------
# Touchpad config for wayland
# --------------------------------------------------------

from libqtile.backend.wayland import InputConfig

wl_input_rules = {
    '1739:52781:MSFT0001:00 06CB:CE2D Touchpad': InputConfig(
    middle_emulation=True,
    natural_scroll=True,
    pointer_accel=0.1,
    scroll_method='two_finger',
    tap=True,
    ),
}


# --------------------------------------------------------
# Custom config imports
# --------------------------------------------------------
from groups_config import groups, layout_theme, layouts, floating_layout, dgroups_key_binder, mouse
from keybindings_config import keys, mod, alt

# --------------------------------------------------------
# Screens
# --------------------------------------------------------
from bar_config import top_bar
screens = [
    Screen(
        top=bar.Gap(32)
		# top=top_bar
    ),
]
# --------------------------------------------------------
# General Setup
# --------------------------------------------------------

dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

# --------------------------------------------------------
# Windows Manager Name
# --------------------------------------------------------
wmname = "QTILE"

# --------------------------------------------------------
# Hooks
# --------------------------------------------------------

# Special rules for xfdesktop
@hook.subscribe.client_new
def window_rules(window):
    if "xfdesktop"  == window.window.get_wm_class()[0]:
        os.system("killall xfdesktop")
        # window.window.kill()
    if window.window.get_wm_role() == "pop-up":
        window.window.floating = True
        window.window.opacity = 0.9

# HOOK startup
@hook.subscribe.startup_once
def autostart():
    autostartscript = "~/.config/qtile/autostart.sh"
    home = os.path.expanduser(autostartscript)
    subprocess.Popen([home])

