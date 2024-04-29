# --------------------------------------------------------
# Key bindings for qtile
# --------------------------------------------------------
from libqtile.config import Key
from libqtile.lazy import lazy
from defaults import terminal, home, mod, alt

# --------------------------------------------------------
# Custom imports
# --------------------------------------------------------
from groups_config import latest_group

################################### 
# functions to be used in keybindings
def go_to_group(qtile, index):
    qtile.current_group.use_layout(index)

@lazy.function
def maximize_by_switching_layout(qtile):
    """Toggle between max and last used layout, for the first run if started in Max, will default to monadtall."""
    if qtile.current_group.layout.name != 'max':
        qtile.current_group.last_used_layout = qtile.current_group.layout.name # creating my own attribute
        qtile.current_group.layout = 'max'
    elif hasattr(qtile.current_group, 'last_used_layout'):
        qtile.current_group.layout = qtile.current_group.last_used_layout
    else:
        qtile.current_group.layout = 'monadtall'
###################################
keys = [
    # Focus
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window around"),

    # Move
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod], "Print", lazy.spawn(home + "/dotfiles/qtile/scripts/screenshot.sh")),

    # Size
    Key([mod, "control"], "Down", lazy.layout.shrink(), desc="Grow window to the left"),
    Key([mod, "control"], "Up", lazy.layout.grow(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", maximize_by_switching_layout(), desc="Toggle Max mode"),
    # Key([mod], "t", lazy.function(go_to_group, ), desc="Reset all window sizes"),

    # Floating
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),

    # Split
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle Layouts
    Key([mod], "L", lazy.next_layout(), desc="Toggle between layouts"),

    # Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    
    # Windows
    Key([alt], "Tab", lazy.group.next_window(), desc="Focus next window"),
    Key([alt, "shift"], "Tab", lazy.group.prev_window(), desc="Focus previous window"),

    #System
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "x", lazy.spawn(home + "/dotfiles/qtile/scripts/powermenu.sh"), desc="Open Powermenu"),

    # Apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "z", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    Key([mod, "shift"], "w", lazy.spawn("sh " + home + "/dotfiles/.settings/browser.sh"), desc="Launch Brave"),
    Key([mod, "shift"], "o", lazy.spawn("alacritty -t 'ranger' -e ranger"), desc="Launch Ranger"),
    #Key([mod, "shift"], "w", lazy.spawn(home + "/dotfiles/qtile/scripts/wallpaper.sh"), desc="Update Theme and Wallpaper"),
    #Key([mod, "control"], "w", lazy.spawn(home + "/dotfiles/qtile/scripts/wallpaper.sh select"), desc="Select Theme and Wallpaper"),

    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -q s +20%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -q s 20%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
]

# keybindings to control the group switching
keys += [
        Key([mod], "Tab", lazy.function(latest_group), desc="Switch to last used group"),
        Key([alt, "control"], "Right", lazy.screen.next_group(), desc="Switch to next group"),
        Key([alt, "control"], "Left", lazy.screen.prev_group(), desc="Switch to prev group"),
         ]

# keybindings for scratchpad

keys.extend([
    Key([mod], 'F10', lazy.group["temp"].dropdown_toggle("chatgpt")),
    Key([mod], 'F11', lazy.group["temp"].dropdown_toggle("mousepad")),
    Key([mod], 'F12', lazy.group["temp"].dropdown_toggle("terminal")),
    Key([mod], 'F9', lazy.group["temp"].dropdown_toggle("scrcpy"))
])
